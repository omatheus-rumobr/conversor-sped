import json


def _processar_linha_c110(linha):
    """
    Processa uma única linha do registro C110 e retorna um dicionário.
    
    Formato:
      |C110|COD_INF|TXT_COMPL|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "C110"
    - COD_INF: obrigatório, código da informação complementar do documento fiscal (6 caracteres)
      - Validação: o valor informado deve existir no registro 0450 - Tabela de informação complementar (validação em camada superior)
    - TXT_COMPL: opcional, descrição complementar do código de referência (texto livre)
    
    Nota: Este registro tem por objetivo identificar os dados contidos no campo Informações Complementares
    da Nota Fiscal, que sejam de interesse do Fisco ou conforme disponha a legislação, e que estejam
    explicitamente citadas no documento Fiscal, tais como: forma de pagamento, local da prestação/execução
    do serviço, operação realizada com suspensão das contribuições sociais, etc.
    
    Não podem ser informados para um mesmo documento fiscal, dois ou mais registros com o mesmo conteúdo
    no campo COD_INF (validação em camada superior).
    
    Devem ser observadas para este registro as observações constantes no registro pai (C100).
    
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
    # Remove primeiro e último se vazios (formato padrão SPED: |C110|...|)
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
    if reg != "C110":
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
    cod_inf = obter_campo(1)
    txt_compl = obter_campo(2)
    
    # Validações básicas dos campos obrigatórios
    
    # COD_INF: obrigatório, código da informação complementar (6 caracteres)
    if not cod_inf or len(cod_inf) != 6:
        return None
    
    # TXT_COMPL: opcional, descrição complementar (texto livre)
    # Não há validação específica além de ser texto livre
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "COD_INF": {
            "titulo": "Código da informação complementar do documento fiscal (campo 02 do Registro 0450)",
            "valor": cod_inf
        },
        "TXT_COMPL": {
            "titulo": "Descrição complementar do código de referência",
            "valor": txt_compl
        }
    }
    
    return resultado


def validar_c110(linhas):
    """
    Valida uma ou mais linhas do registro C110 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |C110|COD_INF|TXT_COMPL|
        
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
        resultado = _processar_linha_c110(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
