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


def _processar_linha_1510(linha):
    """
    Processa uma única linha do registro 1510 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |1510|NUM_ITEM|COD_ITEM|COD_CLASS|...|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |1510|...|)
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
    if reg != "1510":
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
    
    # Extrai todos os campos (21 campos no total)
    num_item = obter_campo(1)
    cod_item = obter_campo(2)
    cod_class = obter_campo(3)
    qtd = obter_campo(4)
    unid = obter_campo(5)
    vl_item = obter_campo(6)
    vl_desc = obter_campo(7)
    cst_icms = obter_campo(8)
    cfop = obter_campo(9)
    vl_bc_icms = obter_campo(10)
    aliq_icms = obter_campo(11)
    vl_icms = obter_campo(12)
    vl_bc_icms_st = obter_campo(13)
    aliq_st = obter_campo(14)
    vl_icms_st = obter_campo(15)
    ind_rec = obter_campo(16)
    cod_part = obter_campo(17)
    vl_pis = obter_campo(18)
    vl_cofins = obter_campo(19)
    cod_cta = obter_campo(20)
    
    # Validações dos campos obrigatórios
    
    # NUM_ITEM: obrigatório, numérico, até 3 dígitos, maior que 0
    if not num_item:
        return None
    try:
        num_item_int = int(num_item)
        if num_item_int <= 0 or len(num_item) > 3:
            return None
    except ValueError:
        return None
    
    # COD_ITEM: obrigatório, até 60 caracteres
    if not cod_item or len(cod_item) > 60:
        return None
    
    # COD_CLASS: obrigatório, numérico, até 4 dígitos
    if not cod_class:
        return None
    if not cod_class.isdigit() or len(cod_class) > 4:
        return None
    
    # QTD: obrigatório condicional, numérico com 3 decimais
    if qtd:
        qtd_valido, qtd_float, qtd_erro = validar_valor_numerico(qtd, decimais=3, nao_negativo=True)
        if not qtd_valido:
            return None
    
    # UNID: obrigatório condicional, até 6 caracteres
    if unid and len(unid) > 6:
        return None
    
    # VL_ITEM: obrigatório, numérico com 2 decimais, maior que 0
    if not vl_item:
        return None
    vl_item_valido, vl_item_float, vl_item_erro = validar_valor_numerico(vl_item, decimais=2, obrigatorio=True, positivo=True)
    if not vl_item_valido:
        return None
    
    # VL_DESC: obrigatório condicional, numérico com 2 decimais
    if vl_desc:
        vl_desc_valido, vl_desc_float, vl_desc_erro = validar_valor_numerico(vl_desc, decimais=2, nao_negativo=True)
        if not vl_desc_valido:
            return None
    
    # CST_ICMS: obrigatório, numérico, 3 dígitos
    if not cst_icms:
        return None
    if not cst_icms.isdigit() or len(cst_icms) != 3:
        return None
    
    # CFOP: obrigatório, numérico, 4 dígitos, primeiro caractere deve ser 6
    if not cfop:
        return None
    if not cfop.isdigit() or len(cfop) != 4:
        return None
    if cfop[0] != "6":
        return None
    
    # VL_BC_ICMS: obrigatório condicional, numérico com 2 decimais
    if vl_bc_icms:
        vl_bc_icms_valido, vl_bc_icms_float, vl_bc_icms_erro = validar_valor_numerico(vl_bc_icms, decimais=2, nao_negativo=True)
        if not vl_bc_icms_valido:
            return None
    
    # ALIQ_ICMS: obrigatório condicional, numérico com 2 decimais
    if aliq_icms:
        aliq_icms_valido, aliq_icms_float, aliq_icms_erro = validar_valor_numerico(aliq_icms, decimais=2, nao_negativo=True)
        if not aliq_icms_valido:
            return None
    
    # VL_ICMS: obrigatório condicional, numérico com 2 decimais
    if vl_icms:
        vl_icms_valido, vl_icms_float, vl_icms_erro = validar_valor_numerico(vl_icms, decimais=2, nao_negativo=True)
        if not vl_icms_valido:
            return None
    
    # VL_BC_ICMS_ST: obrigatório condicional, numérico com 2 decimais
    if vl_bc_icms_st:
        vl_bc_icms_st_valido, vl_bc_icms_st_float, vl_bc_icms_st_erro = validar_valor_numerico(vl_bc_icms_st, decimais=2, nao_negativo=True)
        if not vl_bc_icms_st_valido:
            return None
    
    # ALIQ_ST: obrigatório condicional, numérico com 2 decimais
    if aliq_st:
        aliq_st_valido, aliq_st_float, aliq_st_erro = validar_valor_numerico(aliq_st, decimais=2, nao_negativo=True)
        if not aliq_st_valido:
            return None
    
    # VL_ICMS_ST: obrigatório condicional, numérico com 2 decimais
    if vl_icms_st:
        vl_icms_st_valido, vl_icms_st_float, vl_icms_st_erro = validar_valor_numerico(vl_icms_st, decimais=2, nao_negativo=True)
        if not vl_icms_st_valido:
            return None
    
    # IND_REC: obrigatório, valores válidos: [0, 1]
    if ind_rec not in ["0", "1"]:
        return None
    
    # COD_PART: obrigatório condicional, até 60 caracteres
    # Se IND_REC = 1, COD_PART é obrigatório
    if ind_rec == "1":
        if not cod_part or len(cod_part) > 60:
            return None
    else:
        # Se IND_REC = 0, COD_PART é opcional, mas se preenchido deve ser válido
        if cod_part and len(cod_part) > 60:
            return None
    
    # VL_PIS: obrigatório condicional, numérico com 2 decimais
    if vl_pis:
        vl_pis_valido, vl_pis_float, vl_pis_erro = validar_valor_numerico(vl_pis, decimais=2, nao_negativo=True)
        if not vl_pis_valido:
            return None
    
    # VL_COFINS: obrigatório condicional, numérico com 2 decimais
    if vl_cofins:
        vl_cofins_valido, vl_cofins_float, vl_cofins_erro = validar_valor_numerico(vl_cofins, decimais=2, nao_negativo=True)
        if not vl_cofins_valido:
            return None
    
    # COD_CTA: obrigatório condicional (sem limite de tamanho especificado)
    # Não há validação específica além de verificar se está presente
    
    # Formatação de valores monetários para exibição
    def formatar_valor(valor_str):
        if not valor_str:
            return ""
        try:
            valor_float = float(valor_str)
            return f"{valor_float:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        except ValueError:
            return valor_str
    
    # Formatação de valores numéricos com 3 decimais
    def formatar_valor_3dec(valor_str):
        if not valor_str:
            return ""
        try:
            valor_float = float(valor_str)
            return f"{valor_float:,.3f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        except ValueError:
            return valor_str
    
    # Formatação de percentual
    def formatar_percentual(valor_str):
        if not valor_str:
            return ""
        try:
            valor_float = float(valor_str)
            return f"{valor_float:,.2f}%".replace(',', 'X').replace('.', ',').replace('X', '.')
        except ValueError:
            return valor_str
    
    # Mapeamento de códigos para descrições
    ind_rec_desc = {
        "0": "Receita própria",
        "1": "Receita de terceiros"
    }
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "NUM_ITEM": {
            "titulo": "Número sequencial do item no documento fiscal",
            "valor": num_item
        },
        "COD_ITEM": {
            "titulo": "Código do item (campo 02 do Registro 0200)",
            "valor": cod_item
        },
        "COD_CLASS": {
            "titulo": "Código de classificação do item de energia elétrica, conforme a Tabela 4.4.1",
            "valor": cod_class
        },
        "QTD": {
            "titulo": "Quantidade do item",
            "valor": qtd if qtd else "",
            "valor_formatado": formatar_valor_3dec(qtd) if qtd else ""
        },
        "UNID": {
            "titulo": "Unidade do item (Campo 02 do registro 0190)",
            "valor": unid if unid else ""
        },
        "VL_ITEM": {
            "titulo": "Valor do item",
            "valor": vl_item,
            "valor_formatado": formatar_valor(vl_item)
        },
        "VL_DESC": {
            "titulo": "Valor total do desconto",
            "valor": vl_desc if vl_desc else "",
            "valor_formatado": formatar_valor(vl_desc) if vl_desc else ""
        },
        "CST_ICMS": {
            "titulo": "Código da Situação Tributária, conforme a Tabela indicada no item 4.3.1",
            "valor": cst_icms
        },
        "CFOP": {
            "titulo": "Código Fiscal de Operação e Prestação",
            "valor": cfop
        },
        "VL_BC_ICMS": {
            "titulo": "Valor da base de cálculo do ICMS",
            "valor": vl_bc_icms if vl_bc_icms else "",
            "valor_formatado": formatar_valor(vl_bc_icms) if vl_bc_icms else ""
        },
        "ALIQ_ICMS": {
            "titulo": "Alíquota do ICMS",
            "valor": aliq_icms if aliq_icms else "",
            "valor_formatado": formatar_percentual(aliq_icms) if aliq_icms else ""
        },
        "VL_ICMS": {
            "titulo": "Valor do ICMS creditado/debitado",
            "valor": vl_icms if vl_icms else "",
            "valor_formatado": formatar_valor(vl_icms) if vl_icms else ""
        },
        "VL_BC_ICMS_ST": {
            "titulo": "Valor da base de cálculo referente à substituição tributária",
            "valor": vl_bc_icms_st if vl_bc_icms_st else "",
            "valor_formatado": formatar_valor(vl_bc_icms_st) if vl_bc_icms_st else ""
        },
        "ALIQ_ST": {
            "titulo": "Alíquota do ICMS da substituição tributária na unidade da federação de destino",
            "valor": aliq_st if aliq_st else "",
            "valor_formatado": formatar_percentual(aliq_st) if aliq_st else ""
        },
        "VL_ICMS_ST": {
            "titulo": "Valor do ICMS referente à substituição tributária",
            "valor": vl_icms_st if vl_icms_st else "",
            "valor_formatado": formatar_valor(vl_icms_st) if vl_icms_st else ""
        },
        "IND_REC": {
            "titulo": "Indicador do tipo de receita",
            "valor": ind_rec,
            "descricao": ind_rec_desc.get(ind_rec, "")
        },
        "COD_PART": {
            "titulo": "Código do participante receptor da receita, terceiro da operação (campo 02 do Registro 0150)",
            "valor": cod_part if cod_part else ""
        },
        "VL_PIS": {
            "titulo": "Valor do PIS",
            "valor": vl_pis if vl_pis else "",
            "valor_formatado": formatar_valor(vl_pis) if vl_pis else ""
        },
        "VL_COFINS": {
            "titulo": "Valor da COFINS",
            "valor": vl_cofins if vl_cofins else "",
            "valor_formatado": formatar_valor(vl_cofins) if vl_cofins else ""
        },
        "COD_CTA": {
            "titulo": "Código da conta analítica contábil debitada/creditada",
            "valor": cod_cta if cod_cta else ""
        }
    }
    
    return resultado


def validar_1510_fiscal(linhas):
    """
    Valida uma ou mais linhas do registro 1510 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |1510|NUM_ITEM|COD_ITEM|COD_CLASS|...|
        
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
        resultado = _processar_linha_1510(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
