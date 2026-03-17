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


def _processar_linha_h005(linha, dt_fin_0000=None):
    """
    Processa uma única linha do registro H005 e retorna um dicionário.

    Formato:
      |H005|DT_INV|VL_INV|MOT_INV|

    Regras (manual 3.1.8):
    - REG deve ser "H005"
    - DT_INV: obrigatório, formato ddmmaaaa
      - Deve ser menor ou igual ao DT_FIN do registro 0000 (quando informado)
    - VL_INV: obrigatório, numérico com 2 decimais, não negativo
      - Deve ser igual à soma do campo VL_ITEM do registro H010 (validação externa)
    - MOT_INV: obrigatório, valores válidos ["01", "02", "03", "04", "05", "06"]

    Args:
        linha: linha SPED
        dt_fin_0000: data ddmmaaaa do DT_FIN do registro 0000 (opcional, para validação)

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
    if reg != "H005":
        return None

    def obter_campo(indice):
        if indice < len(partes):
            valor = partes[indice].strip()
            if valor == "-":
                return ""
            return valor if valor else ""
        return ""

    dt_inv = obter_campo(1)
    vl_inv = obter_campo(2)
    mot_inv = obter_campo(3)

    # DT_INV: obrigatório, ddmmaaaa, data válida
    dt_inv_ok, dt_inv_obj = _validar_data(dt_inv)
    if not dt_inv_ok:
        return None

    # Validação: DT_INV deve ser menor ou igual ao DT_FIN do registro 0000 (quando informado)
    if dt_fin_0000:
        ok_0000_fin, dt_fin_0000_obj = _validar_data(dt_fin_0000)
        if ok_0000_fin and dt_inv_obj > dt_fin_0000_obj:
            return None

    # VL_INV: obrigatório, numérico com 2 decimais, não negativo
    vl_inv_ok, vl_inv_float, _ = validar_valor_numerico(vl_inv, decimais=2, obrigatorio=True, nao_negativo=True)
    if not vl_inv_ok:
        return None

    # MOT_INV: obrigatório, valores válidos
    mot_inv_validos = ["01", "02", "03", "04", "05", "06"]
    if not mot_inv or mot_inv not in mot_inv_validos:
        return None

    def fmt_moeda(v):
        return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def fmt_data(d):
        return d.strftime("%d/%m/%Y") if d else ""

    descricoes_mot_inv = {
        "01": "No final no período",
        "02": "Na mudança de forma de tributação da mercadoria (ICMS)",
        "03": "Na solicitação da baixa cadastral, paralisação temporária e outras situações",
        "04": "Na alteração de regime de pagamento – condição do contribuinte",
        "05": "Por determinação dos fiscos",
        "06": "Para controle das mercadorias sujeitas ao regime de substituição tributária – restituição/ ressarcimento/ complementação",
    }

    return {
        "REG": {"titulo": "Registro", "valor": reg},
        "DT_INV": {
            "titulo": "Data do inventário",
            "valor": dt_inv,
            "valor_formatado": fmt_data(dt_inv_obj),
        },
        "VL_INV": {
            "titulo": "Valor total do estoque",
            "valor": vl_inv,
            "valor_formatado": fmt_moeda(vl_inv_float),
        },
        "MOT_INV": {
            "titulo": "Informe o motivo do Inventário",
            "valor": mot_inv,
            "descricao": descricoes_mot_inv.get(mot_inv, ""),
        },
    }


def validar_h005(linhas, dt_fin_0000=None):
    """
    Valida uma ou mais linhas do registro H005 do SPED EFD Fiscal.

    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |H005|DT_INV|VL_INV|MOT_INV|
        dt_fin_0000: DT_FIN do registro 0000 (ddmmaaaa) para validação da data (opcional)

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
        r = _processar_linha_h005(l, dt_fin_0000=dt_fin_0000)
        if r is not None:
            resultados.append(r)

    return json.dumps(resultados, ensure_ascii=False, indent=2)
