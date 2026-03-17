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


def _validar_chave_cte(chave):
    """
    Valida o formato básico da chave do CT-e (44 dígitos).
    Valida também o dígito verificador (DV) usando módulo 11.
    
    Args:
        chave: String com a chave do CT-e
        
    Returns:
        bool: True se válida, False caso contrário
    """
    if not chave:
        return False
    
    # Remove espaços
    chave_limpa = chave.strip()
    
    # Deve ter exatamente 44 dígitos
    if not chave_limpa.isdigit() or len(chave_limpa) != 44:
        return False
    
    # Validação do dígito verificador (DV)
    # O DV é o último dígito (posição 43, índice 43)
    # Calcula o DV usando módulo 11, multiplicadores de 2 a 9 (ciclando)
    chave_43 = chave_limpa[:43]
    dv_informado = int(chave_limpa[43])
    
    soma = 0
    multiplicador = 2
    # Percorre da posição 42 até 0 (do final para o início)
    for i in range(42, -1, -1):
        soma += int(chave_43[i]) * multiplicador
        multiplicador += 1
        if multiplicador > 9:
            multiplicador = 2
    
    resto = soma % 11
    dv_calculado = 0 if resto < 2 else 11 - resto
    
    return dv_calculado == dv_informado


def _processar_linha_d100(linha, dt_ini_0000=None, dt_fin_0000=None):
    """
    Processa uma única linha do registro D100 e retorna um dicionário.
    
    Formato:
      |D100|IND_OPER|IND_EMIT|COD_PART|COD_MOD|COD_SIT|SER|SUB|NUM_DOC|CHV_CTE|DT_DOC|DT_A_P|TP_CT-e|CHV_CTE_REF|VL_DOC|VL_DESC|IND_FRT|VL_SERV|VL_BC_ICMS|VL_ICMS|VL_NT|COD_INF|COD_CTA|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "D100"
    - IND_OPER: obrigatório, valores válidos [0]
    - IND_EMIT: obrigatório, valores válidos [0, 1]
    - COD_PART: obrigatório, máximo 60 caracteres
      - Deve existir no campo COD_PART do registro 0150 (validação em camada superior)
    - COD_MOD: obrigatório, valores válidos [07, 08, 8B, 09, 10, 11, 26, 27, 57, 63, 67]
    - COD_SIT: obrigatório, valores válidos [00, 02, 04, 05, 06, 08]
    - SER: opcional, máximo 4 caracteres
    - SUB: opcional, máximo 3 caracteres
    - NUM_DOC: obrigatório, máximo 9 dígitos, deve ser > 0 ou "000000000"
    - CHV_CTE: opcional, 44 dígitos, obrigatório para COD_MOD=57 a partir de abril/2012
      - Validação de DV e consistência com outros campos (validação em camada superior)
    - DT_DOC: obrigatório, formato ddmmaaaa
      - Deve estar compreendida no período da escrituração ou DT_A_P deve estar (quando informado)
    - DT_A_P: opcional, formato ddmmaaaa
      - Deve estar compreendida no período da escrituração ou DT_DOC deve estar (quando informado)
    - TP_CT-e: opcional, 1 dígito
    - CHV_CTE_REF: opcional, 44 dígitos
    - VL_DOC: obrigatório, numérico com 2 decimais
    - VL_DESC: opcional, numérico com 2 decimais
    - IND_FRT: obrigatório, valores válidos [0, 1, 2, 9]
      - A partir de 01/07/2012: [0, 1, 2, 9] com nova descrição
    - VL_SERV: obrigatório, numérico com 2 decimais
    - VL_BC_ICMS: opcional, numérico com 2 decimais
      - Deve corresponder a VL_SERV - VL_NT (validação em camada superior)
    - VL_ICMS: opcional, numérico com 2 decimais
    - VL_NT: opcional, numérico com 2 decimais
    - COD_INF: opcional, máximo 6 caracteres
      - Deve existir no registro 0450 (validação em camada superior)
    - COD_CTA: opcional, máximo 255 caracteres
      - Obrigatório a partir de novembro/2017, exceto se dispensado de ECD
    
    Nota: Este registro deve ser apresentado por todos os contribuintes adquirentes dos serviços
    relacionados, que utilizem os documentos previstos para este registro, cuja operação dê direito
    à apuração de crédito à pessoa jurídica contratante, na forma da legislação tributária.
    
    Args:
        linha: String com uma linha do SPED
        dt_ini_0000: Data inicial da escrituração (ddmmaaaa) - opcional, para validação
        dt_fin_0000: Data final da escrituração (ddmmaaaa) - opcional, para validação
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |D100|...|)
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
    if reg != "D100":
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
    
    # Extrai todos os campos (23 campos no total)
    ind_oper = obter_campo(1)
    ind_emit = obter_campo(2)
    cod_part = obter_campo(3)
    cod_mod = obter_campo(4)
    cod_sit = obter_campo(5)
    ser = obter_campo(6)
    sub = obter_campo(7)
    num_doc = obter_campo(8)
    chv_cte = obter_campo(9)
    dt_doc = obter_campo(10)
    dt_a_p = obter_campo(11)
    tp_cte = obter_campo(12)
    chv_cte_ref = obter_campo(13)
    vl_doc = obter_campo(14)
    vl_desc = obter_campo(15)
    ind_frt = obter_campo(16)
    vl_serv = obter_campo(17)
    vl_bc_icms = obter_campo(18)
    vl_icms = obter_campo(19)
    vl_nt = obter_campo(20)
    cod_inf = obter_campo(21)
    cod_cta = obter_campo(22)
    
    # Validações básicas dos campos obrigatórios
    
    # IND_OPER: obrigatório, valores válidos [0]
    if not ind_oper or ind_oper != "0":
        return None
    
    # IND_EMIT: obrigatório, valores válidos [0, 1]
    if not ind_emit or ind_emit not in ["0", "1"]:
        return None
    
    # COD_PART: obrigatório, máximo 60 caracteres
    if not cod_part or len(cod_part) > 60:
        return None
    
    # COD_MOD: obrigatório, valores válidos [07, 08, 8B, 09, 10, 11, 26, 27, 57, 63, 67]
    cod_mod_validos = ["07", "08", "8B", "09", "10", "11", "26", "27", "57", "63", "67"]
    if not cod_mod or cod_mod not in cod_mod_validos:
        return None
    
    # COD_SIT: obrigatório, valores válidos [00, 02, 04, 05, 06, 08]
    cod_sit_validos = ["00", "02", "04", "05", "06", "08"]
    if not cod_sit or cod_sit not in cod_sit_validos:
        return None
    
    # SER: opcional, máximo 4 caracteres
    if ser and len(ser) > 4:
        return None
    
    # SUB: opcional, máximo 3 caracteres
    if sub and len(sub) > 3:
        return None
    
    # NUM_DOC: obrigatório, máximo 9 dígitos, deve ser > 0 ou "000000000"
    if not num_doc:
        return None
    if not num_doc.isdigit() or len(num_doc) > 9:
        return None
    if num_doc != "000000000" and int(num_doc) <= 0:
        return None
    
    # CHV_CTE: opcional, 44 dígitos, obrigatório para COD_MOD=57 a partir de abril/2012
    if chv_cte:
        if len(chv_cte) != 44 or not chv_cte.isdigit():
            return None
        # Validação do dígito verificador
        if not _validar_chave_cte(chv_cte):
            return None
    elif cod_mod == "57":
        # Para COD_MOD=57, CHV_CTE é obrigatório a partir de abril/2012
        # Nota: Validação temporal deve ser feita em camada superior
        pass
    
    # DT_DOC: obrigatório, formato ddmmaaaa, data válida
    dt_doc_valido, dt_doc_obj = _validar_data(dt_doc)
    if not dt_doc_valido:
        return None
    
    # DT_A_P: opcional, formato ddmmaaaa, data válida
    dt_a_p_obj = None
    if dt_a_p:
        dt_a_p_valido, dt_a_p_obj = _validar_data(dt_a_p)
        if not dt_a_p_valido:
            return None
    
    # Validação de período da escrituração
    # A data informada em DT_DOC ou DT_A_P deve estar compreendida no período da escrituração
    if dt_ini_0000 and dt_fin_0000:
        ok_ini, dt_ini_obj = _validar_data(dt_ini_0000)
        ok_fin, dt_fin_obj = _validar_data(dt_fin_0000)
        if ok_ini and ok_fin:
            dt_doc_no_periodo = dt_doc_obj and (dt_ini_obj <= dt_doc_obj <= dt_fin_obj)
            dt_a_p_no_periodo = dt_a_p_obj and (dt_ini_obj <= dt_a_p_obj <= dt_fin_obj)
            
            if not dt_doc_no_periodo and not dt_a_p_no_periodo:
                return None
    
    # TP_CT-e: opcional, 1 dígito
    if tp_cte and (not tp_cte.isdigit() or len(tp_cte) != 1):
        return None
    
    # CHV_CTE_REF: opcional, 44 dígitos
    if chv_cte_ref:
        if len(chv_cte_ref) != 44 or not chv_cte_ref.isdigit():
            return None
        # Validação do dígito verificador
        if not _validar_chave_cte(chv_cte_ref):
            return None
    
    # VL_DOC: obrigatório, numérico com 2 decimais
    ok1, val1, _ = validar_valor_numerico(vl_doc, decimais=2, obrigatorio=True)
    if not ok1:
        return None
    
    # VL_DESC: opcional, numérico com 2 decimais
    ok2, val2, _ = validar_valor_numerico(vl_desc, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok2:
        return None
    
    # IND_FRT: obrigatório, valores válidos [0, 1, 2, 9]
    if not ind_frt or ind_frt not in ["0", "1", "2", "9"]:
        return None
    
    # VL_SERV: obrigatório, numérico com 2 decimais
    ok3, val3, _ = validar_valor_numerico(vl_serv, decimais=2, obrigatorio=True)
    if not ok3:
        return None
    
    # VL_BC_ICMS: opcional, numérico com 2 decimais
    ok4, val4, _ = validar_valor_numerico(vl_bc_icms, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok4:
        return None
    
    # VL_ICMS: opcional, numérico com 2 decimais
    ok5, val5, _ = validar_valor_numerico(vl_icms, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok5:
        return None
    
    # VL_NT: opcional, numérico com 2 decimais
    ok6, val6, _ = validar_valor_numerico(vl_nt, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok6:
        return None
    
    # COD_INF: opcional, máximo 6 caracteres
    if cod_inf and len(cod_inf) > 6:
        return None
    
    # COD_CTA: opcional, máximo 255 caracteres
    # Nota: Obrigatório a partir de novembro/2017, exceto se dispensado de ECD (validação em camada superior)
    if cod_cta and len(cod_cta) > 255:
        return None
    
    # Função auxiliar para formatar valores monetários
    def fmt_valor(v):
        if v is None:
            return ""
        return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    # Função auxiliar para formatar data
    def fmt_data(dt):
        if dt:
            return dt.strftime("%d/%m/%Y")
        return ""
    
    # Descrições dos campos
    descricoes_ind_oper = {
        "0": "Aquisição"
    }
    
    descricoes_ind_emit = {
        "0": "Emissão Própria",
        "1": "Emissão por Terceiros"
    }
    
    descricoes_cod_mod = {
        "07": "Nota Fiscal de Serviço de Transporte",
        "08": "Conhecimento de Transporte Rodoviário de Cargas",
        "8B": "Conhecimento de Transporte de Cargas Avulso",
        "09": "Conhecimento de Transporte Aquaviário de Cargas",
        "10": "Conhecimento de Transporte Aéreo",
        "11": "Conhecimento de Transporte Ferroviário de Cargas",
        "26": "Conhecimento de Transporte Multimodal de Cargas",
        "27": "Nota Fiscal de Transporte Ferroviário de Carga",
        "57": "Conhecimento de Transporte Eletrônico – CT-E",
        "63": "Bilhete de Passagem Eletrônico - BP-e",
        "67": "Conhecimento de Transporte Eletrônico para Outros Serviços – CT-e OS"
    }
    
    descricoes_cod_sit = {
        "00": "Documento regular",
        "02": "Documento cancelado",
        "04": "Documento denegado",
        "05": "Documento numeração inutilizada",
        "06": "Documento regular extemporâneo",
        "08": "Documento regular com pendência de entrega"
    }
    
    # Descrições do IND_FRT (a partir de 01/07/2012)
    descricoes_ind_frt = {
        "0": "Por conta do emitente",
        "1": "Por conta do destinatário/remetente",
        "2": "Por conta de terceiros",
        "9": "Sem cobrança de frete"
    }
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "IND_OPER": {
            "titulo": "Indicador do tipo de operação",
            "valor": ind_oper,
            "descricao": descricoes_ind_oper.get(ind_oper, "")
        },
        "IND_EMIT": {
            "titulo": "Indicador do emitente do documento fiscal",
            "valor": ind_emit,
            "descricao": descricoes_ind_emit.get(ind_emit, "")
        },
        "COD_PART": {
            "titulo": "Código do participante (campo 02 do Registro 0150)",
            "valor": cod_part
        },
        "COD_MOD": {
            "titulo": "Código do modelo do documento fiscal, conforme a Tabela 4.1.1",
            "valor": cod_mod,
            "descricao": descricoes_cod_mod.get(cod_mod, "")
        },
        "COD_SIT": {
            "titulo": "Código da situação do documento fiscal, conforme a Tabela 4.1.2",
            "valor": cod_sit,
            "descricao": descricoes_cod_sit.get(cod_sit, "")
        },
        "SER": {
            "titulo": "Série do documento fiscal",
            "valor": ser
        },
        "SUB": {
            "titulo": "Subsérie do documento fiscal",
            "valor": sub
        },
        "NUM_DOC": {
            "titulo": "Número do documento fiscal",
            "valor": num_doc
        },
        "CHV_CTE": {
            "titulo": "Chave do Conhecimento de Transporte Eletrônico",
            "valor": chv_cte
        },
        "DT_DOC": {
            "titulo": "Data de referência/emissão dos documentos fiscais",
            "valor": dt_doc,
            "valor_formatado": fmt_data(dt_doc_obj)
        },
        "DT_A_P": {
            "titulo": "Data da aquisição ou da prestação do serviço",
            "valor": dt_a_p,
            "valor_formatado": fmt_data(dt_a_p_obj) if dt_a_p_obj else ""
        },
        "TP_CT-e": {
            "titulo": "Tipo de Conhecimento de Transporte Eletrônico conforme definido no Manual de Integração do CT-e",
            "valor": tp_cte
        },
        "CHV_CTE_REF": {
            "titulo": "Chave do CT-e de referência cujos valores foram complementados (opção \"1\" do campo anterior) ou cujo débito foi anulado (opção \"2\" do campo anterior)",
            "valor": chv_cte_ref
        },
        "VL_DOC": {
            "titulo": "Valor total do documento fiscal",
            "valor": vl_doc,
            "valor_formatado": fmt_valor(val1)
        },
        "VL_DESC": {
            "titulo": "Valor total do desconto",
            "valor": vl_desc,
            "valor_formatado": fmt_valor(val2) if vl_desc else ""
        },
        "IND_FRT": {
            "titulo": "Indicador do tipo do frete",
            "valor": ind_frt,
            "descricao": descricoes_ind_frt.get(ind_frt, "")
        },
        "VL_SERV": {
            "titulo": "Valor total da prestação de serviço",
            "valor": vl_serv,
            "valor_formatado": fmt_valor(val3)
        },
        "VL_BC_ICMS": {
            "titulo": "Valor da base de cálculo do ICMS",
            "valor": vl_bc_icms,
            "valor_formatado": fmt_valor(val4) if vl_bc_icms else ""
        },
        "VL_ICMS": {
            "titulo": "Valor do ICMS",
            "valor": vl_icms,
            "valor_formatado": fmt_valor(val5) if vl_icms else ""
        },
        "VL_NT": {
            "titulo": "Valor não-tributado do ICMS",
            "valor": vl_nt,
            "valor_formatado": fmt_valor(val6) if vl_nt else ""
        },
        "COD_INF": {
            "titulo": "Código da informação complementar do documento fiscal (campo 02 do Registro 0450)",
            "valor": cod_inf
        },
        "COD_CTA": {
            "titulo": "Código da conta analítica contábil debitada/creditada",
            "valor": cod_cta
        }
    }
    
    return resultado


def validar_d100(linhas, dt_ini_0000=None, dt_fin_0000=None):
    """
    Valida uma ou mais linhas do registro D100 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |D100|IND_OPER|IND_EMIT|COD_PART|COD_MOD|COD_SIT|SER|SUB|NUM_DOC|CHV_CTE|DT_DOC|DT_A_P|TP_CT-e|CHV_CTE_REF|VL_DOC|VL_DESC|IND_FRT|VL_SERV|VL_BC_ICMS|VL_ICMS|VL_NT|COD_INF|COD_CTA|
        dt_ini_0000: Data inicial da escrituração (ddmmaaaa) - opcional, para validação
        dt_fin_0000: Data final da escrituração (ddmmaaaa) - opcional, para validação
        
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
        resultado = _processar_linha_d100(linha, dt_ini_0000, dt_fin_0000)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
