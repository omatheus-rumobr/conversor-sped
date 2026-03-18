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


def _processar_linha_1910(linha):
    """
    Processa uma única linha do registro 1910 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |1910|DT_INI|DT_FIN|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |1910|...|)
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
    if reg != "1910":
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
    
    # Extrai todos os campos (3 campos no total)
    dt_ini = obter_campo(1)
    dt_fin = obter_campo(2)
    
    # Validações dos campos obrigatórios
    
    # DT_INI: obrigatório, formato DDMMAAAA
    if not dt_ini:
        return None
    dt_ini_valida, dt_ini_obj = _validar_data(dt_ini)
    if not dt_ini_valida:
        return None
    
    # DT_FIN: obrigatório, formato DDMMAAAA
    if not dt_fin:
        return None
    dt_fin_valida, dt_fin_obj = _validar_data(dt_fin)
    if not dt_fin_valida:
        return None
    
    # Validação: DT_FIN deve ser maior ou igual a DT_INI
    if dt_fin_obj < dt_ini_obj:
        return None
    
    # Formatação de data para exibição
    def formatar_data(data_str):
        if not data_str or len(data_str) != 8:
            return ""
        try:
            return f"{data_str[:2]}/{data_str[2:4]}/{data_str[4:8]}"
        except:
            return data_str
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "DT_INI": {
            "titulo": "Data inicial da sub-apuração",
            "valor": dt_ini,
            "valor_formatado": formatar_data(dt_ini)
        },
        "DT_FIN": {
            "titulo": "Data final da sub-apuração",
            "valor": dt_fin,
            "valor_formatado": formatar_data(dt_fin)
        }
    }
    
    return resultado


def validar_1910_fiscal(linhas):
    """
    Valida uma ou mais linhas do registro 1910 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |1910|DT_INI|DT_FIN|
        
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
        resultado = _processar_linha_1910(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
