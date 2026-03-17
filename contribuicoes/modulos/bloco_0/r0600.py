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


def _processar_linha_0600(linha, dt_fin_0000=None):
    """
    Processa uma única linha do registro 0600 e retorna um dicionário.
    
    Formato:
      |0600|DT_ALT|COD_CCUS|CCUS|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "0600"
    - DT_ALT: obrigatório, formato ddmmaaaa, data válida
      - Não pode ser maior que DT_FIN do registro 0000 (quando informado)
    - COD_CCUS: obrigatório, até 255 caracteres
    - CCUS: obrigatório, até 60 caracteres
    
    Nota: Não podem ser informados dois ou mais registros com a mesma combinação
    de conteúdo nos campos DT_ALT e COD_CCUS.
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
    # Remove primeiro e último se vazios (formato padrão SPED: |0600|...|)
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
    if reg != "0600":
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
    
    # Extrai todos os campos (4 campos no total)
    dt_alt = obter_campo(1)
    cod_ccus = obter_campo(2)
    ccus = obter_campo(3)
    
    # Validações básicas dos campos obrigatórios
    
    # DT_ALT: obrigatório, formato ddmmaaaa, data válida
    dt_alt_valida, dt_alt_obj = _validar_data(dt_alt)
    if not dt_alt_valida:
        return None
    
    # DT_ALT não pode ser maior que DT_FIN do registro 0000 (quando informado)
    if dt_fin_0000:
        ok_0000_fin, dt_fin_0000_obj = _validar_data(dt_fin_0000)
        if ok_0000_fin and dt_alt_obj:
            if dt_alt_obj > dt_fin_0000_obj:
                return None
    
    # COD_CCUS: obrigatório, até 255 caracteres
    if not cod_ccus or len(cod_ccus) > 255:
        return None
    
    # CCUS: obrigatório, até 60 caracteres
    if not ccus or len(ccus) > 60:
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
        "DT_ALT": {
            "titulo": "Data da inclusão/alteração",
            "valor": dt_alt,
            "valor_formatado": fmt_data(dt_alt_obj)
        },
        "COD_CCUS": {
            "titulo": "Código do centro de custos",
            "valor": cod_ccus
        },
        "CCUS": {
            "titulo": "Nome do centro de custos",
            "valor": ccus
        }
    }
    
    return resultado


def validar_0600(linhas, dt_fin_0000=None):
    """
    Valida uma ou mais linhas do registro 0600 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |0600|DT_ALT|COD_CCUS|CCUS|
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
        resultado = _processar_linha_0600(linha, dt_fin_0000=dt_fin_0000)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
