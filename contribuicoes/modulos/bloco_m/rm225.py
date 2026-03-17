import json
from datetime import datetime
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


def _validar_data_ddmmaaaa(data_str: str) -> Tuple[bool, Optional[datetime]]:
    if not data_str:
        return True, None
    s = str(data_str).strip()
    if len(s) != 8 or not s.isdigit():
        return False, None
    try:
        dia = int(s[:2])
        mes = int(s[2:4])
        ano = int(s[4:8])
        return True, datetime(ano, mes, dia)
    except ValueError:
        return False, None


def validar_registro_m225(
    linha_m225: str,
    *,
    dispensado_ecd: bool = False,
    exigir_cod_cta_a_partir_de: Optional[str] = "01112017",
) -> Dict[str, Any]:
    """
    Valida regras do Registro M225 (Bloco M, EFD-Contribuições 1.35) conforme trecho do manual.

    Campos/validações implementadas (do trecho em `documentacao_blocos/1.35/bloco_M.md:669-701`):
    - REG: obrigatório, valor fixo "M225"
    - DET_VALOR_AJ: obrigatório, numérico
    - CST_PIS: opcional, se informado deve ser numérico com 2 dígitos
    - DET_BC_CRED: opcional, se informado deve ser numérico
    - DET_ALIQ: opcional, se informado deve ser numérico
    - DT_OPER_AJ: obrigatório, formato ddmmaaaa, data válida
    - DESC_AJ: opcional
    - COD_CTA: opcional (tamanho máx. 255)
      Observação do manual: a partir de nov/2017 passa a ser obrigatório, exceto se dispensado da ECD.
    - INFO_COMPL: opcional

    Args:
        dispensado_ecd: se True, não exige COD_CTA mesmo após a data de corte
        exigir_cod_cta_a_partir_de: ddmmaaaa da data de corte para exigir COD_CTA.
            Use None para desabilitar esta regra.
    """
    erros: List[str] = []

    if not linha_m225 or not isinstance(linha_m225, str):
        return {"ok": False, "erros": ["Linha do registro M225 inválida/vazia."], "campos": {}, "contexto": {}}

    partes = _split_sped(linha_m225)
    reg = _obter_campo(partes, 0)
    det_valor_aj = _obter_campo(partes, 1)
    cst_pis = _obter_campo(partes, 2)
    det_bc_cred = _obter_campo(partes, 3)
    det_aliq = _obter_campo(partes, 4)
    dt_oper_aj = _obter_campo(partes, 5)
    desc_aj = _obter_campo(partes, 6)
    cod_cta = _obter_campo(partes, 7)
    info_compl = _obter_campo(partes, 8)

    if reg != "M225":
        erros.append("Campo REG inválido: esperado 'M225'.")

    ok_num, num_det_valor_aj = _parse_num(det_valor_aj)
    if not det_valor_aj:
        erros.append("Campo DET_VALOR_AJ obrigatório não informado.")
    elif not ok_num or num_det_valor_aj is None:
        erros.append("Campo DET_VALOR_AJ inválido: esperado numérico.")

    if cst_pis:
        if not cst_pis.isdigit() or len(cst_pis) != 2:
            erros.append("Campo CST_PIS inválido: esperado numérico com 2 dígitos (ex.: '50', '56').")

    nums: Dict[str, Optional[float]] = {"DET_VALOR_AJ": num_det_valor_aj}
    for nome, valor in {"DET_BC_CRED": det_bc_cred, "DET_ALIQ": det_aliq}.items():
        ok, num = _parse_num(valor)
        if valor and not ok:
            erros.append(f"Campo {nome} inválido: esperado numérico.")
        nums[nome] = num

    ok_dt, dt_obj = _validar_data_ddmmaaaa(dt_oper_aj)
    if not dt_oper_aj:
        erros.append("Campo DT_OPER_AJ obrigatório não informado.")
    elif not ok_dt or dt_obj is None:
        erros.append("Campo DT_OPER_AJ inválido: esperado formato ddmmaaaa e data válida.")

    if cod_cta and len(cod_cta) > 255:
        erros.append("Campo COD_CTA inválido: tamanho máximo 255.")

    # Regra opcional do manual a partir de nov/2017
    dt_corte_obj: Optional[datetime] = None
    if exigir_cod_cta_a_partir_de:
        ok_corte, dt_corte_obj = _validar_data_ddmmaaaa(exigir_cod_cta_a_partir_de)
        if not ok_corte:
            dt_corte_obj = None

    if dt_obj and dt_corte_obj and dt_obj >= dt_corte_obj and (not dispensado_ecd) and not cod_cta:
        erros.append("A partir de 11/2017: COD_CTA é obrigatório (exceto se dispensado de ECD).")

    return {
        "ok": len(erros) == 0,
        "erros": erros,
        "campos": {
            "REG": reg,
            "DET_VALOR_AJ": det_valor_aj,
            "CST_PIS": cst_pis,
            "DET_BC_CRED": det_bc_cred,
            "DET_ALIQ": det_aliq,
            "DT_OPER_AJ": dt_oper_aj,
            "DESC_AJ": desc_aj,
            "COD_CTA": cod_cta,
            "INFO_COMPL": info_compl,
        },
        "contexto": {
            "numeros": nums,
            "datas": {"DT_OPER_AJ": dt_obj.strftime("%d/%m/%Y") if dt_obj else ""},
            "dispensado_ecd": dispensado_ecd,
            "exigir_cod_cta_a_partir_de": exigir_cod_cta_a_partir_de or "",
        },
    }


def validar_m225(
    linhas: Union[str, List[str], None],
    *,
    dispensado_ecd: bool = False,
    exigir_cod_cta_a_partir_de: Optional[str] = "01112017",
) -> str:
    """
    Wrapper que retorna JSON (array) e valida cada linha M225 encontrada.
    """
    linhas_para_processar = _normalizar_linhas(linhas)
    resultados: List[Dict[str, Any]] = []

    for linha in linhas_para_processar:
        if _extrair_reg(linha) != "M225":
            continue
        resultados.append(
            validar_registro_m225(
                linha,
                dispensado_ecd=dispensado_ecd,
                exigir_cod_cta_a_partir_de=exigir_cod_cta_a_partir_de,
            )
        )

    return json.dumps(resultados, ensure_ascii=False, indent=2)