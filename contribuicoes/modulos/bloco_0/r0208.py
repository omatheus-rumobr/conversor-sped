import json


def _processar_linha_0208(linha):
    """
    Processa uma única linha do registro 0208 e retorna um dicionário.
    
    Formato:
      |0208|COD_TAB|COD_GRU|MARCA_COM|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "0208"
    - COD_TAB: obrigatório, valores válidos [01, 02, 03, 04, 05, 06, 07, 08, 09, 10, 11, 12, 13]
      - Valores 01-12: válidos desde o início
      - Valor 13: válido a partir de outubro de 2012
    - COD_GRU: obrigatório, 2 caracteres
      - Para Tabelas I e II: código "SN"
      - Deve existir conforme Anexo III do Decreto nº 6.707/08 (validação externa)
    - MARCA_COM: obrigatório, até 60 caracteres
      - Deve existir conforme Anexo III do Decreto nº 6.707/08 (validação externa)
    
    Nota: Este registro é obrigatório para importadores e pessoas jurídicas que procedam
    à industrialização dos produtos listados no art. 1o do Decreto nº 6.707, de 2008.
    Deve estar vinculado ao código do item (Campo COD_ITEM do Registro 0200).
    Para fatos geradores até 30 de abril de 2015.
    Para períodos a partir de maio de 2015, este registro não precisa mais ser escriturado.
    Estas validações devem ser feitas em uma camada superior.
    
    Args:
        linha: String com uma linha do SPED
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |0208|...|)
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
    if reg != "0208":
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
    cod_tab = obter_campo(1)
    cod_gru = obter_campo(2)
    marca_com = obter_campo(3)
    
    # Validações básicas dos campos obrigatórios
    
    # COD_TAB: obrigatório, valores válidos [01, 02, 03, 04, 05, 06, 07, 08, 09, 10, 11, 12, 13]
    valores_validos_cod_tab = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13"]
    if not cod_tab or cod_tab not in valores_validos_cod_tab:
        return None
    
    # COD_GRU: obrigatório, 2 caracteres
    if not cod_gru or len(cod_gru) != 2:
        return None
    
    # MARCA_COM: obrigatório, até 60 caracteres
    if not marca_com or len(marca_com) > 60:
        return None
    
    # Monta o resultado
    descricoes_cod_tab = {
        "01": "Tabela I",
        "02": "Tabela II",
        "03": "Tabela III",
        "04": "Tabela IV",
        "05": "Tabela V",
        "06": "Tabela VI",
        "07": "Tabela VII",
        "08": "Tabela VIII",
        "09": "Tabela IX",
        "10": "Tabela X",
        "11": "Tabela XI",
        "12": "Tabela XII",
        "13": "Tabela XIII"
    }
    
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "COD_TAB": {
            "titulo": "Código indicador da Tabela de Incidência, conforme Anexo III do Decreto nº 6.707/08",
            "valor": cod_tab,
            "descricao": descricoes_cod_tab.get(cod_tab, "")
        },
        "COD_GRU": {
            "titulo": "Código do grupo, conforme Anexo III do Decreto nº 6.707/08",
            "valor": cod_gru
        },
        "MARCA_COM": {
            "titulo": "Marca Comercial",
            "valor": marca_com
        }
    }
    
    return resultado


def validar_0208(linhas):
    """
    Valida uma ou mais linhas do registro 0208 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |0208|COD_TAB|COD_GRU|MARCA_COM|
        
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
        resultado = _processar_linha_0208(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
