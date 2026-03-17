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


def _extrair_reg(linha: str) -> str:
    """
    Extrai o código do registro (ex.: "9001") de uma linha SPED.
    Aceita linhas no formato padrão: |9001|...|
    """
    if not linha or not isinstance(linha, str):
        return ""
    partes = linha.strip().split("|")
    # remove vazios no começo/fim (padrão |REG|...|)
    if partes and partes[0] == "":
        partes = partes[1:]
    if partes and partes[-1] == "":
        partes = partes[:-1]
    return (partes[0].strip() if partes else "").strip()


def _obter_campo(partes: List[str], indice: int) -> str:
    if indice < len(partes):
        v = (partes[indice] or "").strip()
        return "" if v == "-" else v
    return ""


def validar_registro_9001(
    linha_9001: str,
    *,
    linhas_bloco9: Union[str, List[str], None] = None,
) -> Dict[str, Any]:
    """
    Valida as regras do Registro 9001 (Bloco 9, EFD-Contribuições 1.35).

    Regras do manual (conforme `documentacao_blocos/1.35/bloco_9.md`):
    - REG: obrigatório, valor fixo "9001"
    - IND_MOV: obrigatório, valores válidos ["0", "1"]
    - Se IND_MOV == "1": somente podem existir registros de abertura/encerramento do bloco
      (no Bloco 9: 9001 e 9990).
    - Se IND_MOV == "0": deve existir pelo menos um registro além da abertura/encerramento.

    Args:
        linha_9001: linha do arquivo SPED contendo o registro 9001
        linhas_bloco9: opcional; linhas do Bloco 9 para validar a regra cruzada do IND_MOV

    Returns:
        dict com:
          - ok (bool)
          - erros (list[str])
          - campos (dict) com REG e IND_MOV normalizados
          - contexto (dict) com informações calculadas quando `linhas_bloco9` é informado
    """
    erros: List[str] = []

    if not linha_9001 or not isinstance(linha_9001, str):
        return {"ok": False, "erros": ["Linha do registro 9001 inválida/vazia."], "campos": {}, "contexto": {}}

    partes = linha_9001.strip().split("|")
    if partes and partes[0] == "":
        partes = partes[1:]
    if partes and partes[-1] == "":
        partes = partes[:-1]

    reg = _obter_campo(partes, 0)
    ind_mov = _obter_campo(partes, 1)

    if reg != "9001":
        erros.append("Campo REG inválido: esperado '9001'.")

    if ind_mov not in {"0", "1"}:
        erros.append("Campo IND_MOV inválido: valores válidos são '0' ou '1'.")

    contexto: Dict[str, Any] = {}
    linhas_norm = _normalizar_linhas(linhas_bloco9)
    if linhas_norm:
        regs_encontrados = [_extrair_reg(l) for l in linhas_norm]
        regs_encontrados = [r for r in regs_encontrados if r]

        # Considera a "existência" de registros além de abertura/encerramento do bloco 9
        regs_abertura_encerramento = {"9001", "9990"}
        regs_outros = [r for r in regs_encontrados if r not in regs_abertura_encerramento]

        contexto = {
            "qtd_linhas_bloco9": len(linhas_norm),
            "regs_encontrados": regs_encontrados,
            "qtd_regs_outros": len(regs_outros),
            "regs_outros": regs_outros,
        }

        if ind_mov == "1":
            # Só 9001/9990 no bloco 9
            regs_invalidos = sorted({r for r in regs_encontrados if r not in regs_abertura_encerramento})
            if regs_invalidos:
                erros.append(
                    "IND_MOV=1: bloco 9 não pode conter registros além de 9001 e 9990. "
                    f"Encontrado(s): {', '.join(regs_invalidos)}."
                )
        elif ind_mov == "0":
            if len(regs_outros) == 0:
                erros.append(
                    "IND_MOV=0: deve existir pelo menos um registro no bloco 9 além de 9001 e 9990."
                )

    return {
        "ok": len(erros) == 0,
        "erros": erros,
        "campos": {
            "REG": reg,
            "IND_MOV": ind_mov,
        },
        "contexto": contexto,
    }


def validar_9001(
    linhas: Union[str, List[str], None],
    *,
    linhas_bloco9: Union[str, List[str], None] = None,
) -> str:
    """
    Wrapper compatível com o padrão de outros módulos: retorna JSON.

    - Se `linhas` tiver múltiplas linhas, valida cada 9001 encontrado.
    - Se `linhas_bloco9` for informado, aplica também a validação cruzada do IND_MOV.
    """
    linhas_para_processar = _normalizar_linhas(linhas)
    resultados: List[Dict[str, Any]] = []

    for linha in linhas_para_processar:
        if _extrair_reg(linha) != "9001":
            continue
        resultados.append(validar_registro_9001(linha, linhas_bloco9=linhas_bloco9))

    return json.dumps(resultados, ensure_ascii=False, indent=2)