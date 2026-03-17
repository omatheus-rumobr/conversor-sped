import json

from datetime import datetime


def _validar_data(data_str):
    """
    Valida se a data está no formato ddmmaaaa e se é uma data válida.

    Returns:
        tuple: (True/False, datetime ou None)
    """
    if not data_str or len(data_str) != 8 or not data_str.isdigit():
        return False, None
    try:
        dia = int(data_str[:2])
        mes = int(data_str[2:4])
        ano = int(data_str[4:8])
        return True, datetime(ano, mes, dia)
    except ValueError:
        return False, None


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


def _processar_linha_k255(linha, dt_ini_k100=None, dt_fin_k100=None, cod_item_k250=None):
    """
    Processa uma única linha do registro K255 e retorna um dicionário.

    Formato:
      |K255|DT_CONS|COD_ITEM|QTD|COD_INS_SUBST|

    Regras (manual 3.1.8):
    - REG deve ser "K255"
    - DT_CONS: obrigatório, formato ddmmaaaa
      - Deve estar no período do K100 (quando informado)
    - COD_ITEM: obrigatório, até 60 caracteres
      - Deve existir no registro 0200 (validação externa)
      - Deve ser diferente do código do produto resultante (COD_ITEM do K250)
      - TIPO_ITEM deve ser 00, 01, 02, 03, 04, 05 ou 10 (validação externa)
    - QTD: obrigatório, numérico com 6 decimais, não negativo
    - COD_INS_SUBST: opcional condicional, até 60 caracteres
      - Não deve ser preenchido a partir de 01/01/2022
      - Deve existir no Registro 0210 para o mesmo produto resultante (validação externa)

    Args:
        linha: linha SPED
        dt_ini_k100: data ddmmaaaa do DT_INI do registro K100 (opcional, para validação)
        dt_fin_k100: data ddmmaaaa do DT_FIN do registro K100 (opcional, para validação)
        cod_item_k250: COD_ITEM do registro K250 relacionado (opcional, para validação)

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
    if reg != "K255":
        return None

    def obter_campo(indice):
        if indice < len(partes):
            valor = partes[indice].strip()
            if valor == "-":
                return ""
            return valor if valor else ""
        return ""

    dt_cons = obter_campo(1)
    cod_item = obter_campo(2)
    qtd = obter_campo(3)
    cod_ins_subst = obter_campo(4)

    # DT_CONS: obrigatório, ddmmaaaa, data válida
    dt_cons_ok, dt_cons_obj = _validar_data(dt_cons)
    if not dt_cons_ok:
        return None

    # Validação: DT_CONS deve estar no período do K100 (quando informado)
    if dt_ini_k100 and dt_fin_k100:
        ok_k100_ini, dt_ini_k100_obj = _validar_data(dt_ini_k100)
        ok_k100_fin, dt_fin_k100_obj = _validar_data(dt_fin_k100)
        if ok_k100_ini and ok_k100_fin:
            if dt_cons_obj < dt_ini_k100_obj or dt_cons_obj > dt_fin_k100_obj:
                return None

    # COD_ITEM: obrigatório, até 60 caracteres
    if not cod_item or len(cod_item) > 60:
        return None

    # Validação: COD_ITEM deve ser diferente do código do produto resultante (COD_ITEM do K250)
    if cod_item_k250 and cod_item == cod_item_k250:
        return None

    # QTD: obrigatório, numérico com 6 decimais, não negativo
    qtd_ok, qtd_float, _ = validar_valor_numerico(qtd, decimais=6, obrigatorio=True, nao_negativo=True)
    if not qtd_ok:
        return None

    # COD_INS_SUBST: opcional condicional, até 60 caracteres
    if cod_ins_subst and len(cod_ins_subst) > 60:
        return None

    def fmt_quantidade(v):
        return f"{v:,.6f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def fmt_data(d):
        return d.strftime("%d/%m/%Y") if d else ""

    return {
        "REG": {"titulo": "Registro", "valor": reg},
        "DT_CONS": {
            "titulo": "Data do reconhecimento do consumo do insumo referente ao produto informado no campo 04 do Registro K250",
            "valor": dt_cons,
            "valor_formatado": fmt_data(dt_cons_obj),
        },
        "COD_ITEM": {
            "titulo": "Código do insumo (campo 02 do Registro 0200)",
            "valor": cod_item,
        },
        "QTD": {
            "titulo": "Quantidade de consumo do insumo",
            "valor": qtd,
            "valor_formatado": fmt_quantidade(qtd_float),
        },
        "COD_INS_SUBST": {
            "titulo": "Código do insumo que foi substituído, caso ocorra a substituição (campo 02 do Registro 0210)",
            "valor": cod_ins_subst if cod_ins_subst else "",
        },
    }


def validar_k255(linhas, dt_ini_k100=None, dt_fin_k100=None, cod_item_k250=None):
    """
    Valida uma ou mais linhas do registro K255 do SPED EFD Fiscal.

    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |K255|DT_CONS|COD_ITEM|QTD|COD_INS_SUBST|
        dt_ini_k100: DT_INI do registro K100 (ddmmaaaa) para validação do período (opcional)
        dt_fin_k100: DT_FIN do registro K100 (ddmmaaaa) para validação do período (opcional)
        cod_item_k250: COD_ITEM do registro K250 relacionado para validação (opcional)

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
        r = _processar_linha_k255(
            l,
            dt_ini_k100=dt_ini_k100,
            dt_fin_k100=dt_fin_k100,
            cod_item_k250=cod_item_k250,
        )
        if r is not None:
            resultados.append(r)

    return json.dumps(resultados, ensure_ascii=False, indent=2)
