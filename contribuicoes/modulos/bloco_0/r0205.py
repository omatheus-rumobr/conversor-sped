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


def _processar_linha_0205(linha, dt_fin_0000=None):
    """
    Processa uma única linha do registro 0205 e retorna um dicionário.
    
    Formato:
      |0205|DESCR_ANT_ITEM|DT_INI|DT_FIN|COD_ANT_ITEM|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "0205"
    - DESCR_ANT_ITEM: opcional, descrição anterior do item
    - DT_INI: obrigatório, formato ddmmaaaa, data válida
    - DT_FIN: obrigatório, formato ddmmaaaa, data válida
      - Deve ser menor que DT_FIN do registro 0000 (quando informado)
      - Deve ser maior ou igual a DT_INI
    - COD_ANT_ITEM: opcional, até 60 caracteres
    
    Nota: Este registro informa alterações ocorridas na descrição do produto.
    Não podem ser informados dois ou mais registros com sobreposição de períodos.
    Esta validação deve ser feita em uma camada superior.
    
    Args:
        linha: String com uma linha do SPED
        dt_fin_0000: Data final (ddmmaaaa) do registro 0000 (opcional, para validação)
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |0205|...|)
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
    if reg != "0205":
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
    
    # Extrai todos os campos (5 campos no total)
    descr_ant_item = obter_campo(1)
    dt_ini = obter_campo(2)
    dt_fin = obter_campo(3)
    cod_ant_item = obter_campo(4)
    
    # Validações básicas dos campos obrigatórios
    
    # DESCR_ANT_ITEM: opcional, sem validação específica
    
    # DT_INI: obrigatório, formato ddmmaaaa, data válida
    dt_ini_valida, dt_ini_obj = _validar_data(dt_ini)
    if not dt_ini_valida:
        return None
    
    # DT_FIN: obrigatório, formato ddmmaaaa, data válida
    dt_fin_valida, dt_fin_obj = _validar_data(dt_fin)
    if not dt_fin_valida:
        return None
    
    # DT_FIN deve ser >= DT_INI
    if dt_ini_obj and dt_fin_obj and dt_fin_obj < dt_ini_obj:
        return None
    
    # DT_FIN deve ser menor que DT_FIN do registro 0000 (quando informado)
    if dt_fin_0000:
        ok_0000_fin, dt_fin_0000_obj = _validar_data(dt_fin_0000)
        if ok_0000_fin and dt_fin_obj:
            if dt_fin_obj >= dt_fin_0000_obj:
                return None
    
    # COD_ANT_ITEM: opcional, até 60 caracteres
    if cod_ant_item and len(cod_ant_item) > 60:
        return None
    
    # Função auxiliar para formatar data
    def fmt_data(d):
        return d.strftime("%d/%m/%Y") if d else ""
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "DT_INI": {
            "titulo": "Data inicial de utilização da descrição do item",
            "valor": dt_ini,
            "valor_formatado": fmt_data(dt_ini_obj)
        },
        "DT_FIN": {
            "titulo": "Data final de utilização da descrição do item",
            "valor": dt_fin,
            "valor_formatado": fmt_data(dt_fin_obj)
        }
    }
    
    # DESCR_ANT_ITEM: opcional
    if descr_ant_item:
        resultado["DESCR_ANT_ITEM"] = {
            "titulo": "Descrição anterior do item",
            "valor": descr_ant_item
        }
    else:
        resultado["DESCR_ANT_ITEM"] = {
            "titulo": "Descrição anterior do item",
            "valor": ""
        }
    
    # COD_ANT_ITEM: opcional
    if cod_ant_item:
        resultado["COD_ANT_ITEM"] = {
            "titulo": "Código anterior do item com relação à última informação apresentada",
            "valor": cod_ant_item
        }
    else:
        resultado["COD_ANT_ITEM"] = {
            "titulo": "Código anterior do item com relação à última informação apresentada",
            "valor": ""
        }
    
    return resultado


def validar_0205(linhas, dt_fin_0000=None):
    """
    Valida uma ou mais linhas do registro 0205 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |0205|DESCR_ANT_ITEM|DT_INI|DT_FIN|COD_ANT_ITEM|
        dt_fin_0000: Data final (ddmmaaaa) do registro 0000 (opcional, para validação)
        
    Returns:
        String JSON com array de objetos contendo os campos validados.
        Cada objeto tem a estrutura {"CAMPO": {"titulo": "...", "valor": "..."}}.
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
        resultado = _processar_linha_0205(linha, dt_fin_0000=dt_fin_0000)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
