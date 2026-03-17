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


def _eq(a: float, b: float, tol: float = 1e-6) -> bool:
    return abs(a - b) <= tol


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


def _validar_periodo_mmaaaa(valor: str) -> bool:
    if not valor or len(valor) != 6 or not valor.isdigit():
        return False
    mes = int(valor[:2])
    ano = int(valor[2:6])
    return 1 <= mes <= 12 and 1900 <= ano <= 3000


def validar_registro_m700(
    linha_m700: str,
    *,
    periodo_atual_mmaaaa: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Valida regras do Registro M700 (Bloco M, EFD-Contribuições 1.35) conforme trecho do manual.

    Campos/validações implementadas (do trecho em `documentacao_blocos/1.35/bloco_M.md:1565-1593`):
    - REG: obrigatório, valor fixo "M700"
    - COD_CONT: obrigatório, tamanho 2
    - VL_CONT_APUR_DIFER: obrigatório, numérico
    - NAT_CRED_DESC: opcional, valores válidos ["01","02","03","04"] (se informado)
    - VL_CRED_DESC_DIFER: opcional, numérico (se informado)
    - VL_CONT_DIFER_ANT: obrigatório, numérico
      Consistência: VL_CONT_DIFER_ANT = VL_CONT_APUR_DIFER - VL_CRED_DESC_DIFER (se VL_CRED_DESC_DIFER informado)
    - PER_APUR: obrigatório, formato MMAAAA (6 dígitos)
      Preenchimento do manual: PER_APUR não pode ser o mesmo da escrituração atual (se `periodo_atual_mmaaaa` for informado)
    - DT_RECEB: opcional, ddmmaaaa (se informado, data válida)
      Validação do manual: deve estar compreendida no período da atual escrituração (se `periodo_atual_mmaaaa` for informado)
    """
    erros: List[str] = []

    if not linha_m700 or not isinstance(linha_m700, str):
        return {"ok": False, "erros": ["Linha do registro M700 inválida/vazia."], "campos": {}, "contexto": {}}

    partes = _split_sped(linha_m700)
    reg = _obter_campo(partes, 0)
    cod_cont = _obter_campo(partes, 1)
    vl_cont_apur_difer = _obter_campo(partes, 2)
    nat_cred_desc = _obter_campo(partes, 3)
    vl_cred_desc_difer = _obter_campo(partes, 4)
    vl_cont_difer_ant = _obter_campo(partes, 5)
    per_apur = _obter_campo(partes, 6)
    dt_receb = _obter_campo(partes, 7)

    if reg != "M700":
        erros.append("Campo REG inválido: esperado 'M700'.")

    if not cod_cont:
        erros.append("Campo COD_CONT obrigatório não informado.")
    elif len(cod_cont) != 2:
        erros.append("Campo COD_CONT inválido: esperado tamanho 2.")

    nums: Dict[str, Optional[float]] = {}

    ok, n_apur = _parse_num(vl_cont_apur_difer)
    if not vl_cont_apur_difer:
        erros.append("Campo VL_CONT_APUR_DIFER obrigatório não informado.")
    elif not ok or n_apur is None:
        erros.append("Campo VL_CONT_APUR_DIFER inválido: esperado numérico.")
    nums["VL_CONT_APUR_DIFER"] = n_apur

    if nat_cred_desc:
        if nat_cred_desc not in {"01", "02", "03", "04"}:
            erros.append("Campo NAT_CRED_DESC inválido: valores válidos são 01, 02, 03, 04.")

    ok, n_cred = _parse_num(vl_cred_desc_difer)
    if vl_cred_desc_difer and (not ok):
        erros.append("Campo VL_CRED_DESC_DIFER inválido: esperado numérico.")
    nums["VL_CRED_DESC_DIFER"] = n_cred

    ok, n_ant = _parse_num(vl_cont_difer_ant)
    if not vl_cont_difer_ant:
        erros.append("Campo VL_CONT_DIFER_ANT obrigatório não informado.")
    elif not ok or n_ant is None:
        erros.append("Campo VL_CONT_DIFER_ANT inválido: esperado numérico.")
    nums["VL_CONT_DIFER_ANT"] = n_ant

    if n_apur is not None and n_ant is not None:
        esperado = n_apur - (n_cred or 0.0)
        if not _eq(n_ant, esperado):
            erros.append("Consistência: VL_CONT_DIFER_ANT deve ser igual a (VL_CONT_APUR_DIFER - VL_CRED_DESC_DIFER).")

    if not per_apur:
        erros.append("Campo PER_APUR obrigatório não informado.")
    elif not _validar_periodo_mmaaaa(per_apur):
        erros.append("Campo PER_APUR inválido: esperado formato MMAAAA (6 dígitos).")
    else:
        if periodo_atual_mmaaaa and _validar_periodo_mmaaaa(periodo_atual_mmaaaa):
            if per_apur == periodo_atual_mmaaaa:
                erros.append("Campo PER_APUR inválido: não pode ser o mesmo período da escrituração atual.")

    ok_dt, dt_obj = _validar_data_ddmmaaaa(dt_receb)
    if dt_receb and (not ok_dt or dt_obj is None):
        erros.append("Campo DT_RECEB inválido: esperado formato ddmmaaaa e data válida.")
    else:
        if dt_obj and periodo_atual_mmaaaa and _validar_periodo_mmaaaa(periodo_atual_mmaaaa):
            mes = int(periodo_atual_mmaaaa[:2])
            ano = int(periodo_atual_mmaaaa[2:6])
            if dt_obj.month != mes or dt_obj.year != ano:
                erros.append("Validação: DT_RECEB deve estar compreendida no período da escrituração atual.")

    return {
        "ok": len(erros) == 0,
        "erros": erros,
        "campos": {
            "REG": reg,
            "COD_CONT": cod_cont,
            "VL_CONT_APUR_DIFER": vl_cont_apur_difer,
            "NAT_CRED_DESC": nat_cred_desc,
            "VL_CRED_DESC_DIFER": vl_cred_desc_difer,
            "VL_CONT_DIFER_ANT": vl_cont_difer_ant,
            "PER_APUR": per_apur,
            "DT_RECEB": dt_receb,
        },
        "contexto": {
            "numeros": nums,
            "datas": {"DT_RECEB": dt_obj.strftime("%d/%m/%Y") if dt_obj else ""},
            "periodo_atual_mmaaaa": periodo_atual_mmaaaa or "",
        },
    }


def validar_m700(
    linhas: Union[str, List[str], None],
    *,
    periodo_atual_mmaaaa: Optional[str] = None,
) -> str:
    """
    Wrapper que retorna JSON (array) e valida cada linha M700 encontrada.
    """
    linhas_para_processar = _normalizar_linhas(linhas)
    resultados: List[Dict[str, Any]] = []

    for linha in linhas_para_processar:
        if _extrair_reg(linha) != "M700":
            continue
        resultados.append(validar_registro_m700(linha, periodo_atual_mmaaaa=periodo_atual_mmaaaa))

    return json.dumps(resultados, ensure_ascii=False, indent=2)