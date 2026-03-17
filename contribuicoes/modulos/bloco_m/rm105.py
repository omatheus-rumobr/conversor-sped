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


def validar_registro_m105(linha_m105: str) -> Dict[str, Any]:
    """
    Valida regras do Registro M105 (Bloco M, EFD-Contribuições 1.35) conforme trecho do manual.

    Campos/validações implementadas (do trecho em `documentacao_blocos/1.35/bloco_M.md:87-191`):
    - REG: obrigatório, valor fixo "M105"
    - NAT_BC_CRED: obrigatório, tamanho 2
    - CST_PIS: obrigatório, numérico (2 dígitos)
    - VL_BC_PIS_TOT, VL_BC_PIS_CUM, VL_BC_PIS_NC, VL_BC_PIS: opcionais, se informados devem ser numéricos
    - QUANT_BC_PIS_TOT, QUANT_BC_PIS: opcionais, se informados devem ser numéricos
    - DESC_CRED: opcional (tamanho até 60)
    - Validação explícita: quando NAT_BC_CRED = "13", DESC_CRED é obrigatório
    """
    erros: List[str] = []

    if not linha_m105 or not isinstance(linha_m105, str):
        return {"ok": False, "erros": ["Linha do registro M105 inválida/vazia."], "campos": {}, "contexto": {}}

    partes = _split_sped(linha_m105)
    reg = _obter_campo(partes, 0)
    nat_bc_cred = _obter_campo(partes, 1)
    cst_pis = _obter_campo(partes, 2)
    vl_bc_pis_tot = _obter_campo(partes, 3)
    vl_bc_pis_cum = _obter_campo(partes, 4)
    vl_bc_pis_nc = _obter_campo(partes, 5)
    vl_bc_pis = _obter_campo(partes, 6)
    quant_bc_pis_tot = _obter_campo(partes, 7)
    quant_bc_pis = _obter_campo(partes, 8)
    desc_cred = _obter_campo(partes, 9)

    if reg != "M105":
        erros.append("Campo REG inválido: esperado 'M105'.")

    if not nat_bc_cred:
        erros.append("Campo NAT_BC_CRED obrigatório não informado.")
    elif len(nat_bc_cred) != 2:
        erros.append("Campo NAT_BC_CRED inválido: esperado tamanho 2.")

    if not cst_pis:
        erros.append("Campo CST_PIS obrigatório não informado.")
    elif not cst_pis.isdigit() or len(cst_pis) != 2:
        erros.append("Campo CST_PIS inválido: esperado numérico com 2 dígitos (ex.: '50', '56').")

    # Numéricos opcionais
    numeros: Dict[str, Optional[float]] = {}
    for nome, valor in {
        "VL_BC_PIS_TOT": vl_bc_pis_tot,
        "VL_BC_PIS_CUM": vl_bc_pis_cum,
        "VL_BC_PIS_NC": vl_bc_pis_nc,
        "VL_BC_PIS": vl_bc_pis,
        "QUANT_BC_PIS_TOT": quant_bc_pis_tot,
        "QUANT_BC_PIS": quant_bc_pis,
    }.items():
        ok_num, num = _parse_num(valor)
        if valor and not ok_num:
            erros.append(f"Campo {nome} inválido: esperado numérico.")
        numeros[nome] = num

    if desc_cred and len(desc_cred) > 60:
        erros.append("Campo DESC_CRED inválido: tamanho máximo 60.")

    if nat_bc_cred == "13" and not desc_cred:
        erros.append("NAT_BC_CRED=13: campo DESC_CRED é obrigatório.")

    return {
        "ok": len(erros) == 0,
        "erros": erros,
        "campos": {
            "REG": reg,
            "NAT_BC_CRED": nat_bc_cred,
            "CST_PIS": cst_pis,
            "VL_BC_PIS_TOT": vl_bc_pis_tot,
            "VL_BC_PIS_CUM": vl_bc_pis_cum,
            "VL_BC_PIS_NC": vl_bc_pis_nc,
            "VL_BC_PIS": vl_bc_pis,
            "QUANT_BC_PIS_TOT": quant_bc_pis_tot,
            "QUANT_BC_PIS": quant_bc_pis,
            "DESC_CRED": desc_cred,
        },
        "contexto": {"numeros": numeros},
    }


def validar_m105(linhas: Union[str, List[str], None]) -> str:
    """
    Wrapper que retorna JSON (array) e valida cada linha M105 encontrada.
    """
    linhas_para_processar = _normalizar_linhas(linhas)
    resultados: List[Dict[str, Any]] = []

    for linha in linhas_para_processar:
        if _extrair_reg(linha) != "M105":
            continue
        resultados.append(validar_registro_m105(linha))

    return json.dumps(resultados, ensure_ascii=False, indent=2)