import json


def validar_valor_numerico(valor_str, decimais=2, obrigatorio=False, positivo=False, nao_negativo=False):
    """
    Valida um valor numérico com precisão decimal específica.
    """
    if valor_str is None:
        valor_str = ""

    if not valor_str:
        if obrigatorio:
            return False, None, "Campo obrigatório não preenchido"
        return True, 0.0, None

    try:
        valor_float = float(valor_str)

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


def _processar_linha_k265(linha, cod_item_k260=None):
    """
    Processa uma única linha do registro K265 e retorna um dicionário.

    Formato:
      |K265|COD_ITEM|QTD_CONS|QTD_RET|

    Regras (manual 3.1.8):
    - REG deve ser "K265"
    - COD_ITEM: obrigatório, até 60 caracteres
      - Deve existir no registro 0200 (validação externa)
      - Deve ser diferente do código do produto/insumo reprocessado/reparado (COD_ITEM do K260)
      - TIPO_ITEM deve ser 00, 01, 02, 03, 04, 05 ou 10 (validação externa)
    - QTD_CONS: opcional condicional, numérico com 6 decimais, não negativo
    - QTD_RET: opcional condicional, numérico com 6 decimais, não negativo
      - Pelo menos um dos campos QTD_CONS ou QTD_RET é obrigatório

    Args:
        linha: linha SPED
        cod_item_k260: COD_ITEM do registro K260 relacionado (opcional, para validação)

    Returns:
        dict ou None
    """
    if not linha or not isinstance(linha, str):
        return None

    linha = linha.strip()
    if not linha:
        return None

    partes = linha.split("|")
    if partes and not partes[0]:
        partes = partes[1:]
    if partes and not partes[-1]:
        partes = partes[:-1]

    if len(partes) < 1:
        return None

    reg = partes[0].strip() if partes else ""
    if reg != "K265":
        return None

    def obter_campo(indice):
        if indice < len(partes):
            valor = partes[indice].strip()
            if valor == "-":
                return ""
            return valor if valor else ""
        return ""

    cod_item = obter_campo(1)
    qtd_cons = obter_campo(2)
    qtd_ret = obter_campo(3)

    # COD_ITEM: obrigatório, até 60 caracteres
    if not cod_item or len(cod_item) > 60:
        return None

    # Validação: COD_ITEM deve ser diferente do código do produto/insumo reprocessado/reparado (COD_ITEM do K260)
    if cod_item_k260 and cod_item == cod_item_k260:
        return None

    # QTD_CONS: opcional condicional, numérico com 6 decimais, não negativo
    qtd_cons_ok, qtd_cons_float, _ = validar_valor_numerico(qtd_cons, decimais=6, obrigatorio=False, nao_negativo=True)
    if not qtd_cons_ok:
        return None

    # QTD_RET: opcional condicional, numérico com 6 decimais, não negativo
    qtd_ret_ok, qtd_ret_float, _ = validar_valor_numerico(qtd_ret, decimais=6, obrigatorio=False, nao_negativo=True)
    if not qtd_ret_ok:
        return None

    # Validação: pelo menos um dos campos QTD_CONS ou QTD_RET é obrigatório
    # Pelo menos um deve ter valor maior que zero
    if (not qtd_cons or qtd_cons_float == 0.0) and (not qtd_ret or qtd_ret_float == 0.0):
        return None

    def fmt_quantidade(v):
        return f"{v:,.6f}".replace(",", "X").replace(".", ",").replace("X", ".")

    return {
        "REG": {"titulo": "Registro", "valor": reg},
        "COD_ITEM": {
            "titulo": "Código da mercadoria (campo 02 do Registro 0200)",
            "valor": cod_item,
        },
        "QTD_CONS": {
            "titulo": "Quantidade consumida – saída do estoque",
            "valor": qtd_cons if qtd_cons else "",
            "valor_formatado": fmt_quantidade(qtd_cons_float) if qtd_cons_float is not None else "",
        },
        "QTD_RET": {
            "titulo": "Quantidade retornada – entrada em estoque",
            "valor": qtd_ret if qtd_ret else "",
            "valor_formatado": fmt_quantidade(qtd_ret_float) if qtd_ret_float is not None else "",
        },
    }


def validar_k265_fiscal(linhas, cod_item_k260=None):
    """
    Valida uma ou mais linhas do registro K265 do SPED EFD Fiscal.

    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |K265|COD_ITEM|QTD_CONS|QTD_RET|
        cod_item_k260: COD_ITEM do registro K260 relacionado para validação (opcional)

    Returns:
        String JSON com array de objetos contendo os campos validados.
        Retorna "[]" se nenhuma linha for válida.
    """
    if not linhas:
        return json.dumps([], ensure_ascii=False, indent=2)

    if isinstance(linhas, str):
        if "\n" in linhas:
            linhas_para_processar = [l.strip() for l in linhas.split("\n") if l.strip()]
        else:
            linhas_para_processar = [linhas.strip()] if linhas.strip() else []
    elif isinstance(linhas, list):
        linhas_para_processar = [l.strip() if isinstance(l, str) else str(l).strip() for l in linhas if l]
    else:
        linhas_para_processar = [str(linhas).strip()] if str(linhas).strip() else []

    resultados = []
    for l in linhas_para_processar:
        r = _processar_linha_k265(l, cod_item_k260=cod_item_k260)
        if r is not None:
            resultados.append(r)

    return json.dumps(resultados, ensure_ascii=False, indent=2)
