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


def _validar_periodo_fiscal(periodo_str):
    """
    Valida se o período fiscal está no formato mmaaaa e se é válido.
    
    Args:
        periodo_str: String com período no formato mmaaaa
        
    Returns:
        tuple: (True/False, dict com mes e ano ou None)
    """
    if not periodo_str or len(periodo_str) != 6 or not periodo_str.isdigit():
        return False, None
    
    try:
        mes = int(periodo_str[:2])
        ano = int(periodo_str[2:6])
        
        # Valida mês (1-12)
        if mes < 1 or mes > 12:
            return False, None
        
        # Valida ano (deve ser razoável, por exemplo entre 1900 e 2100)
        if ano < 1900 or ano > 2100:
            return False, None
        
        return True, {"mes": mes, "ano": ano}
    except ValueError:
        return False, None


def _processar_linha_d530(linha):
    """
    Processa uma única linha do registro D530 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |D530|IND_SERV|DT_INI_SERV|DT_FIN_SERV|PER_FISCAL|COD_AREA|TERMINAL|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |D530|...|)
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
    if reg != "D530":
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
    ind_serv = obter_campo(1)
    dt_ini_serv = obter_campo(2)
    dt_fin_serv = obter_campo(3)
    per_fiscal = obter_campo(4)
    cod_area = obter_campo(5)
    terminal = obter_campo(6)
    
    # Validações dos campos obrigatórios
    
    # IND_SERV: obrigatório, valores válidos: ["0", "1", "2", "3", "4", "9"]
    if not ind_serv or ind_serv not in ["0", "1", "2", "3", "4", "9"]:
        return None
    
    # PER_FISCAL: obrigatório, formato mmaaaa (6 dígitos)
    per_fiscal_valido, per_fiscal_dict = _validar_periodo_fiscal(per_fiscal)
    if not per_fiscal_valido:
        return None
    
    # DT_INI_SERV: opcional condicional, formato ddmmaaaa
    dt_ini_serv_valido, dt_ini_serv_obj = None, None
    if dt_ini_serv:
        dt_ini_serv_valido, dt_ini_serv_obj = _validar_data(dt_ini_serv)
        if not dt_ini_serv_valido:
            return None
    
    # DT_FIN_SERV: opcional condicional, formato ddmmaaaa
    dt_fin_serv_valido, dt_fin_serv_obj = None, None
    if dt_fin_serv:
        dt_fin_serv_valido, dt_fin_serv_obj = _validar_data(dt_fin_serv)
        if not dt_fin_serv_valido:
            return None
    
    # Validação: DT_FIN_SERV deve ser maior ou igual a DT_INI_SERV (se ambas estiverem preenchidas)
    if dt_ini_serv_obj and dt_fin_serv_obj:
        if dt_fin_serv_obj < dt_ini_serv_obj:
            return None
    
    # TERMINAL: opcional condicional, numérico
    terminal_valido = True
    terminal_int = None
    if terminal:
        if not terminal.isdigit():
            return None
        try:
            terminal_int = int(terminal)
        except ValueError:
            return None
    
    # Formatação de data
    def formatar_data(data_obj):
        if data_obj is None:
            return ""
        return data_obj.strftime("%d/%m/%Y")
    
    # Formatação de período fiscal
    def formatar_periodo_fiscal(per_dict):
        if per_dict is None:
            return ""
        return f"{per_dict['mes']:02d}/{per_dict['ano']}"
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "IND_SERV": {
            "titulo": "Indicador do tipo de serviço prestado: 0 - Telefonia; 1 - Comunicação de dados; 2 - TV por assinatura; 3 - Provimento de acesso à Internet; 4 - Multimídia; 9 - Outros",
            "valor": ind_serv,
            "descricao": {
                "0": "Telefonia",
                "1": "Comunicação de dados",
                "2": "TV por assinatura",
                "3": "Provimento de acesso à Internet",
                "4": "Multimídia",
                "9": "Outros"
            }.get(ind_serv, "")
        },
        "DT_INI_SERV": {
            "titulo": "Data em que se iniciou a prestação do serviço",
            "valor": dt_ini_serv if dt_ini_serv else "",
            "valor_formatado": formatar_data(dt_ini_serv_obj) if dt_ini_serv_obj else ""
        },
        "DT_FIN_SERV": {
            "titulo": "Data em que se encerrou a prestação do serviço",
            "valor": dt_fin_serv if dt_fin_serv else "",
            "valor_formatado": formatar_data(dt_fin_serv_obj) if dt_fin_serv_obj else ""
        },
        "PER_FISCAL": {
            "titulo": "Período fiscal da prestação do serviço (MMAAAA)",
            "valor": per_fiscal,
            "valor_formatado": formatar_periodo_fiscal(per_fiscal_dict)
        },
        "COD_AREA": {
            "titulo": "Código de área do terminal faturado",
            "valor": cod_area if cod_area else ""
        },
        "TERMINAL": {
            "titulo": "Identificação do terminal faturado",
            "valor": terminal if terminal else ""
        }
    }
    
    return resultado


def validar_d530_fiscal(linhas):
    """
    Valida uma ou mais linhas do registro D530 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |D530|IND_SERV|DT_INI_SERV|DT_FIN_SERV|PER_FISCAL|COD_AREA|TERMINAL|
        
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
        resultado = _processar_linha_d530(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
