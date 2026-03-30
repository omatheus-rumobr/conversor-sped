import json


def _processar_linha_1990(linha):
    """
    Processa uma única linha do registro 1990 e retorna um dicionário.

    Formato: |1990|QTD_LIN_1|

    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "1990"
    - QTD_LIN_1: obrigatório, numérico (quantidade total de linhas do Bloco 1)

    Validação (camada superior):
    - O número de linhas (registros) existentes no bloco 1 deve ser igual ao valor informado em QTD_LIN_1,
      considerando também os próprios registros de abertura e encerramento do bloco.

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
    if reg != "1990":
        return None

    def obter_campo(indice):
        if indice < len(partes):
            valor = partes[indice].strip()
            if valor == "-":
                return ""
            return valor if valor else ""
        return ""

    qtd_lin_1 = obter_campo(1)

    # QTD_LIN_1: obrigatório, numérico inteiro
    if not qtd_lin_1 or not qtd_lin_1.isdigit():
        return None

    # deve ser > 0 (quantidade de linhas do bloco)
    if int(qtd_lin_1) <= 0:
        return None

    return {
        "REG": {"titulo": "Registro", "valor": reg},
        "QTD_LIN_1": {
            "titulo": "Quantidade total de linhas do Bloco 1",
            "valor": qtd_lin_1,
        },
    }


def validar_1990(linhas):
    """
    Valida uma ou mais linhas do registro 1990 do SPED EFD-Contribuições.

    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |1990|QTD_LIN_1|

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
        resultado = _processar_linha_1990(linha)
        if resultado is not None:
            resultados.append(resultado)

    return json.dumps(resultados, ensure_ascii=False, indent=2)