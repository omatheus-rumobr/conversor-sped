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


def validar_registro_m230(linha_m230: str) -> Dict[str, Any]:
    """
    Valida regras do Registro M230 (Bloco M, EFD-Contribuições 1.35) conforme trecho do manual.

    Campos/validações implementadas (do trecho em `documentacao_blocos/1.35/bloco_M.md:702-729`):
    - REG: obrigatório, valor fixo "M230"
    - CNPJ: obrigatório, 14 dígitos numéricos
    - VL_VEND: obrigatório, numérico
    - VL_NAO_RECEB: obrigatório, numérico
    - VL_CONT_DIF: obrigatório, numérico
    - VL_CRED_DIF: opcional, se informado deve ser numérico
    - COD_CRED: opcional, se informado deve ter tamanho 3

    Regras de consistência locais:
    - Se informar VL_CRED_DIF, então COD_CRED deve ser informado (e vice-versa).
    """
    erros: List[str] = []

    if not linha_m230 or not isinstance(linha_m230, str):
        return {"ok": False, "erros": ["Linha do registro M230 inválida/vazia."], "campos": {}, "contexto": {}}

    partes = _split_sped(linha_m230)
    reg = _obter_campo(partes, 0)
    cnpj = _obter_campo(partes, 1)
    vl_vend = _obter_campo(partes, 2)
    vl_nao_receb = _obter_campo(partes, 3)
    vl_cont_dif = _obter_campo(partes, 4)
    vl_cred_dif = _obter_campo(partes, 5)
    cod_cred = _obter_campo(partes, 6)

    if reg != "M230":
        erros.append("Campo REG inválido: esperado 'M230'.")

    if not cnpj:
        erros.append("Campo CNPJ obrigatório não informado.")
    elif (not cnpj.isdigit()) or len(cnpj) != 14:
        erros.append("Campo CNPJ inválido: esperado numérico com 14 dígitos.")

    nums: Dict[str, Optional[float]] = {}

    for nome, valor in {
        "VL_VEND": vl_vend,
        "VL_NAO_RECEB": vl_nao_receb,
        "VL_CONT_DIF": vl_cont_dif,
    }.items():
        ok, num = _parse_num(valor)
        if not valor:
            erros.append(f"Campo {nome} obrigatório não informado.")
        elif not ok or num is None:
            erros.append(f"Campo {nome} inválido: esperado numérico.")
        nums[nome] = num

    ok, num_vl_cred_dif = _parse_num(vl_cred_dif)
    if vl_cred_dif and (not ok):
        erros.append("Campo VL_CRED_DIF inválido: esperado numérico.")
    nums["VL_CRED_DIF"] = num_vl_cred_dif

    if cod_cred and len(cod_cred) != 3:
        erros.append("Campo COD_CRED inválido: esperado tamanho 3.")

    if bool(vl_cred_dif) != bool(cod_cred):
        erros.append("Campos VL_CRED_DIF e COD_CRED devem ser informados em conjunto (ambos ou nenhum).")

    return {
        "ok": len(erros) == 0,
        "erros": erros,
        "campos": {
            "REG": reg,
            "CNPJ": cnpj,
            "VL_VEND": vl_vend,
            "VL_NAO_RECEB": vl_nao_receb,
            "VL_CONT_DIF": vl_cont_dif,
            "VL_CRED_DIF": vl_cred_dif,
            "COD_CRED": cod_cred,
        },
        "contexto": {"numeros": nums},
    }


def validar_m230(linhas: Union[str, List[str], None]) -> str:
    """
    Wrapper que retorna JSON (array) e valida cada linha M230 encontrada.
    """
    linhas_para_processar = _normalizar_linhas(linhas)
    resultados: List[Dict[str, Any]] = []

    for linha in linhas_para_processar:
        if _extrair_reg(linha) != "M230":
            continue
        resultados.append(validar_registro_m230(linha))

    return json.dumps(resultados, ensure_ascii=False, indent=2)