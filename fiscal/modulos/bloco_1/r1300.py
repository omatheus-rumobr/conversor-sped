import re
import json
from datetime import datetime


def _validar_data(data_str):
    """
    Valida se a data está no formato ddmmaaaa e se é uma data válida.
    
    Args:
        data_str: String com data no formato ddmmaaaa
        
    Returns:
        tuple: (True/False, datetime object ou None)
    """
    if not data_str or len(data_str) != 8 or not data_str.isdigit():
        return False, None
    
    try:
        dia = int(data_str[:2])
        mes = int(data_str[2:4])
        ano = int(data_str[4:8])
        data_obj = datetime(ano, mes, dia)
        return True, data_obj
    except ValueError:
        return False, None


def _processar_linha_1300(linha):
    """
    Processa uma única linha do registro 1300 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |1300|COD_ITEM|DT_FECH|ESTQ_ABERT|VOL_ENTR|VOL_DISP|VOL_SAIDAS|ESTQ_ESCR|VAL_AJ_PERDA|VAL_AJ_GANHO|FECH_FISICO|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |1300|...|)
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
    if reg != "1300":
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
    cod_item = obter_campo(1)
    dt_fech = obter_campo(2)
    estq_abert = obter_campo(3)
    vol_entr = obter_campo(4)
    vol_disp = obter_campo(5)
    vol_saidas = obter_campo(6)
    estq_escr = obter_campo(7)
    val_aj_perda = obter_campo(8)
    val_aj_ganho = obter_campo(9)
    fech_fisico = obter_campo(10)
    
    # Validações básicas dos campos obrigatórios
    # COD_ITEM: obrigatório, até 60 caracteres
    if not cod_item or len(cod_item) > 60:
        return None
    
    # DT_FECH: obrigatório, formato DDMMAAAA
    if not dt_fech:
        return None
    dt_fech_valida, dt_fech_obj = _validar_data(dt_fech)
    if not dt_fech_valida:
        return None
    
    # ESTQ_ABERT: obrigatório, numérico com 3 decimais
    if not estq_abert:
        return None
    try:
        estq_abert_float = float(estq_abert)
        # Verifica se tem mais de 3 casas decimais
        partes_decimal = estq_abert.split('.')
        if len(partes_decimal) == 2 and len(partes_decimal[1]) > 3:
            return None
    except ValueError:
        return None
    
    # VOL_ENTR: obrigatório, numérico com 3 decimais
    if not vol_entr:
        return None
    try:
        vol_entr_float = float(vol_entr)
        # Verifica se tem mais de 3 casas decimais
        partes_decimal = vol_entr.split('.')
        if len(partes_decimal) == 2 and len(partes_decimal[1]) > 3:
            return None
    except ValueError:
        return None
    
    # VOL_DISP: obrigatório, numérico com 3 decimais
    if not vol_disp:
        return None
    try:
        vol_disp_float = float(vol_disp)
        # Verifica se tem mais de 3 casas decimais
        partes_decimal = vol_disp.split('.')
        if len(partes_decimal) == 2 and len(partes_decimal[1]) > 3:
            return None
    except ValueError:
        return None
    
    # Validação: VOL_DISP deve ser igual a ESTQ_ABERT + VOL_ENTR
    vol_disp_calculado = estq_abert_float + vol_entr_float
    # Usa uma tolerância pequena para comparação de ponto flutuante
    if abs(vol_disp_float - vol_disp_calculado) > 0.001:
        return None
    
    # VOL_SAIDAS: obrigatório, numérico com 3 decimais
    if not vol_saidas:
        return None
    try:
        vol_saidas_float = float(vol_saidas)
        # Verifica se tem mais de 3 casas decimais
        partes_decimal = vol_saidas.split('.')
        if len(partes_decimal) == 2 and len(partes_decimal[1]) > 3:
            return None
    except ValueError:
        return None
    
    # ESTQ_ESCR: obrigatório, numérico com 3 decimais
    if not estq_escr:
        return None
    try:
        estq_escr_float = float(estq_escr)
        # Verifica se tem mais de 3 casas decimais
        partes_decimal = estq_escr.split('.')
        if len(partes_decimal) == 2 and len(partes_decimal[1]) > 3:
            return None
    except ValueError:
        return None
    
    # Validação: ESTQ_ESCR deve ser igual a VOL_DISP - VOL_SAIDAS
    estq_escr_calculado = vol_disp_float - vol_saidas_float
    # Usa uma tolerância pequena para comparação de ponto flutuante
    if abs(estq_escr_float - estq_escr_calculado) > 0.001:
        return None
    
    # VAL_AJ_PERDA: obrigatório, numérico com 3 decimais
    if not val_aj_perda:
        return None
    try:
        val_aj_perda_float = float(val_aj_perda)
        # Verifica se tem mais de 3 casas decimais
        partes_decimal = val_aj_perda.split('.')
        if len(partes_decimal) == 2 and len(partes_decimal[1]) > 3:
            return None
    except ValueError:
        return None
    
    # VAL_AJ_GANHO: obrigatório, numérico com 3 decimais
    if not val_aj_ganho:
        return None
    try:
        val_aj_ganho_float = float(val_aj_ganho)
        # Verifica se tem mais de 3 casas decimais
        partes_decimal = val_aj_ganho.split('.')
        if len(partes_decimal) == 2 and len(partes_decimal[1]) > 3:
            return None
    except ValueError:
        return None
    
    # FECH_FISICO: obrigatório, numérico com 3 decimais
    if not fech_fisico:
        return None
    try:
        fech_fisico_float = float(fech_fisico)
        # Verifica se tem mais de 3 casas decimais
        partes_decimal = fech_fisico.split('.')
        if len(partes_decimal) == 2 and len(partes_decimal[1]) > 3:
            return None
    except ValueError:
        return None
    
    # Formatação de valores para exibição
    def formatar_volume(valor_str):
        try:
            valor_float = float(valor_str)
            # Formata com até 3 casas decimais
            return f"{valor_float:,.3f}".rstrip('0').rstrip('.').replace(',', 'X').replace('.', ',').replace('X', '.')
        except ValueError:
            return valor_str
    
    # Formatação de data para exibição
    def formatar_data(data_str):
        if len(data_str) == 8 and data_str.isdigit():
            return f"{data_str[:2]}/{data_str[2:4]}/{data_str[4:8]}"
        return data_str
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "COD_ITEM": {
            "titulo": "Código do Produto, constante do registro 0200",
            "valor": cod_item
        },
        "DT_FECH": {
            "titulo": "Data do fechamento da movimentação",
            "valor": dt_fech,
            "valor_formatado": formatar_data(dt_fech)
        },
        "ESTQ_ABERT": {
            "titulo": "Estoque no início do dia, em litros",
            "valor": estq_abert,
            "valor_formatado": formatar_volume(estq_abert)
        },
        "VOL_ENTR": {
            "titulo": "Volume Recebido no dia (em litros)",
            "valor": vol_entr,
            "valor_formatado": formatar_volume(vol_entr)
        },
        "VOL_DISP": {
            "titulo": "Volume Disponível (ESTQ_ABERT + VOL_ENTR), em litros",
            "valor": vol_disp,
            "valor_formatado": formatar_volume(vol_disp)
        },
        "VOL_SAIDAS": {
            "titulo": "Volume Total das Saídas, em litros",
            "valor": vol_saidas,
            "valor_formatado": formatar_volume(vol_saidas)
        },
        "ESTQ_ESCR": {
            "titulo": "Estoque Escritural (VOL_DISP - VOL_SAIDAS), litros",
            "valor": estq_escr,
            "valor_formatado": formatar_volume(estq_escr)
        },
        "VAL_AJ_PERDA": {
            "titulo": "Valor da Perda, em litros",
            "valor": val_aj_perda,
            "valor_formatado": formatar_volume(val_aj_perda)
        },
        "VAL_AJ_GANHO": {
            "titulo": "Valor do ganho, em litros",
            "valor": val_aj_ganho,
            "valor_formatado": formatar_volume(val_aj_ganho)
        },
        "FECH_FISICO": {
            "titulo": "Estoque de Fechamento, em litros",
            "valor": fech_fisico,
            "valor_formatado": formatar_volume(fech_fisico)
        }
    }
    
    return resultado


def validar_1300(linhas):
    """
    Valida uma ou mais linhas do registro 1300 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |1300|COD_ITEM|DT_FECH|ESTQ_ABERT|VOL_ENTR|VOL_DISP|VOL_SAIDAS|ESTQ_ESCR|VAL_AJ_PERDA|VAL_AJ_GANHO|FECH_FISICO|
        
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
        resultado = _processar_linha_1300(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
