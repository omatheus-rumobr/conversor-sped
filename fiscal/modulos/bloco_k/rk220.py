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


def _processar_linha_k220(linha, dt_ini_k100=None, dt_fin_k100=None):
    """
    Processa uma única linha do registro K220 e retorna um dicionário.

    Formato:
      |K220|DT_MOV|COD_ITEM_ORI|COD_ITEM_DEST|QTD_ORI|QTD_DEST|

    Regras (manual 3.1.8):
    - REG deve ser "K220"
    - DT_MOV: obrigatório, formato ddmmaaaa
      - Deve estar no período do K100 (quando informado)
    - COD_ITEM_ORI: obrigatório, até 60 caracteres
      - Deve existir no registro 0200 (validação externa)
    - COD_ITEM_DEST: obrigatório, até 60 caracteres
      - Deve existir no registro 0200 (validação externa)
      - Deve ser diferente de COD_ITEM_ORI
    - QTD_ORI: obrigatório, numérico com 6 decimais, maior que zero
    - QTD_DEST: obrigatório, numérico com 6 decimais, maior que zero

    Args:
        linha: linha SPED
        dt_ini_k100: data ddmmaaaa do DT_INI do registro K100 (opcional, para validação)
        dt_fin_k100: data ddmmaaaa do DT_FIN do registro K100 (opcional, para validação)

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
    if reg != "K220":
        return None

    def obter_campo(indice):
        if indice < len(partes):
            valor = partes[indice].strip()
            if valor == "-":
                return ""
            return valor if valor else ""
        return ""

    dt_mov = obter_campo(1)
    cod_item_ori = obter_campo(2)
    cod_item_dest = obter_campo(3)
    qtd_ori = obter_campo(4)
    qtd_dest = obter_campo(5)

    # DT_MOV: obrigatório, ddmmaaaa, data válida
    dt_mov_ok, dt_mov_obj = _validar_data(dt_mov)
    if not dt_mov_ok:
        return None

    # Validação: DT_MOV deve estar no período do K100 (quando informado)
    if dt_ini_k100 and dt_fin_k100:
        ok_k100_ini, dt_ini_k100_obj = _validar_data(dt_ini_k100)
        ok_k100_fin, dt_fin_k100_obj = _validar_data(dt_fin_k100)
        if ok_k100_ini and ok_k100_fin:
            if dt_mov_obj < dt_ini_k100_obj or dt_mov_obj > dt_fin_k100_obj:
                return None

    # COD_ITEM_ORI: obrigatório, até 60 caracteres
    if not cod_item_ori or len(cod_item_ori) > 60:
        return None

    # COD_ITEM_DEST: obrigatório, até 60 caracteres
    if not cod_item_dest or len(cod_item_dest) > 60:
        return None

    # Validação: COD_ITEM_DEST deve ser diferente de COD_ITEM_ORI
    if cod_item_dest == cod_item_ori:
        return None

    # QTD_ORI: obrigatório, numérico com 6 decimais, maior que zero
    qtd_ori_ok, qtd_ori_float, _ = validar_valor_numerico(qtd_ori, decimais=6, obrigatorio=True, positivo=True)
    if not qtd_ori_ok:
        return None

    # QTD_DEST: obrigatório, numérico com 6 decimais, maior que zero
    qtd_dest_ok, qtd_dest_float, _ = validar_valor_numerico(qtd_dest, decimais=6, obrigatorio=True, positivo=True)
    if not qtd_dest_ok:
        return None

    def fmt_quantidade(v):
        return f"{v:,.6f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def fmt_data(d):
        return d.strftime("%d/%m/%Y") if d else ""

    return {
        "REG": {"titulo": "Registro", "valor": reg},
        "DT_MOV": {
            "titulo": "Data da movimentação interna",
            "valor": dt_mov,
            "valor_formatado": fmt_data(dt_mov_obj),
        },
        "COD_ITEM_ORI": {
            "titulo": "Código do item de origem (campo 02 do Registro 0200)",
            "valor": cod_item_ori,
        },
        "COD_ITEM_DEST": {
            "titulo": "Código do item de destino (campo 02 do Registro 0200)",
            "valor": cod_item_dest,
        },
        "QTD_ORI": {
            "titulo": "Quantidade movimentada do item de origem",
            "valor": qtd_ori,
            "valor_formatado": fmt_quantidade(qtd_ori_float),
        },
        "QTD_DEST": {
            "titulo": "Quantidade movimentada do item de destino",
            "valor": qtd_dest,
            "valor_formatado": fmt_quantidade(qtd_dest_float),
        },
    }


def validar_k220_fiscal(linhas, dt_ini_k100=None, dt_fin_k100=None):
    """
    Valida uma ou mais linhas do registro K220 do SPED EFD Fiscal.

    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |K220|DT_MOV|COD_ITEM_ORI|COD_ITEM_DEST|QTD_ORI|QTD_DEST|
        dt_ini_k100: DT_INI do registro K100 (ddmmaaaa) para validação do período (opcional)
        dt_fin_k100: DT_FIN do registro K100 (ddmmaaaa) para validação do período (opcional)

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
        r = _processar_linha_k220(l, dt_ini_k100=dt_ini_k100, dt_fin_k100=dt_fin_k100)
        if r is not None:
            resultados.append(r)

    return json.dumps(resultados, ensure_ascii=False, indent=2)
