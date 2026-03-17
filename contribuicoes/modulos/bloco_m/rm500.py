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


def validar_registro_m500(linha_m500: str) -> Dict[str, Any]:
    """
    Valida regras do Registro M500 (Bloco M, EFD-Contribuições 1.35) conforme trecho do manual.

    Campos/validações implementadas (do trecho em `documentacao_blocos/1.35/bloco_M.md:857-924`):
    - REG: obrigatório, valor fixo "M500"
    - COD_CRED: obrigatório, tamanho 3
    - IND_CRED_ORI: obrigatório, valores válidos ["0", "1"]
    - VL_BC_COFINS, ALIQ_COFINS, QUANT_BC_COFINS, ALIQ_COFINS_QUANT: opcionais, se informados devem ser numéricos
    - VL_CRED, VL_AJUS_ACRES, VL_AJUS_REDUC, VL_CRED_DIFER, VL_CRED_DISP, SLD_CRED: obrigatórios e numéricos
    - IND_DESC_CRED: obrigatório, valores válidos ["0", "1"]
    - VL_CRED_DESC: opcional e numérico (se informado)
    - Validação explícita: VL_CRED_DIFER não pode ser maior que (VL_CRED + VL_AJUS_ACRES - VL_AJUS_REDUC)
    - Regras do IND_DESC_CRED (quando há dados para comparar):
      - se IND_DESC_CRED=0 e VL_CRED_DESC informado e VL_CRED_DISP informado: VL_CRED_DESC deve ser igual a VL_CRED_DISP
      - se IND_DESC_CRED=1 e VL_CRED_DESC informado e VL_CRED_DISP informado: VL_CRED_DESC deve ser <= VL_CRED_DISP
    """
    erros: List[str] = []

    if not linha_m500 or not isinstance(linha_m500, str):
        return {"ok": False, "erros": ["Linha do registro M500 inválida/vazia."], "campos": {}, "contexto": {}}

    partes = _split_sped(linha_m500)
    reg = _obter_campo(partes, 0)
    cod_cred = _obter_campo(partes, 1)
    ind_cred_ori = _obter_campo(partes, 2)
    vl_bc_cofins = _obter_campo(partes, 3)
    aliq_cofins = _obter_campo(partes, 4)
    quant_bc_cofins = _obter_campo(partes, 5)
    aliq_cofins_quant = _obter_campo(partes, 6)
    vl_cred = _obter_campo(partes, 7)
    vl_ajus_acres = _obter_campo(partes, 8)
    vl_ajus_reduc = _obter_campo(partes, 9)
    vl_cred_difer = _obter_campo(partes, 10)
    vl_cred_disp = _obter_campo(partes, 11)
    ind_desc_cred = _obter_campo(partes, 12)
    vl_cred_desc = _obter_campo(partes, 13)
    sld_cred = _obter_campo(partes, 14)

    if reg != "M500":
        erros.append("Campo REG inválido: esperado 'M500'.")

    if not cod_cred:
        erros.append("Campo COD_CRED obrigatório não informado.")
    elif len(cod_cred) != 3:
        erros.append("Campo COD_CRED inválido: esperado tamanho 3.")

    if ind_cred_ori not in {"0", "1"}:
        erros.append("Campo IND_CRED_ORI inválido: valores válidos são '0' ou '1'.")

    # Numéricos opcionais
    nums: Dict[str, Optional[float]] = {}
    for nome, valor in {
        "VL_BC_COFINS": vl_bc_cofins,
        "ALIQ_COFINS": aliq_cofins,
        "QUANT_BC_COFINS": quant_bc_cofins,
        "ALIQ_COFINS_QUANT": aliq_cofins_quant,
    }.items():
        ok, num = _parse_num(valor)
        if valor and not ok:
            erros.append(f"Campo {nome} inválido: esperado numérico.")
        nums[nome] = num

    # Numéricos obrigatórios
    obrig_num = {
        "VL_CRED": vl_cred,
        "VL_AJUS_ACRES": vl_ajus_acres,
        "VL_AJUS_REDUC": vl_ajus_reduc,
        "VL_CRED_DIFER": vl_cred_difer,
        "VL_CRED_DISP": vl_cred_disp,
        "SLD_CRED": sld_cred,
    }
    for nome, valor in obrig_num.items():
        ok, num = _parse_num(valor)
        if not valor:
            erros.append(f"Campo {nome} obrigatório não informado.")
        elif not ok or num is None:
            erros.append(f"Campo {nome} inválido: esperado numérico.")
        nums[nome] = num

    if ind_desc_cred not in {"0", "1"}:
        erros.append("Campo IND_DESC_CRED inválido: valores válidos são '0' ou '1'.")

    ok, num_vl_cred_desc = _parse_num(vl_cred_desc)
    if vl_cred_desc and not ok:
        erros.append("Campo VL_CRED_DESC inválido: esperado numérico.")
    nums["VL_CRED_DESC"] = num_vl_cred_desc

    # Validação explícita do manual (Campo 11 - VL_CRED_DIFER)
    v_vl_cred = nums.get("VL_CRED")
    v_acres = nums.get("VL_AJUS_ACRES")
    v_reduc = nums.get("VL_AJUS_REDUC")
    v_difer = nums.get("VL_CRED_DIFER")
    if None not in (v_vl_cred, v_acres, v_reduc, v_difer):
        limite = (v_vl_cred or 0.0) + (v_acres or 0.0) - (v_reduc or 0.0)
        if (v_difer or 0.0) > limite + 1e-9:
            erros.append("VL_CRED_DIFER inválido: não pode ser maior que VL_CRED + VL_AJUS_ACRES - VL_AJUS_REDUC.")

    # Regras do IND_DESC_CRED
    v_disp = nums.get("VL_CRED_DISP")
    if ind_desc_cred in {"0", "1"} and num_vl_cred_desc is not None and v_disp is not None:
        if ind_desc_cred == "0":
            if abs(num_vl_cred_desc - v_disp) > 1e-6:
                erros.append("IND_DESC_CRED=0: VL_CRED_DESC deve ser igual a VL_CRED_DISP.")
        else:
            if num_vl_cred_desc - v_disp > 1e-6:
                erros.append("IND_DESC_CRED=1: VL_CRED_DESC não pode ser maior que VL_CRED_DISP.")

    return {
        "ok": len(erros) == 0,
        "erros": erros,
        "campos": {
            "REG": reg,
            "COD_CRED": cod_cred,
            "IND_CRED_ORI": ind_cred_ori,
            "VL_BC_COFINS": vl_bc_cofins,
            "ALIQ_COFINS": aliq_cofins,
            "QUANT_BC_COFINS": quant_bc_cofins,
            "ALIQ_COFINS_QUANT": aliq_cofins_quant,
            "VL_CRED": vl_cred,
            "VL_AJUS_ACRES": vl_ajus_acres,
            "VL_AJUS_REDUC": vl_ajus_reduc,
            "VL_CRED_DIFER": vl_cred_difer,
            "VL_CRED_DISP": vl_cred_disp,
            "IND_DESC_CRED": ind_desc_cred,
            "VL_CRED_DESC": vl_cred_desc,
            "SLD_CRED": sld_cred,
        },
        "contexto": {"numeros": nums},
    }


def validar_m500(linhas: Union[str, List[str], None]) -> str:
    """
    Wrapper que retorna JSON (array) e valida cada linha M500 encontrada.
    """
    linhas_para_processar = _normalizar_linhas(linhas)
    resultados: List[Dict[str, Any]] = []

    for linha in linhas_para_processar:
        if _extrair_reg(linha) != "M500":
            continue
        resultados.append(validar_registro_m500(linha))

    return json.dumps(resultados, ensure_ascii=False, indent=2)