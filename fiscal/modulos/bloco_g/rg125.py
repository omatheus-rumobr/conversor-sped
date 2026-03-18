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


def _processar_linha_g125(linha, dt_ini_g110=None, dt_fin_g110=None):
    """
    Processa uma única linha do registro G125 e retorna um dicionário.

    Formato:
      |G125|COD_IND_BEM|DT_MOV|TIPO_MOV|VL_IMOB_ICMS_OP|VL_IMOB_ICMS_ST|VL_IMOB_ICMS_FRT|VL_IMOB_ICMS_DIF|NUM_PARC|VL_PARC_PASS|

    Regras (manual 3.1.8):
    - REG deve ser "G125"
    - COD_IND_BEM: obrigatório, até 60 caracteres
    - DT_MOV: obrigatório, formato ddmmaaaa
      - Se TIPO_MOV = "SI", deve ser igual à DT_INI do G110
      - Se TIPO_MOV = "IA", "IM", "CI", "MC", "BA", "AT", "PE" ou "OT", deve ser <= DT_FIN do G110
    - TIPO_MOV: obrigatório, valores válidos: ["SI", "IM", "IA", "CI", "MC", "BA", "AT", "PE", "OT"]
    - VL_IMOB_ICMS_*: para TIPO_MOV = "SI", "IM", "IA", "CI", "MC": pelo menos um deve ser > 0
    - VL_IMOB_ICMS_*: para TIPO_MOV = "BA", "AT", "PE", "OT": não devem ser informados
    - NUM_PARC e VL_PARC_PASS: obrigatórios quando informados (um requer o outro)
    - NUM_PARC e VL_PARC_PASS: para TIPO_MOV = "SI", "IM", "IA", "MC": devem ser informados
    - NUM_PARC e VL_PARC_PASS: para TIPO_MOV = "BA", "AT", "PE", "OT": não devem ser informados

    Args:
        linha: linha SPED
        dt_ini_g110: data ddmmaaaa do DT_INI do G110 (opcional, para validação)
        dt_fin_g110: data ddmmaaaa do DT_FIN do G110 (opcional, para validação)

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
    if reg != "G125":
        return None

    def obter_campo(indice):
        if indice < len(partes):
            valor = partes[indice].strip()
            if valor == "-":
                return ""
            return valor if valor else ""
        return ""

    cod_ind_bem = obter_campo(1)
    dt_mov = obter_campo(2)
    tipo_mov = obter_campo(3)
    vl_imob_icms_op = obter_campo(4)
    vl_imob_icms_st = obter_campo(5)
    vl_imob_icms_frt = obter_campo(6)
    vl_imob_icms_dif = obter_campo(7)
    num_parc = obter_campo(8)
    vl_parc_pass = obter_campo(9)

    # COD_IND_BEM: obrigatório, até 60 caracteres
    if not cod_ind_bem or len(cod_ind_bem) > 60:
        return None

    # TIPO_MOV: obrigatório, valores válidos
    tipos_mov_validos = ["SI", "IM", "IA", "CI", "MC", "BA", "AT", "PE", "OT"]
    if not tipo_mov or tipo_mov not in tipos_mov_validos:
        return None

    # DT_MOV: obrigatório, ddmmaaaa, data válida
    dt_mov_ok, dt_mov_obj = _validar_data(dt_mov)
    if not dt_mov_ok:
        return None

    # Validação de DT_MOV conforme TIPO_MOV
    if tipo_mov == "SI":
        # DT_MOV deve ser igual à DT_INI do G110 (quando informado)
        if dt_ini_g110:
            ok_g110_ini, dt_ini_g110_obj = _validar_data(dt_ini_g110)
            if ok_g110_ini and dt_mov_obj != dt_ini_g110_obj:
                return None
    elif tipo_mov in ["IA", "IM", "CI", "MC", "BA", "AT", "PE", "OT"]:
        # DT_MOV deve ser <= DT_FIN do G110 (quando informado)
        if dt_fin_g110:
            ok_g110_fin, dt_fin_g110_obj = _validar_data(dt_fin_g110)
            if ok_g110_fin and dt_mov_obj > dt_fin_g110_obj:
                return None

    # Tipos de movimentação que permitem valores ICMS
    tipos_com_valores = ["SI", "IM", "IA", "CI", "MC"]
    tipos_sem_valores = ["BA", "AT", "PE", "OT"]

    # Validação dos campos VL_IMOB_ICMS_*
    vl_imob_icms_op_ok, vl_imob_icms_op_float, _ = validar_valor_numerico(
        vl_imob_icms_op, decimais=2, obrigatorio=False, nao_negativo=True
    )
    if not vl_imob_icms_op_ok:
        return None

    vl_imob_icms_st_ok, vl_imob_icms_st_float, _ = validar_valor_numerico(
        vl_imob_icms_st, decimais=2, obrigatorio=False, nao_negativo=True
    )
    if not vl_imob_icms_st_ok:
        return None

    vl_imob_icms_frt_ok, vl_imob_icms_frt_float, _ = validar_valor_numerico(
        vl_imob_icms_frt, decimais=2, obrigatorio=False, nao_negativo=True
    )
    if not vl_imob_icms_frt_ok:
        return None

    vl_imob_icms_dif_ok, vl_imob_icms_dif_float, _ = validar_valor_numerico(
        vl_imob_icms_dif, decimais=2, obrigatorio=False, nao_negativo=True
    )
    if not vl_imob_icms_dif_ok:
        return None

    # Para tipos com valores: pelo menos um dos VL_IMOB_ICMS_* deve ser > 0
    if tipo_mov in tipos_com_valores:
        soma_valores = vl_imob_icms_op_float + vl_imob_icms_st_float + vl_imob_icms_frt_float + vl_imob_icms_dif_float
        if soma_valores <= 0:
            return None

    # Para tipos sem valores: nenhum dos VL_IMOB_ICMS_* deve ser informado (> 0)
    if tipo_mov in tipos_sem_valores:
        if (
            vl_imob_icms_op_float > 0
            or vl_imob_icms_st_float > 0
            or vl_imob_icms_frt_float > 0
            or vl_imob_icms_dif_float > 0
        ):
            return None

    # NUM_PARC: opcional condicional, numérico até 3 dígitos
    num_parc_int = None
    if num_parc:
        if not num_parc.isdigit() or len(num_parc) > 3:
            return None
        num_parc_int = int(num_parc)
        if num_parc_int <= 0:
            return None

    # VL_PARC_PASS: opcional condicional, numérico com 2 decimais
    vl_parc_pass_ok, vl_parc_pass_float, _ = validar_valor_numerico(
        vl_parc_pass, decimais=2, obrigatorio=False, nao_negativo=True
    )
    if not vl_parc_pass_ok:
        return None

    # Validação de dependência entre NUM_PARC e VL_PARC_PASS
    # NUM_PARC obrigatório quando VL_PARC_PASS > 0
    if vl_parc_pass_float > 0 and (not num_parc or num_parc_int is None):
        return None

    # VL_PARC_PASS obrigatório quando NUM_PARC > 0
    if num_parc_int and num_parc_int > 0 and vl_parc_pass_float <= 0:
        return None

    # Para tipos com valores: NUM_PARC e VL_PARC_PASS devem ser informados
    if tipo_mov in ["SI", "IM", "IA", "MC"]:
        if not num_parc or num_parc_int is None or num_parc_int <= 0:
            return None
        if vl_parc_pass_float <= 0:
            return None

    # Para tipos sem valores: NUM_PARC e VL_PARC_PASS não devem ser informados
    if tipo_mov in tipos_sem_valores:
        if num_parc and num_parc_int and num_parc_int > 0:
            return None
        if vl_parc_pass_float > 0:
            return None

    # Validação: VL_PARC_PASS <= soma dos VL_IMOB_ICMS_* / NUM_PARC
    # Nota: Não temos acesso ao NR_PARC do registro 0300 aqui, então validamos apenas a relação básica
    if num_parc_int and num_parc_int > 0 and vl_parc_pass_float > 0:
        soma_total_icms = vl_imob_icms_op_float + vl_imob_icms_st_float + vl_imob_icms_frt_float + vl_imob_icms_dif_float
        if soma_total_icms > 0:
            vl_max_parc = soma_total_icms / num_parc_int
            # Tolerância de 0.01 para valores monetários
            if vl_parc_pass_float > vl_max_parc + 0.01:
                return None

    def fmt_moeda(v):
        return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def fmt_data(d):
        return d.strftime("%d/%m/%Y") if d else ""

    descricoes_tipo_mov = {
        "SI": "Saldo inicial de bens imobilizados",
        "IM": "Imobilização de bem individual",
        "IA": "Imobilização em Andamento - Componente",
        "CI": "Conclusão de Imobilização em Andamento – Bem Resultante",
        "MC": "Imobilização oriunda do Ativo Circulante",
        "BA": "Baixa do bem - Fim do período de apropriação",
        "AT": "Alienação ou Transferência",
        "PE": "Perecimento, Extravio ou Deterioração",
        "OT": "Outras Saídas do Imobilizado",
    }

    return {
        "REG": {"titulo": "Registro", "valor": reg},
        "COD_IND_BEM": {
            "titulo": "Código individualizado do bem ou componente adotado no controle patrimonial do estabelecimento informante",
            "valor": cod_ind_bem,
        },
        "DT_MOV": {
            "titulo": "Data da movimentação ou do saldo inicial",
            "valor": dt_mov,
            "valor_formatado": fmt_data(dt_mov_obj),
        },
        "TIPO_MOV": {
            "titulo": "Tipo de movimentação do bem ou componente",
            "valor": tipo_mov,
            "descricao": descricoes_tipo_mov.get(tipo_mov, ""),
        },
        "VL_IMOB_ICMS_OP": {
            "titulo": "Valor do ICMS da Operação Própria na entrada do bem ou componente",
            "valor": vl_imob_icms_op if vl_imob_icms_op else "",
            "valor_formatado": fmt_moeda(vl_imob_icms_op_float) if vl_imob_icms_op_float > 0 else "",
        },
        "VL_IMOB_ICMS_ST": {
            "titulo": "Valor do ICMS da Oper. por Sub. Tributária na entrada do bem ou componente",
            "valor": vl_imob_icms_st if vl_imob_icms_st else "",
            "valor_formatado": fmt_moeda(vl_imob_icms_st_float) if vl_imob_icms_st_float > 0 else "",
        },
        "VL_IMOB_ICMS_FRT": {
            "titulo": "Valor do ICMS sobre Frete do Conhecimento de Transporte na entrada do bem ou componente",
            "valor": vl_imob_icms_frt if vl_imob_icms_frt else "",
            "valor_formatado": fmt_moeda(vl_imob_icms_frt_float) if vl_imob_icms_frt_float > 0 else "",
        },
        "VL_IMOB_ICMS_DIF": {
            "titulo": "Valor do ICMS - Diferencial de Alíquota, conforme Doc. de Arrecadação, na entrada do bem ou componente",
            "valor": vl_imob_icms_dif if vl_imob_icms_dif else "",
            "valor_formatado": fmt_moeda(vl_imob_icms_dif_float) if vl_imob_icms_dif_float > 0 else "",
        },
        "NUM_PARC": {
            "titulo": "Número da parcela do ICMS",
            "valor": num_parc if num_parc else "",
        },
        "VL_PARC_PASS": {
            "titulo": "Valor da parcela de ICMS passível de apropriação",
            "valor": vl_parc_pass if vl_parc_pass else "",
            "valor_formatado": fmt_moeda(vl_parc_pass_float) if vl_parc_pass_float > 0 else "",
        },
    }


def validar_g125_fiscal(linhas, dt_ini_g110=None, dt_fin_g110=None):
    """
    Valida uma ou mais linhas do registro G125 do SPED EFD Fiscal.

    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |G125|COD_IND_BEM|DT_MOV|TIPO_MOV|VL_IMOB_ICMS_OP|VL_IMOB_ICMS_ST|VL_IMOB_ICMS_FRT|VL_IMOB_ICMS_DIF|NUM_PARC|VL_PARC_PASS|
        dt_ini_g110: DT_INI do registro G110 (ddmmaaaa) para validação da data (opcional)
        dt_fin_g110: DT_FIN do registro G110 (ddmmaaaa) para validação da data (opcional)

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
        r = _processar_linha_g125(l, dt_ini_g110=dt_ini_g110, dt_fin_g110=dt_fin_g110)
        if r is not None:
            resultados.append(r)

    return json.dumps(resultados, ensure_ascii=False, indent=2)
