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


def _float_igual(a, b, tolerancia=0.01):
    """Compara dois floats com tolerância."""
    if a is None or b is None:
        return False
    return abs(a - b) <= tolerancia


def _processar_linha_g110(linha, dt_ini_0000=None, dt_fin_0000=None):
    """
    Processa uma única linha do registro G110 e retorna um dicionário.

    Formato:
      |G110|DT_INI|DT_FIN|SALDO_IN_ICMS|SOM_PARC|VL_TRIB_EXP|VL_TOTAL|IND_PER_SAI|ICMS_APROP|SOM_ICMS_OC|

    Regras (manual 3.1.8):
    - REG deve ser "G110"
    - DT_INI e DT_FIN devem estar no período do registro 0000 (quando informados)
    - DT_INI <= DT_FIN
    - VL_TRIB_EXP <= VL_TOTAL
    - IND_PER_SAI = VL_TRIB_EXP / VL_TOTAL (com tolerância para arredondamento)
    - IND_PER_SAI <= 1
    - ICMS_APROP = SOM_PARC * IND_PER_SAI (com tolerância para arredondamento)

    Args:
        linha: linha SPED
        dt_ini_0000: data ddmmaaaa do 0000 (opcional, para validação do intervalo)
        dt_fin_0000: data ddmmaaaa do 0000 (opcional, para validação do intervalo)

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
    if reg != "G110":
        return None

    def obter_campo(indice):
        if indice < len(partes):
            valor = partes[indice].strip()
            if valor == "-":
                return ""
            return valor if valor else ""
        return ""

    dt_ini = obter_campo(1)
    dt_fin = obter_campo(2)
    saldo_in_icms = obter_campo(3)
    som_parc = obter_campo(4)
    vl_trib_exp = obter_campo(5)
    vl_total = obter_campo(6)
    ind_per_sai = obter_campo(7)
    icms_aprop = obter_campo(8)
    som_icms_oc = obter_campo(9)

    # DT_INI: obrigatório, ddmmaaaa, data válida
    dt_ini_ok, dt_ini_obj = _validar_data(dt_ini)
    if not dt_ini_ok:
        return None

    # DT_FIN: obrigatório, ddmmaaaa, data válida
    dt_fin_ok, dt_fin_obj = _validar_data(dt_fin)
    if not dt_fin_ok:
        return None

    # DT_INI <= DT_FIN
    if dt_ini_obj and dt_fin_obj and dt_ini_obj > dt_fin_obj:
        return None

    # Validação contra período do 0000 (quando informado)
    if dt_ini_0000:
        ok_0000_ini, dt_ini_0000_obj = _validar_data(dt_ini_0000)
        if ok_0000_ini and dt_ini_obj < dt_ini_0000_obj:
            return None
    if dt_fin_0000:
        ok_0000_fin, dt_fin_0000_obj = _validar_data(dt_fin_0000)
        if ok_0000_fin and dt_fin_obj > dt_fin_0000_obj:
            return None

    # Quando ambos informados, garante que período do G110 está contido no 0000
    if dt_ini_0000 and dt_fin_0000:
        ok_0000_ini, dt_ini_0000_obj = _validar_data(dt_ini_0000)
        ok_0000_fin, dt_fin_0000_obj = _validar_data(dt_fin_0000)
        if ok_0000_ini and ok_0000_fin:
            if dt_ini_obj < dt_ini_0000_obj or dt_fin_obj > dt_fin_0000_obj:
                return None

    # SALDO_IN_ICMS: obrigatório, numérico com 2 decimais, não negativo
    saldo_ok, saldo_float, _ = validar_valor_numerico(saldo_in_icms, decimais=2, obrigatorio=True, nao_negativo=True)
    if not saldo_ok:
        return None

    # SOM_PARC: obrigatório, numérico com 2 decimais, não negativo
    som_parc_ok, som_parc_float, _ = validar_valor_numerico(som_parc, decimais=2, obrigatorio=True, nao_negativo=True)
    if not som_parc_ok:
        return None

    # VL_TRIB_EXP: obrigatório, numérico com 2 decimais, não negativo
    vl_trib_exp_ok, vl_trib_exp_float, _ = validar_valor_numerico(vl_trib_exp, decimais=2, obrigatorio=True, nao_negativo=True)
    if not vl_trib_exp_ok:
        return None

    # VL_TOTAL: obrigatório, numérico com 2 decimais, não negativo
    vl_total_ok, vl_total_float, _ = validar_valor_numerico(vl_total, decimais=2, obrigatorio=True, nao_negativo=True)
    if not vl_total_ok:
        return None

    # VL_TRIB_EXP <= VL_TOTAL
    if vl_trib_exp_float > vl_total_float:
        return None

    # IND_PER_SAI: obrigatório, numérico com 8 decimais, não negativo, <= 1
    ind_per_sai_ok, ind_per_sai_float, _ = validar_valor_numerico(ind_per_sai, decimais=8, obrigatorio=True, nao_negativo=True)
    if not ind_per_sai_ok:
        return None

    # IND_PER_SAI <= 1
    if ind_per_sai_float > 1.0:
        return None

    # Validação: IND_PER_SAI = VL_TRIB_EXP / VL_TOTAL (com tolerância para arredondamento)
    if vl_total_float > 0:
        ind_per_sai_calc = vl_trib_exp_float / vl_total_float
        # Tolerância maior para índice (até 0.00000001 devido a 8 decimais)
        if not _float_igual(ind_per_sai_float, ind_per_sai_calc, tolerancia=0.00000001):
            return None
    else:
        # Se VL_TOTAL = 0, então VL_TRIB_EXP também deve ser 0 e IND_PER_SAI deve ser 0
        if vl_trib_exp_float != 0.0 or ind_per_sai_float != 0.0:
            return None

    # ICMS_APROP: obrigatório, numérico com 2 decimais, não negativo
    icms_aprop_ok, icms_aprop_float, _ = validar_valor_numerico(icms_aprop, decimais=2, obrigatorio=True, nao_negativo=True)
    if not icms_aprop_ok:
        return None

    # Validação: ICMS_APROP = SOM_PARC * IND_PER_SAI (com tolerância para arredondamento)
    icms_aprop_calc = som_parc_float * ind_per_sai_float
    # Tolerância de 0.01 para valores monetários (2 decimais)
    if not _float_igual(icms_aprop_float, icms_aprop_calc, tolerancia=0.01):
        return None

    # SOM_ICMS_OC: obrigatório, numérico com 2 decimais, não negativo
    som_icms_oc_ok, som_icms_oc_float, _ = validar_valor_numerico(som_icms_oc, decimais=2, obrigatorio=True, nao_negativo=True)
    if not som_icms_oc_ok:
        return None

    def fmt_moeda(v):
        return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def fmt_data(d):
        return d.strftime("%d/%m/%Y") if d else ""

    def fmt_percentual(v):
        return f"{v * 100:.8f}%"

    return {
        "REG": {"titulo": "Registro", "valor": reg},
        "DT_INI": {
            "titulo": "Data inicial a que a apuração se refere",
            "valor": dt_ini,
            "valor_formatado": fmt_data(dt_ini_obj),
        },
        "DT_FIN": {
            "titulo": "Data final a que a apuração se refere",
            "valor": dt_fin,
            "valor_formatado": fmt_data(dt_fin_obj),
        },
        "SALDO_IN_ICMS": {
            "titulo": "Saldo inicial de ICMS do CIAP, composto por ICMS de bens que entraram anteriormente ao período de apuração",
            "valor": saldo_in_icms,
            "valor_formatado": fmt_moeda(saldo_float),
        },
        "SOM_PARC": {
            "titulo": "Somatório das parcelas de ICMS passível de apropriação de cada bem",
            "valor": som_parc,
            "valor_formatado": fmt_moeda(som_parc_float),
        },
        "VL_TRIB_EXP": {
            "titulo": "Valor do somatório das saídas tributadas e saídas para exportação",
            "valor": vl_trib_exp,
            "valor_formatado": fmt_moeda(vl_trib_exp_float),
        },
        "VL_TOTAL": {
            "titulo": "Valor total de saídas",
            "valor": vl_total,
            "valor_formatado": fmt_moeda(vl_total_float),
        },
        "IND_PER_SAI": {
            "titulo": "Índice de participação do valor do somatório das saídas tributadas e saídas para exportação no valor total de saídas",
            "valor": ind_per_sai,
            "valor_formatado": fmt_percentual(ind_per_sai_float),
        },
        "ICMS_APROP": {
            "titulo": "Valor de ICMS a ser apropriado na apuração do ICMS",
            "valor": icms_aprop,
            "valor_formatado": fmt_moeda(icms_aprop_float),
        },
        "SOM_ICMS_OC": {
            "titulo": "Valor de outros créditos a ser apropriado na Apuração do ICMS",
            "valor": som_icms_oc,
            "valor_formatado": fmt_moeda(som_icms_oc_float),
        },
    }


def validar_g110_fiscal(linhas, dt_ini_0000=None, dt_fin_0000=None):
    """
    Valida uma ou mais linhas do registro G110 do SPED EFD Fiscal.

    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |G110|DT_INI|DT_FIN|SALDO_IN_ICMS|SOM_PARC|VL_TRIB_EXP|VL_TOTAL|IND_PER_SAI|ICMS_APROP|SOM_ICMS_OC|
        dt_ini_0000: DT_INI do registro 0000 (ddmmaaaa) para validação do intervalo (opcional)
        dt_fin_0000: DT_FIN do registro 0000 (ddmmaaaa) para validação do intervalo (opcional)

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
        r = _processar_linha_g110(l, dt_ini_0000=dt_ini_0000, dt_fin_0000=dt_fin_0000)
        if r is not None:
            resultados.append(r)

    return json.dumps(resultados, ensure_ascii=False, indent=2)
