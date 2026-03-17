import json
from typing import Any, Dict, List, Optional, Union


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


def validar_registro_9900(
    linha_9900: str,
    *,
    linhas_arquivo: Union[str, List[str], None] = None,
) -> Dict[str, Any]:
    """
    Valida as regras do Registro 9900 (Bloco 9, EFD-Contribuições 1.35).

    Regras do manual (conforme `documentacao_blocos/1.35/bloco_9.md`):
    - REG: obrigatório, valor fixo "9900"
    - REG_BLC: obrigatório, código do registro a ser totalizado (tamanho 4)
    - QTD_REG_BLC: obrigatório, total de registros do tipo REG_BLC
    - Validação (opcional): verificar se o número de linhas do tipo REG_BLC no arquivo
      é igual ao QTD_REG_BLC informado.

    Args:
        linha_9900: linha do arquivo SPED contendo o registro 9900
        linhas_arquivo: opcional; linhas do arquivo (ou de onde você quiser contar)
                      para validar QTD_REG_BLC vs ocorrências reais de REG_BLC

    Returns:
        dict com:
          - ok (bool)
          - erros (list[str])
          - campos (dict) com REG, REG_BLC, QTD_REG_BLC
          - contexto (dict) com contagem real quando `linhas_arquivo` é informado
    """
    erros: List[str] = []

    if not linha_9900 or not isinstance(linha_9900, str):
        return {"ok": False, "erros": ["Linha do registro 9900 inválida/vazia."], "campos": {}, "contexto": {}}

    partes = _split_sped(linha_9900)
    reg = _obter_campo(partes, 0)
    reg_blc = _obter_campo(partes, 1)
    qtd_reg_blc = _obter_campo(partes, 2)

    if reg != "9900":
        erros.append("Campo REG inválido: esperado '9900'.")

    if not reg_blc:
        erros.append("Campo REG_BLC obrigatório não informado.")
    elif len(reg_blc) != 4:
        erros.append("Campo REG_BLC inválido: esperado tamanho 4 (ex.: '9001', '9990').")

    if not _eh_inteiro_nao_negativo(qtd_reg_blc):
        erros.append("Campo QTD_REG_BLC inválido: esperado inteiro não-negativo.")

    contexto: Dict[str, Any] = {}
    linhas_norm = _normalizar_linhas(linhas_arquivo)
    if linhas_norm and reg_blc and _eh_inteiro_nao_negativo(qtd_reg_blc):
        regs = [_extrair_reg(l) for l in linhas_norm]
        regs = [r for r in regs if r]
        qtd_real = sum(1 for r in regs if r == reg_blc)

        contexto = {
            "reg_blc": reg_blc,
            "qtd_informada": int(qtd_reg_blc),
            "qtd_real_encontrada": qtd_real,
        }

        if qtd_real != int(qtd_reg_blc):
            erros.append(
                f"QTD_REG_BLC inconsistente para REG_BLC={reg_blc}: informado {qtd_reg_blc}, encontrado {qtd_real}."
            )

    return {
        "ok": len(erros) == 0,
        "erros": erros,
        "campos": {
            "REG": reg,
            "REG_BLC": reg_blc,
            "QTD_REG_BLC": qtd_reg_blc,
        },
        "contexto": contexto,
    }


def validar_9900(
    linhas: Union[str, List[str], None],
    *,
    linhas_arquivo: Union[str, List[str], None] = None,
) -> str:
    """
    Wrapper que retorna JSON (array) e valida cada linha 9900 encontrada.

    - Se `linhas_arquivo` for informado, valida também QTD_REG_BLC vs contagem real.
    """
    linhas_para_processar = _normalizar_linhas(linhas)
    resultados: List[Dict[str, Any]] = []

    for linha in linhas_para_processar:
        if _extrair_reg(linha) != "9900":
            continue
        resultados.append(validar_registro_9900(linha, linhas_arquivo=linhas_arquivo))

    return json.dumps(resultados, ensure_ascii=False, indent=2)