import json
from typing import Any, Dict, List, Union


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
    return bool(valor) and valor.isdigit()


def validar_registro_9990(
    linha_9990: str,
    *,
    linhas_bloco9: Union[str, List[str], None] = None,
    incluir_9999: bool = True,
) -> Dict[str, Any]:
    """
    Valida as regras do Registro 9990 (Bloco 9, EFD-Contribuições 1.35).

    Regras do manual (conforme `documentacao_blocos/1.35/bloco_9.md`):
    - REG: obrigatório, valor fixo "9990"
    - QTD_LIN_9: obrigatório, quantidade total de linhas do Bloco 9
    - Para cálculo do QTD_LIN_9, o registro 9999 (fora do Bloco 9) também deve ser contabilizado
    - Validação (opcional): nº de linhas existentes no bloco 9 = QTD_LIN_9

    Args:
        linha_9990: linha do arquivo SPED contendo o registro 9990
        linhas_bloco9: opcional; linhas do Bloco 9 (ex.: 9001, 9900..., 9990)
        incluir_9999: se True, soma +1 na contagem para considerar o registro 9999

    Returns:
        dict com:
          - ok (bool)
          - erros (list[str])
          - campos (dict) com REG e QTD_LIN_9
          - contexto (dict) com contagem real quando `linhas_bloco9` é informado
    """
    erros: List[str] = []

    if not linha_9990 or not isinstance(linha_9990, str):
        return {"ok": False, "erros": ["Linha do registro 9990 inválida/vazia."], "campos": {}, "contexto": {}}

    partes = _split_sped(linha_9990)
    reg = _obter_campo(partes, 0)
    qtd_lin_9 = _obter_campo(partes, 1)

    if reg != "9990":
        erros.append("Campo REG inválido: esperado '9990'.")

    if not _eh_inteiro_nao_negativo(qtd_lin_9):
        erros.append("Campo QTD_LIN_9 inválido: esperado inteiro não-negativo.")

    contexto: Dict[str, Any] = {}
    linhas_norm = _normalizar_linhas(linhas_bloco9)
    if linhas_norm and _eh_inteiro_nao_negativo(qtd_lin_9):
        qtd_bloco9 = len(linhas_norm)
        qtd_real = qtd_bloco9 + (1 if incluir_9999 else 0)

        contexto = {
            "qtd_linhas_bloco9": qtd_bloco9,
            "incluir_9999": incluir_9999,
            "qtd_real_calculada": qtd_real,
            "qtd_informada": int(qtd_lin_9),
        }

        if qtd_real != int(qtd_lin_9):
            erros.append(
                f"QTD_LIN_9 inconsistente: informado {qtd_lin_9}, calculado {qtd_real} "
                f"(linhas do Bloco 9: {qtd_bloco9}{' + 9999' if incluir_9999 else ''})."
            )

    return {
        "ok": len(erros) == 0,
        "erros": erros,
        "campos": {
            "REG": reg,
            "QTD_LIN_9": qtd_lin_9,
        },
        "contexto": contexto,
    }


def validar_9990(
    linhas: Union[str, List[str], None],
    *,
    linhas_bloco9: Union[str, List[str], None] = None,
    incluir_9999: bool = True,
) -> str:
    """
    Wrapper que retorna JSON (array) e valida cada linha 9990 encontrada.

    - Se `linhas_bloco9` for informado, valida também QTD_LIN_9 vs contagem real (+9999).
    """
    linhas_para_processar = _normalizar_linhas(linhas)
    resultados: List[Dict[str, Any]] = []

    for linha in linhas_para_processar:
        if _extrair_reg(linha) != "9990":
            continue
        resultados.append(
            validar_registro_9990(linha, linhas_bloco9=linhas_bloco9, incluir_9999=incluir_9999)
        )

    return json.dumps(resultados, ensure_ascii=False, indent=2)