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


def _processar_linha_e520(linha):
    """
    Processa uma única linha do registro E520 e retorna um dicionário.

    Formato:
      |E520|VL_SD_ANT_IPI|VL_DEB_IPI|VL_CRED_IPI|VL_OD_IPI|VL_OC_IPI|VL_SC_IPI|VL_SD_IPI|

    Regras (manual 3.1.8):
    - REG deve ser "E520"
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
    if reg != "E520":
        return None

    def obter_campo(indice):
        if indice < len(partes):
            valor = partes[indice].strip()
            if valor == "-":
                return ""
            return valor if valor else ""
        return ""

    # Extrai todos os campos (8 campos no total)
    vl_sd_ant_ipi = obter_campo(1)
    vl_deb_ipi = obter_campo(2)
    vl_cred_ipi = obter_campo(3)
    vl_od_ipi = obter_campo(4)
    vl_oc_ipi = obter_campo(5)
    vl_sc_ipi = obter_campo(6)
    vl_sd_ipi = obter_campo(7)

    # Valida todos os campos numéricos obrigatórios (todos com 2 decimais, não negativos)
    validacoes = [
        ("VL_SD_ANT_IPI", vl_sd_ant_ipi, True),
        ("VL_DEB_IPI", vl_deb_ipi, True),
        ("VL_CRED_IPI", vl_cred_ipi, True),
        ("VL_OD_IPI", vl_od_ipi, True),
        ("VL_OC_IPI", vl_oc_ipi, True),
        ("VL_SC_IPI", vl_sc_ipi, True),
        ("VL_SD_IPI", vl_sd_ipi, True),
    ]

    valores_float = {}
    for nome, valor_str, obrig in validacoes:
        ok, f, _ = validar_valor_numerico(valor_str, decimais=2, obrigatorio=obrig, nao_negativo=True)
        if not ok:
            return None
        valores_float[nome] = f

    # Validação Campo 07 (VL_SC_IPI) e Campo 08 (VL_SD_IPI) - Manual linha 1241-1246
    # Expressão: (VL_DEB_IPI + VL_OD_IPI) - (VL_SD_ANT_IPI + VL_CRED_IPI + VL_OC_IPI)
    resultado_apuracao = (
        valores_float["VL_DEB_IPI"]
        + valores_float["VL_OD_IPI"]
        - valores_float["VL_SD_ANT_IPI"]
        - valores_float["VL_CRED_IPI"]
        - valores_float["VL_OC_IPI"]
    )

    # Se resultado < 0: VL_SC_IPI = valor absoluto, VL_SD_IPI = 0
    # Se resultado >= 0: VL_SD_IPI = resultado, VL_SC_IPI = 0
    if resultado_apuracao < 0:
        vl_sc_ipi_esperado = abs(resultado_apuracao)
        vl_sd_ipi_esperado = 0.0
    else:
        vl_sc_ipi_esperado = 0.0
        vl_sd_ipi_esperado = resultado_apuracao

    if not _float_igual(valores_float["VL_SC_IPI"], vl_sc_ipi_esperado):
        return None

    if not _float_igual(valores_float["VL_SD_IPI"], vl_sd_ipi_esperado):
        return None

    # Formatação monetária
    def fmt_moeda(v):
        return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    return {
        "REG": {"titulo": "Registro", "valor": reg},
        "VL_SD_ANT_IPI": {
            "titulo": "Saldo credor do IPI transferido do período anterior",
            "valor": vl_sd_ant_ipi,
            "valor_formatado": fmt_moeda(valores_float["VL_SD_ANT_IPI"]),
        },
        "VL_DEB_IPI": {
            "titulo": 'Valor total dos débitos por "Saídas com débito do imposto"',
            "valor": vl_deb_ipi,
            "valor_formatado": fmt_moeda(valores_float["VL_DEB_IPI"]),
        },
        "VL_CRED_IPI": {
            "titulo": 'Valor total dos créditos por "Entradas e aquisições com crédito do imposto"',
            "valor": vl_cred_ipi,
            "valor_formatado": fmt_moeda(valores_float["VL_CRED_IPI"]),
        },
        "VL_OD_IPI": {
            "titulo": 'Valor de "Outros débitos" do IPI (inclusive estornos de crédito)',
            "valor": vl_od_ipi,
            "valor_formatado": fmt_moeda(valores_float["VL_OD_IPI"]),
        },
        "VL_OC_IPI": {
            "titulo": 'Valor de "Outros créditos" do IPI (inclusive estornos de débitos)',
            "valor": vl_oc_ipi,
            "valor_formatado": fmt_moeda(valores_float["VL_OC_IPI"]),
        },
        "VL_SC_IPI": {
            "titulo": "Valor do saldo credor do IPI a transportar para o período seguinte",
            "valor": vl_sc_ipi,
            "valor_formatado": fmt_moeda(valores_float["VL_SC_IPI"]),
        },
        "VL_SD_IPI": {
            "titulo": "Valor do saldo devedor do IPI a recolher",
            "valor": vl_sd_ipi,
            "valor_formatado": fmt_moeda(valores_float["VL_SD_IPI"]),
        },
    }


def validar_e520_fiscal(linhas):
    """
    Valida uma ou mais linhas do registro E520 do SPED EFD Fiscal.

    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |E520|VL_SD_ANT_IPI|VL_DEB_IPI|VL_CRED_IPI|VL_OD_IPI|VL_OC_IPI|VL_SC_IPI|VL_SD_IPI|

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
        r = _processar_linha_e520(l)
        if r is not None:
            resultados.append(r)

    return json.dumps(resultados, ensure_ascii=False, indent=2)
