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


def _parse_num(valor: str) -> Tuple[bool, Optional[float]]:
    """
    Converte número do SPED para float.
    Aceita decimal com vírgula ou ponto. Vazio retorna (True, None).
    """
    if valor is None:
        return True, None
    v = str(valor).strip()
    if not v or v == "-":
        return True, None
    try:
        v = v.replace(".", "").replace(",", ".") if ("," in v and "." in v) else v.replace(",", ".")
        return True, float(v)
    except ValueError:
        return False, None


def _eq(a: float, b: float, tol: float = 1e-6) -> bool:
    return abs(a - b) <= tol


def validar_registro_m600(linha_m600: str) -> Dict[str, Any]:
    """
    Valida regras do Registro M600 (Bloco M, EFD-Contribuições 1.35) conforme trecho do manual.

    Layout (do trecho em `documentacao_blocos/1.35/bloco_M.md:1090-1159`):
    - 01 REG (obrigatório, "M600")
    - 02 VL_TOT_CONT_NC_PER (obrigatório, numérico)
    - 03 VL_TOT_CRED_DESC (obrigatório, numérico)
    - 04 VL_TOT_CRED_DESC_ANT (obrigatório, numérico)
    - 05 VL_TOT_CONT_NC_DEV (obrigatório, numérico) = 02 - 03 - 04
    - 06 VL_RET_NC (obrigatório, numérico) <= 05
    - 07 VL_OUT_DED_NC (obrigatório, numérico)
    - 08 VL_CONT_NC_REC (obrigatório, numérico) = 05 - 06 - 07
    - 09 VL_TOT_CONT_CUM_PER (obrigatório, numérico)
    - 10 VL_RET_CUM (obrigatório, numérico) <= 09
    - 11 VL_OUT_DED_CUM (obrigatório, numérico)
    - 12 VL_CONT_CUM_REC (obrigatório, numérico) = 09 - 10 - 11
    - 13 VL_TOT_CONT_REC (obrigatório, numérico) = 08 + 12

    Validações explícitas do manual:
    - (03 + 04) <= 02
    - 06 <= 05
    - 10 <= 09
    """
    erros: List[str] = []

    if not linha_m600 or not isinstance(linha_m600, str):
        return {"ok": False, "erros": ["Linha do registro M600 inválida/vazia."], "campos": {}, "contexto": {}}

    partes = _split_sped(linha_m600)
    reg = _obter_campo(partes, 0)

    campos = {
        "VL_TOT_CONT_NC_PER": _obter_campo(partes, 1),
        "VL_TOT_CRED_DESC": _obter_campo(partes, 2),
        "VL_TOT_CRED_DESC_ANT": _obter_campo(partes, 3),
        "VL_TOT_CONT_NC_DEV": _obter_campo(partes, 4),
        "VL_RET_NC": _obter_campo(partes, 5),
        "VL_OUT_DED_NC": _obter_campo(partes, 6),
        "VL_CONT_NC_REC": _obter_campo(partes, 7),
        "VL_TOT_CONT_CUM_PER": _obter_campo(partes, 8),
        "VL_RET_CUM": _obter_campo(partes, 9),
        "VL_OUT_DED_CUM": _obter_campo(partes, 10),
        "VL_CONT_CUM_REC": _obter_campo(partes, 11),
        "VL_TOT_CONT_REC": _obter_campo(partes, 12),
    }

    if reg != "M600":
        erros.append("Campo REG inválido: esperado 'M600'.")

    nums: Dict[str, Optional[float]] = {}
    for nome, valor in campos.items():
        ok, num = _parse_num(valor)
        if not valor:
            erros.append(f"Campo {nome} obrigatório não informado.")
        elif not ok or num is None:
            erros.append(f"Campo {nome} inválido: esperado numérico.")
        nums[nome] = num

    v02 = nums.get("VL_TOT_CONT_NC_PER")
    v03 = nums.get("VL_TOT_CRED_DESC")
    v04 = nums.get("VL_TOT_CRED_DESC_ANT")
    v05 = nums.get("VL_TOT_CONT_NC_DEV")
    v06 = nums.get("VL_RET_NC")
    v07 = nums.get("VL_OUT_DED_NC")
    v08 = nums.get("VL_CONT_NC_REC")
    v09 = nums.get("VL_TOT_CONT_CUM_PER")
    v10 = nums.get("VL_RET_CUM")
    v11 = nums.get("VL_OUT_DED_CUM")
    v12 = nums.get("VL_CONT_CUM_REC")
    v13 = nums.get("VL_TOT_CONT_REC")

    if None not in (v02, v03, v04):
        if (v03 + v04) - v02 > 1e-6:
            erros.append("Validação: VL_TOT_CRED_DESC + VL_TOT_CRED_DESC_ANT deve ser <= VL_TOT_CONT_NC_PER.")

    if None not in (v06, v05):
        if v06 - v05 > 1e-6:
            erros.append("Validação: VL_RET_NC deve ser <= VL_TOT_CONT_NC_DEV.")

    if None not in (v10, v09):
        if v10 - v09 > 1e-6:
            erros.append("Validação: VL_RET_CUM deve ser <= VL_TOT_CONT_CUM_PER.")

    if None not in (v05, v02, v03, v04):
        esperado = v02 - v03 - v04
        if not _eq(v05, esperado):
            erros.append("Consistência: VL_TOT_CONT_NC_DEV deve ser igual a (VL_TOT_CONT_NC_PER - VL_TOT_CRED_DESC - VL_TOT_CRED_DESC_ANT).")

    if None not in (v08, v05, v06, v07):
        esperado = v05 - v06 - v07
        if not _eq(v08, esperado):
            erros.append("Consistência: VL_CONT_NC_REC deve ser igual a (VL_TOT_CONT_NC_DEV - VL_RET_NC - VL_OUT_DED_NC).")

    if None not in (v12, v09, v10, v11):
        esperado = v09 - v10 - v11
        if not _eq(v12, esperado):
            erros.append("Consistência: VL_CONT_CUM_REC deve ser igual a (VL_TOT_CONT_CUM_PER - VL_RET_CUM - VL_OUT_DED_CUM).")

    if None not in (v13, v08, v12):
        esperado = v08 + v12
        if not _eq(v13, esperado):
            erros.append("Consistência: VL_TOT_CONT_REC deve ser igual a (VL_CONT_NC_REC + VL_CONT_CUM_REC).")

    return {
        "ok": len(erros) == 0,
        "erros": erros,
        "campos": {"REG": reg, **campos},
        "contexto": {"numeros": nums},
    }


def validar_m600(linhas: Union[str, List[str], None]) -> str:
    """
    Wrapper que retorna JSON (array) e valida cada linha M600 encontrada.
    """
    linhas_para_processar = _normalizar_linhas(linhas)
    resultados: List[Dict[str, Any]] = []

    for linha in linhas_para_processar:
        if _extrair_reg(linha) != "M600":
            continue
        resultados.append(validar_registro_m600(linha))

    return json.dumps(resultados, ensure_ascii=False, indent=2)