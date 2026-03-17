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


def validar_registro_m205(
    linha_m205: str,
    *,
    total_debito_para_o_campo: Optional[float] = None,
) -> Dict[str, Any]:
    """
    Valida regras do Registro M205 (Bloco M, EFD-Contribuições 1.35) conforme trecho do manual.

    Campos/validações implementadas (do trecho em `documentacao_blocos/1.35/bloco_M.md:321-347`):
    - REG: obrigatório, valor fixo "M205"
    - NUM_CAMPO: obrigatório, deve referenciar o campo do M200 detalhado (Campo 08 ou Campo 12)
      -> aceita "08" e "12" (também tolera "8" e "12", normalizando)
    - COD_REC: obrigatório, 6 dígitos
    - VL_DEBITO: obrigatório, numérico
    - Validação (opcional): se `total_debito_para_o_campo` for informado, VL_DEBITO deve ser <= esse total
      (a validação do somatório de vários M205 contra o M200 deve ser feita na camada que tem acesso a todas as linhas)
    """
    erros: List[str] = []

    if not linha_m205 or not isinstance(linha_m205, str):
        return {"ok": False, "erros": ["Linha do registro M205 inválida/vazia."], "campos": {}, "contexto": {}}

    partes = _split_sped(linha_m205)
    reg = _obter_campo(partes, 0)
    num_campo = _obter_campo(partes, 1)
    cod_rec = _obter_campo(partes, 2)
    vl_debito = _obter_campo(partes, 3)

    if reg != "M205":
        erros.append("Campo REG inválido: esperado 'M205'.")

    # NUM_CAMPO: Campo 08 ou 12 do M200
    if not num_campo:
        erros.append("Campo NUM_CAMPO obrigatório não informado.")
    else:
        nc = num_campo.zfill(2) if num_campo.isdigit() else num_campo
        if nc not in {"08", "12"}:
            erros.append("Campo NUM_CAMPO inválido: valores esperados '08' (campo 08 do M200) ou '12' (campo 12 do M200).")
        num_campo = nc

    if not cod_rec:
        erros.append("Campo COD_REC obrigatório não informado.")
    elif not cod_rec.isdigit() or len(cod_rec) != 6:
        erros.append("Campo COD_REC inválido: esperado numérico com 6 dígitos.")

    ok_num, num_vl_debito = _parse_num(vl_debito)
    if not vl_debito:
        erros.append("Campo VL_DEBITO obrigatório não informado.")
    elif not ok_num or num_vl_debito is None:
        erros.append("Campo VL_DEBITO inválido: esperado numérico.")

    if total_debito_para_o_campo is not None and num_vl_debito is not None:
        if num_vl_debito - float(total_debito_para_o_campo) > 1e-6:
            erros.append("VL_DEBITO não pode ser maior que o total a recolher do campo detalhado no M200.")

    return {
        "ok": len(erros) == 0,
        "erros": erros,
        "campos": {
            "REG": reg,
            "NUM_CAMPO": num_campo,
            "COD_REC": cod_rec,
            "VL_DEBITO": vl_debito,
        },
        "contexto": {
            "numeros": {"VL_DEBITO": num_vl_debito},
            "total_debito_para_o_campo": total_debito_para_o_campo,
        },
    }


def validar_m205(
    linhas: Union[str, List[str], None],
    *,
    total_debito_para_o_campo: Optional[float] = None,
) -> str:
    """
    Wrapper que retorna JSON (array) e valida cada linha M205 encontrada.
    """
    linhas_para_processar = _normalizar_linhas(linhas)
    resultados: List[Dict[str, Any]] = []

    for linha in linhas_para_processar:
        if _extrair_reg(linha) != "M205":
            continue
        resultados.append(validar_registro_m205(linha, total_debito_para_o_campo=total_debito_para_o_campo))

    return json.dumps(resultados, ensure_ascii=False, indent=2)