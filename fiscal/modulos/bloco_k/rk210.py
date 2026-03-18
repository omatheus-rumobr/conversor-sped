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


def _processar_linha_k210(linha, dt_ini_k100=None, dt_fin_k100=None):
    """
    Processa uma única linha do registro K210 e retorna um dicionário.

    Formato:
      |K210|DT_INI_OS|DT_FIN_OS|COD_DOC_OS|COD_ITEM_ORI|QTD_ORI|

    Regras (manual 3.1.8):
    - REG deve ser "K210"
    - DT_INI_OS: opcional condicional, formato ddmmaaaa
      - Obrigatório se informado COD_DOC_OS ou DT_FIN_OS
      - Deve ser <= DT_FIN do K100 (quando informado)
    - DT_FIN_OS: opcional condicional, formato ddmmaaaa
      - Se preenchido, deve estar no período do K100 e ser >= DT_INI_OS
    - COD_DOC_OS: opcional condicional, até 30 caracteres
      - Obrigatório se informado DT_INI_OS
    - COD_ITEM_ORI: obrigatório, até 60 caracteres
    - QTD_ORI: obrigatório, numérico com 6 decimais, não negativo

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
    if reg != "K210":
        return None

    def obter_campo(indice):
        if indice < len(partes):
            valor = partes[indice].strip()
            if valor == "-":
                return ""
            return valor if valor else ""
        return ""

    dt_ini_os = obter_campo(1)
    dt_fin_os = obter_campo(2)
    cod_doc_os = obter_campo(3)
    cod_item_ori = obter_campo(4)
    qtd_ori = obter_campo(5)

    # Validação condicional dos campos de ordem de serviço
    # DT_INI_OS é obrigatório se informado COD_DOC_OS ou DT_FIN_OS
    if cod_doc_os or dt_fin_os:
        if not dt_ini_os:
            return None

    # COD_DOC_OS é obrigatório se informado DT_INI_OS
    if dt_ini_os:
        if not cod_doc_os:
            return None

    # DT_INI_OS: opcional condicional, ddmmaaaa, data válida
    dt_ini_os_obj = None
    if dt_ini_os:
        dt_ini_os_ok, dt_ini_os_obj = _validar_data(dt_ini_os)
        if not dt_ini_os_ok:
            return None

        # Validação: DT_INI_OS deve ser <= DT_FIN do K100 (quando informado)
        if dt_fin_k100:
            ok_k100_fin, dt_fin_k100_obj = _validar_data(dt_fin_k100)
            if ok_k100_fin and dt_ini_os_obj > dt_fin_k100_obj:
                return None

    # DT_FIN_OS: opcional condicional, ddmmaaaa, data válida
    dt_fin_os_obj = None
    if dt_fin_os:
        dt_fin_os_ok, dt_fin_os_obj = _validar_data(dt_fin_os)
        if not dt_fin_os_ok:
            return None

        # Validação: DT_FIN_OS deve ser >= DT_INI_OS
        if dt_ini_os_obj and dt_fin_os_obj < dt_ini_os_obj:
            return None

        # Validação: DT_FIN_OS deve estar no período do K100 (quando informado)
        if dt_ini_k100 and dt_fin_k100:
            ok_k100_ini, dt_ini_k100_obj = _validar_data(dt_ini_k100)
            ok_k100_fin, dt_fin_k100_obj = _validar_data(dt_fin_k100)
            if ok_k100_ini and ok_k100_fin:
                if dt_fin_os_obj < dt_ini_k100_obj or dt_fin_os_obj > dt_fin_k100_obj:
                    return None

    # COD_DOC_OS: opcional condicional, até 30 caracteres
    if cod_doc_os and len(cod_doc_os) > 30:
        return None

    # COD_ITEM_ORI: obrigatório, até 60 caracteres
    if not cod_item_ori or len(cod_item_ori) > 60:
        return None

    # QTD_ORI: obrigatório, numérico com 6 decimais, não negativo
    qtd_ori_ok, qtd_ori_float, _ = validar_valor_numerico(qtd_ori, decimais=6, obrigatorio=True, nao_negativo=True)
    if not qtd_ori_ok:
        return None

    def fmt_quantidade(v):
        return f"{v:,.6f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def fmt_data(d):
        return d.strftime("%d/%m/%Y") if d else ""

    return {
        "REG": {"titulo": "Registro", "valor": reg},
        "DT_INI_OS": {
            "titulo": "Data de início da ordem de serviço",
            "valor": dt_ini_os if dt_ini_os else "",
            "valor_formatado": fmt_data(dt_ini_os_obj) if dt_ini_os_obj else "",
        },
        "DT_FIN_OS": {
            "titulo": "Data de conclusão da ordem de serviço",
            "valor": dt_fin_os if dt_fin_os else "",
            "valor_formatado": fmt_data(dt_fin_os_obj) if dt_fin_os_obj else "",
        },
        "COD_DOC_OS": {
            "titulo": "Código de identificação da ordem de serviço",
            "valor": cod_doc_os if cod_doc_os else "",
        },
        "COD_ITEM_ORI": {
            "titulo": "Código do item de origem (campo 02 do Registro 0200)",
            "valor": cod_item_ori,
        },
        "QTD_ORI": {
            "titulo": "Quantidade de origem – saída do estoque",
            "valor": qtd_ori,
            "valor_formatado": fmt_quantidade(qtd_ori_float),
        },
    }


def validar_k210_fiscal(linhas, dt_ini_k100=None, dt_fin_k100=None):
    """
    Valida uma ou mais linhas do registro K210 do SPED EFD Fiscal.

    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |K210|DT_INI_OS|DT_FIN_OS|COD_DOC_OS|COD_ITEM_ORI|QTD_ORI|
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
        r = _processar_linha_k210(l, dt_ini_k100=dt_ini_k100, dt_fin_k100=dt_fin_k100)
        if r is not None:
            resultados.append(r)

    return json.dumps(resultados, ensure_ascii=False, indent=2)
