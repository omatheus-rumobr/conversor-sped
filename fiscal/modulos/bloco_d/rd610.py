import re
import json
from datetime import datetime


def validar_valor_numerico(valor_str, decimais=2, obrigatorio=False, positivo=False, nao_negativo=False):
    """
    Valida um valor numérico com precisão decimal específica.
    
    Args:
        valor_str: String com o valor numérico
        decimais: Número máximo de casas decimais permitidas
        obrigatorio: Se True, o campo não pode estar vazio
        positivo: Se True, o valor deve ser maior que 0
        nao_negativo: Se True, o valor deve ser maior ou igual a 0
        
    Returns:
        tuple: (True/False, valor float ou None, mensagem de erro ou None)
    """
    if not valor_str:
        if obrigatorio:
            return False, None, f"Campo obrigatório não preenchido"
        return True, 0.0, None
    
    try:
        valor_float = float(valor_str)
        
        # Verifica precisão decimal
        partes_decimal = valor_str.split('.')
        if len(partes_decimal) == 2 and len(partes_decimal[1]) > decimais:
            return False, None, f"Valor com mais de {decimais} casas decimais"
        
        # Validações de sinal
        if positivo and valor_float <= 0:
            return False, None, "Valor deve ser maior que zero"
        if nao_negativo and valor_float < 0:
            return False, None, "Valor não pode ser negativo"
        
        return True, valor_float, None
    except ValueError:
        return False, None, "Valor não é numérico válido"


def _processar_linha_d610(linha):
    """
    Processa uma única linha do registro D610 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |D610|COD_CLASS|COD_ITEM|QTD|UNID|VL_ITEM|VL_DESC|CST_ICMS|CFOP|ALIQ_ICMS|VL_BC_ICMS|VL_ICMS|VL_BC_ICMS_UF|VL_ICMS_UF|VL_RED_BC|VL_PIS|VL_COFINS|COD_CTA|
        
    Returns:
        dict: Dicionário com os campos validados contendo título e valor, ou None se inválido
    """
    if not linha or not isinstance(linha, str):
        return None
    
    linha = linha.strip()
    
    # Ignora linhas vazias
    if not linha:
        return None
    
    # Divide por pipe e remove partes vazias
    partes = linha.split('|')
    # Remove primeiro e último se vazios (formato padrão SPED: |D610|...|)
    if partes and not partes[0]:
        partes = partes[1:]
    if partes and not partes[-1]:
        partes = partes[:-1]
    
    # Verifica se tem pelo menos o campo REG
    if len(partes) < 1:
        return None
    
    # Extrai o campo REG
    reg = partes[0].strip() if partes else ""
    
    # Validação do campo REG
    if reg != "D610":
        return None
    
    # Função auxiliar para obter campo ou string vazia
    def obter_campo(indice):
        if indice < len(partes):
            valor = partes[indice].strip()
            # Trata "-" como campo vazio (padrão SPED para campos opcionais não preenchidos)
            if valor == "-":
                return ""
            return valor if valor else ""
        return ""
    
    # Extrai todos os campos (18 campos no total)
    cod_class = obter_campo(1)
    cod_item = obter_campo(2)
    qtd = obter_campo(3)
    unid = obter_campo(4)
    vl_item = obter_campo(5)
    vl_desc = obter_campo(6)
    cst_icms = obter_campo(7)
    cfop = obter_campo(8)
    aliq_icms = obter_campo(9)
    vl_bc_icms = obter_campo(10)
    vl_icms = obter_campo(11)
    vl_bc_icms_uf = obter_campo(12)
    vl_icms_uf = obter_campo(13)
    vl_red_bc = obter_campo(14)
    vl_pis = obter_campo(15)
    vl_cofins = obter_campo(16)
    cod_cta = obter_campo(17)
    
    # Validações dos campos obrigatórios
    
    # COD_CLASS: obrigatório, 4 dígitos
    if not cod_class or len(cod_class) != 4 or not cod_class.isdigit():
        return None
    
    # COD_ITEM: obrigatório, até 60 caracteres
    if not cod_item or len(cod_item) > 60:
        return None
    
    # QTD: obrigatório, numérico com 3 decimais, maior que zero
    qtd_valido, qtd_float, _ = validar_valor_numerico(qtd, decimais=3, obrigatorio=True, positivo=True)
    if not qtd_valido:
        return None
    
    # UNID: obrigatório, até 6 caracteres
    if not unid or len(unid) > 6:
        return None
    
    # VL_ITEM: obrigatório, numérico com 2 decimais, maior que zero
    vl_item_valido, vl_item_float, _ = validar_valor_numerico(vl_item, decimais=2, obrigatorio=True, positivo=True)
    if not vl_item_valido:
        return None
    
    # VL_DESC: opcional condicional, numérico com 2 decimais, não negativo
    vl_desc_valido, vl_desc_float, _ = validar_valor_numerico(vl_desc, decimais=2, obrigatorio=False, nao_negativo=True)
    if not vl_desc_valido:
        return None
    
    # CST_ICMS: obrigatório, 3 dígitos, primeiro dígito sempre 0
    if not cst_icms or len(cst_icms) != 3 or not cst_icms.isdigit() or cst_icms[0] != '0':
        return None
    
    # CFOP: obrigatório, 4 dígitos, primeiro caractere deve ser 5, 6 ou 7
    if not cfop or len(cfop) != 4 or not cfop.isdigit() or cfop[0] not in ['5', '6', '7']:
        return None
    
    # Validações condicionais baseadas no CST_ICMS
    cst_icms_ultimos_dois = cst_icms[1:]
    
    # Validação de ALIQ_ICMS, VL_BC_ICMS e VL_ICMS baseada no CST_ICMS
    if cst_icms_ultimos_dois in ["30", "40", "41", "50", "60"]:
        # Se CST_ICMS terminar em 30, 40, 41, 50 ou 60, então VL_BC_ICMS, ALIQ_ICMS e VL_ICMS devem ser 0
        vl_bc_icms_valido, vl_bc_icms_float, _ = validar_valor_numerico(vl_bc_icms, decimais=2, obrigatorio=False, nao_negativo=True)
        if not vl_bc_icms_valido or abs(vl_bc_icms_float) > 0.001:
            return None
        
        aliq_icms_valido, aliq_icms_float, _ = validar_valor_numerico(aliq_icms, decimais=2, obrigatorio=False, nao_negativo=True)
        if not aliq_icms_valido or abs(aliq_icms_float) > 0.001:
            return None
        
        vl_icms_valido, vl_icms_float, _ = validar_valor_numerico(vl_icms, decimais=2, obrigatorio=False, nao_negativo=True)
        if not vl_icms_valido or abs(vl_icms_float) > 0.001:
            return None
    elif cst_icms_ultimos_dois in ["51", "90"]:
        # Se CST_ICMS terminar em 51 ou 90, então VL_BC_ICMS, ALIQ_ICMS e VL_ICMS devem ser >= 0
        vl_bc_icms_valido, vl_bc_icms_float, _ = validar_valor_numerico(vl_bc_icms, decimais=2, obrigatorio=False, nao_negativo=True)
        if not vl_bc_icms_valido:
            return None
        
        aliq_icms_valido, aliq_icms_float, _ = validar_valor_numerico(aliq_icms, decimais=2, obrigatorio=False, nao_negativo=True)
        if not aliq_icms_valido:
            return None
        
        vl_icms_valido, vl_icms_float, _ = validar_valor_numerico(vl_icms, decimais=2, obrigatorio=False, nao_negativo=True)
        if not vl_icms_valido:
            return None
    else:
        # Para outros CST_ICMS, VL_BC_ICMS, ALIQ_ICMS e VL_ICMS devem ser > 0
        vl_bc_icms_valido, vl_bc_icms_float, _ = validar_valor_numerico(vl_bc_icms, decimais=2, obrigatorio=False, positivo=True)
        if not vl_bc_icms_valido:
            return None
        
        aliq_icms_valido, aliq_icms_float, _ = validar_valor_numerico(aliq_icms, decimais=2, obrigatorio=False, positivo=True)
        if not aliq_icms_valido:
            return None
        
        vl_icms_valido, vl_icms_float, _ = validar_valor_numerico(vl_icms, decimais=2, obrigatorio=False, positivo=True)
        if not vl_icms_valido:
            return None
    
    # VL_BC_ICMS_UF: opcional condicional, numérico com 2 decimais, não negativo
    vl_bc_icms_uf_valido, vl_bc_icms_uf_float, _ = validar_valor_numerico(vl_bc_icms_uf, decimais=2, obrigatorio=False, nao_negativo=True)
    if not vl_bc_icms_uf_valido:
        return None
    
    # VL_ICMS_UF: opcional condicional, numérico com 2 decimais, não negativo
    vl_icms_uf_valido, vl_icms_uf_float, _ = validar_valor_numerico(vl_icms_uf, decimais=2, obrigatorio=False, nao_negativo=True)
    if not vl_icms_uf_valido:
        return None
    
    # VL_RED_BC: opcional condicional, numérico com 2 decimais, não negativo
    vl_red_bc_valido, vl_red_bc_float, _ = validar_valor_numerico(vl_red_bc, decimais=2, obrigatorio=False, nao_negativo=True)
    if not vl_red_bc_valido:
        return None
    
    # VL_PIS: opcional condicional, numérico com 2 decimais, não negativo
    vl_pis_valido, vl_pis_float, _ = validar_valor_numerico(vl_pis, decimais=2, obrigatorio=False, nao_negativo=True)
    if not vl_pis_valido:
        return None
    
    # VL_COFINS: opcional condicional, numérico com 2 decimais, não negativo
    vl_cofins_valido, vl_cofins_float, _ = validar_valor_numerico(vl_cofins, decimais=2, obrigatorio=False, nao_negativo=True)
    if not vl_cofins_valido:
        return None
    
    # Formatação de valores monetários
    def formatar_valor_monetario(valor_float):
        if valor_float is None:
            return ""
        return f"R$ {valor_float:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    # Formatação de quantidade (3 decimais)
    def formatar_quantidade(valor_float):
        if valor_float is None:
            return ""
        return f"{valor_float:,.3f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    # Formatação de percentual
    def formatar_percentual(valor_float):
        if valor_float is None:
            return ""
        return f"{valor_float:.2f}%"
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "COD_CLASS": {
            "titulo": "Código de classificação do item do serviço de comunicação ou de telecomunicação, conforme a Tabela 4.4.1",
            "valor": cod_class
        },
        "COD_ITEM": {
            "titulo": "Código do item (campo 02 do Registro 0200)",
            "valor": cod_item
        },
        "QTD": {
            "titulo": "Quantidade acumulada do item",
            "valor": qtd,
            "valor_formatado": formatar_quantidade(qtd_float)
        },
        "UNID": {
            "titulo": "Unidade do item (Campo 02 do registro 0190)",
            "valor": unid
        },
        "VL_ITEM": {
            "titulo": "Valor acumulado do item",
            "valor": vl_item,
            "valor_formatado": formatar_valor_monetario(vl_item_float)
        },
        "VL_DESC": {
            "titulo": "Valor acumulado dos descontos",
            "valor": vl_desc if vl_desc else "",
            "valor_formatado": formatar_valor_monetario(vl_desc_float) if vl_desc else ""
        },
        "CST_ICMS": {
            "titulo": "Código da Situação Tributária, conforme a Tabela indicada no item 4.3.1",
            "valor": cst_icms
        },
        "CFOP": {
            "titulo": "Código Fiscal de Operação e Prestação conforme tabela indicada no item 4.2.2",
            "valor": cfop
        },
        "ALIQ_ICMS": {
            "titulo": "Alíquota do ICMS",
            "valor": aliq_icms if aliq_icms else "",
            "valor_formatado": formatar_percentual(aliq_icms_float) if aliq_icms else ""
        },
        "VL_BC_ICMS": {
            "titulo": "Valor acumulado da base de cálculo do ICMS",
            "valor": vl_bc_icms if vl_bc_icms else "",
            "valor_formatado": formatar_valor_monetario(vl_bc_icms_float) if vl_bc_icms else ""
        },
        "VL_ICMS": {
            "titulo": "Valor acumulado do ICMS debitado",
            "valor": vl_icms if vl_icms else "",
            "valor_formatado": formatar_valor_monetario(vl_icms_float) if vl_icms else ""
        },
        "VL_BC_ICMS_UF": {
            "titulo": "Valor da base de cálculo do ICMS de outras UFs",
            "valor": vl_bc_icms_uf if vl_bc_icms_uf else "",
            "valor_formatado": formatar_valor_monetario(vl_bc_icms_uf_float) if vl_bc_icms_uf else ""
        },
        "VL_ICMS_UF": {
            "titulo": "Valor do ICMS de outras UFs",
            "valor": vl_icms_uf if vl_icms_uf else "",
            "valor_formatado": formatar_valor_monetario(vl_icms_uf_float) if vl_icms_uf else ""
        },
        "VL_RED_BC": {
            "titulo": "Valor não tributado em função da redução da base de cálculo do ICMS, referente à combinação de CST_ICMS, CFOP e alíquota do ICMS",
            "valor": vl_red_bc if vl_red_bc else "",
            "valor_formatado": formatar_valor_monetario(vl_red_bc_float) if vl_red_bc else ""
        },
        "VL_PIS": {
            "titulo": "Valor acumulado do PIS",
            "valor": vl_pis if vl_pis else "",
            "valor_formatado": formatar_valor_monetario(vl_pis_float) if vl_pis else ""
        },
        "VL_COFINS": {
            "titulo": "Valor acumulado da COFINS",
            "valor": vl_cofins if vl_cofins else "",
            "valor_formatado": formatar_valor_monetario(vl_cofins_float) if vl_cofins else ""
        },
        "COD_CTA": {
            "titulo": "Código da conta analítica contábil debitada/creditada",
            "valor": cod_cta if cod_cta else ""
        }
    }
    
    return resultado


def validar_d610(linhas):
    """
    Valida uma ou mais linhas do registro D610 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |D610|COD_CLASS|COD_ITEM|QTD|UNID|VL_ITEM|VL_DESC|CST_ICMS|CFOP|ALIQ_ICMS|VL_BC_ICMS|VL_ICMS|VL_BC_ICMS_UF|VL_ICMS_UF|VL_RED_BC|VL_PIS|VL_COFINS|COD_CTA|
        
    Returns:
        String JSON com array de objetos contendo os campos validados.
        Cada objeto tem a estrutura {"CAMPO": {"titulo": "...", "valor": "...", "valor_formatado": "...", "descricao": "..."}}.
        Retorna "[]" se nenhuma linha for válida.
    """
    if not linhas:
        return json.dumps([], ensure_ascii=False, indent=2)
    
    # Normaliza a entrada para uma lista de linhas
    if isinstance(linhas, str):
        # Se for string, verifica se tem múltiplas linhas
        if '\n' in linhas:
            linhas_para_processar = [linha.strip() for linha in linhas.split('\n') if linha.strip()]
        else:
            linhas_para_processar = [linhas.strip()] if linhas.strip() else []
    elif isinstance(linhas, list):
        linhas_para_processar = [linha.strip() if isinstance(linha, str) else str(linha).strip() for linha in linhas if linha]
    else:
        linhas_para_processar = [str(linhas).strip()] if str(linhas).strip() else []
    
    resultados = []
    
    for linha in linhas_para_processar:
        resultado = _processar_linha_d610(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
