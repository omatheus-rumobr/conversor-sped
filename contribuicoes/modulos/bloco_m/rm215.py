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


def validar_registro_m215(
    linha_m215: str,
    *,
    dispensado_ecd: bool = False,
    exigir_cod_cta_a_partir_de: Optional[str] = "01112017",
) -> Dict[str, Any]:
    """
    Valida regras do Registro M215 (Bloco M, EFD-Contribuições 1.35) conforme trecho do manual.

    Campos/validações implementadas (do trecho em `documentacao_blocos/1.35/bloco_M.md:604-642`):
    - REG: obrigatório, valor fixo "M215"
    - IND_AJ_BC: obrigatório, valores válidos ["0", "1"]
    - VL_AJ_BC: obrigatório, numérico
    - COD_AJ_BC: obrigatório, tamanho 2
    - NUM_DOC: opcional
    - DESCR_AJ_BC: opcional
    - DT_REF: opcional, formato ddmmaaaa, data válida
    - COD_CTA: opcional (tamanho máx. 255)
      Observação do manual: a partir de nov/2017 passa a ser obrigatório, exceto se dispensado da ECD.
    - CNPJ: obrigatório, 14 dígitos numéricos
    - INFO_COMPL: opcional
    """
    erros: List[str] = []

    if not linha_m215 or not isinstance(linha_m215, str):
        return {"ok": False, "erros": ["Linha do registro M215 inválida/vazia."], "campos": {}, "contexto": {}}

    partes = _split_sped(linha_m215)
    reg = _obter_campo(partes, 0)
    ind_aj_bc = _obter_campo(partes, 1)
    vl_aj_bc = _obter_campo(partes, 2)
    cod_aj_bc = _obter_campo(partes, 3)
    num_doc = _obter_campo(partes, 4)
    descr_aj_bc = _obter_campo(partes, 5)
    dt_ref = _obter_campo(partes, 6)
    cod_cta = _obter_campo(partes, 7)
    cnpj = _obter_campo(partes, 8)
    info_compl = _obter_campo(partes, 9)

    if reg != "M215":
        erros.append("Campo REG inválido: esperado 'M215'.")

    if ind_aj_bc not in {"0", "1"}:
        erros.append("Campo IND_AJ_BC inválido: valores válidos são '0' ou '1'.")

    ok_num, num_vl_aj_bc = _parse_num(vl_aj_bc)
    if not vl_aj_bc:
        erros.append("Campo VL_AJ_BC obrigatório não informado.")
    elif not ok_num or num_vl_aj_bc is None:
        erros.append("Campo VL_AJ_BC inválido: esperado numérico.")

    if not cod_aj_bc:
        erros.append("Campo COD_AJ_BC obrigatório não informado.")
    elif len(cod_aj_bc) != 2:
        erros.append("Campo COD_AJ_BC inválido: esperado tamanho 2.")

    ok_dt, dt_obj = _validar_data_ddmmaaaa(dt_ref)
    if dt_ref and not ok_dt:
        erros.append("Campo DT_REF inválido: esperado formato ddmmaaaa e data válida.")

    if cod_cta and len(cod_cta) > 255:
        erros.append("Campo COD_CTA inválido: tamanho máximo 255.")

    if not cnpj:
        erros.append("Campo CNPJ obrigatório não informado.")
    elif (not cnpj.isdigit()) or len(cnpj) != 14:
        erros.append("Campo CNPJ inválido: esperado numérico com 14 dígitos.")

    # Regra opcional do manual a partir de nov/2017
    dt_corte_obj: Optional[datetime] = None
    if exigir_cod_cta_a_partir_de:
        ok_corte, dt_corte_obj = _validar_data_ddmmaaaa(exigir_cod_cta_a_partir_de)
        if not ok_corte:
            dt_corte_obj = None

    # Usa DT_REF como referência temporal (quando informado).
    if dt_obj and dt_corte_obj and dt_obj >= dt_corte_obj and (not dispensado_ecd) and not cod_cta:
        erros.append("A partir de 11/2017: COD_CTA é obrigatório (exceto se dispensado de ECD).")

    return {
        "ok": len(erros) == 0,
        "erros": erros,
        "campos": {
            "REG": reg,
            "IND_AJ_BC": ind_aj_bc,
            "VL_AJ_BC": vl_aj_bc,
            "COD_AJ_BC": cod_aj_bc,
            "NUM_DOC": num_doc,
            "DESCR_AJ_BC": descr_aj_bc,
            "DT_REF": dt_ref,
            "COD_CTA": cod_cta,
            "CNPJ": cnpj,
            "INFO_COMPL": info_compl,
        },
        "contexto": {
            "numeros": {"VL_AJ_BC": num_vl_aj_bc},
            "datas": {"DT_REF": dt_obj.strftime("%d/%m/%Y") if dt_obj else ""},
            "dispensado_ecd": dispensado_ecd,
            "exigir_cod_cta_a_partir_de": exigir_cod_cta_a_partir_de or "",
        },
    }


def validar_m215(
    linhas: Union[str, List[str], None],
    *,
    dispensado_ecd: bool = False,
    exigir_cod_cta_a_partir_de: Optional[str] = "01112017",
) -> str:
    """
    Wrapper que retorna JSON (array) e valida cada linha M215 encontrada.
    """
    linhas_para_processar = _normalizar_linhas(linhas)
    resultados: List[Dict[str, Any]] = []

    for linha in linhas_para_processar:
        if _extrair_reg(linha) != "M215":
            continue
        resultados.append(
            validar_registro_m215(
                linha,
                dispensado_ecd=dispensado_ecd,
                exigir_cod_cta_a_partir_de=exigir_cod_cta_a_partir_de,
            )
        )

    return json.dumps(resultados, ensure_ascii=False, indent=2)