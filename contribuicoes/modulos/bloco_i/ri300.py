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


def _processar_linha_i300(linha):
    """
    Processa uma única linha do registro I300 e retorna um dicionário.
    
    Formato:
      |I300|COD_COMP|DET_VALOR|COD_CTA|INFO_COMPL|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "I300"
    - COD_COMP: obrigatório, código das Tabelas 7.1.3 e/ou 7.1.4 (máximo 60 caracteres)
      - Tabela 7.1.3 (Receitas – Visão Analítica/Referenciada), no caso de informações referentes a receitas
      - Tabela 7.1.4 (Deduções e Exclusões – Visão Analítica/Referenciada), no caso de informações referentes a deduções ou exclusões
    - DET_VALOR: obrigatório, valor da receita, dedução ou exclusão (numérico, 2 decimais)
    - COD_CTA: opcional, código da conta contábil (máximo 255 caracteres)
      - Opcional para fatos geradores até outubro de 2017
      - Obrigatório para fatos geradores a partir de novembro de 2017, exceto se a pessoa jurídica
        estiver dispensada de escrituração contábil (ECD)
    - INFO_COMPL: opcional, informação complementar (texto livre)
    
    Nota: Registro específico para o detalhamento do valor da receita, dedução ou exclusão, informada
    de forma consolidada no Registro Pai I200, de preenchimento a partir do período de apuração Janeiro de 2014.
    
    O valor da receita ou dedução, conforme o caso, informado no Campo 04 do registro pai I200, deve
    corresponder ao somatório dos valores informados no Campo 03 dos registros filhos I300, correspondentes.
    Ou seja, a escrituração dos valores informados no registro I300 vem a ser, tão somente, a demonstração
    num nível mais analítico, mais detalhado (conforme codificação constante nas diversas tabelas analíticas
    7.1.3 e/ou 7.1.4), dos valores informados de forma sintética no registro I200.
    
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
    # Remove primeiro e último se vazios (formato padrão SPED: |I300|...|)
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
    if reg != "I300":
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
    cod_comp = obter_campo(1)
    det_valor = obter_campo(2)
    cod_cta = obter_campo(3)
    info_compl = obter_campo(4)
    
    # Validações básicas dos campos obrigatórios
    
    # COD_COMP: obrigatório, código das Tabelas 7.1.3 e/ou 7.1.4 (máximo 60 caracteres)
    if not cod_comp or len(cod_comp) > 60:
        return None
    
    # DET_VALOR: obrigatório, valor da receita, dedução ou exclusão (numérico, 2 decimais)
    ok1, val1, _ = validar_valor_numerico(det_valor, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok1:
        return None
    
    # COD_CTA: opcional, código da conta contábil (máximo 255 caracteres)
    if cod_cta and len(cod_cta) > 255:
        return None
    
    # INFO_COMPL: opcional, informação complementar (texto livre)
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
        "COD_COMP": {
            "titulo": "Código das Tabelas 7.1.3 (Receitas – Visão Analítica/Referenciada) e/ou 7.1.4 (Deduções e exclusões – Visão Analítica/Referenciada), objeto de complemento neste registro",
            "valor": cod_comp
        },
        "DET_VALOR": {
            "titulo": "Valor da receita, dedução ou exclusão, objeto de complemento/detalhamento neste registro, conforme código informado no campo 02 (especificados nas tabelas analíticas 7.1.3 e 7.1.4) ou no campo 04 (código da conta contábil)",
            "valor": det_valor,
            "valor_formatado": fmt_valor(val1)
        },
        "COD_CTA": {
            "titulo": "Código da conta contábil referente ao valor informado no campo 03",
            "valor": cod_cta
        },
        "INFO_COMPL": {
            "titulo": "Informação Complementar dos dados informados no registro",
            "valor": info_compl
        }
    }
    
    return resultado


def validar_i300(linhas):
    """
    Valida uma ou mais linhas do registro I300 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |I300|COD_COMP|DET_VALOR|COD_CTA|INFO_COMPL|
        
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
        resultado = _processar_linha_i300(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
