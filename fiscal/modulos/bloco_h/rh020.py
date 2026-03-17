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


def _processar_linha_h020(linha):
    """
    Processa uma única linha do registro H020 e retorna um dicionário.

    Formato:
      |H020|CST_ICMS|BC_ICMS|VL_ICMS|

    Regras (manual 3.1.8):
    - REG deve ser "H020"
    - CST_ICMS: obrigatório, código CST (3 dígitos numéricos) conforme Tabela 4.3.1
    - BC_ICMS: obrigatório, numérico com 2 decimais, não negativo (base de cálculo do ICMS - valor unitário)
    - VL_ICMS: obrigatório, numérico com 2 decimais (valor do ICMS - valor unitário)
    
    Observação: Este registro deve ser preenchido quando MOT_INV do H005 for de "02" a "05".
    Registro válido a partir de julho/2012.

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
    if reg != "H020":
        return None

    def obter_campo(indice):
        if indice < len(partes):
            valor = partes[indice].strip()
            if valor == "-":
                return ""
            return valor if valor else ""
        return ""

    cst_icms = obter_campo(1)
    bc_icms = obter_campo(2)
    vl_icms = obter_campo(3)

    # CST_ICMS: obrigatório, código CST (3 dígitos numéricos)
    if not cst_icms or not cst_icms.isdigit() or len(cst_icms) != 3:
        return None

    # BC_ICMS: obrigatório, numérico com 2 decimais, não negativo
    bc_icms_ok, bc_icms_float, _ = validar_valor_numerico(bc_icms, decimais=2, obrigatorio=True, nao_negativo=True)
    if not bc_icms_ok:
        return None

    # VL_ICMS: obrigatório, numérico com 2 decimais
    # Pode ser negativo (débito) ou positivo (crédito)
    vl_icms_ok, vl_icms_float, _ = validar_valor_numerico(vl_icms, decimais=2, obrigatorio=True)
    if not vl_icms_ok:
        return None

    def fmt_moeda(v):
        return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    # Códigos CST mais comuns (validação básica - CST válidos são muitos)
    # CST válidos: 000, 010, 020, 030, 040, 041, 050, 051, 060, 070, 090, 101, 102, 103, 201, 202, 203, 300, 400, 500, 900
    # Mas não vou restringir aqui, apenas validar formato (3 dígitos numéricos)

    return {
        "REG": {"titulo": "Registro", "valor": reg},
        "CST_ICMS": {
            "titulo": "Código da Situação Tributária referente ao ICMS, conforme a Tabela indicada no item 4.3.1",
            "valor": cst_icms,
        },
        "BC_ICMS": {
            "titulo": "Informe a base de cálculo do ICMS",
            "valor": bc_icms,
            "valor_formatado": fmt_moeda(bc_icms_float),
        },
        "VL_ICMS": {
            "titulo": "Informe o valor do ICMS a ser debitado ou creditado",
            "valor": vl_icms,
            "valor_formatado": fmt_moeda(vl_icms_float),
        },
    }


def validar_h020(linhas):
    """
    Valida uma ou mais linhas do registro H020 do SPED EFD Fiscal.

    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |H020|CST_ICMS|BC_ICMS|VL_ICMS|

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
        r = _processar_linha_h020(l)
        if r is not None:
            resultados.append(r)

    return json.dumps(resultados, ensure_ascii=False, indent=2)
