import json
from typing import Any, Dict, List, Optional, Tuple, Union


def _normalizar_linhas(linhas: Union[str, List[str], None]) -> List[str]:
    if not linhas:
        return []
    if isinstance(linhas, list):
        return [l.strip() for l in linhas if isinstance(l, str) and l.strip()]
    if isinstance(linhas, str):
        if "\n" in linhas:
            return [l.strip() for l in linhas.split("\n") if l.strip()]
        return [linhas.strip()] if linhas.strip() else []
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


def _eh_inteiro_nao_negativo(valor: str) -> bool:
    return bool(valor) and str(valor).isdigit()


def validar_registro_m990(
    linha_m990: str,
    *,
    linhas_bloco_m: Union[str, List[str], None] = None,
) -> Dict[str, Any]:
    """
    Valida regras do Registro M990 (Bloco M, EFD-Contribuições 1.35) conforme trecho do manual.

    Regras do manual (conforme `documentacao_blocos/1.35/bloco_M.md:1667-1682`):
    - REG: obrigatório, valor fixo "M990"
    - QTD_LIN_M: obrigatório, quantidade total de linhas do Bloco M (inclui abertura e encerramento)
    - Validação (opcional): nº de linhas existentes no bloco M = QTD_LIN_M

    Args:
        linha_m990: linha do arquivo SPED contendo o registro M990
        linhas_bloco_m: opcional; linhas do Bloco M para validar QTD_LIN_M

    Returns:
        dict com:
          - ok (bool)
          - erros (list[str])
          - campos (dict) com REG e QTD_LIN_M
          - contexto (dict) com contagem real quando `linhas_bloco_m` é informado
    """
    erros: List[str] = []

    if not linha_m990 or not isinstance(linha_m990, str):
        return {"ok": False, "erros": ["Linha do registro M990 inválida/vazia."], "campos": {}, "contexto": {}}

    partes = _split_sped(linha_m990)
    reg = _obter_campo(partes, 0)
    qtd_lin_m = _obter_campo(partes, 1)

    if reg != "M990":
        erros.append("Campo REG inválido: esperado 'M990'.")

    if not _eh_inteiro_nao_negativo(qtd_lin_m):
        erros.append("Campo QTD_LIN_M inválido: esperado inteiro não-negativo.")

    contexto: Dict[str, Any] = {}
    linhas_norm = _normalizar_linhas(linhas_bloco_m)
    if linhas_norm and _eh_inteiro_nao_negativo(qtd_lin_m):
        qtd_real = len(linhas_norm)
        contexto = {"qtd_linhas_bloco_m": qtd_real, "qtd_informada": int(qtd_lin_m)}
        if qtd_real != int(qtd_lin_m):
            erros.append(f"QTD_LIN_M inconsistente: informado {qtd_lin_m}, calculado {qtd_real}.")

    return {
        "ok": len(erros) == 0,
        "erros": erros,
        "campos": {"REG": reg, "QTD_LIN_M": qtd_lin_m},
        "contexto": contexto,
    }


def validar_m990(
    linhas: Union[str, List[str], None],
    *,
    linhas_bloco_m: Union[str, List[str], None] = None,
) -> str:
    """
    Wrapper que retorna JSON (array) e valida cada linha M990 encontrada.

    - Se `linhas_bloco_m` for informado, valida também QTD_LIN_M vs contagem real.
    """
    linhas_para_processar = _normalizar_linhas(linhas)
    resultados: List[Dict[str, Any]] = []

    for linha in linhas_para_processar:
        if _extrair_reg(linha) != "M990":
            continue
        resultados.append(validar_registro_m990(linha, linhas_bloco_m=linhas_bloco_m))

    return json.dumps(resultados, ensure_ascii=False, indent=2)