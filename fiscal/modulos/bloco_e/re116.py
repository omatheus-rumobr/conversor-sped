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


def _validar_periodo_mmaaaa(periodo_str):
    """
    Valida se o período está no formato mmaaaa e se é válido.
    """
    if not periodo_str or len(periodo_str) != 6 or not periodo_str.isdigit():
        return False, None
    try:
        mes = int(periodo_str[:2])
        ano = int(periodo_str[2:6])
        if mes < 1 or mes > 12:
            return False, None
        if ano < 1900 or ano > 2100:
            return False, None
        return True, {"mes": mes, "ano": ano}
    except ValueError:
        return False, None


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


def _processar_linha_e116(linha):
    """
    Processa uma única linha do registro E116 e retorna um dicionário.

    Formato:
      |E116|COD_OR|VL_OR|DT_VCTO|COD_REC|NUM_PROC|IND_PROC|PROC|TXT_COMPL|MES_REF|
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
    if reg != "E116":
        return None

    def obter_campo(indice):
        if indice < len(partes):
            valor = partes[indice].strip()
            if valor == "-":
                return ""
            return valor if valor else ""
        return ""

    cod_or = obter_campo(1)
    vl_or = obter_campo(2)
    dt_vcto = obter_campo(3)
    cod_rec = obter_campo(4)
    num_proc = obter_campo(5)
    ind_proc = obter_campo(6)
    proc = obter_campo(7)
    txt_compl = obter_campo(8)
    mes_ref = obter_campo(9)

    # COD_OR: obrigatório, valores válidos [000, 003, 004, 005, 006, 090]
    cod_or_validos = ["000", "003", "004", "005", "006", "090"]
    if cod_or not in cod_or_validos:
        return None

    # VL_OR: obrigatório, numérico com 2 decimais, não negativo
    vl_ok, vl_float, _ = validar_valor_numerico(vl_or, decimais=2, obrigatorio=True, nao_negativo=True)
    if not vl_ok:
        return None

    # DT_VCTO: obrigatório, ddmmaaaa, data válida
    dt_ok, dt_obj = _validar_data(dt_vcto)
    if not dt_ok:
        return None

    # COD_REC: obrigatório (sem tamanho fixo no manual)
    if not cod_rec:
        return None

    # NUM_PROC: opcional, até 60
    if num_proc and len(num_proc) > 60:
        return None

    # IND_PROC: opcional, valores válidos [0,1,2,9]
    if ind_proc and ind_proc not in ["0", "1", "2", "9"]:
        return None

    # PROC: opcional
    if proc and not proc.strip():
        return None

    # Regra: se NUM_PROC preenchido, IND_PROC e PROC também devem estar preenchidos
    if num_proc:
        if not ind_proc or not proc:
            return None

    # TXT_COMPL: opcional
    if txt_compl and not txt_compl.strip():
        return None

    # MES_REF: obrigatório, mmaaaa
    mes_ok, mes_dict = _validar_periodo_mmaaaa(mes_ref)
    if not mes_ok:
        return None

    def fmt_moeda(v):
        return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def fmt_data(d):
        return d.strftime("%d/%m/%Y") if d else ""

    def fmt_mes_ref(m):
        if not m:
            return ""
        return f"{m['mes']:02d}/{m['ano']}"

    desc_ind_proc = {
        "0": "SEFAZ",
        "1": "Justiça Federal",
        "2": "Justiça Estadual",
        "9": "Outros",
    }.get(ind_proc, "") if ind_proc else ""

    return {
        "REG": {"titulo": "Registro", "valor": reg},
        "COD_OR": {"titulo": "Código da obrigação a recolher, conforme a Tabela 5.4", "valor": cod_or},
        "VL_OR": {"titulo": "Valor da obrigação a recolher", "valor": vl_or, "valor_formatado": fmt_moeda(vl_float)},
        "DT_VCTO": {"titulo": "Data de vencimento da obrigação", "valor": dt_vcto, "valor_formatado": fmt_data(dt_obj)},
        "COD_REC": {"titulo": "Código de receita referente à obrigação (UF), conforme legislação estadual", "valor": cod_rec},
        "NUM_PROC": {"titulo": "Número do processo ou auto de infração ao qual a obrigação está vinculada, se houver", "valor": num_proc if num_proc else ""},
        "IND_PROC": {"titulo": "Indicador da origem do processo", "valor": ind_proc if ind_proc else "", "descricao": desc_ind_proc},
        "PROC": {"titulo": "Descrição resumida do processo que embasou o lançamento", "valor": proc if proc else ""},
        "TXT_COMPL": {"titulo": "Descrição complementar das obrigações a recolher", "valor": txt_compl if txt_compl else ""},
        "MES_REF": {"titulo": "Mês de referência (MMAAAA)", "valor": mes_ref, "valor_formatado": fmt_mes_ref(mes_dict)},
    }


def validar_e116_fiscal(linhas):
    """
    Valida uma ou mais linhas do registro E116 do SPED EFD Fiscal.
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
        r = _processar_linha_e116(l)
        if r is not None:
            resultados.append(r)

    return json.dumps(resultados, ensure_ascii=False, indent=2)