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


def validar_registro_m610(linha_m610: str) -> Dict[str, Any]:
    """
    Valida regras do Registro M610 (Bloco M, EFD-Contribuições 1.35) conforme trecho do manual.

    O manual descreve 2 leiautes:
    - **Até 31/12/2018** (campos 01..13)
      VL_CONT_PER (campo 13) = VL_CONT_APUR + VL_AJUS_ACRES - VL_AJUS_REDUC - VL_CONT_DIFER + VL_CONT_DIFER_ANT
    - **A partir de 01/01/2019** (campos 01..16)
      VL_BC_CONT_AJUS (campo 07) = VL_BC_CONT + VL_AJUS_ACRES_BC_COFINS - VL_AJUS_REDUC_BC_COFINS
      VL_CONT_PER (campo 16) = VL_CONT_APUR + VL_AJUS_ACRES - VL_AJUS_REDUC - VL_CONT_DIFER + VL_CONT_DIFER_ANT

    Observação: validações que dependem de cruzamento com outros blocos/tabelas não são feitas aqui.
    """
    erros: List[str] = []

    if not linha_m610 or not isinstance(linha_m610, str):
        return {"ok": False, "erros": ["Linha do registro M610 inválida/vazia."], "campos": {}, "contexto": {}}

    partes = _split_sped(linha_m610)
    reg = _obter_campo(partes, 0)
    if reg != "M610":
        erros.append("Campo REG inválido: esperado 'M610'.")

    layout: str
    if len(partes) >= 16:
        layout = "2019+"
    elif len(partes) >= 13:
        layout = "ate_2018"
    else:
        layout = "desconhecido"
        erros.append("Linha M610 incompleta: quantidade de campos insuficiente para validar.")
        return {"ok": False, "erros": erros, "campos": {"REG": reg}, "contexto": {"layout": layout}}

    campos: Dict[str, str] = {"REG": reg}
    nums: Dict[str, Optional[float]] = {}

    if layout == "ate_2018":
        campos.update(
            {
                "COD_CONT": _obter_campo(partes, 1),
                "VL_REC_BRT": _obter_campo(partes, 2),
                "VL_BC_CONT": _obter_campo(partes, 3),
                "ALIQ_COFINS": _obter_campo(partes, 4),
                "QUANT_BC_COFINS": _obter_campo(partes, 5),
                "ALIQ_COFINS_QUANT": _obter_campo(partes, 6),
                "VL_CONT_APUR": _obter_campo(partes, 7),
                "VL_AJUS_ACRES": _obter_campo(partes, 8),
                "VL_AJUS_REDUC": _obter_campo(partes, 9),
                "VL_CONT_DIFER": _obter_campo(partes, 10),
                "VL_CONT_DIFER_ANT": _obter_campo(partes, 11),
                "VL_CONT_PER": _obter_campo(partes, 12),
            }
        )

        cod_cont = campos["COD_CONT"]
        if not cod_cont:
            erros.append("Campo COD_CONT obrigatório não informado.")
        elif len(cod_cont) != 2:
            erros.append("Campo COD_CONT inválido: esperado tamanho 2.")

        obrig = ["VL_REC_BRT", "VL_BC_CONT", "VL_CONT_APUR", "VL_AJUS_ACRES", "VL_AJUS_REDUC", "VL_CONT_PER"]
        opc = ["ALIQ_COFINS", "QUANT_BC_COFINS", "ALIQ_COFINS_QUANT", "VL_CONT_DIFER", "VL_CONT_DIFER_ANT"]

        for nome in obrig:
            v = campos[nome]
            ok, num = _parse_num(v)
            if not v:
                erros.append(f"Campo {nome} obrigatório não informado.")
            elif not ok or num is None:
                erros.append(f"Campo {nome} inválido: esperado numérico.")
            nums[nome] = num

        for nome in opc:
            v = campos[nome]
            ok, num = _parse_num(v)
            if v and (not ok):
                erros.append(f"Campo {nome} inválido: esperado numérico.")
            nums[nome] = num

        v_cont_per = nums.get("VL_CONT_PER")
        v_cont_apur = nums.get("VL_CONT_APUR")
        v_acres = nums.get("VL_AJUS_ACRES")
        v_reduc = nums.get("VL_AJUS_REDUC")
        v_difer = nums.get("VL_CONT_DIFER") or 0.0
        v_difer_ant = nums.get("VL_CONT_DIFER_ANT") or 0.0
        if None not in (v_cont_per, v_cont_apur, v_acres, v_reduc):
            esperado = (v_cont_apur or 0.0) + (v_acres or 0.0) - (v_reduc or 0.0) - v_difer + v_difer_ant
            if not _eq(v_cont_per, esperado):
                erros.append(
                    "Consistência: VL_CONT_PER deve ser igual a (VL_CONT_APUR + VL_AJUS_ACRES - VL_AJUS_REDUC - VL_CONT_DIFER + VL_CONT_DIFER_ANT)."
                )

    else:
        campos.update(
            {
                "COD_CONT": _obter_campo(partes, 1),
                "VL_REC_BRT": _obter_campo(partes, 2),
                "VL_BC_CONT": _obter_campo(partes, 3),
                "VL_AJUS_ACRES_BC_COFINS": _obter_campo(partes, 4),
                "VL_AJUS_REDUC_BC_COFINS": _obter_campo(partes, 5),
                "VL_BC_CONT_AJUS": _obter_campo(partes, 6),
                "ALIQ_COFINS": _obter_campo(partes, 7),
                "QUANT_BC_COFINS": _obter_campo(partes, 8),
                "ALIQ_COFINS_QUANT": _obter_campo(partes, 9),
                "VL_CONT_APUR": _obter_campo(partes, 10),
                "VL_AJUS_ACRES": _obter_campo(partes, 11),
                "VL_AJUS_REDUC": _obter_campo(partes, 12),
                "VL_CONT_DIFER": _obter_campo(partes, 13),
                "VL_CONT_DIFER_ANT": _obter_campo(partes, 14),
                "VL_CONT_PER": _obter_campo(partes, 15),
            }
        )

        cod_cont = campos["COD_CONT"]
        if not cod_cont:
            erros.append("Campo COD_CONT obrigatório não informado.")
        elif len(cod_cont) != 2:
            erros.append("Campo COD_CONT inválido: esperado tamanho 2.")

        obrig = [
            "VL_REC_BRT",
            "VL_BC_CONT",
            "VL_AJUS_ACRES_BC_COFINS",
            "VL_AJUS_REDUC_BC_COFINS",
            "VL_BC_CONT_AJUS",
            "VL_CONT_APUR",
            "VL_AJUS_ACRES",
            "VL_AJUS_REDUC",
            "VL_CONT_PER",
        ]
        opc = ["ALIQ_COFINS", "QUANT_BC_COFINS", "ALIQ_COFINS_QUANT", "VL_CONT_DIFER", "VL_CONT_DIFER_ANT"]

        for nome in obrig:
            v = campos[nome]
            ok, num = _parse_num(v)
            if not v:
                erros.append(f"Campo {nome} obrigatório não informado.")
            elif not ok or num is None:
                erros.append(f"Campo {nome} inválido: esperado numérico.")
            nums[nome] = num

        for nome in opc:
            v = campos[nome]
            ok, num = _parse_num(v)
            if v and (not ok):
                erros.append(f"Campo {nome} inválido: esperado numérico.")
            nums[nome] = num

        v_bc = nums.get("VL_BC_CONT")
        v_acres_bc = nums.get("VL_AJUS_ACRES_BC_COFINS")
        v_reduc_bc = nums.get("VL_AJUS_REDUC_BC_COFINS")
        v_bc_ajus = nums.get("VL_BC_CONT_AJUS")
        if None not in (v_bc, v_acres_bc, v_reduc_bc, v_bc_ajus):
            esperado = (v_bc or 0.0) + (v_acres_bc or 0.0) - (v_reduc_bc or 0.0)
            if not _eq(v_bc_ajus, esperado):
                erros.append(
                    "Consistência: VL_BC_CONT_AJUS deve ser igual a (VL_BC_CONT + VL_AJUS_ACRES_BC_COFINS - VL_AJUS_REDUC_BC_COFINS)."
                )

        v_cont_per = nums.get("VL_CONT_PER")
        v_cont_apur = nums.get("VL_CONT_APUR")
        v_acres = nums.get("VL_AJUS_ACRES")
        v_reduc = nums.get("VL_AJUS_REDUC")
        v_difer = nums.get("VL_CONT_DIFER") or 0.0
        v_difer_ant = nums.get("VL_CONT_DIFER_ANT") or 0.0
        if None not in (v_cont_per, v_cont_apur, v_acres, v_reduc):
            esperado = (v_cont_apur or 0.0) + (v_acres or 0.0) - (v_reduc or 0.0) - v_difer + v_difer_ant
            if not _eq(v_cont_per, esperado):
                erros.append(
                    "Consistência: VL_CONT_PER deve ser igual a (VL_CONT_APUR + VL_AJUS_ACRES - VL_AJUS_REDUC - VL_CONT_DIFER + VL_CONT_DIFER_ANT)."
                )

    return {
        "ok": len(erros) == 0,
        "erros": erros,
        "campos": campos,
        "contexto": {"layout": layout, "numeros": nums},
    }


def validar_m610(linhas: Union[str, List[str], None]) -> str:
    """
    Wrapper que retorna JSON (array) e valida cada linha M610 encontrada.
    """
    linhas_para_processar = _normalizar_linhas(linhas)
    resultados: List[Dict[str, Any]] = []

    for linha in linhas_para_processar:
        if _extrair_reg(linha) != "M610":
            continue
        resultados.append(validar_registro_m610(linha))

    return json.dumps(resultados, ensure_ascii=False, indent=2)