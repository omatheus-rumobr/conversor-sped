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


def _processar_linha_k270(linha, dt_ini_0000=None):
    """
    Processa uma única linha do registro K270 e retorna um dicionário.

    Formato:
      |K270|DT_INI_AP|DT_FIN_AP|COD_OP_OS|COD_ITEM|QTD_COR_POS|QTD_COR_NEG|ORIGEM|

    Regras (manual 3.1.8):
    - REG deve ser "K270"
    - DT_INI_AP: opcional condicional, formato ddmmaaaa
      - Deve ser anterior à data inicial do período informado no Registro 0000 (quando informado)
      - Pode não ser preenchido em casos específicos relacionados a ordens em aberto (validação externa)
    - DT_FIN_AP: opcional condicional, formato ddmmaaaa
      - Deve ser anterior à data inicial do período informado no Registro 0000 (quando informado)
      - Se DT_INI_AP estiver preenchido, DT_FIN_AP deve ser >= DT_INI_AP
      - Pode não ser preenchido em casos específicos relacionados a ordens em aberto (validação externa)
    - COD_OP_OS: opcional condicional, até 30 caracteres
    - COD_ITEM: obrigatório, até 60 caracteres
      - Deve existir no registro 0200 (validação externa)
    - QTD_COR_POS: opcional condicional, numérico com 6 decimais, não negativo
    - QTD_COR_NEG: opcional condicional, numérico com 6 decimais, não negativo
      - Somente um dos campos QTD_COR_POS ou QTD_COR_NEG pode ser preenchido
    - ORIGEM: obrigatório, valores válidos ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

    Args:
        linha: linha SPED
        dt_ini_0000: data ddmmaaaa do DT_INI do registro 0000 (opcional, para validação)

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
    if reg != "K270":
        return None

    def obter_campo(indice):
        if indice < len(partes):
            valor = partes[indice].strip()
            if valor == "-":
                return ""
            return valor if valor else ""
        return ""

    dt_ini_ap = obter_campo(1)
    dt_fin_ap = obter_campo(2)
    cod_op_os = obter_campo(3)
    cod_item = obter_campo(4)
    qtd_cor_pos = obter_campo(5)
    qtd_cor_neg = obter_campo(6)
    origem = obter_campo(7)

    # ORIGEM: obrigatório, valores válidos
    origens_validas = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    if not origem or origem not in origens_validas:
        return None

    # DT_INI_AP: opcional condicional, ddmmaaaa, data válida
    dt_ini_ap_obj = None
    if dt_ini_ap:
        dt_ini_ap_ok, dt_ini_ap_obj = _validar_data(dt_ini_ap)
        if not dt_ini_ap_ok:
            return None

        # Validação: DT_INI_AP deve ser anterior à data inicial do período informado no Registro 0000
        if dt_ini_0000:
            ok_0000_ini, dt_ini_0000_obj = _validar_data(dt_ini_0000)
            if ok_0000_ini and dt_ini_ap_obj >= dt_ini_0000_obj:
                return None

    # DT_FIN_AP: opcional condicional, ddmmaaaa, data válida
    dt_fin_ap_obj = None
    if dt_fin_ap:
        dt_fin_ap_ok, dt_fin_ap_obj = _validar_data(dt_fin_ap)
        if not dt_fin_ap_ok:
            return None

        # Validação: DT_FIN_AP deve ser >= DT_INI_AP (quando DT_INI_AP estiver preenchido)
        if dt_ini_ap_obj and dt_fin_ap_obj < dt_ini_ap_obj:
            return None

        # Validação: DT_FIN_AP deve ser anterior à data inicial do período informado no Registro 0000
        if dt_ini_0000:
            ok_0000_ini, dt_ini_0000_obj = _validar_data(dt_ini_0000)
            if ok_0000_ini and dt_fin_ap_obj >= dt_ini_0000_obj:
                return None

    # COD_OP_OS: opcional condicional, até 30 caracteres
    if cod_op_os and len(cod_op_os) > 30:
        return None

    # COD_ITEM: obrigatório, até 60 caracteres
    if not cod_item or len(cod_item) > 60:
        return None

    # QTD_COR_POS: opcional condicional, numérico com 6 decimais, não negativo
    qtd_cor_pos_ok, qtd_cor_pos_float, _ = validar_valor_numerico(
        qtd_cor_pos, decimais=6, obrigatorio=False, nao_negativo=True
    )
    if not qtd_cor_pos_ok:
        return None

    # QTD_COR_NEG: opcional condicional, numérico com 6 decimais, não negativo
    qtd_cor_neg_ok, qtd_cor_neg_float, _ = validar_valor_numerico(
        qtd_cor_neg, decimais=6, obrigatorio=False, nao_negativo=True
    )
    if not qtd_cor_neg_ok:
        return None

    # Validação: somente um dos campos QTD_COR_POS ou QTD_COR_NEG pode ser preenchido
    tem_qtd_pos = qtd_cor_pos and qtd_cor_pos_float > 0
    tem_qtd_neg = qtd_cor_neg and qtd_cor_neg_float > 0
    if tem_qtd_pos and tem_qtd_neg:
        return None

    def fmt_quantidade(v):
        return f"{v:,.6f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def fmt_data(d):
        return d.strftime("%d/%m/%Y") if d else ""

    descricoes_origem = {
        "1": "Correção de apontamento de produção e/ou consumo relativo aos Registros K230/K235",
        "2": "Correção de apontamento de produção e/ou consumo relativo aos Registros K250/K255",
        "3": "Correção de apontamento de desmontagem e/ou consumo relativo aos Registros K210/K215",
        "4": "Correção de apontamento de reprocessamento/reparo e/ou consumo relativo aos Registros K260/K265",
        "5": "Correção de apontamento de movimentação interna relativo ao Registro K220",
        "6": "Correção de apontamento de produção relativo ao Registro K291",
        "7": "Correção de apontamento de consumo relativo ao Registro K292",
        "8": "Correção de apontamento de produção relativo ao Registro K301",
        "9": "Correção de apontamento de consumo relativo ao Registro K302",
    }

    return {
        "REG": {"titulo": "Registro", "valor": reg},
        "DT_INI_AP": {
            "titulo": "Data inicial do período de apuração em que ocorreu o apontamento que está sendo corrigido",
            "valor": dt_ini_ap if dt_ini_ap else "",
            "valor_formatado": fmt_data(dt_ini_ap_obj) if dt_ini_ap_obj else "",
        },
        "DT_FIN_AP": {
            "titulo": "Data final do período de apuração em que ocorreu o apontamento que está sendo corrigido",
            "valor": dt_fin_ap if dt_fin_ap else "",
            "valor_formatado": fmt_data(dt_fin_ap_obj) if dt_fin_ap_obj else "",
        },
        "COD_OP_OS": {
            "titulo": "Código de identificação da ordem de produção ou da ordem de serviço que está sendo corrigida",
            "valor": cod_op_os if cod_op_os else "",
        },
        "COD_ITEM": {
            "titulo": "Código da mercadoria que está sendo corrigido (campo 02 do Registro 0200)",
            "valor": cod_item,
        },
        "QTD_COR_POS": {
            "titulo": "Quantidade de correção positiva de apontamento ocorrido em período de apuração anterior",
            "valor": qtd_cor_pos if qtd_cor_pos else "",
            "valor_formatado": fmt_quantidade(qtd_cor_pos_float) if qtd_cor_pos_float is not None else "",
        },
        "QTD_COR_NEG": {
            "titulo": "Quantidade de correção negativa de apontamento ocorrido em período de apuração anterior",
            "valor": qtd_cor_neg if qtd_cor_neg else "",
            "valor_formatado": fmt_quantidade(qtd_cor_neg_float) if qtd_cor_neg_float is not None else "",
        },
        "ORIGEM": {
            "titulo": "Origem da correção",
            "valor": origem,
            "descricao": descricoes_origem.get(origem, ""),
        },
    }


def validar_k270(linhas, dt_ini_0000=None):
    """
    Valida uma ou mais linhas do registro K270 do SPED EFD Fiscal.

    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |K270|DT_INI_AP|DT_FIN_AP|COD_OP_OS|COD_ITEM|QTD_COR_POS|QTD_COR_NEG|ORIGEM|
        dt_ini_0000: DT_INI do registro 0000 (ddmmaaaa) para validação (opcional)

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
        r = _processar_linha_k270(l, dt_ini_0000=dt_ini_0000)
        if r is not None:
            resultados.append(r)

    return json.dumps(resultados, ensure_ascii=False, indent=2)
