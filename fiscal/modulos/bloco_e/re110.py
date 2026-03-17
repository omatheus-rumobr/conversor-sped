import json


def validar_valor_numerico(valor_str, decimais=2, obrigatorio=False, positivo=False, nao_negativo=False):
    """
    Valida um valor numérico com precisão decimal específica.

    Args:
        valor_str: String com o valor numérico
        decimais: Número máximo de casas decimais permitidas
        obrigatorio: Se True, o campo não pode estar vazio
        positivo: Se True, o valor deve ser maior que 0
        nao_negativo: Se True, o valor deve ser maior ou igual a 0

    Returns:
        tuple: (True/False, valor float ou None, mensagem de erro ou None)
    """
    if valor_str is None:
        valor_str = ""

    if not valor_str:
        if obrigatorio:
            return False, None, "Campo obrigatório não preenchido"
        return True, 0.0, None

    try:
        valor_float = float(valor_str)

        # Verifica precisão decimal (quando houver ponto decimal)
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
    if a is None or b is None:
        return False
    return abs(a - b) <= tolerancia


def _processar_linha_e110(linha):
    """
    Processa uma única linha do registro E110 e retorna um dicionário.

    Args:
        linha: String com uma linha do SPED no formato:
              |E110|VL_TOT_DEBITOS|VL_AJ_DEBITOS|VL_TOT_AJ_DEBITOS|VL_ESTORNOS_CRED|VL_TOT_CREDITOS|VL_AJ_CREDITOS|VL_TOT_AJ_CREDITOS|VL_ESTORNOS_DEB|VL_SLD_CREDOR_ANT|VL_SLD_APURADO|VL_TOT_DED|VL_ICMS_RECOLHER|VL_SLD_CREDOR_TRANSPORTAR|DEB_ESP|

    Returns:
        dict: Dicionário com os campos validados contendo título e valor, ou None se inválido
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
    if reg != "E110":
        return None

    def obter_campo(indice):
        if indice < len(partes):
            valor = partes[indice].strip()
            if valor == "-":
                return ""
            return valor if valor else ""
        return ""

    # Campos (15 no total, contando REG)
    vl_tot_debitos = obter_campo(1)
    vl_aj_debitos = obter_campo(2)
    vl_tot_aj_debitos = obter_campo(3)
    vl_estornos_cred = obter_campo(4)
    vl_tot_creditos = obter_campo(5)
    vl_aj_creditos = obter_campo(6)
    vl_tot_aj_creditos = obter_campo(7)
    vl_estornos_deb = obter_campo(8)
    vl_sld_credor_ant = obter_campo(9)
    vl_sld_apurado = obter_campo(10)
    vl_tot_ded = obter_campo(11)
    vl_icms_recolher = obter_campo(12)
    vl_sld_credor_transportar = obter_campo(13)
    deb_esp = obter_campo(14)

    # Todos os campos numéricos do E110 são obrigatórios (manual), inclusive em período sem movimento (zerados)
    validacoes = [
        ("VL_TOT_DEBITOS", vl_tot_debitos, True, True),
        ("VL_AJ_DEBITOS", vl_aj_debitos, True, True),
        ("VL_TOT_AJ_DEBITOS", vl_tot_aj_debitos, True, True),
        ("VL_ESTORNOS_CRED", vl_estornos_cred, True, True),
        ("VL_TOT_CREDITOS", vl_tot_creditos, True, True),
        ("VL_AJ_CREDITOS", vl_aj_creditos, True, True),
        ("VL_TOT_AJ_CREDITOS", vl_tot_aj_creditos, True, True),
        ("VL_ESTORNOS_DEB", vl_estornos_deb, True, True),
        ("VL_SLD_CREDOR_ANT", vl_sld_credor_ant, True, True),
        ("VL_SLD_APURADO", vl_sld_apurado, True, True),
        ("VL_TOT_DED", vl_tot_ded, True, True),
        ("VL_ICMS_RECOLHER", vl_icms_recolher, True, True),
        ("VL_SLD_CREDOR_TRANSPORTAR", vl_sld_credor_transportar, True, True),
        ("DEB_ESP", deb_esp, True, True),
    ]

    valores_float = {}
    for nome, valor_str, obrig, nao_neg in validacoes:
        ok, f, _ = validar_valor_numerico(valor_str, decimais=2, obrigatorio=obrig, nao_negativo=nao_neg)
        if not ok:
            return None
        valores_float[nome] = f

    # Validação de consistência interna (Manual - Campo 11 e 14; Campo 13)
    # Expressão do saldo base (antes de deduções):
    # (Débitos + ajustes a débito + total ajustes a débito + estornos de débito)
    # - (Créditos + ajustes a crédito + total ajustes a crédito + estornos de crédito + saldo credor anterior)
    sld_base = (
        valores_float["VL_TOT_DEBITOS"]
        + valores_float["VL_AJ_DEBITOS"]
        + valores_float["VL_TOT_AJ_DEBITOS"]
        + valores_float["VL_ESTORNOS_DEB"]
        - valores_float["VL_TOT_CREDITOS"]
        - valores_float["VL_AJ_CREDITOS"]
        - valores_float["VL_TOT_AJ_CREDITOS"]
        - valores_float["VL_ESTORNOS_CRED"]
        - valores_float["VL_SLD_CREDOR_ANT"]
    )

    sld_apurado_esperado = max(sld_base, 0.0)
    if not _float_igual(valores_float["VL_SLD_APURADO"], sld_apurado_esperado):
        return None

    # Campo 13: ICMS a recolher = VL_SLD_APURADO - VL_TOT_DED (se negativo, informar 0)
    icms_recolher_calc = valores_float["VL_SLD_APURADO"] - valores_float["VL_TOT_DED"]
    icms_recolher_esperado = max(icms_recolher_calc, 0.0)
    if not _float_igual(valores_float["VL_ICMS_RECOLHER"], icms_recolher_esperado):
        return None

    # Campo 14: Saldo credor a transportar.
    # Se (saldo base - deduções) >= 0 => 0
    # Senão => valor absoluto (equivalente a VL_TOT_DED - saldo base)
    sld_apos_ded = sld_base - valores_float["VL_TOT_DED"]
    sld_transportar_esperado = 0.0 if sld_apos_ded >= 0 else abs(sld_apos_ded)
    if not _float_igual(valores_float["VL_SLD_CREDOR_TRANSPORTAR"], sld_transportar_esperado):
        return None

    # Formatação monetária
    def fmt_moeda(v):
        return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    resultado = {
        "REG": {"titulo": "Registro", "valor": reg},
        "VL_TOT_DEBITOS": {"titulo": "Valor total dos débitos por \"Saídas e prestações com débito do imposto\"", "valor": vl_tot_debitos, "valor_formatado": fmt_moeda(valores_float["VL_TOT_DEBITOS"])},
        "VL_AJ_DEBITOS": {"titulo": "Valor total dos ajustes a débito decorrentes do documento fiscal", "valor": vl_aj_debitos, "valor_formatado": fmt_moeda(valores_float["VL_AJ_DEBITOS"])},
        "VL_TOT_AJ_DEBITOS": {"titulo": "Valor total de \"Ajustes a débito\"", "valor": vl_tot_aj_debitos, "valor_formatado": fmt_moeda(valores_float["VL_TOT_AJ_DEBITOS"])},
        "VL_ESTORNOS_CRED": {"titulo": "Valor total de Ajustes \"Estornos de créditos\"", "valor": vl_estornos_cred, "valor_formatado": fmt_moeda(valores_float["VL_ESTORNOS_CRED"])},
        "VL_TOT_CREDITOS": {"titulo": "Valor total dos créditos por \"Entradas e aquisições com crédito do imposto\"", "valor": vl_tot_creditos, "valor_formatado": fmt_moeda(valores_float["VL_TOT_CREDITOS"])},
        "VL_AJ_CREDITOS": {"titulo": "Valor total dos ajustes a crédito decorrentes do documento fiscal", "valor": vl_aj_creditos, "valor_formatado": fmt_moeda(valores_float["VL_AJ_CREDITOS"])},
        "VL_TOT_AJ_CREDITOS": {"titulo": "Valor total de \"Ajustes a crédito\"", "valor": vl_tot_aj_creditos, "valor_formatado": fmt_moeda(valores_float["VL_TOT_AJ_CREDITOS"])},
        "VL_ESTORNOS_DEB": {"titulo": "Valor total de Ajustes \"Estornos de Débitos\"", "valor": vl_estornos_deb, "valor_formatado": fmt_moeda(valores_float["VL_ESTORNOS_DEB"])},
        "VL_SLD_CREDOR_ANT": {"titulo": "Valor total de \"Saldo credor do período anterior\"", "valor": vl_sld_credor_ant, "valor_formatado": fmt_moeda(valores_float["VL_SLD_CREDOR_ANT"])},
        "VL_SLD_APURADO": {"titulo": "Valor do saldo devedor apurado", "valor": vl_sld_apurado, "valor_formatado": fmt_moeda(valores_float["VL_SLD_APURADO"])},
        "VL_TOT_DED": {"titulo": "Valor total de \"Deduções\"", "valor": vl_tot_ded, "valor_formatado": fmt_moeda(valores_float["VL_TOT_DED"])},
        "VL_ICMS_RECOLHER": {"titulo": "Valor total de \"ICMS a recolher (11-12)\"", "valor": vl_icms_recolher, "valor_formatado": fmt_moeda(valores_float["VL_ICMS_RECOLHER"])},
        "VL_SLD_CREDOR_TRANSPORTAR": {"titulo": "Valor total de \"Saldo credor a transportar para o período seguinte\"", "valor": vl_sld_credor_transportar, "valor_formatado": fmt_moeda(valores_float["VL_SLD_CREDOR_TRANSPORTAR"])},
        "DEB_ESP": {"titulo": "Valores recolhidos ou a recolher, extra-apuração", "valor": deb_esp, "valor_formatado": fmt_moeda(valores_float["DEB_ESP"])},
    }

    return resultado


def validar_e110(linhas):
    """
    Valida uma ou mais linhas do registro E110 do SPED EFD Fiscal.

    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |E110|VL_TOT_DEBITOS|VL_AJ_DEBITOS|VL_TOT_AJ_DEBITOS|VL_ESTORNOS_CRED|VL_TOT_CREDITOS|VL_AJ_CREDITOS|VL_TOT_AJ_CREDITOS|VL_ESTORNOS_DEB|VL_SLD_CREDOR_ANT|VL_SLD_APURADO|VL_TOT_DED|VL_ICMS_RECOLHER|VL_SLD_CREDOR_TRANSPORTAR|DEB_ESP|

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
        r = _processar_linha_e110(l)
        if r is not None:
            resultados.append(r)

    return json.dumps(resultados, ensure_ascii=False, indent=2)