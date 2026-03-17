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


def _processar_linha_h030(linha):
    """
    Processa uma única linha do registro H030 e retorna um dicionário.

    Formato:
      |H030|VL_ICMS_OP|VL_BC_ICMS_ST|VL_ICMS_ST|VL_FCP|

    Regras (manual 3.1.8):
    - REG deve ser "H030"
    - VL_ICMS_OP: obrigatório, numérico com 6 decimais, não negativo (valor médio unitário do ICMS OP)
    - VL_BC_ICMS_ST: obrigatório, numérico com 6 decimais, não negativo (valor médio unitário da base de cálculo do ICMS ST)
    - VL_ICMS_ST: obrigatório, numérico com 6 decimais, não negativo (valor médio unitário do ICMS ST)
    - VL_FCP: obrigatório, numérico com 6 decimais, não negativo (valor médio unitário do FCP)
    
    Observação: Este registro é obrigatório quando MOT_INV do H005 for igual a "06".
    Para os demais motivos, não deve ser informado.

    Args:
        linha: linha SPED

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
    if reg != "H030":
        return None

    def obter_campo(indice):
        if indice < len(partes):
            valor = partes[indice].strip()
            if valor == "-":
                return ""
            return valor if valor else ""
        return ""

    vl_icms_op = obter_campo(1)
    vl_bc_icms_st = obter_campo(2)
    vl_icms_st = obter_campo(3)
    vl_fcp = obter_campo(4)

    # VL_ICMS_OP: obrigatório, numérico com 6 decimais, não negativo
    vl_icms_op_ok, vl_icms_op_float, _ = validar_valor_numerico(
        vl_icms_op, decimais=6, obrigatorio=True, nao_negativo=True
    )
    if not vl_icms_op_ok:
        return None

    # VL_BC_ICMS_ST: obrigatório, numérico com 6 decimais, não negativo
    vl_bc_icms_st_ok, vl_bc_icms_st_float, _ = validar_valor_numerico(
        vl_bc_icms_st, decimais=6, obrigatorio=True, nao_negativo=True
    )
    if not vl_bc_icms_st_ok:
        return None

    # VL_ICMS_ST: obrigatório, numérico com 6 decimais, não negativo
    vl_icms_st_ok, vl_icms_st_float, _ = validar_valor_numerico(
        vl_icms_st, decimais=6, obrigatorio=True, nao_negativo=True
    )
    if not vl_icms_st_ok:
        return None

    # VL_FCP: obrigatório, numérico com 6 decimais, não negativo
    vl_fcp_ok, vl_fcp_float, _ = validar_valor_numerico(vl_fcp, decimais=6, obrigatorio=True, nao_negativo=True)
    if not vl_fcp_ok:
        return None

    def fmt_valor_unitario(v):
        return f"{v:,.6f}".replace(",", "X").replace(".", ",").replace("X", ".")

    return {
        "REG": {"titulo": "Registro", "valor": reg},
        "VL_ICMS_OP": {
            "titulo": "Valor médio unitário do ICMS OP",
            "valor": vl_icms_op,
            "valor_formatado": fmt_valor_unitario(vl_icms_op_float),
        },
        "VL_BC_ICMS_ST": {
            "titulo": "Valor médio unitário da base de cálculo do ICMS ST",
            "valor": vl_bc_icms_st,
            "valor_formatado": fmt_valor_unitario(vl_bc_icms_st_float),
        },
        "VL_ICMS_ST": {
            "titulo": "Valor médio unitário do ICMS ST",
            "valor": vl_icms_st,
            "valor_formatado": fmt_valor_unitario(vl_icms_st_float),
        },
        "VL_FCP": {
            "titulo": "Valor médio unitário do FCP",
            "valor": vl_fcp,
            "valor_formatado": fmt_valor_unitario(vl_fcp_float),
        },
    }


def validar_h030(linhas):
    """
    Valida uma ou mais linhas do registro H030 do SPED EFD Fiscal.

    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |H030|VL_ICMS_OP|VL_BC_ICMS_ST|VL_ICMS_ST|VL_FCP|

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
        r = _processar_linha_h030(l)
        if r is not None:
            resultados.append(r)

    return json.dumps(resultados, ensure_ascii=False, indent=2)
