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


def _processar_linha_k250(linha, dt_ini_k100=None, dt_fin_k100=None):
    """
    Processa uma única linha do registro K250 e retorna um dicionário.

    Formato:
      |K250|DT_PROD|COD_ITEM|QTD|

    Regras (manual 3.1.8):
    - REG deve ser "K250"
    - DT_PROD: obrigatório, formato ddmmaaaa
      - Deve estar no período do K100 (quando informado)
    - COD_ITEM: obrigatório, até 60 caracteres
      - Deve existir no registro 0200 (validação externa)
      - TIPO_ITEM deve ser 03 (Produto em Processo) ou 04 (Produto Acabado) (validação externa)
    - QTD: obrigatório, numérico com 6 decimais, não negativo

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
    if reg != "K250":
        return None

    def obter_campo(indice):
        if indice < len(partes):
            valor = partes[indice].strip()
            if valor == "-":
                return ""
            return valor if valor else ""
        return ""

    dt_prod = obter_campo(1)
    cod_item = obter_campo(2)
    qtd = obter_campo(3)

    # DT_PROD: obrigatório, ddmmaaaa, data válida
    dt_prod_ok, dt_prod_obj = _validar_data(dt_prod)
    if not dt_prod_ok:
        return None

    # Validação: DT_PROD deve estar no período do K100 (quando informado)
    if dt_ini_k100 and dt_fin_k100:
        ok_k100_ini, dt_ini_k100_obj = _validar_data(dt_ini_k100)
        ok_k100_fin, dt_fin_k100_obj = _validar_data(dt_fin_k100)
        if ok_k100_ini and ok_k100_fin:
            if dt_prod_obj < dt_ini_k100_obj or dt_prod_obj > dt_fin_k100_obj:
                return None

    # COD_ITEM: obrigatório, até 60 caracteres
    if not cod_item or len(cod_item) > 60:
        return None

    # QTD: obrigatório, numérico com 6 decimais, não negativo
    qtd_ok, qtd_float, _ = validar_valor_numerico(qtd, decimais=6, obrigatorio=True, nao_negativo=True)
    if not qtd_ok:
        return None

    def fmt_quantidade(v):
        return f"{v:,.6f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def fmt_data(d):
        return d.strftime("%d/%m/%Y") if d else ""

    return {
        "REG": {"titulo": "Registro", "valor": reg},
        "DT_PROD": {
            "titulo": "Data do reconhecimento da produção ocorrida no terceiro",
            "valor": dt_prod,
            "valor_formatado": fmt_data(dt_prod_obj),
        },
        "COD_ITEM": {
            "titulo": "Código do item produzido (campo 02 do Registro 0200)",
            "valor": cod_item,
        },
        "QTD": {
            "titulo": "Quantidade produzida",
            "valor": qtd,
            "valor_formatado": fmt_quantidade(qtd_float),
        },
    }


def validar_k250(linhas, dt_ini_k100=None, dt_fin_k100=None):
    """
    Valida uma ou mais linhas do registro K250 do SPED EFD Fiscal.

    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |K250|DT_PROD|COD_ITEM|QTD|
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
        r = _processar_linha_k250(l, dt_ini_k100=dt_ini_k100, dt_fin_k100=dt_fin_k100)
        if r is not None:
            resultados.append(r)

    return json.dumps(resultados, ensure_ascii=False, indent=2)
