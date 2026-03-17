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


def validar_registro_m211(linha_m211: str) -> Dict[str, Any]:
    """
    Valida regras do Registro M211 (Bloco M, EFD-Contribuições 1.35) conforme trecho do manual.

    Campos/validações implementadas (do trecho em `documentacao_blocos/1.35/bloco_M.md:572-603`):
    - REG: obrigatório, valor fixo "M211"
    - IND_TIP_COOP: obrigatório, valores válidos ["01","02","03","04","05","06","99"]
    - VL_BC_CONT_ANT_EXC_COOP: obrigatório, numérico
    - VL_EXC_COOP_GER: opcional, se informado deve ser numérico
    - VL_EXC_ESP_COOP: opcional, se informado deve ser numérico
    - VL_BC_CONT: obrigatório, numérico
    - Consistência: VL_BC_CONT = VL_BC_CONT_ANT_EXC_COOP - VL_EXC_COOP_GER - VL_EXC_ESP_COOP
      (quando todos os números estiverem válidos; campos opcionais ausentes contam como 0)
    """
    erros: List[str] = []

    if not linha_m211 or not isinstance(linha_m211, str):
        return {"ok": False, "erros": ["Linha do registro M211 inválida/vazia."], "campos": {}, "contexto": {}}

    partes = _split_sped(linha_m211)
    reg = _obter_campo(partes, 0)
    ind_tip_coop = _obter_campo(partes, 1)
    vl_bc_ant = _obter_campo(partes, 2)
    vl_exc_ger = _obter_campo(partes, 3)
    vl_exc_esp = _obter_campo(partes, 4)
    vl_bc_cont = _obter_campo(partes, 5)

    if reg != "M211":
        erros.append("Campo REG inválido: esperado 'M211'.")

    valores_validos = {"01", "02", "03", "04", "05", "06", "99"}
    if not ind_tip_coop:
        erros.append("Campo IND_TIP_COOP obrigatório não informado.")
    elif ind_tip_coop not in valores_validos:
        erros.append("Campo IND_TIP_COOP inválido: valores válidos são 01, 02, 03, 04, 05, 06, 99.")

    nums: Dict[str, Optional[float]] = {}

    ok, n_bc_ant = _parse_num(vl_bc_ant)
    if not vl_bc_ant:
        erros.append("Campo VL_BC_CONT_ANT_EXC_COOP obrigatório não informado.")
    elif not ok or n_bc_ant is None:
        erros.append("Campo VL_BC_CONT_ANT_EXC_COOP inválido: esperado numérico.")
    nums["VL_BC_CONT_ANT_EXC_COOP"] = n_bc_ant

    ok, n_exc_ger = _parse_num(vl_exc_ger)
    if vl_exc_ger and (not ok):
        erros.append("Campo VL_EXC_COOP_GER inválido: esperado numérico.")
    nums["VL_EXC_COOP_GER"] = n_exc_ger

    ok, n_exc_esp = _parse_num(vl_exc_esp)
    if vl_exc_esp and (not ok):
        erros.append("Campo VL_EXC_ESP_COOP inválido: esperado numérico.")
    nums["VL_EXC_ESP_COOP"] = n_exc_esp

    ok, n_bc_cont = _parse_num(vl_bc_cont)
    if not vl_bc_cont:
        erros.append("Campo VL_BC_CONT obrigatório não informado.")
    elif not ok or n_bc_cont is None:
        erros.append("Campo VL_BC_CONT inválido: esperado numérico.")
    nums["VL_BC_CONT"] = n_bc_cont

    if None not in (n_bc_ant, n_bc_cont):
        esperado = (n_bc_ant or 0.0) - (n_exc_ger or 0.0) - (n_exc_esp or 0.0)
        if not _eq(n_bc_cont, esperado):
            erros.append(
                "Consistência: VL_BC_CONT deve ser igual a (VL_BC_CONT_ANT_EXC_COOP - VL_EXC_COOP_GER - VL_EXC_ESP_COOP)."
            )

    return {
        "ok": len(erros) == 0,
        "erros": erros,
        "campos": {
            "REG": reg,
            "IND_TIP_COOP": ind_tip_coop,
            "VL_BC_CONT_ANT_EXC_COOP": vl_bc_ant,
            "VL_EXC_COOP_GER": vl_exc_ger,
            "VL_EXC_ESP_COOP": vl_exc_esp,
            "VL_BC_CONT": vl_bc_cont,
        },
        "contexto": {"numeros": nums},
    }


def validar_m211(linhas: Union[str, List[str], None]) -> str:
    """
    Wrapper que retorna JSON (array) e valida cada linha M211 encontrada.
    """
    linhas_para_processar = _normalizar_linhas(linhas)
    resultados: List[Dict[str, Any]] = []

    for linha in linhas_para_processar:
        if _extrair_reg(linha) != "M211":
            continue
        resultados.append(validar_registro_m211(linha))

    return json.dumps(resultados, ensure_ascii=False, indent=2)