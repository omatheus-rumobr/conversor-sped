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


def _processar_linha_e115(linha):
    """
    Processa uma única linha do registro E115 e retorna um dicionário.

    Formato:
      |E115|COD_INF_ADIC|VL_INF_ADIC|DESCR_COMPL_AJ|
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
    if reg != "E115":
        return None

    def obter_campo(indice):
        if indice < len(partes):
            valor = partes[indice].strip()
            if valor == "-":
                return ""
            return valor if valor else ""
        return ""

    cod_inf_adic = obter_campo(1)
    vl_inf_adic = obter_campo(2)
    descr_compl_aj = obter_campo(3)

    # COD_INF_ADIC: obrigatório, até 8 caracteres (tabela 5.2 depende da UF/tabela externa)
    if not cod_inf_adic:
        return None
    if len(cod_inf_adic) > 8:
        return None

    # VL_INF_ADIC: obrigatório, numérico com 2 decimais, não negativo
    vl_ok, vl_float, _ = validar_valor_numerico(vl_inf_adic, decimais=2, obrigatorio=True, nao_negativo=True)
    if not vl_ok:
        return None

    # DESCR_COMPL_AJ: opcional (se informado, não pode ser só espaços)
    if descr_compl_aj and not descr_compl_aj.strip():
        return None

    def fmt_moeda(v):
        return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    return {
        "REG": {"titulo": "Registro", "valor": reg},
        "COD_INF_ADIC": {
            "titulo": "Código da informação adicional conforme tabela definida no item 5.2",
            "valor": cod_inf_adic,
        },
        "VL_INF_ADIC": {
            "titulo": "Valor referente à informação adicional",
            "valor": vl_inf_adic,
            "valor_formatado": fmt_moeda(vl_float),
        },
        "DESCR_COMPL_AJ": {
            "titulo": "Descrição complementar do ajuste",
            "valor": descr_compl_aj if descr_compl_aj else "",
        },
    }


def validar_e115_fiscal(linhas):
    """
    Valida uma ou mais linhas do registro E115 do SPED EFD Fiscal.
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
        r = _processar_linha_e115(l)
        if r is not None:
            resultados.append(r)

    return json.dumps(resultados, ensure_ascii=False, indent=2)