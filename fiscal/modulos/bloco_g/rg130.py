import json

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


def _processar_linha_g130(linha):
    """
    Processa uma única linha do registro G130 e retorna um dicionário.

    Formato:
      |G130|IND_EMIT|COD_PART|COD_MOD|SERIE|NUM_DOC|CHV_NFE_CTE|DT_DOC|NUM_DA|

    Regras (manual 3.1.8):
    - REG deve ser "G130"
    - IND_EMIT: obrigatório, valores válidos ["0", "1"]
    - COD_PART: obrigatório, até 60 caracteres
    - COD_MOD: obrigatório, valores válidos ["01", "1B", "04", "07", "08", "8B", "09", "10", "26", "27", "55", "57"]
    - SERIE: opcional condicional, até 3 caracteres
    - NUM_DOC: obrigatório, numérico até 9 dígitos, > 0
    - CHV_NFE_CTE: opcional condicional, 44 dígitos (chave eletrônica)
      - Quando COD_MOD = "55" ou "57", deve validar a chave eletrônica e consistência
    - DT_DOC: obrigatório, formato ddmmaaaa
    - NUM_DA: opcional condicional

    Args:
        linha: linha SPED

    Returns:
        dict ou None
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
    if reg != "G130":
        return None

    def obter_campo(indice):
        if indice < len(partes):
            valor = partes[indice].strip()
            if valor == "-":
                return ""
            return valor if valor else ""
        return ""

    ind_emit = obter_campo(1)
    cod_part = obter_campo(2)
    cod_mod = obter_campo(3)
    serie = obter_campo(4)
    num_doc = obter_campo(5)
    chv_nfe_cte = obter_campo(6)
    dt_doc = obter_campo(7)
    num_da = obter_campo(8)

    # IND_EMIT: obrigatório, valores válidos ["0", "1"]
    if not ind_emit or ind_emit not in ["0", "1"]:
        return None

    # COD_PART: obrigatório, até 60 caracteres
    if not cod_part or len(cod_part) > 60:
        return None

    # COD_MOD: obrigatório, valores válidos
    cod_mod_validos = ["01", "1B", "04", "07", "08", "8B", "09", "10", "26", "27", "55", "57"]
    if not cod_mod or cod_mod not in cod_mod_validos:
        return None

    # SERIE: opcional condicional, até 3 caracteres
    if serie and len(serie) > 3:
        return None

    # NUM_DOC: obrigatório, numérico até 9 dígitos, > 0
    if not num_doc or not num_doc.isdigit() or len(num_doc) > 9 or int(num_doc) <= 0:
        return None

    # CHV_NFE_CTE: opcional condicional, 44 dígitos
    # Quando COD_MOD = "55" (NF-e) ou "57" (CT-e), deve validar a chave eletrônica
    if chv_nfe_cte:
        if len(chv_nfe_cte) != 44 or not chv_nfe_cte.isdigit():
            return None

        # Validação do dígito verificador para documentos eletrônicos
        if cod_mod in ["55", "57"]:
            if not _validar_chave_doc_eletronico(chv_nfe_cte):
                return None

            # Extrai informações da chave
            infos = _extrair_infos_chave_44(chv_nfe_cte)
            if not infos:
                return None

            # Valida consistência do modelo
            if infos["COD_MOD"] != cod_mod:
                return None

            # Valida consistência de NUM_DOC
            if int(infos["NUM_DOC"]) != int(num_doc):
                return None

            # Valida consistência de SERIE quando preenchido
            if serie:
                if not serie.isdigit():
                    return None
                serie_norm = serie.zfill(3)
                if serie_norm != infos["SER"]:
                    return None

    # DT_DOC: obrigatório, ddmmaaaa
    dt_ok, dt_obj = _validar_data(dt_doc)
    if not dt_ok:
        return None

    # NUM_DA: opcional condicional (sem validação específica de tamanho no manual)

    def fmt_data(d):
        return d.strftime("%d/%m/%Y") if d else ""

    descricoes_ind_emit = {
        "0": "Emissão própria",
        "1": "Terceiros",
    }

    descricoes_cod_mod = {
        "01": "Nota Fiscal",
        "1B": "Nota Fiscal Avulsa",
        "04": "Nota Fiscal de Produtor",
        "07": "Nota Fiscal de Serviço de Transporte",
        "08": "Conhecimento de Transporte Rodoviário de Cargas",
        "8B": "Conhecimento de Transporte de Cargas Avulso",
        "09": "Conhecimento de Transporte Aquaviário de Cargas",
        "10": "Conhecimento Aéreo",
        "26": "Conhecimento de Transporte Multimodal de Cargas",
        "27": "Nota Fiscal de Transporte Ferroviário de Cargas",
        "55": "Nota Fiscal Eletrônica",
        "57": "Conhecimento de Transporte Eletrônico",
    }

    return {
        "REG": {"titulo": "Registro", "valor": reg},
        "IND_EMIT": {
            "titulo": "Indicador do emitente do documento fiscal",
            "valor": ind_emit,
            "descricao": descricoes_ind_emit.get(ind_emit, ""),
        },
        "COD_PART": {
            "titulo": "Código do participante: do emitente do documento ou do remetente das mercadorias, no caso de entradas; do adquirente, no caso de saídas",
            "valor": cod_part,
        },
        "COD_MOD": {
            "titulo": "Código do modelo de documento fiscal, conforme tabela 4.1.1",
            "valor": cod_mod,
            "descricao": descricoes_cod_mod.get(cod_mod, ""),
        },
        "SERIE": {"titulo": "Série do documento fiscal", "valor": serie if serie else ""},
        "NUM_DOC": {"titulo": "Número de documento fiscal", "valor": num_doc},
        "CHV_NFE_CTE": {
            "titulo": "Chave do documento fiscal eletrônico",
            "valor": chv_nfe_cte if chv_nfe_cte else "",
        },
        "DT_DOC": {
            "titulo": "Data da emissão do documento fiscal",
            "valor": dt_doc,
            "valor_formatado": fmt_data(dt_obj),
        },
        "NUM_DA": {
            "titulo": "Número do documento de arrecadação estadual, se houver",
            "valor": num_da if num_da else "",
        },
    }


def validar_g130(linhas):
    """
    Valida uma ou mais linhas do registro G130 do SPED EFD Fiscal.

    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |G130|IND_EMIT|COD_PART|COD_MOD|SERIE|NUM_DOC|CHV_NFE_CTE|DT_DOC|NUM_DA|

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
        r = _processar_linha_g130(l)
        if r is not None:
            resultados.append(r)

    return json.dumps(resultados, ensure_ascii=False, indent=2)
