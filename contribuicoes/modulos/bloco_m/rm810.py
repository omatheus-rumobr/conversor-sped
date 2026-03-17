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


def _validar_periodo_mmaaaa(valor: str) -> bool:
    if not valor or len(valor) != 6 or not valor.isdigit():
        return False
    mes = int(valor[:2])
    ano = int(valor[2:6])
    return 1 <= mes <= 12 and 1900 <= ano <= 3000


def validar_registro_m810(
    linha_m810: str,
    *,
    periodo_atual_mmaaaa: Optional[str] = None,
    dispensado_ecd: bool = False,
    exigir_cod_cta_a_partir_de: Optional[str] = "112017",
    vl_tot_rec_m800: Optional[float] = None,
) -> Dict[str, Any]:
    """
    Valida regras do Registro M810 (Bloco M, EFD-Contribuições 1.35) conforme trecho do manual.

    Campos/validações implementadas (do trecho em `documentacao_blocos/1.35/bloco_M.md:1635-1666`):
    - REG: obrigatório, valor fixo "M810"
    - NAT_REC: obrigatório, tamanho 3
    - VL_REC: obrigatório, numérico
    - COD_CTA: opcional (tamanho máx. 255)
      Observação do manual: a partir de nov/2017 passa a ser obrigatório, exceto se dispensado da ECD.
      Como o registro não possui data, esta regra é aplicada se `periodo_atual_mmaaaa` >= `exigir_cod_cta_a_partir_de`.
    - DESC_COMPL: opcional
    - Observação (validação cruzada): soma de VL_REC dos M810 deve corresponder ao VL_TOT_REC do M800.
      Aqui isso pode ser verificado na camada superior; opcionalmente, se `vl_tot_rec_m800` for informado,
      validamos apenas que o VL_REC individual não excede o total do M800.
    """
    erros: List[str] = []

    if not linha_m810 or not isinstance(linha_m810, str):
        return {"ok": False, "erros": ["Linha do registro M810 inválida/vazia."], "campos": {}, "contexto": {}}

    partes = _split_sped(linha_m810)
    reg = _obter_campo(partes, 0)
    nat_rec = _obter_campo(partes, 1)
    vl_rec = _obter_campo(partes, 2)
    cod_cta = _obter_campo(partes, 3)
    desc_compl = _obter_campo(partes, 4)

    if reg != "M810":
        erros.append("Campo REG inválido: esperado 'M810'.")

    if not nat_rec:
        erros.append("Campo NAT_REC obrigatório não informado.")
    elif len(nat_rec) != 3:
        erros.append("Campo NAT_REC inválido: esperado tamanho 3.")

    ok_num, num_vl_rec = _parse_num(vl_rec)
    if not vl_rec:
        erros.append("Campo VL_REC obrigatório não informado.")
    elif not ok_num or num_vl_rec is None:
        erros.append("Campo VL_REC inválido: esperado numérico.")

    if cod_cta and len(cod_cta) > 255:
        erros.append("Campo COD_CTA inválido: tamanho máximo 255.")

    exigir_cod_cta = False
    if exigir_cod_cta_a_partir_de and periodo_atual_mmaaaa and _validar_periodo_mmaaaa(periodo_atual_mmaaaa):
        if len(exigir_cod_cta_a_partir_de) == 6 and exigir_cod_cta_a_partir_de.isdigit():
            exigir_cod_cta = int(periodo_atual_mmaaaa) >= int(exigir_cod_cta_a_partir_de)

    if exigir_cod_cta and (not dispensado_ecd) and not cod_cta:
        erros.append("A partir de 11/2017: COD_CTA é obrigatório (exceto se dispensado de ECD).")

    if vl_tot_rec_m800 is not None and num_vl_rec is not None:
        if num_vl_rec - float(vl_tot_rec_m800) > 1e-6:
            erros.append("VL_REC não pode ser maior que o VL_TOT_REC do registro pai M800.")

    return {
        "ok": len(erros) == 0,
        "erros": erros,
        "campos": {
            "REG": reg,
            "NAT_REC": nat_rec,
            "VL_REC": vl_rec,
            "COD_CTA": cod_cta,
            "DESC_COMPL": desc_compl,
        },
        "contexto": {
            "numeros": {"VL_REC": num_vl_rec},
            "periodo_atual_mmaaaa": periodo_atual_mmaaaa or "",
            "dispensado_ecd": dispensado_ecd,
            "exigir_cod_cta_a_partir_de": exigir_cod_cta_a_partir_de or "",
            "vl_tot_rec_m800": vl_tot_rec_m800,
        },
    }


def validar_m810(
    linhas: Union[str, List[str], None],
    *,
    periodo_atual_mmaaaa: Optional[str] = None,
    dispensado_ecd: bool = False,
    exigir_cod_cta_a_partir_de: Optional[str] = "112017",
    vl_tot_rec_m800: Optional[float] = None,
) -> str:
    """
    Wrapper que retorna JSON (array) e valida cada linha M810 encontrada.
    """
    linhas_para_processar = _normalizar_linhas(linhas)
    resultados: List[Dict[str, Any]] = []

    for linha in linhas_para_processar:
        if _extrair_reg(linha) != "M810":
            continue
        resultados.append(
            validar_registro_m810(
                linha,
                periodo_atual_mmaaaa=periodo_atual_mmaaaa,
                dispensado_ecd=dispensado_ecd,
                exigir_cod_cta_a_partir_de=exigir_cod_cta_a_partir_de,
                vl_tot_rec_m800=vl_tot_rec_m800,
            )
        )

    return json.dumps(resultados, ensure_ascii=False, indent=2)