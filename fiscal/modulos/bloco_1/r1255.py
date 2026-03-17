import re
import json
from datetime import datetime


def _processar_linha_1255(linha):
    """
    Processa uma única linha do registro 1255 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |1255|COD_MOT_REST_COMPL|VL_CREDITO_ICMS_OP_MOT|VL_ICMS_ST_REST_MOT|VL_FCP_ST_REST_MOT|VL_ICMS_ST_COMPL_MOT|VL_FCP_ST_COMPL_MOT|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |1255|...|)
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
    if reg != "1255":
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
    
    # Extrai todos os campos (7 campos no total)
    cod_mot_rest_compl = obter_campo(1)
    vl_credito_icms_op_mot = obter_campo(2)
    vl_icms_st_rest_mot = obter_campo(3)
    vl_fcp_st_rest_mot = obter_campo(4)
    vl_icms_st_compl_mot = obter_campo(5)
    vl_fcp_st_compl_mot = obter_campo(6)
    
    # Validações básicas dos campos obrigatórios
    # COD_MOT_REST_COMPL: obrigatório, até 5 caracteres
    if not cod_mot_rest_compl or len(cod_mot_rest_compl) > 5:
        return None
    
    # VL_CREDITO_ICMS_OP_MOT: obrigatório, numérico com 2 decimais
    if not vl_credito_icms_op_mot:
        return None
    try:
        vl_credito_icms_op_mot_float = float(vl_credito_icms_op_mot)
        # Verifica se tem mais de 2 casas decimais
        partes_decimal = vl_credito_icms_op_mot.split('.')
        if len(partes_decimal) == 2 and len(partes_decimal[1]) > 2:
            return None
    except ValueError:
        return None
    
    # VL_ICMS_ST_REST_MOT: obrigatório, numérico com 2 decimais
    if not vl_icms_st_rest_mot:
        return None
    try:
        vl_icms_st_rest_mot_float = float(vl_icms_st_rest_mot)
        # Verifica se tem mais de 2 casas decimais
        partes_decimal = vl_icms_st_rest_mot.split('.')
        if len(partes_decimal) == 2 and len(partes_decimal[1]) > 2:
            return None
    except ValueError:
        return None
    
    # VL_FCP_ST_REST_MOT: obrigatório, numérico com 2 decimais
    if not vl_fcp_st_rest_mot:
        return None
    try:
        vl_fcp_st_rest_mot_float = float(vl_fcp_st_rest_mot)
        # Verifica se tem mais de 2 casas decimais
        partes_decimal = vl_fcp_st_rest_mot.split('.')
        if len(partes_decimal) == 2 and len(partes_decimal[1]) > 2:
            return None
    except ValueError:
        return None
    
    # VL_ICMS_ST_COMPL_MOT: obrigatório, numérico com 2 decimais
    if not vl_icms_st_compl_mot:
        return None
    try:
        vl_icms_st_compl_mot_float = float(vl_icms_st_compl_mot)
        # Verifica se tem mais de 2 casas decimais
        partes_decimal = vl_icms_st_compl_mot.split('.')
        if len(partes_decimal) == 2 and len(partes_decimal[1]) > 2:
            return None
    except ValueError:
        return None
    
    # VL_FCP_ST_COMPL_MOT: obrigatório, numérico com 2 decimais
    if not vl_fcp_st_compl_mot:
        return None
    try:
        vl_fcp_st_compl_mot_float = float(vl_fcp_st_compl_mot)
        # Verifica se tem mais de 2 casas decimais
        partes_decimal = vl_fcp_st_compl_mot.split('.')
        if len(partes_decimal) == 2 and len(partes_decimal[1]) > 2:
            return None
    except ValueError:
        return None
    
    # Formatação de valores monetários para exibição
    def formatar_valor(valor_str):
        try:
            valor_float = float(valor_str)
            return f"{valor_float:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        except ValueError:
            return valor_str
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "COD_MOT_REST_COMPL": {
            "titulo": "Código do motivo da restituição ou complementação conforme Tabela 5.7",
            "valor": cod_mot_rest_compl
        },
        "VL_CREDITO_ICMS_OP_MOT": {
            "titulo": "Valor total do ICMS operação própria que o informante tem direito ao crédito, na forma prevista na legislação, referente às hipóteses de restituição em que há previsão deste crédito, para o mesmo COD_MOT_REST_COMPL",
            "valor": vl_credito_icms_op_mot,
            "valor_formatado": formatar_valor(vl_credito_icms_op_mot)
        },
        "VL_ICMS_ST_REST_MOT": {
            "titulo": "Valor total do ICMS ST que o informante tem direito ao crédito, na forma prevista na legislação, referente às hipóteses de restituição em que há previsão deste crédito, para o mesmo COD_MOT_REST_COMPL",
            "valor": vl_icms_st_rest_mot,
            "valor_formatado": formatar_valor(vl_icms_st_rest_mot)
        },
        "VL_FCP_ST_REST_MOT": {
            "titulo": "Valor total do FCP_ST agregado ao valor do ICMS ST informado no campo VL_ICMS_ST_REST_MOT",
            "valor": vl_fcp_st_rest_mot,
            "valor_formatado": formatar_valor(vl_fcp_st_rest_mot)
        },
        "VL_ICMS_ST_COMPL_MOT": {
            "titulo": "Valor total do débito referente ao complemento do imposto, nos casos previstos na legislação, para o mesmo COD_MOT_REST_COMPL",
            "valor": vl_icms_st_compl_mot,
            "valor_formatado": formatar_valor(vl_icms_st_compl_mot)
        },
        "VL_FCP_ST_COMPL_MOT": {
            "titulo": "Valor total do FCP_ST agregado ao valor informado no campo VL_ICMS_ST_COMPL_MOT",
            "valor": vl_fcp_st_compl_mot,
            "valor_formatado": formatar_valor(vl_fcp_st_compl_mot)
        }
    }
    
    return resultado


def validar_1255(linhas):
    """
    Valida uma ou mais linhas do registro 1255 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |1255|COD_MOT_REST_COMPL|VL_CREDITO_ICMS_OP_MOT|VL_ICMS_ST_REST_MOT|VL_FCP_ST_REST_MOT|VL_ICMS_ST_COMPL_MOT|VL_FCP_ST_COMPL_MOT|
        
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
        resultado = _processar_linha_1255(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
