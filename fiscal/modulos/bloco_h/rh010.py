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


def _float_igual(a, b, tolerancia=0.01):
    """Compara dois floats com tolerância."""
    if a is None or b is None:
        return False
    return abs(a - b) <= tolerancia


def _processar_linha_h010(linha):
    """
    Processa uma única linha do registro H010 e retorna um dicionário.

    Formato:
      |H010|COD_ITEM|UNID|QTD|VL_UNIT|VL_ITEM|IND_PROP|COD_PART|TXT_COMPL|COD_CTA|VL_ITEM_IR|

    Regras (manual 3.1.8):
    - REG deve ser "H010"
    - COD_ITEM: obrigatório, até 60 caracteres
    - UNID: obrigatório, até 6 caracteres
    - QTD: obrigatório, numérico com 3 decimais, não negativo
    - VL_UNIT: obrigatório, numérico com 6 decimais, não negativo
    - VL_ITEM: obrigatório, numérico com 2 decimais, não negativo
      - VL_ITEM = QTD * VL_UNIT (com tolerância para arredondamento)
    - IND_PROP: obrigatório, valores válidos ["0", "1", "2"]
      - Se IND_PROP = "1" ou "2", COD_PART é obrigatório
    - COD_PART: opcional condicional, até 60 caracteres
      - Obrigatório quando IND_PROP = "1" ou "2"
    - TXT_COMPL: opcional condicional
    - COD_CTA: opcional condicional
    - VL_ITEM_IR: opcional condicional, numérico com 2 decimais, não negativo

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
    if reg != "H010":
        return None

    def obter_campo(indice):
        if indice < len(partes):
            valor = partes[indice].strip()
            if valor == "-":
                return ""
            return valor if valor else ""
        return ""

    cod_item = obter_campo(1)
    unid = obter_campo(2)
    qtd = obter_campo(3)
    vl_unit = obter_campo(4)
    vl_item = obter_campo(5)
    ind_prop = obter_campo(6)
    cod_part = obter_campo(7)
    txt_compl = obter_campo(8)
    cod_cta = obter_campo(9)
    vl_item_ir = obter_campo(10)

    # COD_ITEM: obrigatório, até 60 caracteres
    if not cod_item or len(cod_item) > 60:
        return None

    # UNID: obrigatório, até 6 caracteres
    if not unid or len(unid) > 6:
        return None

    # QTD: obrigatório, numérico com 3 decimais, não negativo
    qtd_ok, qtd_float, _ = validar_valor_numerico(qtd, decimais=3, obrigatorio=True, nao_negativo=True)
    if not qtd_ok:
        return None

    # VL_UNIT: obrigatório, numérico com 6 decimais, não negativo
    vl_unit_ok, vl_unit_float, _ = validar_valor_numerico(vl_unit, decimais=6, obrigatorio=True, nao_negativo=True)
    if not vl_unit_ok:
        return None

    # VL_ITEM: obrigatório, numérico com 2 decimais, não negativo
    vl_item_ok, vl_item_float, _ = validar_valor_numerico(vl_item, decimais=2, obrigatorio=True, nao_negativo=True)
    if not vl_item_ok:
        return None

    # Validação: VL_ITEM = QTD * VL_UNIT (com tolerância para arredondamento)
    vl_item_calc = qtd_float * vl_unit_float
    # Tolerância de 0.01 para valores monetários (2 decimais)
    if not _float_igual(vl_item_float, vl_item_calc, tolerancia=0.01):
        return None

    # IND_PROP: obrigatório, valores válidos
    ind_prop_validos = ["0", "1", "2"]
    if not ind_prop or ind_prop not in ind_prop_validos:
        return None

    # COD_PART: opcional condicional, até 60 caracteres
    # Obrigatório quando IND_PROP = "1" ou "2"
    if ind_prop in ["1", "2"]:
        if not cod_part or len(cod_part) > 60:
            return None
    else:
        # Para IND_PROP = "0", COD_PART é opcional mas se informado deve ter até 60 caracteres
        if cod_part and len(cod_part) > 60:
            return None

    # TXT_COMPL: opcional condicional (sem validação específica de tamanho no manual)

    # COD_CTA: opcional condicional (sem validação específica de tamanho no manual)

    # VL_ITEM_IR: opcional condicional, numérico com 2 decimais, não negativo
    vl_item_ir_ok, vl_item_ir_float, _ = validar_valor_numerico(
        vl_item_ir, decimais=2, obrigatorio=False, nao_negativo=True
    )
    if not vl_item_ir_ok:
        return None

    def fmt_moeda(v):
        return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def fmt_quantidade(v):
        return f"{v:,.3f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def fmt_valor_unitario(v):
        return f"{v:,.6f}".replace(",", "X").replace(".", ",").replace("X", ".")

    descricoes_ind_prop = {
        "0": "Item de propriedade do informante e em seu poder",
        "1": "Item de propriedade do informante em posse de terceiros",
        "2": "Item de propriedade de terceiros em posse do informante",
    }

    return {
        "REG": {"titulo": "Registro", "valor": reg},
        "COD_ITEM": {
            "titulo": "Código do item (campo 02 do Registro 0200)",
            "valor": cod_item,
        },
        "UNID": {
            "titulo": "Unidade do item",
            "valor": unid,
        },
        "QTD": {
            "titulo": "Quantidade do item",
            "valor": qtd,
            "valor_formatado": fmt_quantidade(qtd_float),
        },
        "VL_UNIT": {
            "titulo": "Valor unitário do item",
            "valor": vl_unit,
            "valor_formatado": fmt_valor_unitario(vl_unit_float),
        },
        "VL_ITEM": {
            "titulo": "Valor do item",
            "valor": vl_item,
            "valor_formatado": fmt_moeda(vl_item_float),
        },
        "IND_PROP": {
            "titulo": "Indicador de propriedade/posse do item",
            "valor": ind_prop,
            "descricao": descricoes_ind_prop.get(ind_prop, ""),
        },
        "COD_PART": {
            "titulo": "Código do participante (campo 02 do Registro 0150): proprietário/possuidor que não seja o informante do arquivo",
            "valor": cod_part if cod_part else "",
        },
        "TXT_COMPL": {
            "titulo": "Descrição complementar",
            "valor": txt_compl if txt_compl else "",
        },
        "COD_CTA": {
            "titulo": "Código da conta analítica contábil debitada/creditada",
            "valor": cod_cta if cod_cta else "",
        },
        "VL_ITEM_IR": {
            "titulo": "Valor do item para efeitos do Imposto de Renda",
            "valor": vl_item_ir if vl_item_ir else "",
            "valor_formatado": fmt_moeda(vl_item_ir_float) if vl_item_ir_float > 0 else "",
        },
    }


def validar_h010(linhas):
    """
    Valida uma ou mais linhas do registro H010 do SPED EFD Fiscal.

    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |H010|COD_ITEM|UNID|QTD|VL_UNIT|VL_ITEM|IND_PROP|COD_PART|TXT_COMPL|COD_CTA|VL_ITEM_IR|

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
        r = _processar_linha_h010(l)
        if r is not None:
            resultados.append(r)

    return json.dumps(resultados, ensure_ascii=False, indent=2)
