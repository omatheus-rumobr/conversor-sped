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


def _processar_linha_k260(linha, dt_ini_k100=None, dt_fin_k100=None):
    """
    Processa uma única linha do registro K260 e retorna um dicionário.

    Formato:
      |K260|COD_OP_OS|COD_ITEM|DT_SAÍDA|QTD_SAÍDA|DT_RET|QTD_RET|

    Regras (manual 3.1.8):
    - REG deve ser "K260"
    - COD_OP_OS: opcional condicional, até 30 caracteres
      - Obrigatório se DT_RET não for preenchido e DT_SAÍDA estiver no período de apuração do K100
    - COD_ITEM: obrigatório, até 60 caracteres
      - Deve existir no registro 0200 (validação externa)
    - DT_SAÍDA: obrigatório, formato ddmmaaaa
      - Deve ser menor ou igual a DT_FIN do registro K100
    - QTD_SAÍDA: obrigatório, numérico com 6 decimais, não negativo
    - DT_RET: opcional condicional, formato ddmmaaaa
      - Deve estar no período de apuração K100
      - Deve ser maior ou igual a DT_SAÍDA
    - QTD_RET: opcional condicional, numérico com 6 decimais, não negativo
      - Obrigatório se DT_RET estiver preenchido

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
    if reg != "K260":
        return None

    def obter_campo(indice):
        if indice < len(partes):
            valor = partes[indice].strip()
            if valor == "-":
                return ""
            return valor if valor else ""
        return ""

    cod_op_os = obter_campo(1)
    cod_item = obter_campo(2)
    dt_saida = obter_campo(3)
    qtd_saida = obter_campo(4)
    dt_ret = obter_campo(5)
    qtd_ret = obter_campo(6)

    # DT_SAÍDA: obrigatório, ddmmaaaa, data válida
    dt_saida_ok, dt_saida_obj = _validar_data(dt_saida)
    if not dt_saida_ok:
        return None

    # Validação: DT_SAÍDA deve ser menor ou igual a DT_FIN do registro K100
    if dt_fin_k100:
        ok_k100_fin, dt_fin_k100_obj = _validar_data(dt_fin_k100)
        if ok_k100_fin and dt_saida_obj > dt_fin_k100_obj:
            return None

    # DT_RET: opcional condicional, ddmmaaaa, data válida
    dt_ret_obj = None
    if dt_ret:
        dt_ret_ok, dt_ret_obj = _validar_data(dt_ret)
        if not dt_ret_ok:
            return None

        # Validação: DT_RET deve estar no período de apuração K100
        if dt_ini_k100 and dt_fin_k100:
            ok_k100_ini, dt_ini_k100_obj = _validar_data(dt_ini_k100)
            ok_k100_fin, dt_fin_k100_obj = _validar_data(dt_fin_k100)
            if ok_k100_ini and ok_k100_fin:
                if dt_ret_obj < dt_ini_k100_obj or dt_ret_obj > dt_fin_k100_obj:
                    return None

        # Validação: DT_RET deve ser maior ou igual a DT_SAÍDA
        if dt_ret_obj < dt_saida_obj:
            return None

    # COD_OP_OS: opcional condicional, até 30 caracteres
    # Obrigatório se DT_RET não for preenchido e DT_SAÍDA estiver no período de apuração do K100
    if not dt_ret and dt_ini_k100 and dt_fin_k100:
        ok_k100_ini, dt_ini_k100_obj = _validar_data(dt_ini_k100)
        ok_k100_fin, dt_fin_k100_obj = _validar_data(dt_fin_k100)
        if ok_k100_ini and ok_k100_fin:
            # Se DT_SAÍDA está no período de apuração do K100, COD_OP_OS é obrigatório
            if dt_saida_obj >= dt_ini_k100_obj and dt_saida_obj <= dt_fin_k100_obj:
                if not cod_op_os or len(cod_op_os) > 30:
                    return None
    else:
        # Se COD_OP_OS for informado, deve ter até 30 caracteres
        if cod_op_os and len(cod_op_os) > 30:
            return None

    # COD_ITEM: obrigatório, até 60 caracteres
    if not cod_item or len(cod_item) > 60:
        return None

    # QTD_SAÍDA: obrigatório, numérico com 6 decimais, não negativo
    qtd_saida_ok, qtd_saida_float, _ = validar_valor_numerico(qtd_saida, decimais=6, obrigatorio=True, nao_negativo=True)
    if not qtd_saida_ok:
        return None

    # QTD_RET: opcional condicional, numérico com 6 decimais, não negativo
    # Obrigatório se DT_RET estiver preenchido
    if dt_ret:
        qtd_ret_ok, qtd_ret_float, _ = validar_valor_numerico(qtd_ret, decimais=6, obrigatorio=True, nao_negativo=True)
        if not qtd_ret_ok:
            return None
    else:
        # Se DT_RET não estiver preenchido, QTD_RET é opcional mas se informado deve ser válido
        if qtd_ret:
            qtd_ret_ok, qtd_ret_float, _ = validar_valor_numerico(qtd_ret, decimais=6, obrigatorio=False, nao_negativo=True)
            if not qtd_ret_ok:
                return None
        else:
            qtd_ret_float = None

    def fmt_quantidade(v):
        return f"{v:,.6f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def fmt_data(d):
        return d.strftime("%d/%m/%Y") if d else ""

    return {
        "REG": {"titulo": "Registro", "valor": reg},
        "COD_OP_OS": {
            "titulo": "Código de identificação da ordem de produção, no reprocessamento, ou da ordem de serviço, no reparo",
            "valor": cod_op_os if cod_op_os else "",
        },
        "COD_ITEM": {
            "titulo": "Código do produto/insumo a ser reprocessado/reparado ou já reprocessado/reparado (campo 02 do Registro 0200)",
            "valor": cod_item,
        },
        "DT_SAÍDA": {
            "titulo": "Data de saída do estoque",
            "valor": dt_saida,
            "valor_formatado": fmt_data(dt_saida_obj),
        },
        "QTD_SAÍDA": {
            "titulo": "Quantidade de saída do estoque",
            "valor": qtd_saida,
            "valor_formatado": fmt_quantidade(qtd_saida_float),
        },
        "DT_RET": {
            "titulo": "Data de retorno ao estoque (entrada)",
            "valor": dt_ret if dt_ret else "",
            "valor_formatado": fmt_data(dt_ret_obj) if dt_ret_obj else "",
        },
        "QTD_RET": {
            "titulo": "Quantidade de retorno ao estoque (entrada)",
            "valor": qtd_ret if qtd_ret else "",
            "valor_formatado": fmt_quantidade(qtd_ret_float) if qtd_ret_float is not None else "",
        },
    }


def validar_k260(linhas, dt_ini_k100=None, dt_fin_k100=None):
    """
    Valida uma ou mais linhas do registro K260 do SPED EFD Fiscal.

    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |K260|COD_OP_OS|COD_ITEM|DT_SAÍDA|QTD_SAÍDA|DT_RET|QTD_RET|
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
        r = _processar_linha_k260(l, dt_ini_k100=dt_ini_k100, dt_fin_k100=dt_fin_k100)
        if r is not None:
            resultados.append(r)

    return json.dumps(resultados, ensure_ascii=False, indent=2)
