import json
from datetime import datetime


def _validar_data(data_str):
    """
    Valida se a data está no formato ddmmaaaa e se é uma data válida.
    
    Args:
        data_str: String com data no formato ddmmaaaa
        
    Returns:
        tuple: (True/False, datetime object ou None)
    """
    if not data_str or len(data_str) != 8 or not data_str.isdigit():
        return False, None
    
    try:
        dia = int(data_str[:2])
        mes = int(data_str[2:4])
        ano = int(data_str[4:8])
        data_obj = datetime(ano, mes, dia)
        return True, data_obj
    except ValueError:
        return False, None


def validar_valor_numerico(valor_str, decimais=2, obrigatorio=False, positivo=False, nao_negativo=False):
    """
    Valida um valor numérico com precisão decimal específica.

    Args:
        valor_str: String com o valor numérico
        decimais: Número máximo de casas decimais permitidas
        obrigatorio: Se True, o campo não pode estar vazio
        positivo: Se True, o valor deve ser maior que 0
        nao_negativo: Se True, o valor deve ser maior ou igual a 0

    Returns:
        tuple: (True/False, valor float ou None, mensagem de erro ou None)
    """
    if valor_str is None:
        valor_str = ""

    if not valor_str:
        if obrigatorio:
            return False, None, "Campo obrigatório não preenchido"
        return True, 0.0, None

    try:
        valor_float = float(valor_str)

        # Verifica precisão decimal (quando houver ponto decimal)
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


def validar_valor_inteiro(valor_str, obrigatorio=False, positivo=False, nao_negativo=False):
    """
    Valida um valor inteiro.

    Args:
        valor_str: String com o valor inteiro
        obrigatorio: Se True, o campo não pode estar vazio
        positivo: Se True, o valor deve ser maior que 0
        nao_negativo: Se True, o valor deve ser maior ou igual a 0

    Returns:
        tuple: (True/False, valor int ou None, mensagem de erro ou None)
    """
    if valor_str is None:
        valor_str = ""

    if not valor_str:
        if obrigatorio:
            return False, None, "Campo obrigatório não preenchido"
        return True, 0, None

    try:
        valor_int = int(valor_str)

        if positivo and valor_int <= 0:
            return False, None, "Valor deve ser maior que zero"
        if nao_negativo and valor_int < 0:
            return False, None, "Valor não pode ser negativo"

        return True, valor_int, None
    except ValueError:
        return False, None, "Valor não é inteiro válido"


def _processar_linha_c600(linha):
    """
    Processa uma única linha do registro C600 e retorna um dicionário.
    
    Formato:
      |C600|COD_MOD|COD_MUN|SER|SUB|COD_CONS|QTD_CONS|QTD_CANC|DT_DOC|VL_DOC|VL_DESC|CONS|VL_FORN|VL_SERV_NT|VL_TERC|VL_DA|VL_BC_ICMS|VL_ICMS|VL_BC_ICMS_ST|VL_ICMS_ST|VL_PIS|VL_COFINS|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "C600"
    - COD_MOD: obrigatório, código do modelo do documento fiscal (2 caracteres)
      - Valores válidos: [01, 06, 28, 29, 55, 66]
    - COD_MUN: opcional, código do município dos pontos de consumo (7 dígitos)
      - Validação: deve existir na Tabela de Municípios do IBGE (validação em camada superior)
    - SER: opcional, série do documento fiscal (4 caracteres)
    - SUB: opcional, subsérie do documento fiscal (3 dígitos)
    - COD_CONS: opcional, código de classe de consumo (2 dígitos)
    - QTD_CONS: obrigatório, quantidade de documentos consolidados (inteiro, maior que 0)
    - QTD_CANC: opcional, quantidade de documentos cancelados (inteiro)
      - Deve ser menor ou igual a QTD_CONS
    - DT_DOC: obrigatório, data dos documentos consolidados (ddmmaaaa)
    - VL_DOC: obrigatório, valor total dos documentos (numérico, 2 decimais)
    - VL_DESC: opcional, valor acumulado dos descontos (numérico, 2 decimais)
    - CONS: opcional, consumo total acumulado, em kWh (numérico)
    - VL_FORN: opcional, valor acumulado do fornecimento (numérico, 2 decimais)
    - VL_SERV_NT: opcional, valor acumulado dos serviços não-tributados pelo ICMS (numérico, 2 decimais)
    - VL_TERC: opcional, valores cobrados em nome de terceiros (numérico, 2 decimais)
    - VL_DA: opcional, valor acumulado das despesas acessórias (numérico, 2 decimais)
    - VL_BC_ICMS: opcional, valor acumulado da base de cálculo do ICMS (numérico, 2 decimais)
    - VL_ICMS: opcional, valor acumulado do ICMS (numérico, 2 decimais)
    - VL_BC_ICMS_ST: opcional, valor acumulado da base de cálculo do ICMS substituição tributária (numérico, 2 decimais)
    - VL_ICMS_ST: opcional, valor acumulado do ICMS retido por substituição tributária (numérico, 2 decimais)
    - VL_PIS: obrigatório, valor acumulado do PIS/PASEP (numérico, 2 decimais)
    - VL_COFINS: obrigatório, valor acumulado da COFINS (numérico, 2 decimais)
    
    Nota: Este registro deve ser apresentado pelas pessoas jurídicas que auferem receita da venda de energia elétrica,
    água canalizada e gás, informando a consolidação diária de Notas Fiscais/Conta de Energia Elétrica, Nota Fiscal de
    Energia Elétrica Eletrônica – NF3e, Notas Fiscais de Fornecimento D'Água e Notas Fiscais/Conta de Fornecimento de Gás.
    
    Args:
        linha: String com uma linha do SPED
        
    Returns:
        dict: Dicionário com os campos validados contendo título e valor, ou None se inválido
    """
    if not linha or not isinstance(linha, str):
        return None
    
    linha = linha.strip()
    
    # Ignora linhas vazias
    if not linha:
        return None
    
    # Divide por pipe e remove partes vazias
    partes = linha.split('|')
    # Remove primeiro e último se vazios (formato padrão SPED: |C600|...|)
    if partes and not partes[0]:
        partes = partes[1:]
    if partes and not partes[-1]:
        partes = partes[:-1]
    
    # Verifica se tem pelo menos o campo REG
    if len(partes) < 1:
        return None
    
    # Extrai o campo REG
    reg = partes[0].strip() if partes else ""
    
    # Validação do campo REG
    if reg != "C600":
        return None
    
    # Função auxiliar para obter campo ou string vazia
    def obter_campo(indice):
        if indice < len(partes):
            valor = partes[indice].strip()
            # Trata "-" como campo vazio (padrão SPED para campos opcionais não preenchidos)
            if valor == "-":
                return ""
            return valor if valor else ""
        return ""
    
    # Extrai todos os campos (22 campos no total)
    cod_mod = obter_campo(1)
    cod_mun = obter_campo(2)
    ser = obter_campo(3)
    sub = obter_campo(4)
    cod_cons = obter_campo(5)
    qtd_cons = obter_campo(6)
    qtd_canc = obter_campo(7)
    dt_doc = obter_campo(8)
    vl_doc = obter_campo(9)
    vl_desc = obter_campo(10)
    cons = obter_campo(11)
    vl_forn = obter_campo(12)
    vl_serv_nt = obter_campo(13)
    vl_terc = obter_campo(14)
    vl_da = obter_campo(15)
    vl_bc_icms = obter_campo(16)
    vl_icms = obter_campo(17)
    vl_bc_icms_st = obter_campo(18)
    vl_icms_st = obter_campo(19)
    vl_pis = obter_campo(20)
    vl_cofins = obter_campo(21)
    
    # Validações básicas dos campos obrigatórios
    
    # COD_MOD: obrigatório, valores válidos [01, 06, 28, 29, 55, 66]
    cod_mod_validos = ["01", "06", "28", "29", "55", "66"]
    if not cod_mod or cod_mod not in cod_mod_validos:
        return None
    
    # COD_MUN: opcional, código do município (7 dígitos)
    if cod_mun and (not cod_mun.isdigit() or len(cod_mun) != 7):
        return None
    
    # SER: opcional, série do documento fiscal (4 caracteres)
    if ser and len(ser) > 4:
        return None
    
    # SUB: opcional, subsérie do documento fiscal (3 dígitos)
    if sub and (not sub.isdigit() or len(sub) > 3):
        return None
    
    # COD_CONS: opcional, código de classe de consumo (2 dígitos)
    if cod_cons and (not cod_cons.isdigit() or len(cod_cons) > 2):
        return None
    
    # QTD_CONS: obrigatório, quantidade de documentos consolidados (inteiro, maior que 0)
    ok_qtd_cons, val_qtd_cons, _ = validar_valor_inteiro(qtd_cons, obrigatorio=True, positivo=True)
    if not ok_qtd_cons:
        return None
    
    # QTD_CANC: opcional, quantidade de documentos cancelados (inteiro, deve ser <= QTD_CONS)
    ok_qtd_canc, val_qtd_canc, _ = validar_valor_inteiro(qtd_canc, obrigatorio=False, nao_negativo=True)
    if not ok_qtd_canc:
        return None
    if val_qtd_canc is not None and val_qtd_canc > val_qtd_cons:
        return None
    
    # DT_DOC: obrigatório, data dos documentos consolidados (ddmmaaaa)
    ok_dt_doc, data_dt_doc = _validar_data(dt_doc)
    if not ok_dt_doc:
        return None
    
    # VL_DOC: obrigatório, valor total dos documentos (numérico, 2 decimais)
    ok_vl_doc, val_vl_doc, _ = validar_valor_numerico(vl_doc, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok_vl_doc:
        return None
    
    # VL_DESC: opcional, valor acumulado dos descontos (numérico, 2 decimais)
    ok_vl_desc, val_vl_desc, _ = validar_valor_numerico(vl_desc, decimais=2, nao_negativo=True)
    if not ok_vl_desc:
        return None
    
    # CONS: opcional, consumo total acumulado (numérico)
    ok_cons, val_cons, _ = validar_valor_numerico(cons, decimais=0, nao_negativo=True)
    if not ok_cons:
        return None
    
    # VL_FORN: opcional, valor acumulado do fornecimento (numérico, 2 decimais)
    ok_vl_forn, val_vl_forn, _ = validar_valor_numerico(vl_forn, decimais=2, nao_negativo=True)
    if not ok_vl_forn:
        return None
    
    # VL_SERV_NT: opcional, valor acumulado dos serviços não-tributados pelo ICMS (numérico, 2 decimais)
    ok_vl_serv_nt, val_vl_serv_nt, _ = validar_valor_numerico(vl_serv_nt, decimais=2, nao_negativo=True)
    if not ok_vl_serv_nt:
        return None
    
    # VL_TERC: opcional, valores cobrados em nome de terceiros (numérico, 2 decimais)
    ok_vl_terc, val_vl_terc, _ = validar_valor_numerico(vl_terc, decimais=2, nao_negativo=True)
    if not ok_vl_terc:
        return None
    
    # VL_DA: opcional, valor acumulado das despesas acessórias (numérico, 2 decimais)
    ok_vl_da, val_vl_da, _ = validar_valor_numerico(vl_da, decimais=2, nao_negativo=True)
    if not ok_vl_da:
        return None
    
    # VL_BC_ICMS: opcional, valor acumulado da base de cálculo do ICMS (numérico, 2 decimais)
    ok_vl_bc_icms, val_vl_bc_icms, _ = validar_valor_numerico(vl_bc_icms, decimais=2, nao_negativo=True)
    if not ok_vl_bc_icms:
        return None
    
    # VL_ICMS: opcional, valor acumulado do ICMS (numérico, 2 decimais)
    ok_vl_icms, val_vl_icms, _ = validar_valor_numerico(vl_icms, decimais=2)
    if not ok_vl_icms:
        return None
    
    # VL_BC_ICMS_ST: opcional, valor acumulado da base de cálculo do ICMS substituição tributária (numérico, 2 decimais)
    ok_vl_bc_icms_st, val_vl_bc_icms_st, _ = validar_valor_numerico(vl_bc_icms_st, decimais=2, nao_negativo=True)
    if not ok_vl_bc_icms_st:
        return None
    
    # VL_ICMS_ST: opcional, valor acumulado do ICMS retido por substituição tributária (numérico, 2 decimais)
    ok_vl_icms_st, val_vl_icms_st, _ = validar_valor_numerico(vl_icms_st, decimais=2)
    if not ok_vl_icms_st:
        return None
    
    # VL_PIS: obrigatório, valor acumulado do PIS/PASEP (numérico, 2 decimais)
    ok_vl_pis, val_vl_pis, _ = validar_valor_numerico(vl_pis, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok_vl_pis:
        return None
    
    # VL_COFINS: obrigatório, valor acumulado da COFINS (numérico, 2 decimais)
    ok_vl_cofins, val_vl_cofins, _ = validar_valor_numerico(vl_cofins, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok_vl_cofins:
        return None
    
    # Função auxiliar para formatar valores monetários
    def fmt_valor(v):
        if v is None:
            return ""
        return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    # Função auxiliar para formatar data
    def fmt_data(data_str):
        if not data_str or len(data_str) != 8:
            return ""
        return f"{data_str[:2]}/{data_str[2:4]}/{data_str[4:]}"
    
    # Descrições dos campos
    descricoes_cod_mod = {
        "01": "Nota Fiscal",
        "06": "Nota Fiscal/Conta de Energia Elétrica",
        "28": "Nota Fiscal/Conta de Fornecimento de Gás",
        "29": "Nota Fiscal/Conta de Fornecimento D'água Canalizada",
        "55": "NF-e (Nota Fiscal Eletrônica)",
        "66": "Nota Fiscal de Energia Elétrica Eletrônica – NF3e"
    }
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg,
            "descricao": "Texto fixo contendo 'C600'"
        },
        "COD_MOD": {
            "titulo": "Código do modelo do documento fiscal",
            "valor": cod_mod,
            "descricao": descricoes_cod_mod.get(cod_mod, "")
        },
        "COD_MUN": {
            "titulo": "Código do município dos pontos de consumo, conforme a tabela IBGE",
            "valor": cod_mun
        },
        "SER": {
            "titulo": "Série do documento fiscal",
            "valor": ser
        },
        "SUB": {
            "titulo": "Subsérie do documento fiscal",
            "valor": sub
        },
        "COD_CONS": {
            "titulo": "Código de classe de consumo de energia elétrica, conforme a Tabela 4.4.5, ou Código de Consumo de Fornecimento D´água – Tabela 4.4.2 ou Código da classe de consumo de gás canalizado conforme Tabela 4.4.3",
            "valor": cod_cons
        },
        "QTD_CONS": {
            "titulo": "Quantidade de documentos consolidados neste registro",
            "valor": qtd_cons
        },
        "QTD_CANC": {
            "titulo": "Quantidade de documentos cancelados",
            "valor": qtd_canc
        },
        "DT_DOC": {
            "titulo": "Data dos documentos consolidados",
            "valor": dt_doc,
            "valor_formatado": fmt_data(dt_doc)
        },
        "VL_DOC": {
            "titulo": "Valor total dos documentos",
            "valor": vl_doc,
            "valor_formatado": fmt_valor(val_vl_doc)
        },
        "VL_DESC": {
            "titulo": "Valor acumulado dos descontos",
            "valor": vl_desc,
            "valor_formatado": fmt_valor(val_vl_desc)
        },
        "CONS": {
            "titulo": "Consumo total acumulado, em kWh (Código 06)",
            "valor": cons
        },
        "VL_FORN": {
            "titulo": "Valor acumulado do fornecimento",
            "valor": vl_forn,
            "valor_formatado": fmt_valor(val_vl_forn)
        },
        "VL_SERV_NT": {
            "titulo": "Valor acumulado dos serviços não-tributados pelo ICMS",
            "valor": vl_serv_nt,
            "valor_formatado": fmt_valor(val_vl_serv_nt)
        },
        "VL_TERC": {
            "titulo": "Valores cobrados em nome de terceiros",
            "valor": vl_terc,
            "valor_formatado": fmt_valor(val_vl_terc)
        },
        "VL_DA": {
            "titulo": "Valor acumulado das despesas acessórias",
            "valor": vl_da,
            "valor_formatado": fmt_valor(val_vl_da)
        },
        "VL_BC_ICMS": {
            "titulo": "Valor acumulado da base de cálculo do ICMS",
            "valor": vl_bc_icms,
            "valor_formatado": fmt_valor(val_vl_bc_icms)
        },
        "VL_ICMS": {
            "titulo": "Valor acumulado do ICMS",
            "valor": vl_icms,
            "valor_formatado": fmt_valor(val_vl_icms)
        },
        "VL_BC_ICMS_ST": {
            "titulo": "Valor acumulado da base de cálculo do ICMS substituição tributária",
            "valor": vl_bc_icms_st,
            "valor_formatado": fmt_valor(val_vl_bc_icms_st)
        },
        "VL_ICMS_ST": {
            "titulo": "Valor acumulado do ICMS retido por substituição tributária",
            "valor": vl_icms_st,
            "valor_formatado": fmt_valor(val_vl_icms_st)
        },
        "VL_PIS": {
            "titulo": "Valor acumulado do PIS/PASEP",
            "valor": vl_pis,
            "valor_formatado": fmt_valor(val_vl_pis)
        },
        "VL_COFINS": {
            "titulo": "Valor acumulado da COFINS",
            "valor": vl_cofins,
            "valor_formatado": fmt_valor(val_vl_cofins)
        }
    }
    
    return resultado


def validar_c600(linhas):
    """
    Valida uma ou mais linhas do registro C600 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |C600|COD_MOD|COD_MUN|SER|SUB|COD_CONS|QTD_CONS|QTD_CANC|DT_DOC|VL_DOC|VL_DESC|CONS|VL_FORN|VL_SERV_NT|VL_TERC|VL_DA|VL_BC_ICMS|VL_ICMS|VL_BC_ICMS_ST|VL_ICMS_ST|VL_PIS|VL_COFINS|
        
    Returns:
        String JSON com array de objetos contendo os campos validados.
        Cada objeto tem a estrutura {"CAMPO": {"titulo": "...", "valor": "..."}}.
        Retorna "[]" se nenhuma linha for válida.
    """
    if not linhas:
        return json.dumps([], ensure_ascii=False, indent=2)
    
    # Normaliza a entrada para uma lista de linhas
    if isinstance(linhas, str):
        # Se for string, verifica se tem múltiplas linhas
        if '\n' in linhas:
            linhas_para_processar = [linha.strip() for linha in linhas.split('\n') if linha.strip()]
        else:
            linhas_para_processar = [linhas.strip()] if linhas.strip() else []
    elif isinstance(linhas, list):
        linhas_para_processar = [linha.strip() if isinstance(linha, str) else str(linha).strip() for linha in linhas if linha]
    else:
        linhas_para_processar = [str(linhas).strip()] if str(linhas).strip() else []
    
    resultados = []
    
    for linha in linhas_para_processar:
        resultado = _processar_linha_c600(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
