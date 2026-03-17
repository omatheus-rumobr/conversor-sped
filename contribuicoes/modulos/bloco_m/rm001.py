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


def validar_registro_m001(
    linha_m001: str,
    *,
    linhas_bloco_m: Union[str, List[str], None] = None,
) -> Dict[str, Any]:
    """
    Valida as regras do Registro M001 (Bloco M, EFD-Contribuições 1.35).

    Regras do manual (conforme `documentacao_blocos/1.35/bloco_M.md`):
    - REG: obrigatório, valor fixo "M001"
    - IND_MOV: obrigatório, valores válidos ["0", "1"]
    - Se IND_MOV == "1": somente podem existir registros de abertura/encerramento do bloco
      (no Bloco M: M001 e M990).
    - Se IND_MOV == "0": deve existir pelo menos um registro além de abertura/encerramento.

    Args:
        linha_m001: linha do arquivo SPED contendo o registro M001
        linhas_bloco_m: opcional; linhas do Bloco M para validar a regra cruzada do IND_MOV

    Returns:
        dict com:
          - ok (bool)
          - erros (list[str])
          - campos (dict) com REG e IND_MOV normalizados
          - contexto (dict) com informações calculadas quando `linhas_bloco_m` é informado
    """
    erros: List[str] = []

    if not linha_m001 or not isinstance(linha_m001, str):
        return {"ok": False, "erros": ["Linha do registro M001 inválida/vazia."], "campos": {}, "contexto": {}}

    partes = _split_sped(linha_m001)
    reg = _obter_campo(partes, 0)
    ind_mov = _obter_campo(partes, 1)

    if reg != "M001":
        erros.append("Campo REG inválido: esperado 'M001'.")

    if ind_mov not in {"0", "1"}:
        erros.append("Campo IND_MOV inválido: valores válidos são '0' ou '1'.")

    contexto: Dict[str, Any] = {}
    linhas_norm = _normalizar_linhas(linhas_bloco_m)
    if linhas_norm:
        regs_encontrados = [_extrair_reg(l) for l in linhas_norm]
        regs_encontrados = [r for r in regs_encontrados if r]

        regs_abertura_encerramento = {"M001", "M990"}
        regs_outros = [r for r in regs_encontrados if r not in regs_abertura_encerramento]

        contexto = {
            "qtd_linhas_bloco_m": len(linhas_norm),
            "regs_encontrados": regs_encontrados,
            "qtd_regs_outros": len(regs_outros),
            "regs_outros": regs_outros,
        }

        if ind_mov == "1":
            regs_invalidos = sorted({r for r in regs_encontrados if r not in regs_abertura_encerramento})
            if regs_invalidos:
                erros.append(
                    "IND_MOV=1: bloco M não pode conter registros além de M001 e M990. "
                    f"Encontrado(s): {', '.join(regs_invalidos)}."
                )
        elif ind_mov == "0":
            if len(regs_outros) == 0:
                erros.append("IND_MOV=0: deve existir pelo menos um registro no bloco M além de M001 e M990.")

    return {
        "ok": len(erros) == 0,
        "erros": erros,
        "campos": {
            "REG": reg,
            "IND_MOV": ind_mov,
        },
        "contexto": contexto,
    }


def validar_m001(
    linhas: Union[str, List[str], None],
    *,
    linhas_bloco_m: Union[str, List[str], None] = None,
) -> str:
    """
    Wrapper compatível com o padrão dos módulos: retorna JSON (array).

    - Se `linhas` tiver múltiplas linhas, valida cada M001 encontrado.
    - Se `linhas_bloco_m` for informado, aplica também a validação cruzada do IND_MOV.
    """
    linhas_para_processar = _normalizar_linhas(linhas)
    resultados: List[Dict[str, Any]] = []

    for linha in linhas_para_processar:
        if _extrair_reg(linha) != "M001":
            continue
        resultados.append(validar_registro_m001(linha, linhas_bloco_m=linhas_bloco_m))

    return json.dumps(resultados, ensure_ascii=False, indent=2)