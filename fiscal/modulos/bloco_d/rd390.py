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


def _processar_linha_d390(linha):
    """
    Processa uma única linha do registro D390 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |D390|CST_ICMS|CFOP|ALIQ_ICMS|VL_OPR|VL_BC_ISSQN|ALIQ_ISSQN|VL_ISSQN|VL_BC_ICMS|VL_ICMS|COD_OBS|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |D390|...|)
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
    if reg != "D390":
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
    
    # Extrai todos os campos (11 campos no total)
    cst_icms = obter_campo(1)
    cfop = obter_campo(2)
    aliq_icms = obter_campo(3)
    vl_opr = obter_campo(4)
    vl_bc_issqn = obter_campo(5)
    aliq_issqn = obter_campo(6)
    vl_issqn = obter_campo(7)
    vl_bc_icms = obter_campo(8)
    vl_icms = obter_campo(9)
    cod_obs = obter_campo(10)
    
    # Validações dos campos obrigatórios
    
    # CST_ICMS: obrigatório, 3 dígitos, primeiro dígito sempre 0
    if not cst_icms or len(cst_icms) != 3 or not cst_icms.isdigit() or cst_icms[0] != '0':
        return None
    
    # Extrai os dois últimos dígitos do CST_ICMS
    cst_icms_ultimos_2 = cst_icms[1:]
    
    # CFOP: obrigatório, 4 dígitos, primeiro caractere = 5, 6 ou 7, não pode terminar em 00 ou 50
    if not cfop or len(cfop) != 4 or not cfop.isdigit() or cfop[0] not in ['5', '6', '7'] or cfop.endswith("00") or cfop.endswith("50"):
        return None
    
    # VL_OPR: obrigatório, numérico com 2 decimais, maior que zero
    vl_opr_valido, vl_opr_float, _ = validar_valor_numerico(vl_opr, decimais=2, obrigatorio=True, positivo=True)
    if not vl_opr_valido:
        return None
    
    # VL_BC_ISSQN: opcional condicional, numérico com 2 decimais, não negativo
    vl_bc_issqn_valido, vl_bc_issqn_float, _ = validar_valor_numerico(vl_bc_issqn, decimais=2, obrigatorio=False, nao_negativo=True)
    if not vl_bc_issqn_valido:
        return None
    
    # ALIQ_ISSQN: opcional condicional, numérico com 2 decimais, não negativo
    aliq_issqn_valido, aliq_issqn_float, _ = validar_valor_numerico(aliq_issqn, decimais=2, obrigatorio=False, nao_negativo=True)
    if not aliq_issqn_valido:
        return None
    
    # VL_ISSQN: opcional condicional, numérico com 2 decimais, não negativo
    vl_issqn_valido, vl_issqn_float, _ = validar_valor_numerico(vl_issqn, decimais=2, obrigatorio=False, nao_negativo=True)
    if not vl_issqn_valido:
        return None
    
    # COD_OBS: opcional condicional, até 6 caracteres
    if cod_obs and len(cod_obs) > 6:
        return None
    
    # Validações condicionais baseadas nos dois últimos dígitos do CST_ICMS
    # Para CST_ICMS terminando em 30, 40, 41, 50 ou 60: VL_BC_ICMS, ALIQ_ICMS e VL_ICMS devem ser 0
    if cst_icms_ultimos_2 in ["30", "40", "41", "50", "60"]:
        vl_bc_icms_valido, vl_bc_icms_float, _ = validar_valor_numerico(vl_bc_icms, decimais=2, obrigatorio=True, nao_negativo=True)
        if not vl_bc_icms_valido or abs(vl_bc_icms_float) > 0.001:
            return None
        
        aliq_icms_valido, aliq_icms_float, _ = validar_valor_numerico(aliq_icms, decimais=2, obrigatorio=True, nao_negativo=True)
        if not aliq_icms_valido or abs(aliq_icms_float) > 0.001:
            return None
        
        vl_icms_valido, vl_icms_float, _ = validar_valor_numerico(vl_icms, decimais=2, obrigatorio=True, nao_negativo=True)
        if not vl_icms_valido or abs(vl_icms_float) > 0.001:
            return None
    # Para CST_ICMS diferente de 30, 40, 41, 50, 60, 51, 90: VL_BC_ICMS, ALIQ_ICMS e VL_ICMS devem ser > 0
    elif cst_icms_ultimos_2 not in ["51", "90"]:
        vl_bc_icms_valido, vl_bc_icms_float, _ = validar_valor_numerico(vl_bc_icms, decimais=2, obrigatorio=True, positivo=True)
        if not vl_bc_icms_valido:
            return None
        
        aliq_icms_valido, aliq_icms_float, _ = validar_valor_numerico(aliq_icms, decimais=2, obrigatorio=True, positivo=True)
        if not aliq_icms_valido:
            return None
        
        vl_icms_valido, vl_icms_float, _ = validar_valor_numerico(vl_icms, decimais=2, obrigatorio=True, positivo=True)
        if not vl_icms_valido:
            return None
    # Para CST_ICMS terminando em 51 ou 90: VL_BC_ICMS, ALIQ_ICMS e VL_ICMS devem ser >= 0
    else:  # cst_icms_ultimos_2 in ["51", "90"]
        vl_bc_icms_valido, vl_bc_icms_float, _ = validar_valor_numerico(vl_bc_icms, decimais=2, obrigatorio=True, nao_negativo=True)
        if not vl_bc_icms_valido:
            return None
        
        aliq_icms_valido, aliq_icms_float, _ = validar_valor_numerico(aliq_icms, decimais=2, obrigatorio=True, nao_negativo=True)
        if not aliq_icms_valido:
            return None
        
        vl_icms_valido, vl_icms_float, _ = validar_valor_numerico(vl_icms, decimais=2, obrigatorio=True, nao_negativo=True)
        if not vl_icms_valido:
            return None
    
    # Formatação de valores monetários
    def formatar_valor_monetario(valor_float):
        if valor_float is None:
            return ""
        return f"R$ {valor_float:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
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
        "CST_ICMS": {
            "titulo": "Código da Situação Tributária, conforme a Tabela indicada no item 4.3.1",
            "valor": cst_icms
        },
        "CFOP": {
            "titulo": "Código Fiscal de Operação e Prestação",
            "valor": cfop
        },
        "ALIQ_ICMS": {
            "titulo": "Alíquota do ICMS",
            "valor": aliq_icms if aliq_icms else "",
            "valor_formatado": formatar_percentual(aliq_icms_float) if aliq_icms else ""
        },
        "VL_OPR": {
            "titulo": "Valor da operação correspondente à combinação de CST_ICMS, CFOP, e alíquota do ICMS, incluídas as despesas acessórias e acréscimos",
            "valor": vl_opr,
            "valor_formatado": formatar_valor_monetario(vl_opr_float)
        },
        "VL_BC_ISSQN": {
            "titulo": "Valor da base de cálculo do ISSQN",
            "valor": vl_bc_issqn if vl_bc_issqn else "",
            "valor_formatado": formatar_valor_monetario(vl_bc_issqn_float) if vl_bc_issqn else ""
        },
        "ALIQ_ISSQN": {
            "titulo": "Alíquota do ISSQN",
            "valor": aliq_issqn if aliq_issqn else "",
            "valor_formatado": formatar_percentual(aliq_issqn_float) if aliq_issqn else ""
        },
        "VL_ISSQN": {
            "titulo": "Valor do ISSQN",
            "valor": vl_issqn if vl_issqn else "",
            "valor_formatado": formatar_valor_monetario(vl_issqn_float) if vl_issqn else ""
        },
        "VL_BC_ICMS": {
            "titulo": "Base de cálculo do ICMS acumulada relativa à alíquota informada",
            "valor": vl_bc_icms if vl_bc_icms else "",
            "valor_formatado": formatar_valor_monetario(vl_bc_icms_float) if vl_bc_icms else ""
        },
        "VL_ICMS": {
            "titulo": "Valor do ICMS acumulado relativo à alíquota informada",
            "valor": vl_icms if vl_icms else "",
            "valor_formatado": formatar_valor_monetario(vl_icms_float) if vl_icms else ""
        },
        "COD_OBS": {
            "titulo": "Código da observação do lançamento fiscal (campo 02 do Registro 0460)",
            "valor": cod_obs if cod_obs else ""
        }
    }
    
    return resultado


def validar_d390_fiscal(linhas):
    """
    Valida uma ou mais linhas do registro D390 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |D390|CST_ICMS|CFOP|ALIQ_ICMS|VL_OPR|VL_BC_ISSQN|ALIQ_ISSQN|VL_ISSQN|VL_BC_ICMS|VL_ICMS|COD_OBS|
        
    Returns:
        String JSON com array de objetos contendo os campos validados.
        Cada objeto tem a estrutura {"CAMPO": {"titulo": "...", "valor": "...", "valor_formatado": "..."}}.
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
        resultado = _processar_linha_d390(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
