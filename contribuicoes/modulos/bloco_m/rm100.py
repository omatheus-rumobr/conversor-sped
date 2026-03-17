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


def _eh_inteiro_nao_negativo(valor: str) -> bool:
    return bool(valor) and str(valor).isdigit()


def validar_registro_m100(linha_m100: str) -> Dict[str, Any]:
    """
    Valida regras do Registro M100 (Bloco M, EFD-Contribuições 1.35) conforme trecho do manual.

    Campos/validações implementadas (do trecho em `documentacao_blocos/1.35/bloco_M.md:20-86`):
    - REG: obrigatório, valor fixo "M100"
    - COD_CRED: obrigatório, tamanho 3
    - IND_CRED_ORI: obrigatório, valores válidos ["0", "1"]
    - VL_CRED, VL_AJUS_ACRES, VL_AJUS_REDUC, VL_CRED_DIF, VL_CRED_DISP, SLD_CRED: obrigatórios e numéricos
    - IND_DESC_CRED: obrigatório, valores válidos ["0", "1"]
    - VL_CRED_DESC: opcional e numérico
    - Validação explícita: VL_CRED_DIF não pode ser maior que (VL_CRED + VL_AJUS_ACRES - VL_AJUS_REDUC)
    - Regras do IND_DESC_CRED:
      - se IND_DESC_CRED=0 e VL_CRED_DESC informado e VL_CRED_DISP informado: VL_CRED_DESC deve ser igual a VL_CRED_DISP
      - se IND_DESC_CRED=1 e VL_CRED_DESC informado e VL_CRED_DISP informado: VL_CRED_DESC deve ser <= VL_CRED_DISP

    Returns:
        dict com:
          - ok (bool)
          - erros (list[str])
          - campos (dict) com campos extraídos
          - contexto (dict) com números convertidos quando possível
    """
    erros: List[str] = []

    if not linha_m100 or not isinstance(linha_m100, str):
        return {"ok": False, "erros": ["Linha do registro M100 inválida/vazia."], "campos": {}, "contexto": {}}

    partes = _split_sped(linha_m100)
    reg = _obter_campo(partes, 0)
    cod_cred = _obter_campo(partes, 1)
    ind_cred_ori = _obter_campo(partes, 2)
    vl_bc_pis = _obter_campo(partes, 3)
    aliq_pis = _obter_campo(partes, 4)
    quant_bc_pis = _obter_campo(partes, 5)
    aliq_pis_quant = _obter_campo(partes, 6)
    vl_cred = _obter_campo(partes, 7)
    vl_ajus_acres = _obter_campo(partes, 8)
    vl_ajus_reduc = _obter_campo(partes, 9)
    vl_cred_dif = _obter_campo(partes, 10)
    vl_cred_disp = _obter_campo(partes, 11)
    ind_desc_cred = _obter_campo(partes, 12)
    vl_cred_desc = _obter_campo(partes, 13)
    sld_cred = _obter_campo(partes, 14)

    if reg != "M100":
        erros.append("Campo REG inválido: esperado 'M100'.")

    if not cod_cred:
        erros.append("Campo COD_CRED obrigatório não informado.")
    elif len(cod_cred) != 3:
        erros.append("Campo COD_CRED inválido: esperado tamanho 3.")

    if ind_cred_ori not in {"0", "1"}:
        erros.append("Campo IND_CRED_ORI inválido: valores válidos são '0' ou '1'.")

    # Campos numéricos opcionais
    for nome, valor in {
        "VL_BC_PIS": vl_bc_pis,
        "ALIQ_PIS": aliq_pis,
        "QUANT_BC_PIS": quant_bc_pis,
        "ALIQ_PIS_QUANT": aliq_pis_quant,
    }.items():
        ok_num, _ = _parse_num(valor)
        if not ok_num:
            erros.append(f"Campo {nome} inválido: esperado numérico.")

    # Campos numéricos obrigatórios
    obrig_num = {
        "VL_CRED": vl_cred,
        "VL_AJUS_ACRES": vl_ajus_acres,
        "VL_AJUS_REDUC": vl_ajus_reduc,
        "VL_CRED_DIF": vl_cred_dif,
        "VL_CRED_DISP": vl_cred_disp,
        "SLD_CRED": sld_cred,
    }
    numeros: Dict[str, Optional[float]] = {}
    for nome, valor in obrig_num.items():
        ok_num, num = _parse_num(valor)
        if not valor:
            erros.append(f"Campo {nome} obrigatório não informado.")
        elif not ok_num or num is None:
            erros.append(f"Campo {nome} inválido: esperado numérico.")
        numeros[nome] = num

    if ind_desc_cred not in {"0", "1"}:
        erros.append("Campo IND_DESC_CRED inválido: valores válidos são '0' ou '1'.")

    ok_num, num_vl_cred_desc = _parse_num(vl_cred_desc)
    if vl_cred_desc and not ok_num:
        erros.append("Campo VL_CRED_DESC inválido: esperado numérico.")

    # Validação explícita do manual (Campo 11 - VL_CRED_DIF)
    v_vl_cred = numeros.get("VL_CRED")
    v_acres = numeros.get("VL_AJUS_ACRES")
    v_reduc = numeros.get("VL_AJUS_REDUC")
    v_dif = numeros.get("VL_CRED_DIF")
    if None not in (v_vl_cred, v_acres, v_reduc, v_dif):
        limite = (v_vl_cred or 0.0) + (v_acres or 0.0) - (v_reduc or 0.0)
        if (v_dif or 0.0) > limite + 1e-9:
            erros.append(
                "VL_CRED_DIF inválido: não pode ser maior que VL_CRED + VL_AJUS_ACRES - VL_AJUS_REDUC."
            )

    # Regras do IND_DESC_CRED (quando dá para comparar)
    v_disp = numeros.get("VL_CRED_DISP")
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
            "VL_BC_PIS": vl_bc_pis,
            "ALIQ_PIS": aliq_pis,
            "QUANT_BC_PIS": quant_bc_pis,
            "ALIQ_PIS_QUANT": aliq_pis_quant,
            "VL_CRED": vl_cred,
            "VL_AJUS_ACRES": vl_ajus_acres,
            "VL_AJUS_REDUC": vl_ajus_reduc,
            "VL_CRED_DIF": vl_cred_dif,
            "VL_CRED_DISP": vl_cred_disp,
            "IND_DESC_CRED": ind_desc_cred,
            "VL_CRED_DESC": vl_cred_desc,
            "SLD_CRED": sld_cred,
        },
        "contexto": {
            "numeros": {
                "VL_BC_PIS": _parse_num(vl_bc_pis)[1],
                "ALIQ_PIS": _parse_num(aliq_pis)[1],
                "QUANT_BC_PIS": _parse_num(quant_bc_pis)[1],
                "ALIQ_PIS_QUANT": _parse_num(aliq_pis_quant)[1],
                "VL_CRED": v_vl_cred,
                "VL_AJUS_ACRES": v_acres,
                "VL_AJUS_REDUC": v_reduc,
                "VL_CRED_DIF": v_dif,
                "VL_CRED_DISP": v_disp,
                "VL_CRED_DESC": num_vl_cred_desc,
                "SLD_CRED": numeros.get("SLD_CRED"),
            }
        },
    }


def validar_m100(linhas: Union[str, List[str], None]) -> str:
    """
    Wrapper que retorna JSON (array) e valida cada linha M100 encontrada.
    """
    linhas_para_processar = _normalizar_linhas(linhas)
    resultados: List[Dict[str, Any]] = []

    for linha in linhas_para_processar:
        if _extrair_reg(linha) != "M100":
            continue
        resultados.append(validar_registro_m100(linha))

    return json.dumps(resultados, ensure_ascii=False, indent=2)