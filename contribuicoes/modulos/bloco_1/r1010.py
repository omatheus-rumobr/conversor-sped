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


def _processar_linha_1010(linha):
    """
    Processa uma única linha do registro 1010 e retorna um dicionário.
    
    Formato:
      |1010|NUM_PROC|ID_SEC_JUD|ID_VARA|IND_NAT_ACAO|DESC_DEC_JUD|DT_SENT_JUD|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "1010"
    - NUM_PROC: obrigatório, até 20 caracteres
    - ID_SEC_JUD: obrigatório, identificação da seção judiciária
    - ID_VARA: obrigatório, 2 caracteres
    - IND_NAT_ACAO: obrigatório, valores válidos [01, 02, 03, 04, 05, 06, 07, 08, 09, 12, 13, 14, 15, 16, 17, 19, 99]
    - DESC_DEC_JUD: opcional, até 100 caracteres
    - DT_SENT_JUD: opcional, formato ddmmaaaa, data válida
    
    Nota: Este registro deve ser gerado tantas vezes quantas ações judiciais forem utilizadas
    no período da escrituração. A partir do período de apuração Janeiro/2020, ao informar
    um dos códigos de 12 a 19 no campo IND_NAT_ACAO, deve ser detalhado no registro filho "1011".
    Esta validação deve ser feita em uma camada superior.
    
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
    # Remove primeiro e último se vazios (formato padrão SPED: |1010|...|)
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
    if reg != "1010":
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
    
    # Extrai todos os campos (7 campos no total)
    num_proc = obter_campo(1)
    id_sec_jud = obter_campo(2)
    id_vara = obter_campo(3)
    ind_nat_acao = obter_campo(4)
    desc_dec_jud = obter_campo(5)
    dt_sent_jud = obter_campo(6)
    
    # Validações básicas dos campos obrigatórios
    
    # NUM_PROC: obrigatório, até 20 caracteres
    if not num_proc or len(num_proc) > 20:
        return None
    
    # ID_SEC_JUD: obrigatório
    if not id_sec_jud:
        return None
    
    # ID_VARA: obrigatório, 2 caracteres
    if not id_vara or len(id_vara) != 2:
        return None
    
    # IND_NAT_ACAO: obrigatório, valores válidos [01, 02, 03, 04, 05, 06, 07, 08, 09, 12, 13, 14, 15, 16, 17, 19, 99]
    valores_validos_ind_nat_acao = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "12", "13", "14", "15", "16", "17", "19", "99"]
    if not ind_nat_acao or ind_nat_acao not in valores_validos_ind_nat_acao:
        return None
    
    # DESC_DEC_JUD: opcional, até 100 caracteres
    if desc_dec_jud and len(desc_dec_jud) > 100:
        return None
    
    # DT_SENT_JUD: opcional, formato ddmmaaaa, data válida
    dt_sent_jud_valida = False
    dt_sent_jud_obj = None
    if dt_sent_jud:
        dt_sent_jud_valida, dt_sent_jud_obj = _validar_data(dt_sent_jud)
        if not dt_sent_jud_valida:
            return None
    
    # Função auxiliar para formatar data
    def fmt_data(d):
        return d.strftime("%d/%m/%Y") if d else ""
    
    # Monta o resultado
    descricoes_ind_nat_acao = {
        "01": "Decisão judicial transitada em julgado, a favor da pessoa jurídica",
        "02": "Decisão judicial não transitada em julgado, a favor da pessoa jurídica",
        "03": "Decisão judicial oriunda de liminar em mandado de segurança",
        "04": "Decisão judicial oriunda de liminar em medida cautelar",
        "05": "Decisão judicial oriunda de antecipação de tutela",
        "06": "Decisão judicial vinculada a depósito administrativo ou judicial em montante integral",
        "07": "Medida judicial em que a pessoa jurídica não é o autor",
        "08": "Súmula vinculante aprovada pelo STF ou STJ",
        "09": "Decisão judicial oriunda de liminar em mandado de segurança coletivo",
        "12": "Decisão judicial não transitada em julgado, a favor da pessoa jurídica - Exigibilidade suspensa de contribuição",
        "13": "Decisão judicial oriunda de liminar em mandado de segurança - Exigibilidade suspensa de contribuição",
        "14": "Decisão judicial oriunda de liminar em medida cautelar - Exigibilidade suspensa de contribuição",
        "15": "Decisão judicial oriunda de antecipação de tutela - Exigibilidade suspensa de contribuição",
        "16": "Decisão judicial vinculada a depósito administrativo ou judicial em montante integral - Exigibilidade suspensa de contribuição",
        "17": "Medida judicial em que a pessoa jurídica não é o autor - Exigibilidade suspensa de contribuição",
        "19": "Decisão judicial oriunda de liminar em mandado de segurança coletivo - Exigibilidade suspensa de contribuição",
        "99": "Outros"
    }
    
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "NUM_PROC": {
            "titulo": "Identificação do Número do Processo Judicial",
            "valor": num_proc
        },
        "ID_SEC_JUD": {
            "titulo": "Identificação da Seção Judiciária",
            "valor": id_sec_jud
        },
        "ID_VARA": {
            "titulo": "Identificação da Vara",
            "valor": id_vara
        },
        "IND_NAT_ACAO": {
            "titulo": "Indicador da Natureza da Ação Judicial",
            "valor": ind_nat_acao,
            "descricao": descricoes_ind_nat_acao.get(ind_nat_acao, "")
        }
    }
    
    # DESC_DEC_JUD: opcional
    if desc_dec_jud:
        resultado["DESC_DEC_JUD"] = {
            "titulo": "Descrição Resumida dos Efeitos Tributários abrangidos pela Decisão Judicial proferida",
            "valor": desc_dec_jud
        }
    else:
        resultado["DESC_DEC_JUD"] = {
            "titulo": "Descrição Resumida dos Efeitos Tributários abrangidos pela Decisão Judicial proferida",
            "valor": ""
        }
    
    # DT_SENT_JUD: opcional
    if dt_sent_jud:
        resultado["DT_SENT_JUD"] = {
            "titulo": "Data da Sentença/Decisão Judicial",
            "valor": dt_sent_jud,
            "valor_formatado": fmt_data(dt_sent_jud_obj)
        }
    else:
        resultado["DT_SENT_JUD"] = {
            "titulo": "Data da Sentença/Decisão Judicial",
            "valor": "",
            "valor_formatado": ""
        }
    
    return resultado


def validar_1010(linhas):
    """
    Valida uma ou mais linhas do registro 1010 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |1010|NUM_PROC|ID_SEC_JUD|ID_VARA|IND_NAT_ACAO|DESC_DEC_JUD|DT_SENT_JUD|
        
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
        resultado = _processar_linha_1010(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
