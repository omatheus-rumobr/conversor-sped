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


def _processar_linha_k230(linha, dt_ini_k100=None, dt_fin_k100=None, dt_ini_0000=None):
    """
    Processa uma única linha do registro K230 e retorna um dicionário.

    Formato:
      |K230|DT_INI_OP|DT_FIN_OP|COD_DOC_OP|COD_ITEM|QTD_ENC|

    Regras (manual 3.1.8):
    - REG deve ser "K230"
    - DT_INI_OP: opcional condicional, formato ddmmaaaa
      - Obrigatório se informado COD_DOC_OP ou DT_FIN_OP
      - Deve ser <= DT_FIN do K100 (quando informado)
    - DT_FIN_OP: opcional condicional, formato ddmmaaaa
      - Se preenchido: deve ser <= DT_FIN do K100 e >= DT_INI_OP
      - Quando DT_FIN_OP for menor que DT_INI do 0000, deve ser informada no primeiro período
    - COD_DOC_OP: opcional condicional, até 30 caracteres
      - Obrigatório se informado DT_INI_OP
    - COD_ITEM: obrigatório, até 60 caracteres
    - QTD_ENC: obrigatório, numérico com 6 decimais, não negativo
      - Deve ser > 0 quando: DT_INI_OP e DT_FIN_OP preenchidos e no período do K100 OU todos os três campos não preenchidos
      - Deve ser = 0 quando DT_FIN_OP preenchido e < DT_INI do 0000

    Args:
        linha: linha SPED
        dt_ini_k100: data ddmmaaaa do DT_INI do registro K100 (opcional, para validação)
        dt_fin_k100: data ddmmaaaa do DT_FIN do registro K100 (opcional, para validação)
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
    if reg != "K230":
        return None

    def obter_campo(indice):
        if indice < len(partes):
            valor = partes[indice].strip()
            if valor == "-":
                return ""
            return valor if valor else ""
        return ""

    dt_ini_op = obter_campo(1)
    dt_fin_op = obter_campo(2)
    cod_doc_op = obter_campo(3)
    cod_item = obter_campo(4)
    qtd_enc = obter_campo(5)

    # Validação condicional dos campos de ordem de produção
    # DT_INI_OP é obrigatório se informado COD_DOC_OP ou DT_FIN_OP
    if cod_doc_op or dt_fin_op:
        if not dt_ini_op:
            return None

    # COD_DOC_OP é obrigatório se informado DT_INI_OP
    if dt_ini_op:
        if not cod_doc_op:
            return None

    # DT_INI_OP: opcional condicional, ddmmaaaa, data válida
    dt_ini_op_obj = None
    if dt_ini_op:
        dt_ini_op_ok, dt_ini_op_obj = _validar_data(dt_ini_op)
        if not dt_ini_op_ok:
            return None

        # Validação: DT_INI_OP deve ser <= DT_FIN do K100 (quando informado)
        if dt_fin_k100:
            ok_k100_fin, dt_fin_k100_obj = _validar_data(dt_fin_k100)
            if ok_k100_fin and dt_ini_op_obj > dt_fin_k100_obj:
                return None

    # DT_FIN_OP: opcional condicional, ddmmaaaa, data válida
    dt_fin_op_obj = None
    if dt_fin_op:
        dt_fin_op_ok, dt_fin_op_obj = _validar_data(dt_fin_op)
        if not dt_fin_op_ok:
            return None

        # Validação: DT_FIN_OP deve ser >= DT_INI_OP
        if dt_ini_op_obj and dt_fin_op_obj < dt_ini_op_obj:
            return None

        # Validação: DT_FIN_OP deve ser <= DT_FIN do K100 (quando informado)
        if dt_fin_k100:
            ok_k100_fin, dt_fin_k100_obj = _validar_data(dt_fin_k100)
            if ok_k100_fin and dt_fin_op_obj > dt_fin_k100_obj:
                return None

    # COD_DOC_OP: opcional condicional, até 30 caracteres
    if cod_doc_op and len(cod_doc_op) > 30:
        return None

    # COD_ITEM: obrigatório, até 60 caracteres
    if not cod_item or len(cod_item) > 60:
        return None

    # QTD_ENC: obrigatório, numérico com 6 decimais, não negativo
    qtd_enc_ok, qtd_enc_float, _ = validar_valor_numerico(qtd_enc, decimais=6, obrigatorio=True, nao_negativo=True)
    if not qtd_enc_ok:
        return None

    # Validação condicional de QTD_ENC conforme regras do manual
    # QTD_ENC deve ser > 0 quando:
    # a) DT_INI_OP e DT_FIN_OP preenchidos e compreendidos no período do K100
    # b) todos os três campos (DT_FIN_OP, DT_INI_OP, COD_DOC_OP) não preenchidos
    todos_campos_op_vazios = not dt_ini_op and not dt_fin_op and not cod_doc_op

    if todos_campos_op_vazios:
        # Caso b: todos os campos de OP vazios, QTD_ENC deve ser > 0
        if qtd_enc_float <= 0:
            return None
    elif dt_ini_op and dt_fin_op:
        # Caso a: ambos preenchidos, verificar se estão no período do K100
        if dt_ini_k100 and dt_fin_k100:
            ok_k100_ini, dt_ini_k100_obj = _validar_data(dt_ini_k100)
            ok_k100_fin, dt_fin_k100_obj = _validar_data(dt_fin_k100)
            if ok_k100_ini and ok_k100_fin:
                # Se ambas as datas estão no período do K100, QTD_ENC deve ser > 0
                if dt_ini_op_obj >= dt_ini_k100_obj and dt_ini_op_obj <= dt_fin_k100_obj:
                    if dt_fin_op_obj >= dt_ini_k100_obj and dt_fin_op_obj <= dt_fin_k100_obj:
                        if qtd_enc_float <= 0:
                            return None

    # Validação: QTD_ENC deve ser = 0 quando DT_FIN_OP preenchido e < DT_INI do 0000
    if dt_fin_op_obj and dt_ini_0000:
        ok_0000_ini, dt_ini_0000_obj = _validar_data(dt_ini_0000)
        if ok_0000_ini and dt_fin_op_obj < dt_ini_0000_obj:
            if qtd_enc_float != 0.0:
                return None

    def fmt_quantidade(v):
        return f"{v:,.6f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def fmt_data(d):
        return d.strftime("%d/%m/%Y") if d else ""

    return {
        "REG": {"titulo": "Registro", "valor": reg},
        "DT_INI_OP": {
            "titulo": "Data de início da ordem de produção",
            "valor": dt_ini_op if dt_ini_op else "",
            "valor_formatado": fmt_data(dt_ini_op_obj) if dt_ini_op_obj else "",
        },
        "DT_FIN_OP": {
            "titulo": "Data de conclusão da ordem de produção",
            "valor": dt_fin_op if dt_fin_op else "",
            "valor_formatado": fmt_data(dt_fin_op_obj) if dt_fin_op_obj else "",
        },
        "COD_DOC_OP": {
            "titulo": "Código de identificação da ordem de produção",
            "valor": cod_doc_op if cod_doc_op else "",
        },
        "COD_ITEM": {
            "titulo": "Código do item produzido (campo 02 do Registro 0200)",
            "valor": cod_item,
        },
        "QTD_ENC": {
            "titulo": "Quantidade de produção acabada",
            "valor": qtd_enc,
            "valor_formatado": fmt_quantidade(qtd_enc_float),
        },
    }


def validar_k230_fiscal(linhas, dt_ini_k100=None, dt_fin_k100=None, dt_ini_0000=None):
    """
    Valida uma ou mais linhas do registro K230 do SPED EFD Fiscal.

    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |K230|DT_INI_OP|DT_FIN_OP|COD_DOC_OP|COD_ITEM|QTD_ENC|
        dt_ini_k100: DT_INI do registro K100 (ddmmaaaa) para validação do período (opcional)
        dt_fin_k100: DT_FIN do registro K100 (ddmmaaaa) para validação do período (opcional)
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
        r = _processar_linha_k230(l, dt_ini_k100=dt_ini_k100, dt_fin_k100=dt_fin_k100, dt_ini_0000=dt_ini_0000)
        if r is not None:
            resultados.append(r)

    return json.dumps(resultados, ensure_ascii=False, indent=2)
