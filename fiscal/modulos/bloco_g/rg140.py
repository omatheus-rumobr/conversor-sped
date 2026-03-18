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


def _processar_linha_g140(linha):
    """
    Processa uma única linha do registro G140 e retorna um dicionário.

    Formato:
      |G140|NUM_ITEM|COD_ITEM|QTDE|UNID|VL_ICMS_OP_APLICADO|VL_ICMS_ST_APLICADO|VL_ICMS_FRT_APLICADO|VL_ICMS_DIF_APLICADO|

    Regras (manual 3.1.8):
    - REG deve ser "G140"
    - NUM_ITEM: obrigatório, numérico até 3 dígitos, > 0
    - COD_ITEM: obrigatório, até 60 caracteres
    - QTDE: obrigatório, numérico com 5 decimais, não negativo
    - UNID: obrigatório, até 6 caracteres
    - VL_ICMS_OP_APLICADO: obrigatório, numérico com 2 decimais, não negativo
    - VL_ICMS_ST_APLICADO: obrigatório, numérico com 2 decimais, não negativo
    - VL_ICMS_FRT_APLICADO: obrigatório, numérico com 2 decimais, não negativo
    - VL_ICMS_DIF_APLICADO: obrigatório, numérico com 2 decimais, não negativo

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
    if reg != "G140":
        return None

    def obter_campo(indice):
        if indice < len(partes):
            valor = partes[indice].strip()
            if valor == "-":
                return ""
            return valor if valor else ""
        return ""

    num_item = obter_campo(1)
    cod_item = obter_campo(2)
    qtde = obter_campo(3)
    unid = obter_campo(4)
    vl_icms_op_aplicado = obter_campo(5)
    vl_icms_st_aplicado = obter_campo(6)
    vl_icms_frt_aplicado = obter_campo(7)
    vl_icms_dif_aplicado = obter_campo(8)

    # NUM_ITEM: obrigatório, numérico até 3 dígitos, > 0
    if not num_item or not num_item.isdigit() or len(num_item) > 3:
        return None
    num_item_int = int(num_item)
    if num_item_int <= 0:
        return None

    # COD_ITEM: obrigatório, até 60 caracteres
    if not cod_item or len(cod_item) > 60:
        return None

    # QTDE: obrigatório, numérico com 5 decimais, não negativo
    qtde_ok, qtde_float, _ = validar_valor_numerico(qtde, decimais=5, obrigatorio=True, nao_negativo=True)
    if not qtde_ok:
        return None

    # UNID: obrigatório, até 6 caracteres
    if not unid or len(unid) > 6:
        return None

    # VL_ICMS_OP_APLICADO: obrigatório, numérico com 2 decimais, não negativo
    vl_icms_op_ok, vl_icms_op_float, _ = validar_valor_numerico(
        vl_icms_op_aplicado, decimais=2, obrigatorio=True, nao_negativo=True
    )
    if not vl_icms_op_ok:
        return None

    # VL_ICMS_ST_APLICADO: obrigatório, numérico com 2 decimais, não negativo
    vl_icms_st_ok, vl_icms_st_float, _ = validar_valor_numerico(
        vl_icms_st_aplicado, decimais=2, obrigatorio=True, nao_negativo=True
    )
    if not vl_icms_st_ok:
        return None

    # VL_ICMS_FRT_APLICADO: obrigatório, numérico com 2 decimais, não negativo
    vl_icms_frt_ok, vl_icms_frt_float, _ = validar_valor_numerico(
        vl_icms_frt_aplicado, decimais=2, obrigatorio=True, nao_negativo=True
    )
    if not vl_icms_frt_ok:
        return None

    # VL_ICMS_DIF_APLICADO: obrigatório, numérico com 2 decimais, não negativo
    vl_icms_dif_ok, vl_icms_dif_float, _ = validar_valor_numerico(
        vl_icms_dif_aplicado, decimais=2, obrigatorio=True, nao_negativo=True
    )
    if not vl_icms_dif_ok:
        return None

    def fmt_moeda(v):
        return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def fmt_quantidade(v):
        return f"{v:,.5f}".replace(",", "X").replace(".", ",").replace("X", ".")

    return {
        "REG": {"titulo": "Registro", "valor": reg},
        "NUM_ITEM": {
            "titulo": "Número sequencial do item no documento fiscal",
            "valor": num_item,
        },
        "COD_ITEM": {
            "titulo": "Código correspondente do bem no documento fiscal (campo 02 do registro 0200)",
            "valor": cod_item,
        },
        "QTDE": {
            "titulo": "Quantidade, deste item da nota fiscal, que foi aplicada neste bem, expressa na mesma unidade constante no documento fiscal de entrada",
            "valor": qtde,
            "valor_formatado": fmt_quantidade(qtde_float),
        },
        "UNID": {
            "titulo": "Unidade do item constante no documento fiscal de entrada",
            "valor": unid,
        },
        "VL_ICMS_OP_APLICADO": {
            "titulo": "Valor do ICMS da Operação Própria na entrada do item, proporcional à quantidade aplicada no bem ou componente",
            "valor": vl_icms_op_aplicado,
            "valor_formatado": fmt_moeda(vl_icms_op_float),
        },
        "VL_ICMS_ST_APLICADO": {
            "titulo": "Valor do ICMS ST na entrada do item, proporcional à quantidade aplicada no bem ou componente",
            "valor": vl_icms_st_aplicado,
            "valor_formatado": fmt_moeda(vl_icms_st_float),
        },
        "VL_ICMS_FRT_APLICADO": {
            "titulo": "Valor do ICMS sobre Frete do Conhecimento de Transporte na entrada do item, proporcional à quantidade aplicada no bem ou componente",
            "valor": vl_icms_frt_aplicado,
            "valor_formatado": fmt_moeda(vl_icms_frt_float),
        },
        "VL_ICMS_DIF_APLICADO": {
            "titulo": "Valor do ICMS Diferencial de Alíquota, na entrada do item, proporcional à quantidade aplicada no bem ou componente",
            "valor": vl_icms_dif_aplicado,
            "valor_formatado": fmt_moeda(vl_icms_dif_float),
        },
    }


def validar_g140_fiscal(linhas):
    """
    Valida uma ou mais linhas do registro G140 do SPED EFD Fiscal.

    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |G140|NUM_ITEM|COD_ITEM|QTDE|UNID|VL_ICMS_OP_APLICADO|VL_ICMS_ST_APLICADO|VL_ICMS_FRT_APLICADO|VL_ICMS_DIF_APLICADO|

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
        r = _processar_linha_g140(l)
        if r is not None:
            resultados.append(r)

    return json.dumps(resultados, ensure_ascii=False, indent=2)
