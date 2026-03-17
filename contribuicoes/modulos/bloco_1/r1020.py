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


def _processar_linha_1020(linha):
    """
    Processa uma única linha do registro 1020 e retorna um dicionário.
    
    Formato:
      |1020|NUM_PROC|IND_NAT_ACAO|DT_DEC_ADM|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "1020"
    - NUM_PROC: obrigatório, até 20 caracteres
    - IND_NAT_ACAO: obrigatório, valores válidos [01, 02, 03, 04, 05, 06, 99]
    - DT_DEC_ADM: obrigatório, formato ddmmaaaa, data válida
    
    Nota: Este registro deve ser gerado tantas vezes quantos processos administrativos forem
    utilizados no período da escrituração.
    
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
    # Remove primeiro e último se vazios (formato padrão SPED: |1020|...|)
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
    if reg != "1020":
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
    
    # Extrai todos os campos (4 campos no total)
    num_proc = obter_campo(1)
    ind_nat_acao = obter_campo(2)
    dt_dec_adm = obter_campo(3)
    
    # Validações básicas dos campos obrigatórios
    
    # NUM_PROC: obrigatório, até 20 caracteres
    if not num_proc or len(num_proc) > 20:
        return None
    
    # IND_NAT_ACAO: obrigatório, valores válidos [01, 02, 03, 04, 05, 06, 99]
    valores_validos_ind_nat_acao = ["01", "02", "03", "04", "05", "06", "99"]
    if not ind_nat_acao or ind_nat_acao not in valores_validos_ind_nat_acao:
        return None
    
    # DT_DEC_ADM: obrigatório, formato ddmmaaaa, data válida
    dt_dec_adm_valida, dt_dec_adm_obj = _validar_data(dt_dec_adm)
    if not dt_dec_adm_valida:
        return None
    
    # Função auxiliar para formatar data
    def fmt_data(d):
        return d.strftime("%d/%m/%Y") if d else ""
    
    # Monta o resultado
    descricoes_ind_nat_acao = {
        "01": "Processo Administrativo de Consulta",
        "02": "Despacho Decisório",
        "03": "Ato Declaratório Executivo",
        "04": "Ato Declaratório Interpretativo",
        "05": "Decisão Administrativa de DRJ ou do CARF",
        "06": "Auto de Infração",
        "99": "Outros"
    }
    
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "NUM_PROC": {
            "titulo": "Identificação do Processo Administrativo ou da Decisão Administrativa",
            "valor": num_proc
        },
        "IND_NAT_ACAO": {
            "titulo": "Indicador da Natureza da Ação, decorrente de Processo Administrativo na Secretaria da Receita Federal do Brasil",
            "valor": ind_nat_acao,
            "descricao": descricoes_ind_nat_acao.get(ind_nat_acao, "")
        },
        "DT_DEC_ADM": {
            "titulo": "Data do Despacho/Decisão Administrativa",
            "valor": dt_dec_adm,
            "valor_formatado": fmt_data(dt_dec_adm_obj)
        }
    }
    
    return resultado


def validar_1020(linhas):
    """
    Valida uma ou mais linhas do registro 1020 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |1020|NUM_PROC|IND_NAT_ACAO|DT_DEC_ADM|
        
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
        resultado = _processar_linha_1020(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
