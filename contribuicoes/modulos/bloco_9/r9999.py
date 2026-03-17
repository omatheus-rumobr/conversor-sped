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


def validar_registro_9999(
    linha_9999: str,
    *,
    linhas_arquivo: Union[str, List[str], None] = None,
) -> Dict[str, Any]:
    """
    Valida as regras do Registro 9999 (EFD-Contribuições 1.35).

    Regras do manual (conforme `documentacao_blocos/1.35/bloco_9.md`):
    - REG: obrigatório, valor fixo "9999"
    - QTD_LIN: obrigatório, quantidade total de linhas do arquivo digital
    - Para cálculo do QTD_LIN, deve considerar também a linha do próprio registro 9999
    - Validação (opcional): nº de linhas (registros) no arquivo inteiro = QTD_LIN

    Args:
        linha_9999: linha do arquivo SPED contendo o registro 9999
        linhas_arquivo: opcional; todas as linhas do arquivo para validar QTD_LIN

    Returns:
        dict com:
          - ok (bool)
          - erros (list[str])
          - campos (dict) com REG e QTD_LIN
          - contexto (dict) com contagem real quando `linhas_arquivo` é informado
    """
    erros: List[str] = []

    if not linha_9999 or not isinstance(linha_9999, str):
        return {"ok": False, "erros": ["Linha do registro 9999 inválida/vazia."], "campos": {}, "contexto": {}}

    partes = _split_sped(linha_9999)
    reg = _obter_campo(partes, 0)
    qtd_lin = _obter_campo(partes, 1)

    if reg != "9999":
        erros.append("Campo REG inválido: esperado '9999'.")

    if not _eh_inteiro_nao_negativo(qtd_lin):
        erros.append("Campo QTD_LIN inválido: esperado inteiro não-negativo.")

    contexto: Dict[str, Any] = {}
    linhas_norm = _normalizar_linhas(linhas_arquivo)
    if linhas_norm and _eh_inteiro_nao_negativo(qtd_lin):
        # O arquivo inteiro deve contar todas as linhas, incluindo a do próprio 9999.
        qtd_real = len(linhas_norm)
        contexto = {
            "qtd_real_calculada": qtd_real,
            "qtd_informada": int(qtd_lin),
        }
        if qtd_real != int(qtd_lin):
            erros.append(f"QTD_LIN inconsistente: informado {qtd_lin}, calculado {qtd_real}.")

    return {
        "ok": len(erros) == 0,
        "erros": erros,
        "campos": {
            "REG": reg,
            "QTD_LIN": qtd_lin,
        },
        "contexto": contexto,
    }


def validar_9999(
    linhas: Union[str, List[str], None],
    *,
    linhas_arquivo: Union[str, List[str], None] = None,
) -> str:
    """
    Wrapper que retorna JSON (array) e valida cada linha 9999 encontrada.

    - Se `linhas_arquivo` for informado, valida também QTD_LIN vs contagem real.
    """
    linhas_para_processar = _normalizar_linhas(linhas)
    resultados: List[Dict[str, Any]] = []

    for linha in linhas_para_processar:
        if _extrair_reg(linha) != "9999":
            continue
        resultados.append(validar_registro_9999(linha, linhas_arquivo=linhas_arquivo))

    return json.dumps(resultados, ensure_ascii=False, indent=2)