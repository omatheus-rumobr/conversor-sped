import json

from typing import Any, Dict, List, Union


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
    if partes and partes[0] == "":
        partes = partes[1:]
    if partes and partes[-1] == "":
        partes = partes[:-1]
    return [p.strip() for p in partes]


def _extrair_reg(linha: str) -> str:
    partes = _split_sped(linha)
    return (partes[0] if partes else "").strip()


def _obter_campo(partes: List[str], indice: int) -> str:
    if indice < len(partes):
        v = (partes[indice] or "").strip()
        return "" if v == "-" else v
    return ""


def _processar_linha_p001(linha: str) -> Dict[str, Any] | None:
    """
    Processa uma única linha do registro P001 e retorna um dicionário.

    Formato: |P001|IND_MOV|

    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "P001"
    - IND_MOV: obrigatório, valores válidos [0, 1]

    Validação (camada superior):
    - Se IND_MOV = "1": somente registros de abertura e encerramento do bloco (P001 e P990).
    - Se IND_MOV = "0": deve existir pelo menos um registro além de P001 e P990.
    """
    if not linha or not isinstance(linha, str):
        return None

    partes = _split_sped(linha)
    if len(partes) < 2:
        return None

    reg = _obter_campo(partes, 0)
    if reg != "P001":
        return None

    ind_mov = _obter_campo(partes, 1)
    if ind_mov not in {"0", "1"}:
        return None

    descricoes = {
        "0": "Bloco com dados informados",
        "1": "Bloco sem dados informados",
    }

    return {
        "REG": {"titulo": "Registro", "valor": reg},
        "IND_MOV": {
            "titulo": "Indicador de movimento",
            "valor": ind_mov,
            "descricao": descricoes.get(ind_mov, ""),
        },
    }


def _validar_regras_cruzadas_ind_mov_p(
    ind_mov: str,
    linhas_bloco_p: Union[str, List[str], None],
) -> List[str]:
    erros: List[str] = []
    linhas_norm = _normalizar_linhas(linhas_bloco_p)
    if not linhas_norm:
        return erros

    regs_encontrados = [_extrair_reg(l) for l in linhas_norm]
    regs_encontrados = [r for r in regs_encontrados if r]

    regs_abertura_encerramento = {"P001", "P990"}
    regs_outros = [r for r in regs_encontrados if r not in regs_abertura_encerramento]

    if ind_mov == "1":
        regs_invalidos = sorted({r for r in regs_encontrados if r not in regs_abertura_encerramento})
        if regs_invalidos:
            erros.append(
                "IND_MOV=1: bloco P não pode conter registros além de P001 e P990. "
                f"Encontrado(s): {', '.join(regs_invalidos)}."
            )
    elif ind_mov == "0":
        if len(regs_outros) == 0:
            erros.append("IND_MOV=0: deve existir pelo menos um registro no bloco P além de P001 e P990.")

    return erros


def validar_p001(
    linhas: Union[str, List[str], None],
    *,
    linhas_bloco_p: Union[str, List[str], None] = None,
) -> str:
    """
    Valida uma ou mais linhas do registro P001 do SPED EFD-Contribuições.

    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |P001|IND_MOV|
        linhas_bloco_p: opcional; linhas do Bloco P para validar a regra cruzada do IND_MOV

    Returns:
        String JSON com array de objetos contendo os campos validados.
        Retorna "[]" se nenhuma linha for válida.
    """
    linhas_para_processar = _normalizar_linhas(linhas)
    if not linhas_para_processar:
        return json.dumps([], ensure_ascii=False, indent=2)

    resultados: List[Dict[str, Any]] = []
    for linha in linhas_para_processar:
        if _extrair_reg(linha) != "P001":
            continue

        item = _processar_linha_p001(linha)
        if item is None:
            continue

        ind_mov = str(item.get("IND_MOV", {}).get("valor", "") or "")
        erros = _validar_regras_cruzadas_ind_mov_p(ind_mov, linhas_bloco_p) if linhas_bloco_p else []
        if erros:
            item["ERROS"] = {"titulo": "Erros de validação", "valor": " | ".join(erros)}

        resultados.append(item)

    return json.dumps(resultados, ensure_ascii=False, indent=2)
