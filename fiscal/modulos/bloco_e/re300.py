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


def _validar_uf(uf):
    """
    Valida se a UF é uma sigla válida do Brasil (27 UFs).
    """
    if not uf or not isinstance(uf, str):
        return False
    ufs_validas = [
        "AC",
        "AL",
        "AP",
        "AM",
        "BA",
        "CE",
        "DF",
        "ES",
        "GO",
        "MA",
        "MT",
        "MS",
        "MG",
        "PA",
        "PB",
        "PR",
        "PE",
        "PI",
        "RJ",
        "RN",
        "RS",
        "RO",
        "RR",
        "SC",
        "SP",
        "SE",
        "TO",
    ]
    return uf.strip().upper() in ufs_validas


def _processar_linha_e300(linha, dt_ini_0000=None, dt_fin_0000=None):
    """
    Processa uma única linha do registro E300 e retorna um dicionário.

    Formato:
      |E300|UF|DT_INI|DT_FIN|

    Regras (manual 3.1.8):
    - REG deve ser "E300"
    - UF deve existir na tabela de UF
    - DT_INI e DT_FIN devem estar entre DT_INI/DT_FIN do registro 0000 (quando informados)
    - DT_INI deve ser <= DT_FIN

    Args:
        linha: linha SPED
        dt_ini_0000: data ddmmaaaa do 0000 (opcional, para validação do intervalo)
        dt_fin_0000: data ddmmaaaa do 0000 (opcional, para validação do intervalo)

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
    if reg != "E300":
        return None

    def obter_campo(indice):
        if indice < len(partes):
            valor = partes[indice].strip()
            if valor == "-":
                return ""
            return valor if valor else ""
        return ""

    uf = obter_campo(1)
    dt_ini = obter_campo(2)
    dt_fin = obter_campo(3)

    # UF: obrigatório, 2 caracteres, deve ser válida
    if not uf or len(uf.strip()) != 2 or not _validar_uf(uf):
        return None
    uf = uf.strip().upper()

    # DT_INI: obrigatório, ddmmaaaa, data válida
    dt_ini_ok, dt_ini_obj = _validar_data(dt_ini)
    if not dt_ini_ok:
        return None

    # DT_FIN: obrigatório, ddmmaaaa, data válida
    dt_fin_ok, dt_fin_obj = _validar_data(dt_fin)
    if not dt_fin_ok:
        return None

    # DT_INI <= DT_FIN (regra do manual)
    if dt_ini_obj and dt_fin_obj and dt_ini_obj > dt_fin_obj:
        return None

    # Validação contra período do 0000 (quando informado)
    if dt_ini_0000:
        ok_0000_ini, dt_ini_0000_obj = _validar_data(dt_ini_0000)
        if not ok_0000_ini:
            return None
        if dt_ini_obj < dt_ini_0000_obj:
            return None
    if dt_fin_0000:
        ok_0000_fin, dt_fin_0000_obj = _validar_data(dt_fin_0000)
        if not ok_0000_fin:
            return None
        if dt_ini_obj > dt_fin_0000_obj:
            return None
        if dt_fin_obj > dt_fin_0000_obj:
            return None

    # Quando ambos informados, garante que período do E300 está contido no 0000
    if dt_ini_0000 and dt_fin_0000:
        ok_0000_ini, dt_ini_0000_obj = _validar_data(dt_ini_0000)
        ok_0000_fin, dt_fin_0000_obj = _validar_data(dt_fin_0000)
        if not ok_0000_ini or not ok_0000_fin:
            return None
        if dt_ini_obj < dt_ini_0000_obj or dt_fin_obj > dt_fin_0000_obj:
            return None

    def fmt_data(d):
        return d.strftime("%d/%m/%Y") if d else ""

    return {
        "REG": {"titulo": "Registro", "valor": reg},
        "UF": {"titulo": "Sigla da unidade da federação a que se refere à apuração do FCP e do ICMS Diferencial de Alíquota da UF de Origem/Destino", "valor": uf},
        "DT_INI": {
            "titulo": "Data inicial a que a apuração se refere (ddmmaaaa)",
            "valor": dt_ini,
            "valor_formatado": fmt_data(dt_ini_obj),
        },
        "DT_FIN": {
            "titulo": "Data final a que a apuração se refere (ddmmaaaa)",
            "valor": dt_fin,
            "valor_formatado": fmt_data(dt_fin_obj),
        },
    }


def validar_e300(linhas, dt_ini_0000=None, dt_fin_0000=None):
    """
    Valida uma ou mais linhas do registro E300 do SPED EFD Fiscal.

    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |E300|UF|DT_INI|DT_FIN|
        dt_ini_0000: DT_INI do registro 0000 (ddmmaaaa) para validação do intervalo (opcional)
        dt_fin_0000: DT_FIN do registro 0000 (ddmmaaaa) para validação do intervalo (opcional)

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
        r = _processar_linha_e300(l, dt_ini_0000=dt_ini_0000, dt_fin_0000=dt_fin_0000)
        if r is not None:
            resultados.append(r)

    return json.dumps(resultados, ensure_ascii=False, indent=2)
