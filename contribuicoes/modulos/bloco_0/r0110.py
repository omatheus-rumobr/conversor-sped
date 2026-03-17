import json


def _processar_linha_0110(linha):
    """
    Processa uma única linha do registro 0110 e retorna um dicionário.
    
    Formato:
      |0110|COD_INC_TRIB|IND_APRO_CRED|COD_TIPO_CONT|IND_REG_CUM|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "0110"
    - COD_INC_TRIB: obrigatório, valores válidos [1, 2, 3]
    - IND_APRO_CRED: opcional, valores válidos [1, 2]
      - Obrigatório quando COD_INC_TRIB = 1 ou 3
    - COD_TIPO_CONT: opcional, valores válidos [1, 2]
    - IND_REG_CUM: opcional, valores válidos [1, 2, 9]
      - Obrigatório quando COD_INC_TRIB = 2
    
    Notas:
    - Se COD_TIPO_CONT = 2, deve existir algum registro M210/M610 com COD_CONT = 02, 03, 52 ou 53 (validação externa)
    - Se IND_APRO_CRED = 2, o registro 0111 é obrigatório (validação externa)
    - O campo IND_REG_CUM pode não constar no arquivo para versões antigas do PVA (validação externa)
    
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
    # Remove primeiro e último se vazios (formato padrão SPED: |0110|...|)
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
    if reg != "0110":
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
    
    # Extrai todos os campos (5 campos no total)
    cod_inc_trib = obter_campo(1)
    ind_apro_cred = obter_campo(2)
    cod_tipo_cont = obter_campo(3)
    ind_reg_cum = obter_campo(4)
    
    # Validações básicas dos campos obrigatórios
    
    # COD_INC_TRIB: obrigatório, valores válidos [1, 2, 3]
    if not cod_inc_trib or cod_inc_trib not in ["1", "2", "3"]:
        return None
    
    # IND_APRO_CRED: obrigatório quando COD_INC_TRIB = 1 ou 3, opcional caso contrário
    if cod_inc_trib in ["1", "3"]:
        if not ind_apro_cred or ind_apro_cred not in ["1", "2"]:
            return None
    elif ind_apro_cred and ind_apro_cred not in ["1", "2"]:
        return None
    
    # COD_TIPO_CONT: opcional, valores válidos [1, 2]
    if cod_tipo_cont and cod_tipo_cont not in ["1", "2"]:
        return None
    
    # IND_REG_CUM: obrigatório quando COD_INC_TRIB = 2, opcional caso contrário
    if cod_inc_trib == "2":
        if not ind_reg_cum or ind_reg_cum not in ["1", "2", "9"]:
            return None
    elif ind_reg_cum and ind_reg_cum not in ["1", "2", "9"]:
        return None
    
    # Monta o resultado
    descricoes_inc_trib = {
        "1": "Escrituração de operações com incidência exclusivamente no regime não-cumulativo",
        "2": "Escrituração de operações com incidência exclusivamente no regime cumulativo",
        "3": "Escrituração de operações com incidência nos regimes não-cumulativo e cumulativo"
    }
    
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "COD_INC_TRIB": {
            "titulo": "Código indicador da incidência tributária no período",
            "valor": cod_inc_trib,
            "descricao": descricoes_inc_trib.get(cod_inc_trib, "")
        }
    }
    
    # IND_APRO_CRED: obrigatório quando COD_INC_TRIB = 1 ou 3
    if ind_apro_cred:
        descricoes_apro_cred = {
            "1": "Método de Apropriação Direta",
            "2": "Método de Rateio Proporcional (Receita Bruta)"
        }
        resultado["IND_APRO_CRED"] = {
            "titulo": "Código indicador de método de apropriação de créditos comuns",
            "valor": ind_apro_cred,
            "descricao": descricoes_apro_cred.get(ind_apro_cred, "")
        }
    else:
        resultado["IND_APRO_CRED"] = {
            "titulo": "Código indicador de método de apropriação de créditos comuns",
            "valor": ""
        }
    
    # COD_TIPO_CONT: opcional
    if cod_tipo_cont:
        descricoes_tipo_cont = {
            "1": "Apuração da Contribuição Exclusivamente a Alíquota Básica",
            "2": "Apuração da Contribuição a Alíquotas Específicas (Diferenciadas e/ou por Unidade de Medida de Produto)"
        }
        resultado["COD_TIPO_CONT"] = {
            "titulo": "Código indicador do Tipo de Contribuição Apurada no Período",
            "valor": cod_tipo_cont,
            "descricao": descricoes_tipo_cont.get(cod_tipo_cont, "")
        }
    else:
        resultado["COD_TIPO_CONT"] = {
            "titulo": "Código indicador do Tipo de Contribuição Apurada no Período",
            "valor": ""
        }
    
    # IND_REG_CUM: obrigatório quando COD_INC_TRIB = 2
    if ind_reg_cum:
        descricoes_reg_cum = {
            "1": "Regime de Caixa – Escrituração consolidada (Registro F500)",
            "2": "Regime de Competência - Escrituração consolidada (Registro F550)",
            "9": "Regime de Competência - Escrituração detalhada, com base nos registros dos Blocos A, C, D e F"
        }
        resultado["IND_REG_CUM"] = {
            "titulo": "Código indicador do critério de escrituração e apuração adotado",
            "valor": ind_reg_cum,
            "descricao": descricoes_reg_cum.get(ind_reg_cum, "")
        }
    else:
        resultado["IND_REG_CUM"] = {
            "titulo": "Código indicador do critério de escrituração e apuração adotado",
            "valor": ""
        }
    
    return resultado


def validar_0110(linhas):
    """
    Valida uma ou mais linhas do registro 0110 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |0110|COD_INC_TRIB|IND_APRO_CRED|COD_TIPO_CONT|IND_REG_CUM|
        
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
        resultado = _processar_linha_0110(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
