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
    """Compara dois floats com tolerância."""
    if a is None or b is None:
        return False
    return abs(a - b) <= tolerancia


def _processar_linha_e210(linha):
    """
    Processa uma única linha do registro E210 e retorna um dicionário.

    Formato:
      |E210|IND_MOV_ST|VL_SLD_CRED_ANT_ST|VL_DEVOL_ST|VL_RESSARC_ST|VL_OUT_CRED_ST|VL_AJ_CREDITOS_ST|VL_RETENÇAO_ST|VL_OUT_DEB_ST|VL_AJ_DEBITOS_ST|VL_SLD_DEV_ANT_ST|VL_DEDUÇÕES_ST|VL_ICMS_RECOL_ST|VL_SLD_CRED_ST_TRANSPORTAR|DEB_ESP_ST|

    Regras (manual 3.1.8):
    - REG deve ser "E210"
    - IND_MOV_ST deve ser 0 ou 1
    - Todos os campos numéricos são obrigatórios, com 2 decimais, não negativos
    - Validações de consistência interna conforme expressões do manual

    Args:
        linha: String com uma linha do SPED

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
    if reg != "E210":
        return None

    def obter_campo(indice):
        if indice < len(partes):
            valor = partes[indice].strip()
            if valor == "-":
                return ""
            return valor if valor else ""
        return ""

    # Extrai todos os campos (15 campos no total)
    ind_mov_st = obter_campo(1)
    vl_sld_cred_ant_st = obter_campo(2)
    vl_devol_st = obter_campo(3)
    vl_ressarc_st = obter_campo(4)
    vl_out_cred_st = obter_campo(5)
    vl_aj_creditos_st = obter_campo(6)
    vl_retencao_st = obter_campo(7)
    vl_out_deb_st = obter_campo(8)
    vl_aj_debitos_st = obter_campo(9)
    vl_sld_dev_ant_st = obter_campo(10)
    vl_deducoes_st = obter_campo(11)
    vl_icms_recol_st = obter_campo(12)
    vl_sld_cred_st_transportar = obter_campo(13)
    deb_esp_st = obter_campo(14)

    # IND_MOV_ST: obrigatório, valores válidos [0, 1]
    if ind_mov_st not in ["0", "1"]:
        return None

    # Valida todos os campos numéricos obrigatórios (todos com 2 decimais, não negativos)
    validacoes = [
        ("VL_SLD_CRED_ANT_ST", vl_sld_cred_ant_st, True),
        ("VL_DEVOL_ST", vl_devol_st, True),
        ("VL_RESSARC_ST", vl_ressarc_st, True),
        ("VL_OUT_CRED_ST", vl_out_cred_st, True),
        ("VL_AJ_CREDITOS_ST", vl_aj_creditos_st, True),
        ("VL_RETENÇAO_ST", vl_retencao_st, True),
        ("VL_OUT_DEB_ST", vl_out_deb_st, True),
        ("VL_AJ_DEBITOS_ST", vl_aj_debitos_st, True),
        ("VL_SLD_DEV_ANT_ST", vl_sld_dev_ant_st, True),
        ("VL_DEDUÇÕES_ST", vl_deducoes_st, True),
        ("VL_ICMS_RECOL_ST", vl_icms_recol_st, True),
        ("VL_SLD_CRED_ST_TRANSPORTAR", vl_sld_cred_st_transportar, True),
        ("DEB_ESP_ST", deb_esp_st, True),
    ]

    valores_float = {}
    for nome, valor_str, obrig in validacoes:
        ok, f, _ = validar_valor_numerico(valor_str, decimais=2, obrigatorio=obrig, nao_negativo=True)
        if not ok:
            return None
        valores_float[nome] = f

    # Validação Campo 11 (VL_SLD_DEV_ANT_ST) - Manual página 463-470
    # Expressão: (VL_RETENÇAO_ST + VL_OUT_DEB_ST + VL_AJ_DEBITOS_ST) - 
    #            (VL_SLD_CRED_ANT_ST + VL_DEVOL_ST + VL_RESSARC_ST + VL_OUT_CRED_ST + VL_AJ_CREDITOS_ST)
    # Se >= 0, informar o valor; se < 0, informar 0
    sld_dev_ant_calc = (
        valores_float["VL_RETENÇAO_ST"]
        + valores_float["VL_OUT_DEB_ST"]
        + valores_float["VL_AJ_DEBITOS_ST"]
        - valores_float["VL_SLD_CRED_ANT_ST"]
        - valores_float["VL_DEVOL_ST"]
        - valores_float["VL_RESSARC_ST"]
        - valores_float["VL_OUT_CRED_ST"]
        - valores_float["VL_AJ_CREDITOS_ST"]
    )
    sld_dev_ant_esperado = max(sld_dev_ant_calc, 0.0)
    if not _float_igual(valores_float["VL_SLD_DEV_ANT_ST"], sld_dev_ant_esperado):
        return None

    # Validação Campo 13 (VL_ICMS_RECOL_ST) - Manual página 478-479
    # Expressão: VL_SLD_DEV_ANT_ST - VL_DEDUÇÕES_ST
    icms_recol_calc = valores_float["VL_SLD_DEV_ANT_ST"] - valores_float["VL_DEDUÇÕES_ST"]
    icms_recol_esperado = max(icms_recol_calc, 0.0)
    if not _float_igual(valores_float["VL_ICMS_RECOL_ST"], icms_recol_esperado):
        return None

    # Validação Campo 14 (VL_SLD_CRED_ST_TRANSPORTAR) - Manual página 482-489
    # Expressão: (VL_RETENÇAO_ST + VL_OUT_DEB_ST + VL_AJ_DEBITOS_ST) - 
    #            (VL_SLD_CRED_ANT_ST + VL_DEVOL_ST + VL_RESSARC_ST + VL_OUT_CRED_ST + VL_AJ_CREDITOS_ST + VL_DEDUÇÕES_ST)
    # Se >= 0, informar 0; se < 0, informar valor absoluto
    sld_cred_transportar_calc = (
        valores_float["VL_RETENÇAO_ST"]
        + valores_float["VL_OUT_DEB_ST"]
        + valores_float["VL_AJ_DEBITOS_ST"]
        - valores_float["VL_SLD_CRED_ANT_ST"]
        - valores_float["VL_DEVOL_ST"]
        - valores_float["VL_RESSARC_ST"]
        - valores_float["VL_OUT_CRED_ST"]
        - valores_float["VL_AJ_CREDITOS_ST"]
        - valores_float["VL_DEDUÇÕES_ST"]
    )
    sld_cred_transportar_esperado = 0.0 if sld_cred_transportar_calc >= 0 else abs(sld_cred_transportar_calc)
    if not _float_igual(valores_float["VL_SLD_CRED_ST_TRANSPORTAR"], sld_cred_transportar_esperado):
        return None

    # Formatação monetária
    def fmt_moeda(v):
        return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    descricao_ind_mov = {
        "0": "Sem operações com ST",
        "1": "Com operações de ST",
    }.get(ind_mov_st, "")

    return {
        "REG": {"titulo": "Registro", "valor": reg},
        "IND_MOV_ST": {
            "titulo": "Indicador de movimento",
            "valor": ind_mov_st,
            "descricao": descricao_ind_mov,
        },
        "VL_SLD_CRED_ANT_ST": {
            "titulo": 'Valor do "Saldo credor de período anterior – Substituição Tributária"',
            "valor": vl_sld_cred_ant_st,
            "valor_formatado": fmt_moeda(valores_float["VL_SLD_CRED_ANT_ST"]),
        },
        "VL_DEVOL_ST": {
            "titulo": "Valor total do ICMS ST de devolução de mercadorias",
            "valor": vl_devol_st,
            "valor_formatado": fmt_moeda(valores_float["VL_DEVOL_ST"]),
        },
        "VL_RESSARC_ST": {
            "titulo": "Valor total do ICMS ST de ressarcimentos",
            "valor": vl_ressarc_st,
            "valor_formatado": fmt_moeda(valores_float["VL_RESSARC_ST"]),
        },
        "VL_OUT_CRED_ST": {
            "titulo": 'Valor total de Ajustes "Outros créditos ST" e "Estorno de débitos ST"',
            "valor": vl_out_cred_st,
            "valor_formatado": fmt_moeda(valores_float["VL_OUT_CRED_ST"]),
        },
        "VL_AJ_CREDITOS_ST": {
            "titulo": "Valor total dos ajustes a crédito de ICMS ST, provenientes de ajustes do documento fiscal",
            "valor": vl_aj_creditos_st,
            "valor_formatado": fmt_moeda(valores_float["VL_AJ_CREDITOS_ST"]),
        },
        "VL_RETENÇAO_ST": {
            "titulo": "Valor Total do ICMS retido por Substituição Tributária",
            "valor": vl_retencao_st,
            "valor_formatado": fmt_moeda(valores_float["VL_RETENÇAO_ST"]),
        },
        "VL_OUT_DEB_ST": {
            "titulo": 'Valor Total dos ajustes "Outros débitos ST" e "Estorno de créditos ST"',
            "valor": vl_out_deb_st,
            "valor_formatado": fmt_moeda(valores_float["VL_OUT_DEB_ST"]),
        },
        "VL_AJ_DEBITOS_ST": {
            "titulo": "Valor total dos ajustes a débito de ICMS ST, provenientes de ajustes do documento fiscal",
            "valor": vl_aj_debitos_st,
            "valor_formatado": fmt_moeda(valores_float["VL_AJ_DEBITOS_ST"]),
        },
        "VL_SLD_DEV_ANT_ST": {
            "titulo": "Valor total de Saldo devedor antes das deduções",
            "valor": vl_sld_dev_ant_st,
            "valor_formatado": fmt_moeda(valores_float["VL_SLD_DEV_ANT_ST"]),
        },
        "VL_DEDUÇÕES_ST": {
            "titulo": 'Valor total dos ajustes "Deduções ST"',
            "valor": vl_deducoes_st,
            "valor_formatado": fmt_moeda(valores_float["VL_DEDUÇÕES_ST"]),
        },
        "VL_ICMS_RECOL_ST": {
            "titulo": "Imposto a recolher ST (11-12)",
            "valor": vl_icms_recol_st,
            "valor_formatado": fmt_moeda(valores_float["VL_ICMS_RECOL_ST"]),
        },
        "VL_SLD_CRED_ST_TRANSPORTAR": {
            "titulo": "Saldo credor de ST a transportar para o período seguinte [(03+04+05+06+07+12) – (08+09+10)]",
            "valor": vl_sld_cred_st_transportar,
            "valor_formatado": fmt_moeda(valores_float["VL_SLD_CRED_ST_TRANSPORTAR"]),
        },
        "DEB_ESP_ST": {
            "titulo": "Valores recolhidos ou a recolher, extra-apuração",
            "valor": deb_esp_st,
            "valor_formatado": fmt_moeda(valores_float["DEB_ESP_ST"]),
        },
    }


def validar_e210(linhas):
    """
    Valida uma ou mais linhas do registro E210 do SPED EFD Fiscal.

    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |E210|IND_MOV_ST|VL_SLD_CRED_ANT_ST|VL_DEVOL_ST|VL_RESSARC_ST|VL_OUT_CRED_ST|VL_AJ_CREDITOS_ST|VL_RETENÇAO_ST|VL_OUT_DEB_ST|VL_AJ_DEBITOS_ST|VL_SLD_DEV_ANT_ST|VL_DEDUÇÕES_ST|VL_ICMS_RECOL_ST|VL_SLD_CRED_ST_TRANSPORTAR|DEB_ESP_ST|

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
        r = _processar_linha_e210(l)
        if r is not None:
            resultados.append(r)

    return json.dumps(resultados, ensure_ascii=False, indent=2)
