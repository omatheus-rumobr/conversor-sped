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


def _processar_linha_i200(linha):
    """
    Processa uma única linha do registro I200 e retorna um dicionário.
    
    Formato:
      |I200|NUM_CAMPO|COD_DET|DET_VALOR|COD_CTA|INFO_COMPL|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "I200"
    - NUM_CAMPO: obrigatório, número do campo do registro "I100" (Campos 02, 04 ou 05)
      - Valores válidos: ["02", "04", "05"]
    - COD_DET: obrigatório, código do tipo de detalhamento conforme Tabelas 7.1.1 e/ou 7.1.2 (5 caracteres)
    - DET_VALOR: obrigatório, valor detalhado referente ao campo 03 (COD_DET) (numérico, 2 decimais)
    - COD_CTA: opcional, código da conta contábil (máximo 255 caracteres)
      - Opcional para fatos geradores até outubro de 2017
      - Obrigatório para fatos geradores a partir de novembro de 2017, exceto se a pessoa jurídica
        estiver dispensada de escrituração contábil (ECD)
    - INFO_COMPL: opcional, informação complementar (texto livre)
    
    Nota: Registro específico para a identificação e o detalhamento dos valores informados nos campos
    02, 04 e 05 do Registro I100. Deve ser preenchido um registro para cada tipo de receita e/ou
    deduções e exclusões, codificadas nas Tabelas 7.1.1 e 7.1.2, conforme o caso.
    
    O somatório dos valores informados no Registro I200 deve corresponder aos valores totais de
    receitas, deduções gerais ou deduções específicas, escriturados nos campos 02, 04 e 05, do
    registro I100, respectivamente.
    
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
    # Remove primeiro e último se vazios (formato padrão SPED: |I200|...|)
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
    if reg != "I200":
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
    
    # Extrai todos os campos (6 campos no total)
    num_campo = obter_campo(1)
    cod_det = obter_campo(2)
    det_valor = obter_campo(3)
    cod_cta = obter_campo(4)
    info_compl = obter_campo(5)
    
    # Validações básicas dos campos obrigatórios
    
    # NUM_CAMPO: obrigatório, valores válidos ["02", "04", "05"]
    num_campo_validos = ["02", "04", "05"]
    if not num_campo or num_campo not in num_campo_validos:
        return None
    
    # COD_DET: obrigatório, código do tipo de detalhamento (5 caracteres)
    if not cod_det or len(cod_det) != 5:
        return None
    
    # DET_VALOR: obrigatório, valor detalhado (numérico, 2 decimais)
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
    
    # Descrições dos campos
    descricoes_num_campo = {
        "02": "Campo 02 do registro I100 - Valor Total do Faturamento/Receita Bruta no Período",
        "04": "Campo 04 do registro I100 - Valor Total das Deduções e Exclusões de Caráter Geral",
        "05": "Campo 05 do registro I100 - Valor Total das Deduções e Exclusões de Caráter Específico"
    }
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "NUM_CAMPO": {
            "titulo": "Informar o número do campo do registro \"I100\" (Campos 02, 04 ou 05), objeto de informação neste registro",
            "valor": num_campo,
            "descricao": descricoes_num_campo.get(num_campo, "")
        },
        "COD_DET": {
            "titulo": "Código do tipo de detalhamento, conforme Tabelas 7.1.1 e/ou 7.1.2",
            "valor": cod_det
        },
        "DET_VALOR": {
            "titulo": "Valor detalhado referente ao campo 03 (COD_DET) deste registro",
            "valor": det_valor,
            "valor_formatado": fmt_valor(val1)
        },
        "COD_CTA": {
            "titulo": "Código da conta contábil referente ao valor informado no campo 04 (DET_VALOR)",
            "valor": cod_cta
        },
        "INFO_COMPL": {
            "titulo": "Informação Complementar dos dados informados no registro",
            "valor": info_compl
        }
    }
    
    return resultado


def validar_i200(linhas):
    """
    Valida uma ou mais linhas do registro I200 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |I200|NUM_CAMPO|COD_DET|DET_VALOR|COD_CTA|INFO_COMPL|
        
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
        resultado = _processar_linha_i200(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
