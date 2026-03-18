import json
from datetime import datetime


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


def _validar_data(data_str):
    """
    Valida se a data está no formato ddmmaaaa e se é uma data válida.
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


def _determinar_versao_e310(dt_ini_periodo=None):
    """
    Determina qual versão do E310 usar baseado na data do período.
    
    Args:
        dt_ini_periodo: Data inicial do período (ddmmaaaa) ou datetime
        
    Returns:
        bool: True se versão nova (>= 2017-01-01), False se versão antiga (<= 2016-12-31)
    """
    if dt_ini_periodo is None:
        # Por padrão, assume versão nova (mais recente)
        return True
    
    # Converte string para datetime se necessário
    if isinstance(dt_ini_periodo, str):
        ok, dt_obj = _validar_data(dt_ini_periodo)
        if not ok:
            return True  # Por padrão, assume versão nova
        dt_ini_periodo = dt_obj
    
    # Data de corte: 01/01/2017
    data_corte = datetime(2017, 1, 1)
    return dt_ini_periodo >= data_corte


def _processar_linha_e310_antiga(linha):
    """
    Processa uma única linha do registro E310 (versão até 31/12/2016 - 14 campos).
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
    if reg != "E310":
        return None

    def obter_campo(indice):
        if indice < len(partes):
            valor = partes[indice].strip()
            if valor == "-":
                return ""
            return valor if valor else ""
        return ""

    # Versão antiga: 14 campos
    ind_mov_difal = obter_campo(1)
    vl_sld_cred_ant_difal = obter_campo(2)
    vl_tot_debitos_difal = obter_campo(3)
    vl_out_deb_difal = obter_campo(4)
    vl_tot_deb_fcp = obter_campo(5)
    vl_tot_creditos_difal = obter_campo(6)
    vl_tot_cred_fcp = obter_campo(7)
    vl_out_cred_difal = obter_campo(8)
    vl_sld_dev_ant_difal = obter_campo(9)
    vl_deducoes_difal = obter_campo(10)
    vl_recol = obter_campo(11)
    vl_sld_cred_transportar = obter_campo(12)
    deb_esp_difal = obter_campo(13)

    # IND_MOV_DIFAL: obrigatório, valores válidos [0, 1]
    if ind_mov_difal not in ["0", "1"]:
        return None

    # Valida todos os campos numéricos obrigatórios
    validacoes = [
        ("VL_SLD_CRED_ANT_DIFAL", vl_sld_cred_ant_difal, True),
        ("VL_TOT_DEBITOS_DIFAL", vl_tot_debitos_difal, True),
        ("VL_OUT_DEB_DIFAL", vl_out_deb_difal, True),
        ("VL_TOT_DEB_FCP", vl_tot_deb_fcp, True),
        ("VL_TOT_CREDITOS_DIFAL", vl_tot_creditos_difal, True),
        ("VL_TOT_CRED_FCP", vl_tot_cred_fcp, True),
        ("VL_OUT_CRED_DIFAL", vl_out_cred_difal, True),
        ("VL_SLD_DEV_ANT_DIFAL", vl_sld_dev_ant_difal, True),
        ("VL_DEDUÇÕES_DIFAL", vl_deducoes_difal, True),
        ("VL_RECOL", vl_recol, True),
        ("VL_SLD_CRED_TRANSPORTAR", vl_sld_cred_transportar, True),
        ("DEB_ESP_DIFAL", deb_esp_difal, True),
    ]

    valores_float = {}
    for nome, valor_str, obrig in validacoes:
        ok, f, _ = validar_valor_numerico(valor_str, decimais=2, obrigatorio=obrig, nao_negativo=True)
        if not ok:
            return None
        valores_float[nome] = f

    # Validação Campo 10 (VL_SLD_DEV_ANT_DIFAL) - Manual linha 756-759
    # Se (VL_TOT_DEBITOS_DIFAL + VL_OUT_DEB_DIFAL + VL_TOT_DEB_FCP) menos
    # (VL_SLD_CRED_ANT_DIFAL + VL_TOT_CREDITOS_DIFAL + VL_OUT_CRED_DIFAL + VL_TOT_CRED_FCP) >= 0,
    # então igual ao resultado; senão = 0
    sld_dev_ant_calc = (
        valores_float["VL_TOT_DEBITOS_DIFAL"]
        + valores_float["VL_OUT_DEB_DIFAL"]
        + valores_float["VL_TOT_DEB_FCP"]
        - valores_float["VL_SLD_CRED_ANT_DIFAL"]
        - valores_float["VL_TOT_CREDITOS_DIFAL"]
        - valores_float["VL_OUT_CRED_DIFAL"]
        - valores_float["VL_TOT_CRED_FCP"]
    )
    sld_dev_ant_esperado = max(sld_dev_ant_calc, 0.0)
    if not _float_igual(valores_float["VL_SLD_DEV_ANT_DIFAL"], sld_dev_ant_esperado):
        return None

    # Validação Campo 12 (VL_RECOL) - Manual linha 763-764
    # Se (VL_SLD_DEV_ANT_DIFAL - VL_DEDUÇÕES_DIFAL) >= 0, então igual ao resultado; senão = 0
    vl_recol_calc = valores_float["VL_SLD_DEV_ANT_DIFAL"] - valores_float["VL_DEDUÇÕES_DIFAL"]
    vl_recol_esperado = max(vl_recol_calc, 0.0)
    if not _float_igual(valores_float["VL_RECOL"], vl_recol_esperado):
        return None

    # Validação Campo 13 (VL_SLD_CRED_TRANSPORTAR) - Manual linha 766-769
    # Se (VL_SLD_CRED_ANT_DIFAL + VL_TOT_CREDITOS_DIFAL + VL_OUT_CRED_DIFAL + VL_TOT_CRED_FCP) menos
    # (VL_TOT_DEBITOS_DIFAL + VL_OUT_DEB_DIFAL + VL_TOT_DEB_FCP) > 0,
    # então igual ao resultado; senão = 0
    sld_cred_transportar_calc = (
        valores_float["VL_SLD_CRED_ANT_DIFAL"]
        + valores_float["VL_TOT_CREDITOS_DIFAL"]
        + valores_float["VL_OUT_CRED_DIFAL"]
        + valores_float["VL_TOT_CRED_FCP"]
        - valores_float["VL_TOT_DEBITOS_DIFAL"]
        - valores_float["VL_OUT_DEB_DIFAL"]
        - valores_float["VL_TOT_DEB_FCP"]
    )
    sld_cred_transportar_esperado = max(sld_cred_transportar_calc, 0.0)
    if not _float_igual(valores_float["VL_SLD_CRED_TRANSPORTAR"], sld_cred_transportar_esperado):
        return None

    def fmt_moeda(v):
        return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    descricao_ind_mov = {
        "0": "Sem operações com ICMS Diferencial de Alíquota da UF de Origem/Destino",
        "1": "Com operações de ICMS Diferencial de Alíquota da UF de Origem/Destino",
    }.get(ind_mov_difal, "")

    return {
        "REG": {"titulo": "Registro", "valor": reg},
        "IND_MOV_DIFAL": {
            "titulo": "Indicador de movimento",
            "valor": ind_mov_difal,
            "descricao": descricao_ind_mov,
        },
        "VL_SLD_CRED_ANT_DIFAL": {
            "titulo": 'Valor do "Saldo credor de período anterior – ICMS Diferencial de Alíquota da UF de Origem/Destino"',
            "valor": vl_sld_cred_ant_difal,
            "valor_formatado": fmt_moeda(valores_float["VL_SLD_CRED_ANT_DIFAL"]),
        },
        "VL_TOT_DEBITOS_DIFAL": {
            "titulo": 'Valor total dos débitos por "Saídas e prestações com débito do ICMS referente ao diferencial de alíquota devido à UF do Remetente/Destinatário"',
            "valor": vl_tot_debitos_difal,
            "valor_formatado": fmt_moeda(valores_float["VL_TOT_DEBITOS_DIFAL"]),
        },
        "VL_OUT_DEB_DIFAL": {
            "titulo": 'Valor Total dos ajustes "Outros débitos ICMS Diferencial de Alíquota da UF de Origem/Destino" e "Estorno de créditos ICMS Diferencial de Alíquota da UF de Origem/Destino"',
            "valor": vl_out_deb_difal,
            "valor_formatado": fmt_moeda(valores_float["VL_OUT_DEB_DIFAL"]),
        },
        "VL_TOT_DEB_FCP": {
            "titulo": 'Valor total dos débitos FCP por "Saídas e prestações"',
            "valor": vl_tot_deb_fcp,
            "valor_formatado": fmt_moeda(valores_float["VL_TOT_DEB_FCP"]),
        },
        "VL_TOT_CREDITOS_DIFAL": {
            "titulo": "Valor total dos créditos do ICMS referente ao diferencial de alíquota devido à UF dos Remetente/Destinatário",
            "valor": vl_tot_creditos_difal,
            "valor_formatado": fmt_moeda(valores_float["VL_TOT_CREDITOS_DIFAL"]),
        },
        "VL_TOT_CRED_FCP": {
            "titulo": "Valor total dos créditos FCP por Entradas",
            "valor": vl_tot_cred_fcp,
            "valor_formatado": fmt_moeda(valores_float["VL_TOT_CRED_FCP"]),
        },
        "VL_OUT_CRED_DIFAL": {
            "titulo": 'Valor total de Ajustes "Outros créditos ICMS Diferencial de Alíquota da UF de Origem/Destino" e "Estorno de débitos ICMS Diferencial de Alíquota da UF de Origem/Destino"',
            "valor": vl_out_cred_difal,
            "valor_formatado": fmt_moeda(valores_float["VL_OUT_CRED_DIFAL"]),
        },
        "VL_SLD_DEV_ANT_DIFAL": {
            "titulo": "Valor total de Saldo devedor ICMS Diferencial de Alíquota da UF de Origem/Destino antes das deduções",
            "valor": vl_sld_dev_ant_difal,
            "valor_formatado": fmt_moeda(valores_float["VL_SLD_DEV_ANT_DIFAL"]),
        },
        "VL_DEDUÇÕES_DIFAL": {
            "titulo": 'Valor total dos ajustes "Deduções ICMS Diferencial de Alíquota da UF de Origem/Destino"',
            "valor": vl_deducoes_difal,
            "valor_formatado": fmt_moeda(valores_float["VL_DEDUÇÕES_DIFAL"]),
        },
        "VL_RECOL": {
            "titulo": "Valor recolhido ou a recolher referente a FCP e Imposto do Diferencial de Alíquota da UF de Origem/Destino (10-11)",
            "valor": vl_recol,
            "valor_formatado": fmt_moeda(valores_float["VL_RECOL"]),
        },
        "VL_SLD_CRED_TRANSPORTAR": {
            "titulo": "Saldo credor a transportar para o período seguinte referente a FCP e Imposto do Diferencial de Alíquota da UF de Origem/Destino",
            "valor": vl_sld_cred_transportar,
            "valor_formatado": fmt_moeda(valores_float["VL_SLD_CRED_TRANSPORTAR"]),
        },
        "DEB_ESP_DIFAL": {
            "titulo": "Valores recolhidos ou a recolher, extra-apuração",
            "valor": deb_esp_difal,
            "valor_formatado": fmt_moeda(valores_float["DEB_ESP_DIFAL"]),
        },
    }


def _processar_linha_e310_nova(linha):
    """
    Processa uma única linha do registro E310 (versão a partir de 01/01/2017 - 22 campos).
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
    if reg != "E310":
        return None

    def obter_campo(indice):
        if indice < len(partes):
            valor = partes[indice].strip()
            if valor == "-":
                return ""
            return valor if valor else ""
        return ""

    # Versão nova: 22 campos
    ind_mov_fcp_difal = obter_campo(1)
    vl_sld_cred_ant_difal = obter_campo(2)
    vl_tot_debitos_difal = obter_campo(3)
    vl_out_deb_difal = obter_campo(4)
    vl_tot_creditos_difal = obter_campo(5)
    vl_out_cred_difal = obter_campo(6)
    vl_sld_dev_ant_difal = obter_campo(7)
    vl_deducoes_difal = obter_campo(8)
    vl_recol_difal = obter_campo(9)
    vl_sld_cred_transportar_difal = obter_campo(10)
    deb_esp_difal = obter_campo(11)
    vl_sld_cred_ant_fcp = obter_campo(12)
    vl_tot_deb_fcp = obter_campo(13)
    vl_out_deb_fcp = obter_campo(14)
    vl_tot_cred_fcp = obter_campo(15)
    vl_out_cred_fcp = obter_campo(16)
    vl_sld_dev_ant_fcp = obter_campo(17)
    vl_deducoes_fcp = obter_campo(18)
    vl_recol_fcp = obter_campo(19)
    vl_sld_cred_transportar_fcp = obter_campo(20)
    deb_esp_fcp = obter_campo(21)

    # IND_MOV_FCP_DIFAL: obrigatório, valores válidos [0, 1]
    if ind_mov_fcp_difal not in ["0", "1"]:
        return None

    # Valida todos os campos numéricos obrigatórios
    validacoes = [
        ("VL_SLD_CRED_ANT_DIFAL", vl_sld_cred_ant_difal, True),
        ("VL_TOT_DEBITOS_DIFAL", vl_tot_debitos_difal, True),
        ("VL_OUT_DEB_DIFAL", vl_out_deb_difal, True),
        ("VL_TOT_CREDITOS_DIFAL", vl_tot_creditos_difal, True),
        ("VL_OUT_CRED_DIFAL", vl_out_cred_difal, True),
        ("VL_SLD_DEV_ANT_DIFAL", vl_sld_dev_ant_difal, True),
        ("VL_DEDUÇÕES_DIFAL", vl_deducoes_difal, True),
        ("VL_RECOL_DIFAL", vl_recol_difal, True),
        ("VL_SLD_CRED_TRANSPORTAR_DIFAL", vl_sld_cred_transportar_difal, True),
        ("DEB_ESP_DIFAL", deb_esp_difal, True),
        ("VL_SLD_CRED_ANT_FCP", vl_sld_cred_ant_fcp, True),
        ("VL_TOT_DEB_FCP", vl_tot_deb_fcp, True),
        ("VL_OUT_DEB_FCP", vl_out_deb_fcp, True),
        ("VL_TOT_CRED_FCP", vl_tot_cred_fcp, True),
        ("VL_OUT_CRED_FCP", vl_out_cred_fcp, True),
        ("VL_SLD_DEV_ANT_FCP", vl_sld_dev_ant_fcp, True),
        ("VL_DEDUÇÕES_FCP", vl_deducoes_fcp, True),
        ("VL_RECOL_FCP", vl_recol_fcp, True),
        ("VL_SLD_CRED_TRANSPORTAR_FCP", vl_sld_cred_transportar_fcp, True),
        ("DEB_ESP_FCP", deb_esp_fcp, True),
    ]

    valores_float = {}
    for nome, valor_str, obrig in validacoes:
        ok, f, _ = validar_valor_numerico(valor_str, decimais=2, obrigatorio=obrig, nao_negativo=True)
        if not ok:
            return None
        valores_float[nome] = f

    # Validação Campo 08 (VL_SLD_DEV_ANT_DIFAL) - Manual linha 889-892
    sld_dev_ant_difal_calc = (
        valores_float["VL_TOT_DEBITOS_DIFAL"]
        + valores_float["VL_OUT_DEB_DIFAL"]
        - valores_float["VL_SLD_CRED_ANT_DIFAL"]
        - valores_float["VL_TOT_CREDITOS_DIFAL"]
        - valores_float["VL_OUT_CRED_DIFAL"]
    )
    sld_dev_ant_difal_esperado = max(sld_dev_ant_difal_calc, 0.0)
    if not _float_igual(valores_float["VL_SLD_DEV_ANT_DIFAL"], sld_dev_ant_difal_esperado):
        return None

    # Validação Campo 10 (VL_RECOL_DIFAL) - Manual linha 896-898
    vl_recol_difal_calc = valores_float["VL_SLD_DEV_ANT_DIFAL"] - valores_float["VL_DEDUÇÕES_DIFAL"]
    vl_recol_difal_esperado = max(vl_recol_difal_calc, 0.0)
    if not _float_igual(valores_float["VL_RECOL_DIFAL"], vl_recol_difal_esperado):
        return None

    # Validação Campo 11 (VL_SLD_CRED_TRANSPORTAR_DIFAL) - Manual linha 900-904
    sld_cred_transportar_difal_calc = (
        valores_float["VL_SLD_CRED_ANT_DIFAL"]
        + valores_float["VL_TOT_CREDITOS_DIFAL"]
        + valores_float["VL_OUT_CRED_DIFAL"]
        + valores_float["VL_DEDUÇÕES_DIFAL"]
        - valores_float["VL_TOT_DEBITOS_DIFAL"]
        - valores_float["VL_OUT_DEB_DIFAL"]
    )
    sld_cred_transportar_difal_esperado = max(sld_cred_transportar_difal_calc, 0.0)
    if not _float_igual(valores_float["VL_SLD_CRED_TRANSPORTAR_DIFAL"], sld_cred_transportar_difal_esperado):
        return None

    # Validação Campo 18 (VL_SLD_DEV_ANT_FCP) - Manual linha 959-961
    sld_dev_ant_fcp_calc = (
        valores_float["VL_TOT_DEB_FCP"]
        + valores_float["VL_OUT_DEB_FCP"]
        - valores_float["VL_SLD_CRED_ANT_FCP"]
        - valores_float["VL_TOT_CRED_FCP"]
        - valores_float["VL_OUT_CRED_FCP"]
    )
    sld_dev_ant_fcp_esperado = max(sld_dev_ant_fcp_calc, 0.0)
    if not _float_igual(valores_float["VL_SLD_DEV_ANT_FCP"], sld_dev_ant_fcp_esperado):
        return None

    # Validação Campo 20 (VL_RECOL_FCP) - Manual linha 965-967
    vl_recol_fcp_calc = valores_float["VL_SLD_DEV_ANT_FCP"] - valores_float["VL_DEDUÇÕES_FCP"]
    vl_recol_fcp_esperado = max(vl_recol_fcp_calc, 0.0)
    if not _float_igual(valores_float["VL_RECOL_FCP"], vl_recol_fcp_esperado):
        return None

    # Validação Campo 21 (VL_SLD_CRED_TRANSPORTAR_FCP) - Manual linha 968-971
    sld_cred_transportar_fcp_calc = (
        valores_float["VL_SLD_CRED_ANT_FCP"]
        + valores_float["VL_TOT_CRED_FCP"]
        + valores_float["VL_OUT_CRED_FCP"]
        + valores_float["VL_DEDUÇÕES_FCP"]
        - valores_float["VL_TOT_DEB_FCP"]
        - valores_float["VL_OUT_DEB_FCP"]
    )
    sld_cred_transportar_fcp_esperado = max(sld_cred_transportar_fcp_calc, 0.0)
    if not _float_igual(valores_float["VL_SLD_CRED_TRANSPORTAR_FCP"], sld_cred_transportar_fcp_esperado):
        return None

    def fmt_moeda(v):
        return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    descricao_ind_mov = {
        "0": "Sem operações",
        "1": "Com operações",
    }.get(ind_mov_fcp_difal, "")

    return {
        "REG": {"titulo": "Registro", "valor": reg},
        "IND_MOV_FCP_DIFAL": {
            "titulo": "Indicador de movimento",
            "valor": ind_mov_fcp_difal,
            "descricao": descricao_ind_mov,
        },
        "VL_SLD_CRED_ANT_DIFAL": {
            "titulo": 'Valor do "Saldo credor de período anterior – ICMS Diferencial de Alíquota da UF de Origem/Destino"',
            "valor": vl_sld_cred_ant_difal,
            "valor_formatado": fmt_moeda(valores_float["VL_SLD_CRED_ANT_DIFAL"]),
        },
        "VL_TOT_DEBITOS_DIFAL": {
            "titulo": 'Valor total dos débitos por "Saídas e prestações com débito do ICMS referente ao diferencial de alíquota devido à UF de Origem/Destino"',
            "valor": vl_tot_debitos_difal,
            "valor_formatado": fmt_moeda(valores_float["VL_TOT_DEBITOS_DIFAL"]),
        },
        "VL_OUT_DEB_DIFAL": {
            "titulo": 'Valor total dos ajustes "Outros débitos ICMS Diferencial de Alíquota da UF de Origem/Destino" e "Estorno de créditos ICMS Diferencial de Alíquota da UF de Origem/Destino"',
            "valor": vl_out_deb_difal,
            "valor_formatado": fmt_moeda(valores_float["VL_OUT_DEB_DIFAL"]),
        },
        "VL_TOT_CREDITOS_DIFAL": {
            "titulo": "Valor total dos créditos do ICMS referente ao diferencial de alíquota devido à UF de Origem/Destino",
            "valor": vl_tot_creditos_difal,
            "valor_formatado": fmt_moeda(valores_float["VL_TOT_CREDITOS_DIFAL"]),
        },
        "VL_OUT_CRED_DIFAL": {
            "titulo": 'Valor total de Ajustes "Outros créditos ICMS Diferencial de Alíquota da UF de Origem/Destino" e "Estorno de débitos ICMS Diferencial de Alíquota da UF de Origem/Destino"',
            "valor": vl_out_cred_difal,
            "valor_formatado": fmt_moeda(valores_float["VL_OUT_CRED_DIFAL"]),
        },
        "VL_SLD_DEV_ANT_DIFAL": {
            "titulo": 'Valor total de "Saldo devedor ICMS Diferencial de Alíquota da UF de Origem/Destino antes das deduções"',
            "valor": vl_sld_dev_ant_difal,
            "valor_formatado": fmt_moeda(valores_float["VL_SLD_DEV_ANT_DIFAL"]),
        },
        "VL_DEDUÇÕES_DIFAL": {
            "titulo": 'Valor total dos ajustes "Deduções ICMS Diferencial de Alíquota da UF de Origem/Destino"',
            "valor": vl_deducoes_difal,
            "valor_formatado": fmt_moeda(valores_float["VL_DEDUÇÕES_DIFAL"]),
        },
        "VL_RECOL_DIFAL": {
            "titulo": "Valor recolhido ou a recolher referente ao ICMS Diferencial de Alíquota da UF de Origem/Destino (08-09)",
            "valor": vl_recol_difal,
            "valor_formatado": fmt_moeda(valores_float["VL_RECOL_DIFAL"]),
        },
        "VL_SLD_CRED_TRANSPORTAR_DIFAL": {
            "titulo": "Saldo credor a transportar para o período seguinte referente ao ICMS Diferencial de Alíquota da UF de Origem/Destino",
            "valor": vl_sld_cred_transportar_difal,
            "valor_formatado": fmt_moeda(valores_float["VL_SLD_CRED_TRANSPORTAR_DIFAL"]),
        },
        "DEB_ESP_DIFAL": {
            "titulo": "Valores recolhidos ou a recolher, extra-apuração - ICMS Diferencial de Alíquota da UF de Origem/Destino",
            "valor": deb_esp_difal,
            "valor_formatado": fmt_moeda(valores_float["DEB_ESP_DIFAL"]),
        },
        "VL_SLD_CRED_ANT_FCP": {
            "titulo": 'Valor do "Saldo credor de período anterior – FCP"',
            "valor": vl_sld_cred_ant_fcp,
            "valor_formatado": fmt_moeda(valores_float["VL_SLD_CRED_ANT_FCP"]),
        },
        "VL_TOT_DEB_FCP": {
            "titulo": 'Valor total dos débitos FCP por "Saídas e prestações"',
            "valor": vl_tot_deb_fcp,
            "valor_formatado": fmt_moeda(valores_float["VL_TOT_DEB_FCP"]),
        },
        "VL_OUT_DEB_FCP": {
            "titulo": 'Valor total dos ajustes "Outros débitos FCP" e "Estorno de créditos FCP"',
            "valor": vl_out_deb_fcp,
            "valor_formatado": fmt_moeda(valores_float["VL_OUT_DEB_FCP"]),
        },
        "VL_TOT_CRED_FCP": {
            "titulo": "Valor total dos créditos FCP por Entradas",
            "valor": vl_tot_cred_fcp,
            "valor_formatado": fmt_moeda(valores_float["VL_TOT_CRED_FCP"]),
        },
        "VL_OUT_CRED_FCP": {
            "titulo": 'Valor total de Ajustes "Outros créditos FCP" e "Estorno de débitos FCP"',
            "valor": vl_out_cred_fcp,
            "valor_formatado": fmt_moeda(valores_float["VL_OUT_CRED_FCP"]),
        },
        "VL_SLD_DEV_ANT_FCP": {
            "titulo": "Valor total de Saldo devedor FCP antes das deduções",
            "valor": vl_sld_dev_ant_fcp,
            "valor_formatado": fmt_moeda(valores_float["VL_SLD_DEV_ANT_FCP"]),
        },
        "VL_DEDUÇÕES_FCP": {
            "titulo": 'Valor total das deduções "FCP"',
            "valor": vl_deducoes_fcp,
            "valor_formatado": fmt_moeda(valores_float["VL_DEDUÇÕES_FCP"]),
        },
        "VL_RECOL_FCP": {
            "titulo": "Valor recolhido ou a recolher referente ao FCP (18–19)",
            "valor": vl_recol_fcp,
            "valor_formatado": fmt_moeda(valores_float["VL_RECOL_FCP"]),
        },
        "VL_SLD_CRED_TRANSPORTAR_FCP": {
            "titulo": "Saldo credor a transportar para o período seguinte referente ao FCP",
            "valor": vl_sld_cred_transportar_fcp,
            "valor_formatado": fmt_moeda(valores_float["VL_SLD_CRED_TRANSPORTAR_FCP"]),
        },
        "DEB_ESP_FCP": {
            "titulo": "Valores recolhidos ou a recolher, extra-apuração - FCP",
            "valor": deb_esp_fcp,
            "valor_formatado": fmt_moeda(valores_float["DEB_ESP_FCP"]),
        },
    }


def _processar_linha_e310(linha, dt_ini_periodo=None):
    """
    Processa uma única linha do registro E310, escolhendo a versão apropriada baseado na data.
    """
    versao_nova = _determinar_versao_e310(dt_ini_periodo)
    
    if versao_nova:
        return _processar_linha_e310_nova(linha)
    else:
        return _processar_linha_e310_antiga(linha)


def validar_e310_fiscal(linhas, dt_ini_periodo=None):
    """
    Valida uma ou mais linhas do registro E310 do SPED EFD Fiscal.

    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                - Versão até 31/12/2016: |E310|IND_MOV_DIFAL|VL_SLD_CRED_ANT_DIFAL|VL_TOT_DEBITOS_DIFAL|VL_OUT_DEB_DIFAL|VL_TOT_DEB_FCP|VL_TOT_CREDITOS_DIFAL|VL_TOT_CRED_FCP|VL_OUT_CRED_DIFAL|VL_SLD_DEV_ANT_DIFAL|VL_DEDUÇÕES_DIFAL|VL_RECOL|VL_SLD_CRED_TRANSPORTAR|DEB_ESP_DIFAL|
                - Versão a partir de 01/01/2017: |E310|IND_MOV_FCP_DIFAL|VL_SLD_CRED_ANT_DIFAL|VL_TOT_DEBITOS_DIFAL|VL_OUT_DEB_DIFAL|VL_TOT_CREDITOS_DIFAL|VL_OUT_CRED_DIFAL|VL_SLD_DEV_ANT_DIFAL|VL_DEDUÇÕES_DIFAL|VL_RECOL_DIFAL|VL_SLD_CRED_TRANSPORTAR_DIFAL|DEB_ESP_DIFAL|VL_SLD_CRED_ANT_FCP|VL_TOT_DEB_FCP|VL_OUT_DEB_FCP|VL_TOT_CRED_FCP|VL_OUT_CRED_FCP|VL_SLD_DEV_ANT_FCP|VL_DEDUÇÕES_FCP|VL_RECOL_FCP|VL_SLD_CRED_TRANSPORTAR_FCP|DEB_ESP_FCP|
        dt_ini_periodo: Data inicial do período de apuração (ddmmaaaa) para determinar qual versão usar (opcional)

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
        r = _processar_linha_e310(l, dt_ini_periodo=dt_ini_periodo)
        if r is not None:
            resultados.append(r)

    return json.dumps(resultados, ensure_ascii=False, indent=2)
