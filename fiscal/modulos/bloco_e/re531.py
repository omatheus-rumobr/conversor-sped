import json

import re
from datetime import datetime


def _validar_data(data_str):
    """
    Valida se a data está no formato ddmmaaaa e se é uma data válida.

    Returns:
        tuple: (True/False, datetime ou None)
    """
    if not data_str or len(data_str) != 8 or not data_str.isdigit():
        return False, None
    try:
        dia = int(data_str[:2])
        mes = int(data_str[2:4])
        ano = int(data_str[4:8])
        return True, datetime(ano, mes, dia)
    except ValueError:
        return False, None


def _validar_chave_doc_eletronico(chave):
    """
    Valida a chave do documento eletrônico (44 dígitos) e o dígito verificador (módulo 11).
    """
    if not chave or len(chave) != 44 or not chave.isdigit():
        return False

    chave_43 = chave[:43]
    dv_informado = int(chave[43])

    soma = 0
    multiplicador = 2
    for i in range(42, -1, -1):
        soma += int(chave_43[i]) * multiplicador
        multiplicador += 1
        if multiplicador > 9:
            multiplicador = 2

    resto = soma % 11
    dv_calculado = 0 if resto < 2 else 11 - resto
    return dv_calculado == dv_informado


def _extrair_infos_chave_44(chave):
    """
    Extrai informações da chave 44 (layout padrão NF-e/CT-e/NFC-e/NFCom etc):
    - modelo (2 dígitos)
    - série (3 dígitos)
    - número do documento (9 dígitos)
    """
    if not chave or len(chave) != 44 or not chave.isdigit():
        return None

    # 2 (cUF) + 4 (AAMM) + 14 (CNPJ) = 20
    cod_mod = chave[20:22]
    serie = chave[22:25]
    num_doc = chave[25:34]
    return {"COD_MOD": cod_mod, "SER": serie, "NUM_DOC": num_doc}


def validar_valor_numerico(valor_str, decimais=2, obrigatorio=False, positivo=False, nao_negativo=False):
    """
    Valida um valor numérico com precisão decimal específica.
    """
    if valor_str is None:
        valor_str = ""

    if not valor_str:
        if obrigatorio:
            return False, None, "Campo obrigatório não preenchido"
        return True, 0.0, None

    try:
        valor_float = float(valor_str)

        partes_decimal = valor_str.split(".")
        if len(partes_decimal) == 2 and len(partes_decimal[1]) > decimais:
            return False, None, f"Valor com mais de {decimais} casas decimais"

        if positivo and valor_float <= 0:
            return False, None, "Valor deve ser maior que zero"
        if nao_negativo and valor_float < 0:
            return False, None, "Valor não pode ser negativo"

        return True, valor_float, None
    except ValueError:
        return False, None, "Valor não é numérico válido"


def _processar_linha_e531(linha):
    """
    Processa uma única linha do registro E531 e retorna um dicionário.

    Formato:
      |E531|COD_PART|COD_MOD|SER|SUB|NUM_DOC|DT_DOC|COD_ITEM|VL_AJ_ITEM|CHV_NFE|
    """
    if not linha or not isinstance(linha, str):
        return None

    linha = linha.strip()
    if not linha:
        return None

    partes = linha.split("|")
    if partes and not partes[0]:
        partes = partes[1:]
    if partes and not partes[-1]:
        partes = partes[:-1]

    if len(partes) < 1:
        return None

    reg = partes[0].strip() if partes else ""
    if reg != "E531":
        return None

    def obter_campo(indice):
        if indice < len(partes):
            valor = partes[indice].strip()
            if valor == "-":
                return ""
            return valor if valor else ""
        return ""

    cod_part = obter_campo(1)
    cod_mod = obter_campo(2)
    ser = obter_campo(3)
    sub = obter_campo(4)
    num_doc = obter_campo(5)
    dt_doc = obter_campo(6)
    cod_item = obter_campo(7)
    vl_aj_item = obter_campo(8)
    chv_nfe = obter_campo(9)

    # COD_MOD: obrigatório, valores válidos ["01", "55"]
    if not cod_mod or cod_mod not in ["01", "55"]:
        return None

    # COD_PART: opcional condicional, até 60 caracteres
    if cod_part and len(cod_part) > 60:
        return None

    # SER: opcional condicional, até 4 caracteres
    # Para COD_MOD = "55" (NF-e), SER deve ter 3 posições (se não existir, informar "000")
    if cod_mod == "55":
        if not ser:
            ser = "000"
        elif len(ser) != 3:
            return None
    else:
        # Para COD_MOD = "01", SER é opcional mas se informado deve ter até 4 caracteres
        if ser and len(ser) > 4:
            return None

    # SUB: opcional condicional, numérico, até 3 dígitos
    if sub:
        if not sub.isdigit() or len(sub) > 3:
            return None

    # NUM_DOC: obrigatório, numérico, até 9 dígitos, > 0
    if not num_doc or not num_doc.isdigit() or len(num_doc) > 9 or int(num_doc) <= 0:
        return None

    # DT_DOC: obrigatório, ddmmaaaa
    dt_ok, dt_obj = _validar_data(dt_doc)
    if not dt_ok:
        return None

    # COD_ITEM: opcional condicional, até 60 caracteres
    if cod_item and len(cod_item) > 60:
        return None

    # VL_AJ_ITEM: obrigatório, numérico com 2 decimais, maior que zero (positivo)
    vl_ok, vl_float, _ = validar_valor_numerico(vl_aj_item, decimais=2, obrigatorio=True, positivo=True)
    if not vl_ok:
        return None

    # CHV_NFE: opcional condicional, 44 dígitos
    # Obrigatório quando COD_MOD = "55"
    if cod_mod == "55":
        if not chv_nfe or len(chv_nfe) != 44 or not chv_nfe.isdigit():
            return None

        # Validação do dígito verificador
        if not _validar_chave_doc_eletronico(chv_nfe):
            return None

        # Extrai informações da chave
        infos = _extrair_infos_chave_44(chv_nfe)
        if not infos:
            return None

        # Valida consistência do modelo
        if infos["COD_MOD"] != "55":
            return None

        # Valida consistência de NUM_DOC
        if int(infos["NUM_DOC"]) != int(num_doc):
            return None

        # Valida consistência de SER (deve ter 3 posições)
        ser_norm = ser.zfill(3) if ser else "000"
        if ser_norm != infos["SER"]:
            return None
    else:
        # Para COD_MOD = "01", CHV_NFE não deve ser informado
        if chv_nfe:
            return None

    def fmt_moeda(v):
        return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def fmt_data(d):
        return d.strftime("%d/%m/%Y") if d else ""

    return {
        "REG": {"titulo": "Registro", "valor": reg},
        "COD_PART": {
            "titulo": "Código do participante (campo 02 do Registro 0150)",
            "valor": cod_part if cod_part else "",
        },
        "COD_MOD": {
            "titulo": "Código do modelo do documento fiscal, conforme a Tabela 4.1.1",
            "valor": cod_mod,
            "descricao": "Nota Fiscal" if cod_mod == "01" else "Nota Fiscal Eletrônica" if cod_mod == "55" else "",
        },
        "SER": {"titulo": "Série do documento fiscal", "valor": ser if ser else ""},
        "SUB": {"titulo": "Subsérie do documento fiscal", "valor": sub if sub else ""},
        "NUM_DOC": {"titulo": "Número do documento fiscal", "valor": num_doc},
        "DT_DOC": {"titulo": "Data da emissão do documento fiscal", "valor": dt_doc, "valor_formatado": fmt_data(dt_obj)},
        "COD_ITEM": {"titulo": "Código do item (campo 02 do Registro 0200)", "valor": cod_item if cod_item else ""},
        "VL_AJ_ITEM": {"titulo": "Valor do ajuste para a operação/item", "valor": vl_aj_item, "valor_formatado": fmt_moeda(vl_float)},
        "CHV_NFE": {"titulo": "Chave da Nota Fiscal Eletrônica (modelo 55)", "valor": chv_nfe if chv_nfe else ""},
    }


def validar_e531_fiscal(linhas):
    """
    Valida uma ou mais linhas do registro E531 do SPED EFD Fiscal.

    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |E531|COD_PART|COD_MOD|SER|SUB|NUM_DOC|DT_DOC|COD_ITEM|VL_AJ_ITEM|CHV_NFE|

    Returns:
        String JSON com array de objetos contendo os campos validados.
        Retorna "[]" se nenhuma linha for válida.
    """
    if not linhas:
        return json.dumps([], ensure_ascii=False, indent=2)

    if isinstance(linhas, str):
        if "\n" in linhas:
            linhas_para_processar = [l.strip() for l in linhas.split("\n") if l.strip()]
        else:
            linhas_para_processar = [linhas.strip()] if linhas.strip() else []
    elif isinstance(linhas, list):
        linhas_para_processar = [l.strip() if isinstance(l, str) else str(l).strip() for l in linhas if l]
    else:
        linhas_para_processar = [str(linhas).strip()] if str(linhas).strip() else []

    resultados = []
    for l in linhas_para_processar:
        r = _processar_linha_e531(l)
        if r is not None:
            resultados.append(r)

    return json.dumps(resultados, ensure_ascii=False, indent=2)
