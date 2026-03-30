import json

from typing import List, Union


def _normalizar_linhas(linhas: Union[str, List[str], None]) -> List[str]:
    if not linhas:
        return []
    if isinstance(linhas, str):
        if "\n" in linhas:
            return [l.strip() for l in linhas.split("\n") if l.strip()]
        return [linhas.strip()] if linhas.strip() else []
    if isinstance(linhas, list):
        return [l.strip() if isinstance(l, str) else str(l).strip() for l in linhas if str(l).strip()]
    return [str(linhas).strip()] if str(linhas).strip() else []


def _split_sped(linha: str) -> List[str]:
    partes = (linha or "").strip().split("|")
    if partes and not partes[0]:
        partes = partes[1:]
    if partes and not partes[-1]:
        partes = partes[:-1]
    return [p.strip() for p in partes]


def _processar_linha_f990(linha):
    """
    Processa uma única linha do registro F990 e retorna um dicionário.

    Formato: |F990|QTD_LIN_F|

    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "F990"
    - QTD_LIN_F: obrigatório, numérico (quantidade total de linhas do Bloco F)

    Validação (camada superior):
    - O número de linhas (registros) existentes no bloco F deve ser igual ao valor informado em QTD_LIN_F,
      considerando também os próprios registros de abertura e encerramento do bloco.

    Returns:
        dict com os campos validados contendo título e valor, ou None se inválido
    """
    if not linha or not isinstance(linha, str):
        return None

    linha = linha.strip()
    if not linha:
        return None

    partes = _split_sped(linha)
    if len(partes) < 2:
        return None

    reg = partes[0].strip() if partes else ""
    if reg != "F990":
        return None

    qtd_lin_f = partes[1].strip() if len(partes) > 1 else ""
    if qtd_lin_f == "-":
        qtd_lin_f = ""

    # QTD_LIN_F: obrigatório, numérico inteiro
    if not qtd_lin_f or not str(qtd_lin_f).isdigit():
        return None

    # deve ser > 0 (quantidade de linhas do bloco)
    if int(qtd_lin_f) <= 0:
        return None

    return {
        "REG": {"titulo": "Registro", "valor": reg},
        "QTD_LIN_F": {
            "titulo": "Quantidade total de linhas do Bloco F",
            "valor": str(qtd_lin_f),
        },
    }


def validar_f990(linhas, *, linhas_bloco_f=None):
    """
    Valida uma ou mais linhas do registro F990 do SPED EFD-Contribuições.

    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |F990|QTD_LIN_F|
        linhas_bloco_f: opcional; linhas do Bloco F (para validar se QTD_LIN_F confere com a contagem real)

    Returns:
        String JSON com array de objetos contendo os campos validados.
        Retorna "[]" se nenhuma linha for válida.
    """
    linhas_para_processar = _normalizar_linhas(linhas)
    if not linhas_para_processar:
        return json.dumps([], ensure_ascii=False, indent=2)

    linhas_bloco_norm = _normalizar_linhas(linhas_bloco_f)
    qtd_real = len(linhas_bloco_norm) if linhas_bloco_norm else None

    resultados = []
    for linha in linhas_para_processar:
        resultado = _processar_linha_f990(linha)
        if resultado is None:
            continue

        if qtd_real is not None:
            try:
                qtd_inf = int(resultado.get("QTD_LIN_F", {}).get("valor", "0"))
            except Exception:
                qtd_inf = None

            if qtd_inf is None or qtd_inf != qtd_real:
                resultado["ERROS"] = {
                    "titulo": "Erros de validação",
                    "valor": (
                        f"QTD_LIN_F divergente: informado={qtd_inf if qtd_inf is not None else ''} "
                        f"e encontrado={qtd_real} linha(s) no Bloco F."
                    ),
                }

        resultados.append(resultado)

    return json.dumps(resultados, ensure_ascii=False, indent=2)