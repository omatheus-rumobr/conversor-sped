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


def _processar_linha_k292(linha, cod_item_k291=None):
    """
    Processa uma única linha do registro K292 e retorna um dicionário.

    Formato:
      |K292|COD_ITEM|QTD|

    Regras (manual 3.1.8):
    - REG deve ser "K292"
    - COD_ITEM: obrigatório, até 60 caracteres
      - Deve existir no campo COD_ITEM do Registro 0200 (validação externa)
      - Deve ser diferente do código do produto resultante (COD_ITEM do Registro K291) quando informado
      - O tipo do componente/insumo (campo TIPO_ITEM do Registro 0200) deve ser igual a 00, 01, 02, 03, 04, 05 ou 10 (validação externa)
    - QTD: obrigatório, numérico com 6 decimais, não negativo, maior que zero

    Nota: Este registro não deve ser escriturado quando DT_FIN_OP do registro K290 for menor que o campo DT_INI do
    registro 0000. Esta validação deve ser feita em uma camada superior.

    Args:
        linha: linha SPED
        cod_item_k291: COD_ITEM do registro K291 relacionado (opcional, para validação)

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
    if reg != "K292":
        return None

    def obter_campo(indice):
        if indice < len(partes):
            valor = partes[indice].strip()
            if valor == "-":
                return ""
            return valor if valor else ""
        return ""

    cod_item = obter_campo(1)
    qtd = obter_campo(2)

    # COD_ITEM: obrigatório, até 60 caracteres
    if not cod_item or len(cod_item) > 60:
        return None

    # Validação: COD_ITEM deve ser diferente do código do produto resultante (COD_ITEM do K291)
    if cod_item_k291 and cod_item == cod_item_k291:
        return None

    # QTD: obrigatório, numérico com 6 decimais, não negativo, maior que zero
    qtd_ok, qtd_float, _ = validar_valor_numerico(qtd, decimais=6, obrigatorio=True, positivo=True)
    if not qtd_ok:
        return None

    def fmt_quantidade(v):
        return f"{v:,.6f}".replace(",", "X").replace(".", ",").replace("X", ".")

    return {
        "REG": {"titulo": "Registro", "valor": reg},
        "COD_ITEM": {
            "titulo": "Código do insumo/componente consumido (campo 02 do Registro 0200)",
            "valor": cod_item,
        },
        "QTD": {
            "titulo": "Quantidade consumida",
            "valor": qtd,
            "valor_formatado": fmt_quantidade(qtd_float),
        },
    }


def validar_k292_fiscal(linhas, cod_item_k291=None):
    """
    Valida uma ou mais linhas do registro K292 do SPED EFD Fiscal.

    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |K292|COD_ITEM|QTD|
        cod_item_k291: COD_ITEM do registro K291 relacionado para validação (opcional)

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
        r = _processar_linha_k292(l, cod_item_k291=cod_item_k291)
        if r is not None:
            resultados.append(r)

    return json.dumps(resultados, ensure_ascii=False, indent=2)
