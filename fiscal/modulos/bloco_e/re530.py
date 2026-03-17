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


def _processar_linha_e530(linha):
    """
    Processa uma única linha do registro E530 e retorna um dicionário.

    Formato:
      |E530|IND_AJ|VL_AJ|COD_AJ|IND_DOC|NUM_DOC|DESCR_AJ|

    Regras (manual 3.1.8):
    - REG deve ser "E530"
    - IND_AJ deve ser 0 ou 1
    - COD_AJ deve ter natureza compatível com IND_AJ
    - IND_DOC deve ser 0, 1, 2, 3 ou 9
    - DESCR_AJ é obrigatório

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
    if reg != "E530":
        return None

    def obter_campo(indice):
        if indice < len(partes):
            valor = partes[indice].strip()
            if valor == "-":
                return ""
            return valor if valor else ""
        return ""

    ind_aj = obter_campo(1)
    vl_aj = obter_campo(2)
    cod_aj = obter_campo(3)
    ind_doc = obter_campo(4)
    num_doc = obter_campo(5)
    descr_aj = obter_campo(6)

    # IND_AJ: obrigatório, valores válidos [0, 1]
    if ind_aj not in ["0", "1"]:
        return None

    # VL_AJ: obrigatório, numérico com 2 decimais, não negativo
    vl_aj_ok, vl_aj_float, _ = validar_valor_numerico(vl_aj, decimais=2, obrigatorio=True, nao_negativo=True)
    if not vl_aj_ok:
        return None

    # COD_AJ: obrigatório, 3 caracteres
    if not cod_aj or len(cod_aj) != 3:
        return None

    # Validação: COD_AJ deve ter natureza compatível com IND_AJ
    # Códigos de crédito (IND_AJ = 1): 001, 002, 010, 011, 012, 013, 019, 098, 099
    codigos_credito = ["001", "002", "010", "011", "012", "013", "019", "098", "099"]
    # Códigos de débito (IND_AJ = 0): 101, 102, 103, 199
    codigos_debito = ["101", "102", "103", "199"]

    if ind_aj == "0":
        # Ajuste a débito: COD_AJ deve ser código de débito
        if cod_aj not in codigos_debito:
            return None
    else:
        # Ajuste a crédito: COD_AJ deve ser código de crédito
        if cod_aj not in codigos_credito:
            return None

    # IND_DOC: obrigatório, valores válidos [0, 1, 2, 3, 9]
    if ind_doc not in ["0", "1", "2", "3", "9"]:
        return None

    # NUM_DOC: opcional condicional (se informado, não pode ser só espaços)
    if num_doc and not num_doc.strip():
        return None

    # DESCR_AJ: obrigatório (se informado, não pode ser só espaços)
    if not descr_aj or not descr_aj.strip():
        return None

    def fmt_moeda(v):
        return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    descricao_ind_aj = {
        "0": "Ajuste a débito",
        "1": "Ajuste a crédito",
    }.get(ind_aj, "")

    descricao_ind_doc = {
        "0": "Processo Judicial",
        "1": "Processo Administrativo",
        "2": "PER/DCOMP",
        "3": "Documento Fiscal",
        "9": "Outros",
    }.get(ind_doc, "")

    descricao_cod_aj = {
        "001": "Estorno de débito",
        "002": "Crédito recebido por transferência",
        "010": "Crédito Presumido de IPI - ressarcimento do PIS/Pasep e da Cofins - Lei nº 9.363/1996",
        "011": "Crédito Presumido de IPI - ressarcimento do PIS/Pasep e da Cofins - Lei nº 10.276/2001",
        "012": "Crédito Presumido de IPI - regiões incentivadas - Lei nº 9.826/1999",
        "013": "Crédito Presumido de IPI - frete - MP 2.158/2001",
        "019": "Crédito Presumido de IPI - outros",
        "098": "Créditos decorrentes de medida judicial",
        "099": "Outros créditos",
        "101": "Estorno de crédito",
        "102": "Transferência de crédito",
        "103": "Ressarcimento / compensação de créditos de IPI",
        "199": "Outros débitos",
    }.get(cod_aj, "")

    return {
        "REG": {"titulo": "Registro", "valor": reg},
        "IND_AJ": {
            "titulo": "Indicador do tipo de ajuste",
            "valor": ind_aj,
            "descricao": descricao_ind_aj,
        },
        "VL_AJ": {
            "titulo": "Valor do ajuste",
            "valor": vl_aj,
            "valor_formatado": fmt_moeda(vl_aj_float),
        },
        "COD_AJ": {
            "titulo": "Código do ajuste da apuração, conforme a Tabela indicada no item 4.5.4",
            "valor": cod_aj,
            "descricao": descricao_cod_aj,
        },
        "IND_DOC": {
            "titulo": "Indicador da origem do documento vinculado ao ajuste",
            "valor": ind_doc,
            "descricao": descricao_ind_doc,
        },
        "NUM_DOC": {
            "titulo": "Número do documento / processo / declaração ao qual o ajuste está vinculado, se houver",
            "valor": num_doc if num_doc else "",
        },
        "DESCR_AJ": {
            "titulo": "Descrição detalhada do ajuste, com citação dos documentos fiscais",
            "valor": descr_aj,
        },
    }


def validar_e530(linhas):
    """
    Valida uma ou mais linhas do registro E530 do SPED EFD Fiscal.

    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |E530|IND_AJ|VL_AJ|COD_AJ|IND_DOC|NUM_DOC|DESCR_AJ|

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
        r = _processar_linha_e530(l)
        if r is not None:
            resultados.append(r)

    return json.dumps(resultados, ensure_ascii=False, indent=2)
