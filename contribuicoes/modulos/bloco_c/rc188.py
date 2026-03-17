import json


def _processar_linha_c188(linha):
    """
    Processa uma única linha do registro C188 e retorna um dicionário.
    
    Formato:
      |C188|NUM_PROC|IND_PROC|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "C188"
    - NUM_PROC: obrigatório, identificação do processo ou ato concessório (máximo 20 caracteres)
      - Informar o número do processo judicial ou do processo administrativo, conforme o caso,
        que autoriza a adoção de procedimento especifico de apuração das contribuições sociais
        ou dos créditos
    - IND_PROC: obrigatório, indicador da origem do processo (1 dígito)
      - Valores válidos: [1, 3, 9]
      - 1: Justiça Federal
      - 3: Secretaria da Receita Federal do Brasil
      - 9: Outros
    
    Nota: Registro específico para a pessoa jurídica informar a existência de processo administrativo
    ou judicial que autoriza a adoção de tratamento tributário (CST), base de cálculo ou alíquota
    diversa da prevista na legislação. Trata-se de informação essencial a ser prestada na escrituração
    para a adequada validação das contribuições sociais ou dos créditos.
    
    Uma vez procedida à escrituração do Registro "C188", deve a pessoa jurídica gerar os registros
    "1010" ou "1020" referentes ao detalhamento do processo judicial ou do processo administrativo,
    conforme o caso, que autoriza a adoção de procedimento especifico de apuração das contribuições
    sociais ou dos créditos.
    
    Devem ser relacionados todos os processos judiciais ou administrativos que fundamente ou autorize
    a adoção de procedimento especifico na apuração das contribuições sociais e dos créditos.
    
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
    # Remove primeiro e último se vazios (formato padrão SPED: |C188|...|)
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
    if reg != "C188":
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
    num_proc = obter_campo(1)
    ind_proc = obter_campo(2)
    
    # Validações básicas dos campos obrigatórios
    
    # NUM_PROC: obrigatório, máximo 20 caracteres
    if not num_proc or len(num_proc) > 20:
        return None
    
    # IND_PROC: obrigatório, valores válidos [1, 3, 9]
    ind_proc_validos = ["1", "3", "9"]
    if not ind_proc or ind_proc not in ind_proc_validos:
        return None
    
    # Descrições dos campos
    descricoes_ind_proc = {
        "1": "Justiça Federal",
        "3": "Secretaria da Receita Federal do Brasil",
        "9": "Outros"
    }
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "NUM_PROC": {
            "titulo": "Identificação do processo ou ato concessório",
            "valor": num_proc
        },
        "IND_PROC": {
            "titulo": "Indicador da origem do processo",
            "valor": ind_proc,
            "descricao": descricoes_ind_proc.get(ind_proc, "")
        }
    }
    
    return resultado


def validar_c188(linhas):
    """
    Valida uma ou mais linhas do registro C188 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |C188|NUM_PROC|IND_PROC|
        
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
        resultado = _processar_linha_c188(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
