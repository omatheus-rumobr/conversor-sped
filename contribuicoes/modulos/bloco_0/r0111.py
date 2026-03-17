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


def _float_igual(a, b, tolerancia=0.01):
    """Compara dois floats com tolerância."""
    if a is None or b is None:
        return False
    return abs(a - b) <= tolerancia


def _processar_linha_0111(linha):
    """
    Processa uma única linha do registro 0111 e retorna um dicionário.
    
    Formato:
      |0111|REC_BRU_NCUM_TRIB_MI|REC_BRU_NCUM_NT_MI|REC_BRU_NCUM_EXP|REC_BRU_CUM|REC_BRU_TOTAL|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "0111"
    - REC_BRU_NCUM_TRIB_MI: obrigatório, numérico com 2 decimais, não negativo
    - REC_BRU_NCUM_NT_MI: obrigatório, numérico com 2 decimais, não negativo
    - REC_BRU_NCUM_EXP: obrigatório, numérico com 2 decimais, não negativo
    - REC_BRU_CUM: obrigatório, numérico com 2 decimais, não negativo
    - REC_BRU_TOTAL: obrigatório, numérico com 2 decimais, não negativo
    - Validação: REC_BRU_TOTAL deve ser igual à soma dos campos 02, 03, 04 e 05
    
    Nota: Este registro é obrigatório quando IND_APRO_CRED do registro 0110 for igual a "2".
    Esta validação deve ser feita em uma camada superior.
    
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
    # Remove primeiro e último se vazios (formato padrão SPED: |0111|...|)
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
    if reg != "0111":
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
    rec_bru_ncum_trib_mi = obter_campo(1)
    rec_bru_ncum_nt_mi = obter_campo(2)
    rec_bru_ncum_exp = obter_campo(3)
    rec_bru_cum = obter_campo(4)
    rec_bru_total = obter_campo(5)
    
    # Validações dos campos obrigatórios (todos numéricos com 2 decimais, não negativos)
    
    # REC_BRU_NCUM_TRIB_MI: obrigatório, numérico com 2 decimais, não negativo
    ok1, val1, _ = validar_valor_numerico(rec_bru_ncum_trib_mi, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok1:
        return None
    
    # REC_BRU_NCUM_NT_MI: obrigatório, numérico com 2 decimais, não negativo
    ok2, val2, _ = validar_valor_numerico(rec_bru_ncum_nt_mi, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok2:
        return None
    
    # REC_BRU_NCUM_EXP: obrigatório, numérico com 2 decimais, não negativo
    ok3, val3, _ = validar_valor_numerico(rec_bru_ncum_exp, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok3:
        return None
    
    # REC_BRU_CUM: obrigatório, numérico com 2 decimais, não negativo
    ok4, val4, _ = validar_valor_numerico(rec_bru_cum, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok4:
        return None
    
    # REC_BRU_TOTAL: obrigatório, numérico com 2 decimais, não negativo
    ok5, val5, _ = validar_valor_numerico(rec_bru_total, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok5:
        return None
    
    # Validação: REC_BRU_TOTAL deve ser igual à soma dos campos 02, 03, 04 e 05
    soma_parcial = val1 + val2 + val3 + val4
    if not _float_igual(val5, soma_parcial):
        return None
    
    # Função auxiliar para formatar valores monetários
    def fmt_valor(v):
        return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "REC_BRU_NCUM_TRIB_MI": {
            "titulo": "Receita Bruta Não-Cumulativa - Tributada no Mercado Interno",
            "valor": rec_bru_ncum_trib_mi,
            "valor_formatado": fmt_valor(val1)
        },
        "REC_BRU_NCUM_NT_MI": {
            "titulo": "Receita Bruta Não-Cumulativa – Não Tributada no Mercado Interno",
            "valor": rec_bru_ncum_nt_mi,
            "valor_formatado": fmt_valor(val2)
        },
        "REC_BRU_NCUM_EXP": {
            "titulo": "Receita Bruta Não-Cumulativa – Exportação",
            "valor": rec_bru_ncum_exp,
            "valor_formatado": fmt_valor(val3)
        },
        "REC_BRU_CUM": {
            "titulo": "Receita Bruta Cumulativa",
            "valor": rec_bru_cum,
            "valor_formatado": fmt_valor(val4)
        },
        "REC_BRU_TOTAL": {
            "titulo": "Receita Bruta Total",
            "valor": rec_bru_total,
            "valor_formatado": fmt_valor(val5)
        }
    }
    
    return resultado


def validar_0111(linhas):
    """
    Valida uma ou mais linhas do registro 0111 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |0111|REC_BRU_NCUM_TRIB_MI|REC_BRU_NCUM_NT_MI|REC_BRU_NCUM_EXP|REC_BRU_CUM|REC_BRU_TOTAL|
        
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
        resultado = _processar_linha_0111(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
