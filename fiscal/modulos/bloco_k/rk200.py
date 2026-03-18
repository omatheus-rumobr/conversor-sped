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


def _processar_linha_k200(linha, dt_fin_k100=None):
    """
    Processa uma única linha do registro K200 e retorna um dicionário.

    Formato:
      |K200|DT_EST|COD_ITEM|QTD|IND_EST|COD_PART|

    Regras (manual 3.1.8):
    - REG deve ser "K200"
    - DT_EST: obrigatório, formato ddmmaaaa
      - Deve ser igual à data final do período de apuração do K100 (quando informado)
    - COD_ITEM: obrigatório, até 60 caracteres
      - Deve existir no registro 0200
      - Somente tipos 00, 01, 02, 03, 04, 05, 06 e 10 (validação externa)
    - QTD: obrigatório, numérico com 3 decimais, não negativo
    - IND_EST: obrigatório, valores válidos ["0", "1", "2"]
      - Se IND_EST = "1" ou "2", COD_PART é obrigatório
    - COD_PART: opcional condicional, até 60 caracteres
      - Obrigatório quando IND_EST = "1" ou "2"

    Args:
        linha: linha SPED
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
    if reg != "K200":
        return None

    def obter_campo(indice):
        if indice < len(partes):
            valor = partes[indice].strip()
            if valor == "-":
                return ""
            return valor if valor else ""
        return ""

    dt_est = obter_campo(1)
    cod_item = obter_campo(2)
    qtd = obter_campo(3)
    ind_est = obter_campo(4)
    cod_part = obter_campo(5)

    # DT_EST: obrigatório, ddmmaaaa, data válida
    dt_est_ok, dt_est_obj = _validar_data(dt_est)
    if not dt_est_ok:
        return None

    # Validação: DT_EST deve ser igual à DT_FIN do K100 (quando informado)
    if dt_fin_k100:
        ok_k100_fin, dt_fin_k100_obj = _validar_data(dt_fin_k100)
        if ok_k100_fin and dt_est_obj != dt_fin_k100_obj:
            return None

    # COD_ITEM: obrigatório, até 60 caracteres
    if not cod_item or len(cod_item) > 60:
        return None

    # QTD: obrigatório, numérico com 3 decimais, não negativo
    qtd_ok, qtd_float, _ = validar_valor_numerico(qtd, decimais=3, obrigatorio=True, nao_negativo=True)
    if not qtd_ok:
        return None

    # IND_EST: obrigatório, valores válidos
    ind_est_validos = ["0", "1", "2"]
    if not ind_est or ind_est not in ind_est_validos:
        return None

    # COD_PART: opcional condicional, até 60 caracteres
    # Obrigatório quando IND_EST = "1" ou "2"
    if ind_est in ["1", "2"]:
        if not cod_part or len(cod_part) > 60:
            return None
    else:
        # Para IND_EST = "0", COD_PART é opcional mas se informado deve ter até 60 caracteres
        if cod_part and len(cod_part) > 60:
            return None

    def fmt_quantidade(v):
        return f"{v:,.3f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def fmt_data(d):
        return d.strftime("%d/%m/%Y") if d else ""

    descricoes_ind_est = {
        "0": "Estoque de propriedade do informante e em seu poder",
        "1": "Estoque de propriedade do informante e em posse de terceiros",
        "2": "Estoque de propriedade de terceiros e em posse do informante",
    }

    return {
        "REG": {"titulo": "Registro", "valor": reg},
        "DT_EST": {
            "titulo": "Data do estoque final",
            "valor": dt_est,
            "valor_formatado": fmt_data(dt_est_obj),
        },
        "COD_ITEM": {
            "titulo": "Código do item (campo 02 do Registro 0200)",
            "valor": cod_item,
        },
        "QTD": {
            "titulo": "Quantidade em estoque",
            "valor": qtd,
            "valor_formatado": fmt_quantidade(qtd_float),
        },
        "IND_EST": {
            "titulo": "Indicador do tipo de estoque",
            "valor": ind_est,
            "descricao": descricoes_ind_est.get(ind_est, ""),
        },
        "COD_PART": {
            "titulo": "Código do participante (campo 02 do Registro 0150): proprietário/possuidor que não seja o informante do arquivo",
            "valor": cod_part if cod_part else "",
        },
    }


def validar_k200_fiscal(linhas, dt_fin_k100=None):
    """
    Valida uma ou mais linhas do registro K200 do SPED EFD Fiscal.

    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |K200|DT_EST|COD_ITEM|QTD|IND_EST|COD_PART|
        dt_fin_k100: DT_FIN do registro K100 (ddmmaaaa) para validação da data (opcional)

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
        r = _processar_linha_k200(l, dt_fin_k100=dt_fin_k100)
        if r is not None:
            resultados.append(r)

    return json.dumps(resultados, ensure_ascii=False, indent=2)
