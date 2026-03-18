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


def _processar_linha_k275(linha, origem_k270=None):
    """
    Processa uma única linha do registro K275 e retorna um dicionário.

    Formato:
      |K275|COD_ITEM|QTD_COR_POS|QTD_COR_NEG|COD_INS_SUBST|

    Regras (manual 3.1.8):
    - REG deve ser "K275"
    - COD_ITEM: obrigatório, até 60 caracteres
      - Deve existir no registro 0200 (validação externa)
      - Somente tipos 00 a 05 e 10 (validação externa)
    - QTD_COR_POS: opcional condicional, numérico com 6 decimais, não negativo
    - QTD_COR_NEG: opcional condicional, numérico com 6 decimais, não negativo
      - Somente um dos campos QTD_COR_POS ou QTD_COR_NEG pode ser preenchido
    - COD_INS_SUBST: opcional condicional, até 60 caracteres
      - Somente pode existir quando a origem da correção de apontamento for dos tipos 1 ou 2
        (campo ORIGEM do Registro K270)

    Args:
        linha: linha SPED
        origem_k270: ORIGEM do registro K270 relacionado (opcional, para validação)

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
    if reg != "K275":
        return None

    def obter_campo(indice):
        if indice < len(partes):
            valor = partes[indice].strip()
            if valor == "-":
                return ""
            return valor if valor else ""
        return ""

    cod_item = obter_campo(1)
    qtd_cor_pos = obter_campo(2)
    qtd_cor_neg = obter_campo(3)
    cod_ins_subst = obter_campo(4)

    # COD_ITEM: obrigatório, até 60 caracteres
    if not cod_item or len(cod_item) > 60:
        return None

    # QTD_COR_POS: opcional condicional, numérico com 6 decimais, não negativo
    qtd_cor_pos_ok, qtd_cor_pos_float, _ = validar_valor_numerico(
        qtd_cor_pos, decimais=6, obrigatorio=False, nao_negativo=True
    )
    if not qtd_cor_pos_ok:
        return None

    # QTD_COR_NEG: opcional condicional, numérico com 6 decimais, não negativo
    qtd_cor_neg_ok, qtd_cor_neg_float, _ = validar_valor_numerico(
        qtd_cor_neg, decimais=6, obrigatorio=False, nao_negativo=True
    )
    if not qtd_cor_neg_ok:
        return None

    # Validação: somente um dos campos QTD_COR_POS ou QTD_COR_NEG pode ser preenchido
    tem_qtd_pos = qtd_cor_pos and qtd_cor_pos_float > 0
    tem_qtd_neg = qtd_cor_neg and qtd_cor_neg_float > 0
    if tem_qtd_pos and tem_qtd_neg:
        return None

    # COD_INS_SUBST: opcional condicional, até 60 caracteres
    if cod_ins_subst:
        if len(cod_ins_subst) > 60:
            return None
        # Validação: COD_INS_SUBST somente pode existir quando a origem da correção for dos tipos 1 ou 2
        if origem_k270 and origem_k270 not in ["1", "2"]:
            return None

    def fmt_quantidade(v):
        return f"{v:,.6f}".replace(",", "X").replace(".", ",").replace("X", ".")

    return {
        "REG": {"titulo": "Registro", "valor": reg},
        "COD_ITEM": {
            "titulo": "Código da mercadoria (campo 02 do Registro 0200)",
            "valor": cod_item,
        },
        "QTD_COR_POS": {
            "titulo": "Quantidade de correção positiva de apontamento ocorrido em período de apuração anterior",
            "valor": qtd_cor_pos if qtd_cor_pos else "",
            "valor_formatado": fmt_quantidade(qtd_cor_pos_float) if qtd_cor_pos_float is not None else "",
        },
        "QTD_COR_NEG": {
            "titulo": "Quantidade de correção negativa de apontamento ocorrido em período de apuração anterior",
            "valor": qtd_cor_neg if qtd_cor_neg else "",
            "valor_formatado": fmt_quantidade(qtd_cor_neg_float) if qtd_cor_neg_float is not None else "",
        },
        "COD_INS_SUBST": {
            "titulo": "Código do insumo que foi substituído, caso ocorra a substituição, relativo aos Registros K235/K255",
            "valor": cod_ins_subst if cod_ins_subst else "",
        },
    }


def validar_k275_fiscal(linhas, origem_k270=None):
    """
    Valida uma ou mais linhas do registro K275 do SPED EFD Fiscal.

    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |K275|COD_ITEM|QTD_COR_POS|QTD_COR_NEG|COD_INS_SUBST|
        origem_k270: ORIGEM do registro K270 relacionado para validação (opcional)

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
        r = _processar_linha_k275(l, origem_k270=origem_k270)
        if r is not None:
            resultados.append(r)

    return json.dumps(resultados, ensure_ascii=False, indent=2)
