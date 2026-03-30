import json


def _processar_linha_0001(linha: str):
    """
    Processa uma única linha do registro 0001 e retorna um dicionário.

    Formato:
      |0001|IND_MOV|

    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "0001"
    - IND_MOV: obrigatório, valores válidos [0, 1]

    Observação do manual:
    Considerando que no Bloco 0 deve ser escriturado, no mínimo, os registros 0110 e 0140,
    deve sempre ser informado no IND_MOV o indicador "0 – Bloco com dados informados".

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

    if len(partes) < 2:
        return None

    reg = partes[0].strip()
    if reg != "0001":
        return None

    ind_mov = partes[1].strip()
    if ind_mov == "-":
        ind_mov = ""

    # IND_MOV: obrigatório, valores [0,1] e (para o Bloco 0) deve ser sempre "0"
    if ind_mov not in {"0", "1"}:
        return None
    if ind_mov != "0":
        return None

    descricoes_ind_mov = {
        "0": "Bloco com dados informados",
        "1": "Bloco sem dados informados",
    }

    return {
        "REG": {"titulo": "Registro", "valor": reg},
        "IND_MOV": {
            "titulo": "Indicador de movimento",
            "valor": ind_mov,
            "descricao": descricoes_ind_mov.get(ind_mov, ""),
        },
    }


def validar_0001(linhas):
    """
    Valida uma ou mais linhas do registro 0001 do SPED EFD-Contribuições.

    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |0001|IND_MOV|

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
        linhas_para_processar = [
            l.strip() if isinstance(l, str) else str(l).strip() for l in linhas if l
        ]
    else:
        linhas_para_processar = [str(linhas).strip()] if str(linhas).strip() else []

    resultados = []
    for linha in linhas_para_processar:
        resultado = _processar_linha_0001(linha)
        if resultado is not None:
            resultados.append(resultado)

    return json.dumps(resultados, ensure_ascii=False, indent=2)
