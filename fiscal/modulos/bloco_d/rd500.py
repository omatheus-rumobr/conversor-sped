import re
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
    if not valor_str:
        if obrigatorio:
            return False, None, f"Campo obrigatório não preenchido"
        return True, 0.0, None
    
    try:
        valor_float = float(valor_str)
        
        # Verifica precisão decimal
        partes_decimal = valor_str.split('.')
        if len(partes_decimal) == 2 and len(partes_decimal[1]) > decimais:
            return False, None, f"Valor com mais de {decimais} casas decimais"
        
        # Validações de sinal
        if positivo and valor_float <= 0:
            return False, None, "Valor deve ser maior que zero"
        if nao_negativo and valor_float < 0:
            return False, None, "Valor não pode ser negativo"
        
        return True, valor_float, None
    except ValueError:
        return False, None, "Valor não é numérico válido"


def _processar_linha_d500(linha):
    """
    Processa uma única linha do registro D500 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |D500|IND_OPER|IND_EMIT|COD_PART|COD_MOD|COD_SIT|SER|SUB|NUM_DOC|DT_DOC|DT_A_P|VL_DOC|VL_DESC|VL_SERV|VL_SERV_NT|VL_TERC|VL_DA|VL_BC_ICMS|VL_ICMS|COD_INF|VL_PIS|VL_COFINS|COD_CTA|TP_ASSINANTE|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |D500|...|)
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
    if reg != "D500":
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
    
    # Extrai todos os campos (24 campos no total)
    ind_oper = obter_campo(1)
    ind_emit = obter_campo(2)
    cod_part = obter_campo(3)
    cod_mod = obter_campo(4)
    cod_sit = obter_campo(5)
    ser = obter_campo(6)
    sub = obter_campo(7)
    num_doc = obter_campo(8)
    dt_doc = obter_campo(9)
    dt_a_p = obter_campo(10)
    vl_doc = obter_campo(11)
    vl_desc = obter_campo(12)
    vl_serv = obter_campo(13)
    vl_serv_nt = obter_campo(14)
    vl_terc = obter_campo(15)
    vl_da = obter_campo(16)
    vl_bc_icms = obter_campo(17)
    vl_icms = obter_campo(18)
    cod_inf = obter_campo(19)
    vl_pis = obter_campo(20)
    vl_cofins = obter_campo(21)
    cod_cta = obter_campo(22)
    tp_assinante = obter_campo(23)
    
    # Validações dos campos obrigatórios sempre presentes
    
    # IND_OPER: obrigatório, valores válidos: ["0", "1"]
    if not ind_oper or ind_oper not in ["0", "1"]:
        return None
    
    # IND_EMIT: obrigatório, valores válidos: ["0", "1"]
    if not ind_emit or ind_emit not in ["0", "1"]:
        return None
    
    # COD_MOD: obrigatório, valores válidos: ["21", "22"]
    if not cod_mod or cod_mod not in ["21", "22"]:
        return None
    
    # COD_SIT: obrigatório, valores válidos: ["00", "01", "02", "03", "06", "07", "08"]
    if not cod_sit or cod_sit not in ["00", "01", "02", "03", "06", "07", "08"]:
        return None
    
    # NUM_DOC: obrigatório, numérico, maior que zero
    if not num_doc or not num_doc.isdigit() or int(num_doc) <= 0:
        return None
    
    # Validações condicionais baseadas no COD_SIT
    
    # Exceção 1: COD_SIT = "02" ou "03" (cancelado)
    # Apenas REG, IND_OPER, IND_EMIT, COD_MOD, COD_SIT, SER, NUM_DOC e DT_DOC são obrigatórios, demais campos devem estar vazios
    if cod_sit in ["02", "03"]:
        # SER: obrigatório nesta exceção
        if not ser or len(ser) > 4:
            return None
        
        # DT_DOC: obrigatório, formato ddmmaaaa
        dt_doc_valido, dt_doc_obj = _validar_data(dt_doc)
        if not dt_doc_valido:
            return None
        
        # Demais campos devem estar vazios
        if cod_part or sub or dt_a_p or vl_doc or vl_desc or vl_serv or vl_serv_nt or vl_terc or vl_da or vl_bc_icms or vl_icms or cod_inf or vl_pis or vl_cofins or cod_cta or tp_assinante:
            return None
        
        # Formatação de data
        def formatar_data(data_obj):
            if data_obj is None:
                return ""
            return data_obj.strftime("%d/%m/%Y")
        
        # Monta resultado para exceção 1
        resultado = {
            "REG": {"titulo": "Registro", "valor": reg},
            "IND_OPER": {"titulo": "Indicador do tipo de operação: 0- Aquisição; 1- Prestação", "valor": ind_oper, "descricao": {"0": "Aquisição", "1": "Prestação"}.get(ind_oper, "")},
            "IND_EMIT": {"titulo": "Indicador do emitente do documento fiscal: 0- Emissão própria; 1- Terceiros", "valor": ind_emit, "descricao": {"0": "Emissão própria", "1": "Terceiros"}.get(ind_emit, "")},
            "COD_PART": {"titulo": "Código do participante (campo 02 do Registro 0150): - do prestador do serviço, no caso de aquisição; - do tomador do serviço, no caso de prestação", "valor": ""},
            "COD_MOD": {"titulo": "Código do modelo do documento fiscal, conforme a Tabela 4.1.1", "valor": cod_mod, "descricao": {"21": "Nota Fiscal de Serviço de Comunicação", "22": "Nota Fiscal de Serviço de Telecomunicação"}.get(cod_mod, "")},
            "COD_SIT": {"titulo": "Código da situação do documento fiscal, conforme a Tabela 4.1.2", "valor": cod_sit},
            "SER": {"titulo": "Série do documento fiscal", "valor": ser},
            "SUB": {"titulo": "Subsérie do documento fiscal", "valor": ""},
            "NUM_DOC": {"titulo": "Número do documento fiscal", "valor": num_doc},
            "DT_DOC": {"titulo": "Data da emissão do documento fiscal", "valor": dt_doc, "valor_formatado": formatar_data(dt_doc_obj)},
            "DT_A_P": {"titulo": "Data da entrada (aquisição) ou da saída (prestação do serviço)", "valor": "", "valor_formatado": ""},
            "VL_DOC": {"titulo": "Valor total do documento fiscal", "valor": "", "valor_formatado": ""},
            "VL_DESC": {"titulo": "Valor total do desconto", "valor": "", "valor_formatado": ""},
            "VL_SERV": {"titulo": "Valor da prestação de serviços", "valor": "", "valor_formatado": ""},
            "VL_SERV_NT": {"titulo": "Valor total dos serviços não-tributados pelo ICMS", "valor": "", "valor_formatado": ""},
            "VL_TERC": {"titulo": "Valores cobrados em nome de terceiros", "valor": "", "valor_formatado": ""},
            "VL_DA": {"titulo": "Valor de outras despesas indicadas no documento fiscal", "valor": "", "valor_formatado": ""},
            "VL_BC_ICMS": {"titulo": "Valor da base de cálculo do ICMS", "valor": "", "valor_formatado": ""},
            "VL_ICMS": {"titulo": "Valor do ICMS", "valor": "", "valor_formatado": ""},
            "COD_INF": {"titulo": "Código da informação complementar (campo 02 do Registro 0450)", "valor": ""},
            "VL_PIS": {"titulo": "Valor do PIS", "valor": "", "valor_formatado": ""},
            "VL_COFINS": {"titulo": "Valor da COFINS", "valor": "", "valor_formatado": ""},
            "COD_CTA": {"titulo": "Código da conta analítica contábil debitada/creditada", "valor": ""},
            "TP_ASSINANTE": {"titulo": "Código do Tipo de Assinante: 1 - Comercial/Industrial; 2 - Poder Público; 3 - Residencial/Pessoa física; 4 - Público; 5 - Semi-Público; 6 - Outros", "valor": ""}
        }
        return resultado
    
    # Exceção 2 e 3: COD_SIT = "06", "07" ou "08"
    # REG, IND_OPER, IND_EMIT, COD_PART, COD_MOD, COD_SIT, SER, NUM_DOC e DT_DOC são obrigatórios, demais campos são facultativos
    if cod_sit in ["06", "07", "08"]:
        # COD_PART: obrigatório
        if not cod_part or len(cod_part) > 60:
            return None
        
        # SER: obrigatório
        if not ser or len(ser) > 4:
            return None
        
        # SUB: opcional condicional, até 3 caracteres
        if sub and len(sub) > 3:
            return None
        
        # DT_DOC: obrigatório, formato ddmmaaaa
        dt_doc_valido, dt_doc_obj = _validar_data(dt_doc)
        if not dt_doc_valido:
            return None
        
        # DT_A_P: opcional condicional, formato ddmmaaaa
        dt_a_p_valido, dt_a_p_obj = None, None
        if dt_a_p:
            dt_a_p_valido, dt_a_p_obj = _validar_data(dt_a_p)
            if not dt_a_p_valido:
                return None
        
        # Demais campos são facultativos, mas se preenchidos devem ser validados
        vl_doc_valido, vl_doc_float, _ = validar_valor_numerico(vl_doc, decimais=2, obrigatorio=False, positivo=False, nao_negativo=True)
        if not vl_doc_valido:
            return None
        
        vl_desc_valido, vl_desc_float, _ = validar_valor_numerico(vl_desc, decimais=2, obrigatorio=False, nao_negativo=True)
        if not vl_desc_valido:
            return None
        
        vl_serv_valido, vl_serv_float, _ = validar_valor_numerico(vl_serv, decimais=2, obrigatorio=False, positivo=False, nao_negativo=True)
        if not vl_serv_valido:
            return None
        
        vl_serv_nt_valido, vl_serv_nt_float, _ = validar_valor_numerico(vl_serv_nt, decimais=2, obrigatorio=False, nao_negativo=True)
        if not vl_serv_nt_valido:
            return None
        
        vl_terc_valido, vl_terc_float, _ = validar_valor_numerico(vl_terc, decimais=2, obrigatorio=False, nao_negativo=True)
        if not vl_terc_valido:
            return None
        
        vl_da_valido, vl_da_float, _ = validar_valor_numerico(vl_da, decimais=2, obrigatorio=False, nao_negativo=True)
        if not vl_da_valido:
            return None
        
        vl_bc_icms_valido, vl_bc_icms_float, _ = validar_valor_numerico(vl_bc_icms, decimais=2, obrigatorio=False, nao_negativo=True)
        if not vl_bc_icms_valido:
            return None
        
        vl_icms_valido, vl_icms_float, _ = validar_valor_numerico(vl_icms, decimais=2, obrigatorio=False, nao_negativo=True)
        if not vl_icms_valido:
            return None
        
        vl_pis_valido, vl_pis_float, _ = validar_valor_numerico(vl_pis, decimais=2, obrigatorio=False, nao_negativo=True)
        if not vl_pis_valido:
            return None
        
        vl_cofins_valido, vl_cofins_float, _ = validar_valor_numerico(vl_cofins, decimais=2, obrigatorio=False, nao_negativo=True)
        if not vl_cofins_valido:
            return None
        
        # COD_INF: opcional condicional, até 6 caracteres
        if cod_inf and len(cod_inf) > 6:
            return None
        
        # TP_ASSINANTE: opcional condicional, valores válidos: ["1", "2", "3", "4", "5", "6"]
        if tp_assinante and tp_assinante not in ["1", "2", "3", "4", "5", "6"]:
            return None
        
        # Formatação
        def formatar_valor_monetario(valor_float):
            if valor_float is None:
                return ""
            return f"R$ {valor_float:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        
        def formatar_data(data_obj):
            if data_obj is None:
                return ""
            return data_obj.strftime("%d/%m/%Y")
        
        resultado = {
            "REG": {"titulo": "Registro", "valor": reg},
            "IND_OPER": {"titulo": "Indicador do tipo de operação: 0- Aquisição; 1- Prestação", "valor": ind_oper, "descricao": {"0": "Aquisição", "1": "Prestação"}.get(ind_oper, "")},
            "IND_EMIT": {"titulo": "Indicador do emitente do documento fiscal: 0- Emissão própria; 1- Terceiros", "valor": ind_emit, "descricao": {"0": "Emissão própria", "1": "Terceiros"}.get(ind_emit, "")},
            "COD_PART": {"titulo": "Código do participante (campo 02 do Registro 0150): - do prestador do serviço, no caso de aquisição; - do tomador do serviço, no caso de prestação", "valor": cod_part},
            "COD_MOD": {"titulo": "Código do modelo do documento fiscal, conforme a Tabela 4.1.1", "valor": cod_mod, "descricao": {"21": "Nota Fiscal de Serviço de Comunicação", "22": "Nota Fiscal de Serviço de Telecomunicação"}.get(cod_mod, "")},
            "COD_SIT": {"titulo": "Código da situação do documento fiscal, conforme a Tabela 4.1.2", "valor": cod_sit},
            "SER": {"titulo": "Série do documento fiscal", "valor": ser},
            "SUB": {"titulo": "Subsérie do documento fiscal", "valor": sub if sub else ""},
            "NUM_DOC": {"titulo": "Número do documento fiscal", "valor": num_doc},
            "DT_DOC": {"titulo": "Data da emissão do documento fiscal", "valor": dt_doc, "valor_formatado": formatar_data(dt_doc_obj)},
            "DT_A_P": {"titulo": "Data da entrada (aquisição) ou da saída (prestação do serviço)", "valor": dt_a_p if dt_a_p else "", "valor_formatado": formatar_data(dt_a_p_obj) if dt_a_p_obj else ""},
            "VL_DOC": {"titulo": "Valor total do documento fiscal", "valor": vl_doc if vl_doc else "", "valor_formatado": formatar_valor_monetario(vl_doc_float) if vl_doc else ""},
            "VL_DESC": {"titulo": "Valor total do desconto", "valor": vl_desc if vl_desc else "", "valor_formatado": formatar_valor_monetario(vl_desc_float) if vl_desc else ""},
            "VL_SERV": {"titulo": "Valor da prestação de serviços", "valor": vl_serv if vl_serv else "", "valor_formatado": formatar_valor_monetario(vl_serv_float) if vl_serv else ""},
            "VL_SERV_NT": {"titulo": "Valor total dos serviços não-tributados pelo ICMS", "valor": vl_serv_nt if vl_serv_nt else "", "valor_formatado": formatar_valor_monetario(vl_serv_nt_float) if vl_serv_nt else ""},
            "VL_TERC": {"titulo": "Valores cobrados em nome de terceiros", "valor": vl_terc if vl_terc else "", "valor_formatado": formatar_valor_monetario(vl_terc_float) if vl_terc else ""},
            "VL_DA": {"titulo": "Valor de outras despesas indicadas no documento fiscal", "valor": vl_da if vl_da else "", "valor_formatado": formatar_valor_monetario(vl_da_float) if vl_da else ""},
            "VL_BC_ICMS": {"titulo": "Valor da base de cálculo do ICMS", "valor": vl_bc_icms if vl_bc_icms else "", "valor_formatado": formatar_valor_monetario(vl_bc_icms_float) if vl_bc_icms else ""},
            "VL_ICMS": {"titulo": "Valor do ICMS", "valor": vl_icms if vl_icms else "", "valor_formatado": formatar_valor_monetario(vl_icms_float) if vl_icms else ""},
            "COD_INF": {"titulo": "Código da informação complementar (campo 02 do Registro 0450)", "valor": cod_inf if cod_inf else ""},
            "VL_PIS": {"titulo": "Valor do PIS", "valor": vl_pis if vl_pis else "", "valor_formatado": formatar_valor_monetario(vl_pis_float) if vl_pis else ""},
            "VL_COFINS": {"titulo": "Valor da COFINS", "valor": vl_cofins if vl_cofins else "", "valor_formatado": formatar_valor_monetario(vl_cofins_float) if vl_cofins else ""},
            "COD_CTA": {"titulo": "Código da conta analítica contábil debitada/creditada", "valor": cod_cta if cod_cta else ""},
            "TP_ASSINANTE": {"titulo": "Código do Tipo de Assinante: 1 - Comercial/Industrial; 2 - Poder Público; 3 - Residencial/Pessoa física; 4 - Público; 5 - Semi-Público; 6 - Outros", "valor": tp_assinante if tp_assinante else "", "descricao": {"1": "Comercial/Industrial", "2": "Poder Público", "3": "Residencial/Pessoa física", "4": "Público", "5": "Semi-Público", "6": "Outros"}.get(tp_assinante, "") if tp_assinante else ""}
        }
        return resultado
    
    # Caso normal: COD_SIT = "00" ou "01"
    # Todos os campos obrigatórios devem ser preenchidos
    
    # COD_PART: obrigatório, até 60 caracteres
    if not cod_part or len(cod_part) > 60:
        return None
    
    # SER: opcional condicional, até 4 caracteres
    if ser and len(ser) > 4:
        return None
    
    # SUB: opcional condicional, até 3 caracteres
    if sub and len(sub) > 3:
        return None
    
    # DT_DOC: obrigatório, formato ddmmaaaa
    dt_doc_valido, dt_doc_obj = _validar_data(dt_doc)
    if not dt_doc_valido:
        return None
    
    # DT_A_P: opcional condicional, formato ddmmaaaa
    dt_a_p_valido, dt_a_p_obj = None, None
    if dt_a_p:
        dt_a_p_valido, dt_a_p_obj = _validar_data(dt_a_p)
        if not dt_a_p_valido:
            return None
    
    # VL_DOC: obrigatório, numérico com 2 decimais, maior que zero
    vl_doc_valido, vl_doc_float, _ = validar_valor_numerico(vl_doc, decimais=2, obrigatorio=True, positivo=True)
    if not vl_doc_valido:
        return None
    
    # VL_DESC: opcional condicional, numérico com 2 decimais, não negativo
    vl_desc_valido, vl_desc_float, _ = validar_valor_numerico(vl_desc, decimais=2, obrigatorio=False, nao_negativo=True)
    if not vl_desc_valido:
        return None
    
    # VL_SERV: obrigatório, numérico com 2 decimais, maior que zero
    vl_serv_valido, vl_serv_float, _ = validar_valor_numerico(vl_serv, decimais=2, obrigatorio=True, positivo=True)
    if not vl_serv_valido:
        return None
    
    # VL_SERV_NT: opcional condicional, numérico com 2 decimais, não negativo
    vl_serv_nt_valido, vl_serv_nt_float, _ = validar_valor_numerico(vl_serv_nt, decimais=2, obrigatorio=False, nao_negativo=True)
    if not vl_serv_nt_valido:
        return None
    
    # VL_TERC: opcional condicional, numérico com 2 decimais, não negativo
    vl_terc_valido, vl_terc_float, _ = validar_valor_numerico(vl_terc, decimais=2, obrigatorio=False, nao_negativo=True)
    if not vl_terc_valido:
        return None
    
    # VL_DA: opcional condicional, numérico com 2 decimais, não negativo
    vl_da_valido, vl_da_float, _ = validar_valor_numerico(vl_da, decimais=2, obrigatorio=False, nao_negativo=True)
    if not vl_da_valido:
        return None
    
    # VL_BC_ICMS: opcional condicional, numérico com 2 decimais, não negativo
    vl_bc_icms_valido, vl_bc_icms_float, _ = validar_valor_numerico(vl_bc_icms, decimais=2, obrigatorio=False, nao_negativo=True)
    if not vl_bc_icms_valido:
        return None
    
    # VL_ICMS: opcional condicional, numérico com 2 decimais, não negativo
    vl_icms_valido, vl_icms_float, _ = validar_valor_numerico(vl_icms, decimais=2, obrigatorio=False, nao_negativo=True)
    if not vl_icms_valido:
        return None
    
    # COD_INF: opcional condicional, até 6 caracteres
    if cod_inf and len(cod_inf) > 6:
        return None
    
    # VL_PIS: opcional condicional, numérico com 2 decimais, não negativo
    vl_pis_valido, vl_pis_float, _ = validar_valor_numerico(vl_pis, decimais=2, obrigatorio=False, nao_negativo=True)
    if not vl_pis_valido:
        return None
    
    # VL_COFINS: opcional condicional, numérico com 2 decimais, não negativo
    vl_cofins_valido, vl_cofins_float, _ = validar_valor_numerico(vl_cofins, decimais=2, obrigatorio=False, nao_negativo=True)
    if not vl_cofins_valido:
        return None
    
    # TP_ASSINANTE: opcional condicional, valores válidos: ["1", "2", "3", "4", "5", "6"]
    if tp_assinante and tp_assinante not in ["1", "2", "3", "4", "5", "6"]:
        return None
    
    # Formatação
    def formatar_valor_monetario(valor_float):
        if valor_float is None:
            return ""
        return f"R$ {valor_float:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    def formatar_data(data_obj):
        if data_obj is None:
            return ""
        return data_obj.strftime("%d/%m/%Y")
    
    # Monta o resultado
    resultado = {
        "REG": {"titulo": "Registro", "valor": reg},
        "IND_OPER": {"titulo": "Indicador do tipo de operação: 0- Aquisição; 1- Prestação", "valor": ind_oper, "descricao": {"0": "Aquisição", "1": "Prestação"}.get(ind_oper, "")},
        "IND_EMIT": {"titulo": "Indicador do emitente do documento fiscal: 0- Emissão própria; 1- Terceiros", "valor": ind_emit, "descricao": {"0": "Emissão própria", "1": "Terceiros"}.get(ind_emit, "")},
        "COD_PART": {"titulo": "Código do participante (campo 02 do Registro 0150): - do prestador do serviço, no caso de aquisição; - do tomador do serviço, no caso de prestação", "valor": cod_part},
        "COD_MOD": {"titulo": "Código do modelo do documento fiscal, conforme a Tabela 4.1.1", "valor": cod_mod, "descricao": {"21": "Nota Fiscal de Serviço de Comunicação", "22": "Nota Fiscal de Serviço de Telecomunicação"}.get(cod_mod, "")},
        "COD_SIT": {"titulo": "Código da situação do documento fiscal, conforme a Tabela 4.1.2", "valor": cod_sit},
        "SER": {"titulo": "Série do documento fiscal", "valor": ser if ser else ""},
        "SUB": {"titulo": "Subsérie do documento fiscal", "valor": sub if sub else ""},
        "NUM_DOC": {"titulo": "Número do documento fiscal", "valor": num_doc},
        "DT_DOC": {"titulo": "Data da emissão do documento fiscal", "valor": dt_doc, "valor_formatado": formatar_data(dt_doc_obj)},
        "DT_A_P": {"titulo": "Data da entrada (aquisição) ou da saída (prestação do serviço)", "valor": dt_a_p if dt_a_p else "", "valor_formatado": formatar_data(dt_a_p_obj) if dt_a_p_obj else ""},
        "VL_DOC": {"titulo": "Valor total do documento fiscal", "valor": vl_doc, "valor_formatado": formatar_valor_monetario(vl_doc_float)},
        "VL_DESC": {"titulo": "Valor total do desconto", "valor": vl_desc if vl_desc else "", "valor_formatado": formatar_valor_monetario(vl_desc_float) if vl_desc else ""},
        "VL_SERV": {"titulo": "Valor da prestação de serviços", "valor": vl_serv, "valor_formatado": formatar_valor_monetario(vl_serv_float)},
        "VL_SERV_NT": {"titulo": "Valor total dos serviços não-tributados pelo ICMS", "valor": vl_serv_nt if vl_serv_nt else "", "valor_formatado": formatar_valor_monetario(vl_serv_nt_float) if vl_serv_nt else ""},
        "VL_TERC": {"titulo": "Valores cobrados em nome de terceiros", "valor": vl_terc if vl_terc else "", "valor_formatado": formatar_valor_monetario(vl_terc_float) if vl_terc else ""},
        "VL_DA": {"titulo": "Valor de outras despesas indicadas no documento fiscal", "valor": vl_da if vl_da else "", "valor_formatado": formatar_valor_monetario(vl_da_float) if vl_da else ""},
        "VL_BC_ICMS": {"titulo": "Valor da base de cálculo do ICMS", "valor": vl_bc_icms if vl_bc_icms else "", "valor_formatado": formatar_valor_monetario(vl_bc_icms_float) if vl_bc_icms else ""},
        "VL_ICMS": {"titulo": "Valor do ICMS", "valor": vl_icms if vl_icms else "", "valor_formatado": formatar_valor_monetario(vl_icms_float) if vl_icms else ""},
        "COD_INF": {"titulo": "Código da informação complementar (campo 02 do Registro 0450)", "valor": cod_inf if cod_inf else ""},
        "VL_PIS": {"titulo": "Valor do PIS", "valor": vl_pis if vl_pis else "", "valor_formatado": formatar_valor_monetario(vl_pis_float) if vl_pis else ""},
        "VL_COFINS": {"titulo": "Valor da COFINS", "valor": vl_cofins if vl_cofins else "", "valor_formatado": formatar_valor_monetario(vl_cofins_float) if vl_cofins else ""},
        "COD_CTA": {"titulo": "Código da conta analítica contábil debitada/creditada", "valor": cod_cta if cod_cta else ""},
        "TP_ASSINANTE": {"titulo": "Código do Tipo de Assinante: 1 - Comercial/Industrial; 2 - Poder Público; 3 - Residencial/Pessoa física; 4 - Público; 5 - Semi-Público; 6 - Outros", "valor": tp_assinante if tp_assinante else "", "descricao": {"1": "Comercial/Industrial", "2": "Poder Público", "3": "Residencial/Pessoa física", "4": "Público", "5": "Semi-Público", "6": "Outros"}.get(tp_assinante, "") if tp_assinante else ""}
    }
    
    return resultado


def validar_d500_fiscal(linhas):
    """
    Valida uma ou mais linhas do registro D500 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |D500|IND_OPER|IND_EMIT|COD_PART|COD_MOD|COD_SIT|SER|SUB|NUM_DOC|DT_DOC|DT_A_P|VL_DOC|VL_DESC|VL_SERV|VL_SERV_NT|VL_TERC|VL_DA|VL_BC_ICMS|VL_ICMS|COD_INF|VL_PIS|VL_COFINS|COD_CTA|TP_ASSINANTE|
        
    Returns:
        String JSON com array de objetos contendo os campos validados.
        Cada objeto tem a estrutura {"CAMPO": {"titulo": "...", "valor": "...", "valor_formatado": "...", "descricao": "..."}}.
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
        resultado = _processar_linha_d500(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
