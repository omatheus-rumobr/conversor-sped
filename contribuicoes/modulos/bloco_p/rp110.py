import json


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
    if valor_str is None:
        valor_str = ""

    if not valor_str:
        if obrigatorio:
            return False, None, "Campo obrigatório não preenchido"
        return True, 0.0, None

    try:
        valor_float = float(valor_str)

        # Verifica precisão decimal (quando houver ponto decimal)
        partes_decimal = valor_str.split(".")
        if len(partes_decimal) == 2 and len(partes_decimal[1]) > decimais:
            return False, None, f"Valor com mais de {decimais} casas decimais"

        if positivo and valor_float <= 0:
            return False, None, "Valor deve ser maior que zero"
        if nao_negativo and valor_float < 0:
            return False, None, "Valor não pode ser negativo"

        return True, valor_float, None
    except ValueError:
        return False, None, "Valor não é numérico válido"


def _processar_linha_p110(linha):
    """
    Processa uma única linha do registro P110 e retorna um dicionário.
    
    Formato:
      |P110|NUM_CAMPO|COD_DET|DET_VALOR|INF_COMPL|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "P110"
    - NUM_CAMPO: obrigatório, número do campo do registro "P100" objeto de detalhamento (2 caracteres)
    - COD_DET: opcional, código do tipo de detalhamento conforme Tabela 5.1.2 (8 caracteres)
    - DET_VALOR: obrigatório, valor detalhado referente ao campo 02 deste registro (numérico, 2 decimais)
    - INF_COMPL: opcional, informação complementar do detalhamento (texto livre)
    
    Nota: Registro de preenchimento opcional pela pessoa jurídica, tendo por objetivo detalhar de forma
    analítica as informações consolidadas constantes no Registro Pai (P100), com base em quaisquer dos
    critérios definidos na Tabela "5.1.2 – Códigos de Detalhamento da Apuração da Contribuição".
    
    O somatório dos valores informados no Campo "04" (DET_VALOR) dos diversos registros "P110" não
    poderá ser MAIOR que o valor constante no Registro "P100", a que se refere o Campo "02" do registro "P110".
    
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
    # Remove primeiro e último se vazios (formato padrão SPED: |P110|...|)
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
    if reg != "P110":
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
    num_campo = obter_campo(1)
    cod_det = obter_campo(2)
    det_valor = obter_campo(3)
    inf_compl = obter_campo(4)
    
    # Validações básicas dos campos obrigatórios
    
    # NUM_CAMPO: obrigatório, número do campo do registro "P100" (2 caracteres)
    # Valida que é um número de campo válido (formato numérico de 2 dígitos)
    if not num_campo or len(num_campo) != 2 or not num_campo.isdigit():
        return None
    
    # COD_DET: opcional, código do tipo de detalhamento conforme Tabela 5.1.2 (8 caracteres)
    if cod_det and len(cod_det) != 8:
        return None
    
    # DET_VALOR: obrigatório, valor detalhado (numérico, 2 decimais)
    ok1, val1, _ = validar_valor_numerico(det_valor, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok1:
        return None
    
    # INF_COMPL: opcional, informação complementar (texto livre)
    # Não há validação específica além de ser texto livre
    
    # Função auxiliar para formatar valores monetários
    def fmt_valor(v):
        if v is None:
            return ""
        return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "NUM_CAMPO": {
            "titulo": "Informar o número do campo do registro \"P100\", objeto de detalhamento neste registro",
            "valor": num_campo
        },
        "COD_DET": {
            "titulo": "Código do tipo de detalhamento, conforme Tabela 5.1.2",
            "valor": cod_det
        },
        "DET_VALOR": {
            "titulo": "Valor detalhado referente ao campo 02 deste registro",
            "valor": det_valor,
            "valor_formatado": fmt_valor(val1)
        },
        "INF_COMPL": {
            "titulo": "Informação complementar do detalhamento",
            "valor": inf_compl
        }
    }
    
    return resultado


def validar_p110(linhas):
    """
    Valida uma ou mais linhas do registro P110 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |P110|NUM_CAMPO|COD_DET|DET_VALOR|INF_COMPL|
        
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
        resultado = _processar_linha_p110(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
