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


def validar_registro_m620(linha_m620: str) -> Dict[str, Any]:
    """
    Valida regras do Registro M620 (Bloco M, EFD-Contribuições 1.35) conforme trecho do manual.

    Campos/validações implementadas (do trecho em `documentacao_blocos/1.35/bloco_M.md:1478-1503`):
    - REG: obrigatório, valor fixo "M620"
    - IND_AJ: obrigatório, valores válidos ["0", "1"]
    - VL_AJ: obrigatório, numérico
    - COD_AJ: obrigatório, tamanho 2
    - NUM_DOC: opcional
    - DESCR_AJ: opcional
    - DT_REF: opcional, formato ddmmaaaa, data válida
    """
    erros: List[str] = []

    if not linha_m620 or not isinstance(linha_m620, str):
        return {"ok": False, "erros": ["Linha do registro M620 inválida/vazia."], "campos": {}, "contexto": {}}

    partes = _split_sped(linha_m620)
    reg = _obter_campo(partes, 0)
    ind_aj = _obter_campo(partes, 1)
    vl_aj = _obter_campo(partes, 2)
    cod_aj = _obter_campo(partes, 3)
    num_doc = _obter_campo(partes, 4)
    descr_aj = _obter_campo(partes, 5)
    dt_ref = _obter_campo(partes, 6)

    if reg != "M620":
        erros.append("Campo REG inválido: esperado 'M620'.")

    if ind_aj not in {"0", "1"}:
        erros.append("Campo IND_AJ inválido: valores válidos são '0' ou '1'.")

    ok_num, num_vl_aj = _parse_num(vl_aj)
    if not vl_aj:
        erros.append("Campo VL_AJ obrigatório não informado.")
    elif not ok_num or num_vl_aj is None:
        erros.append("Campo VL_AJ inválido: esperado numérico.")

    if not cod_aj:
        erros.append("Campo COD_AJ obrigatório não informado.")
    elif len(cod_aj) != 2:
        erros.append("Campo COD_AJ inválido: esperado tamanho 2.")

    ok_dt, dt_obj = _validar_data_ddmmaaaa(dt_ref)
    if dt_ref and not ok_dt:
        erros.append("Campo DT_REF inválido: esperado formato ddmmaaaa e data válida.")

    return {
        "ok": len(erros) == 0,
        "erros": erros,
        "campos": {
            "REG": reg,
            "IND_AJ": ind_aj,
            "VL_AJ": vl_aj,
            "COD_AJ": cod_aj,
            "NUM_DOC": num_doc,
            "DESCR_AJ": descr_aj,
            "DT_REF": dt_ref,
        },
        "contexto": {
            "numeros": {"VL_AJ": num_vl_aj},
            "datas": {"DT_REF": dt_obj.strftime("%d/%m/%Y") if dt_obj else ""},
        },
    }


def validar_m620(linhas: Union[str, List[str], None]) -> str:
    """
    Wrapper que retorna JSON (array) e valida cada linha M620 encontrada.
    """
    linhas_para_processar = _normalizar_linhas(linhas)
    resultados: List[Dict[str, Any]] = []

    for linha in linhas_para_processar:
        if _extrair_reg(linha) != "M620":
            continue
        resultados.append(validar_registro_m620(linha))

    return json.dumps(resultados, ensure_ascii=False, indent=2)