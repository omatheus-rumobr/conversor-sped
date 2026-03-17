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


def _processar_linha_e111(linha):
    """
    Processa uma única linha do registro E111 e retorna um dicionário.

    Args:
        linha: String com uma linha do SPED no formato |E111|COD_AJ_APUR|DESCR_COMPL_AJ|VL_AJ_APUR|

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
    if reg != "E111":
        return None

    def obter_campo(indice):
        if indice < len(partes):
            valor = partes[indice].strip()
            if valor == "-":
                return ""
            return valor if valor else ""
        return ""

    cod_aj_apur = obter_campo(1)
    descr_compl_aj = obter_campo(2)
    vl_aj_apur = obter_campo(3)

    # COD_AJ_APUR: obrigatório, tam 008*
    # Validação de tabela 5.1.1 depende da UF/tabela externa (não validamos aqui)
    if not cod_aj_apur:
        return None
    if len(cod_aj_apur) != 8:
        return None
    # Regra: terceiro caractere deve ser "0" (ajuste de ICMS próprio, não ICMS ST)
    if len(cod_aj_apur) < 3 or cod_aj_apur[2] != "0":
        return None
    # Regra: quarto caractere deve estar entre 0 e 5
    if len(cod_aj_apur) < 4 or cod_aj_apur[3] not in ["0", "1", "2", "3", "4", "5"]:
        return None

    # DESCR_COMPL_AJ: opcional condicional (se informado, não pode ser só espaços)
    if descr_compl_aj and not descr_compl_aj.strip():
        return None

    # VL_AJ_APUR: obrigatório, numérico com 2 decimais, não negativo
    vl_aj_apur_ok, vl_aj_apur_float, _ = validar_valor_numerico(vl_aj_apur, decimais=2, obrigatorio=True, nao_negativo=True)
    if not vl_aj_apur_ok:
        return None

    def fmt_moeda(v):
        return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    descricao_tipo = {
        "0": "Outros débitos",
        "1": "Estorno de créditos",
        "2": "Outros créditos",
        "3": "Estorno de débitos",
        "4": "Deduções do imposto apurado",
        "5": "Débitos Especiais",
    }.get(cod_aj_apur[3], "")

    return {
        "REG": {"titulo": "Registro", "valor": reg},
        "COD_AJ_APUR": {
            "titulo": "Código do ajuste da apuração e dedução, conforme a Tabela indicada no item 5.1.1",
            "valor": cod_aj_apur,
            "descricao": descricao_tipo,
        },
        "DESCR_COMPL_AJ": {"titulo": "Descrição complementar do ajuste da apuração", "valor": descr_compl_aj if descr_compl_aj else ""},
        "VL_AJ_APUR": {"titulo": "Valor do ajuste da apuração", "valor": vl_aj_apur, "valor_formatado": fmt_moeda(vl_aj_apur_float)},
    }


def validar_e111(linhas):
    """
    Valida uma ou mais linhas do registro E111 do SPED EFD Fiscal.

    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |E111|COD_AJ_APUR|DESCR_COMPL_AJ|VL_AJ_APUR|

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
        r = _processar_linha_e111(l)
        if r is not None:
            resultados.append(r)

    return json.dumps(resultados, ensure_ascii=False, indent=2)