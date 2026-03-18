import json


def _processar_linha_e230(linha):
    """
    Processa uma única linha do registro E230 e retorna um dicionário.

    Args:
        linha: String com uma linha do SPED no formato
              |E230|NUM_DA|NUM_PROC|IND_PROC|PROC|TXT_COMPL|

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
    if reg != "E230":
        return None

    def obter_campo(indice):
        if indice < len(partes):
            valor = partes[indice].strip()
            if valor == "-":
                return ""
            return valor if valor else ""
        return ""

    num_da = obter_campo(1)
    num_proc = obter_campo(2)
    ind_proc = obter_campo(3)
    proc = obter_campo(4)
    txt_compl = obter_campo(5)

    # NUM_DA: opcional condicional (manual: deve ser preenchido se o ajuste for referente a um documento de arrecadação)
    if num_da and not num_da.strip():
        return None

    # NUM_PROC: opcional condicional, até 60 caracteres
    if num_proc and len(num_proc) > 60:
        return None

    # IND_PROC: opcional condicional, valores válidos [0,1,2,9]
    if ind_proc and ind_proc not in ["0", "1", "2", "9"]:
        return None

    # PROC: opcional condicional (se informado, não pode ser só espaços)
    if proc and not proc.strip():
        return None

    # TXT_COMPL: opcional condicional (se informado, não pode ser só espaços)
    if txt_compl and not txt_compl.strip():
        return None

    descricao_ind_proc = {
        "0": "Sefaz",
        "1": "Justiça Federal",
        "2": "Justiça Estadual",
        "9": "Outros",
    }.get(ind_proc, "") if ind_proc else ""

    return {
        "REG": {"titulo": "Registro", "valor": reg},
        "NUM_DA": {"titulo": "Número do documento de arrecadação estadual, se houver", "valor": num_da if num_da else ""},
        "NUM_PROC": {"titulo": "Número do processo ao qual o ajuste está vinculado, se houver", "valor": num_proc if num_proc else ""},
        "IND_PROC": {"titulo": "Indicador da origem do processo", "valor": ind_proc if ind_proc else "", "descricao": descricao_ind_proc},
        "PROC": {"titulo": "Descrição resumida do processo que embasou o lançamento", "valor": proc if proc else ""},
        "TXT_COMPL": {"titulo": "Descrição complementar", "valor": txt_compl if txt_compl else ""},
    }


def validar_e230_fiscal(linhas):
    """
    Valida uma ou mais linhas do registro E230 do SPED EFD Fiscal.

    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato
                |E230|NUM_DA|NUM_PROC|IND_PROC|PROC|TXT_COMPL|

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
        r = _processar_linha_e230(l)
        if r is not None:
            resultados.append(r)

    return json.dumps(resultados, ensure_ascii=False, indent=2)
