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


def validar_registro_m350(linha_m350: str) -> Dict[str, Any]:
    """
    Valida regras do Registro M350 (Bloco M, EFD-Contribuições 1.35) conforme trecho do manual.

    Campos/validações implementadas (do trecho em `documentacao_blocos/1.35/bloco_M.md:760-783`):
    - REG: obrigatório, valor fixo "M350"
    - VL_TOT_FOL: obrigatório, numérico
    - VL_EXC_BC: obrigatório, numérico
    - VL_TOT_BC: obrigatório, numérico
    - ALIQ_PIS_FOL: obrigatório, numérico
      Observação do manual: valor válido [1] (interpretação comum: 1,00%)
    - VL_TOT_CONT_FOL: obrigatório, numérico
      Consistência (manual): VL_TOT_CONT_FOL = VL_TOT_BC x ALIQ_PIS_FOL

    Nota: o manual expressa a multiplicação sem explicitar divisão por 100. Aqui assumimos que
    `ALIQ_PIS_FOL` vem como percentual (ex.: 1 para 1%) e aceitamos também o valor em fração (0.01).
    """
    erros: List[str] = []

    if not linha_m350 or not isinstance(linha_m350, str):
        return {"ok": False, "erros": ["Linha do registro M350 inválida/vazia."], "campos": {}, "contexto": {}}

    partes = _split_sped(linha_m350)
    reg = _obter_campo(partes, 0)
    vl_tot_fol = _obter_campo(partes, 1)
    vl_exc_bc = _obter_campo(partes, 2)
    vl_tot_bc = _obter_campo(partes, 3)
    aliq_pis_fol = _obter_campo(partes, 4)
    vl_tot_cont_fol = _obter_campo(partes, 5)

    if reg != "M350":
        erros.append("Campo REG inválido: esperado 'M350'.")

    nums: Dict[str, Optional[float]] = {}
    for nome, valor in {
        "VL_TOT_FOL": vl_tot_fol,
        "VL_EXC_BC": vl_exc_bc,
        "VL_TOT_BC": vl_tot_bc,
        "ALIQ_PIS_FOL": aliq_pis_fol,
        "VL_TOT_CONT_FOL": vl_tot_cont_fol,
    }.items():
        ok, num = _parse_num(valor)
        if not valor:
            erros.append(f"Campo {nome} obrigatório não informado.")
        elif not ok or num is None:
            erros.append(f"Campo {nome} inválido: esperado numérico.")
        nums[nome] = num

    v_aliq = nums.get("ALIQ_PIS_FOL")
    if v_aliq is not None:
        # Validação do "valor válido [1]" com tolerância.
        if not (_eq(v_aliq, 1.0) or _eq(v_aliq, 0.01)):
            erros.append("Campo ALIQ_PIS_FOL inválido: valor esperado 1 (1%) ou 0,01.")

    v_bc = nums.get("VL_TOT_BC")
    v_cont = nums.get("VL_TOT_CONT_FOL")
    if v_bc is not None and v_aliq is not None and v_cont is not None:
        # aceita aliq como 1 (percentual) ou 0.01 (fração)
        esperado_percent = v_bc * (v_aliq / 100.0)
        esperado_frac = v_bc * v_aliq
        if not (_eq(v_cont, esperado_percent) or _eq(v_cont, esperado_frac)):
            erros.append("Consistência: VL_TOT_CONT_FOL deve ser igual a VL_TOT_BC x ALIQ_PIS_FOL.")

    return {
        "ok": len(erros) == 0,
        "erros": erros,
        "campos": {
            "REG": reg,
            "VL_TOT_FOL": vl_tot_fol,
            "VL_EXC_BC": vl_exc_bc,
            "VL_TOT_BC": vl_tot_bc,
            "ALIQ_PIS_FOL": aliq_pis_fol,
            "VL_TOT_CONT_FOL": vl_tot_cont_fol,
        },
        "contexto": {"numeros": nums},
    }


def validar_m350(linhas: Union[str, List[str], None]) -> str:
    """
    Wrapper que retorna JSON (array) e valida cada linha M350 encontrada.
    """
    linhas_para_processar = _normalizar_linhas(linhas)
    resultados: List[Dict[str, Any]] = []

    for linha in linhas_para_processar:
        if _extrair_reg(linha) != "M350":
            continue
        resultados.append(validar_registro_m350(linha))

    return json.dumps(resultados, ensure_ascii=False, indent=2)