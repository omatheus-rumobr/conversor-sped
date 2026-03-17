import json


def _validar_cnpj(cnpj):
    """
    Valida o formato básico do CNPJ (14 dígitos).
    Valida também o dígito verificador (DV).
    """
    if not cnpj:
        return False
    
    # Remove formatação
    cnpj_limpo = cnpj.replace(".", "").replace("/", "").replace("-", "").replace(" ", "")
    
    if not cnpj_limpo.isdigit() or len(cnpj_limpo) != 14:
        return False
    
    # Validação do dígito verificador
    # Verifica se todos os dígitos são iguais (CNPJ inválido)
    if len(set(cnpj_limpo)) == 1:
        return False
    
    # Calcula primeiro dígito verificador
    multiplicadores1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma = sum(int(cnpj_limpo[i]) * multiplicadores1[i] for i in range(12))
    resto = soma % 11
    dv1 = 0 if resto < 2 else 11 - resto
    
    if int(cnpj_limpo[12]) != dv1:
        return False
    
    # Calcula segundo dígito verificador
    multiplicadores2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma = sum(int(cnpj_limpo[i]) * multiplicadores2[i] for i in range(13))
    resto = soma % 11
    dv2 = 0 if resto < 2 else 11 - resto
    
    if int(cnpj_limpo[13]) != dv2:
        return False
    
    return True


def _processar_linha_i010(linha):
    """
    Processa uma única linha do registro I010 e retorna um dicionário.
    
    Formato:
      |I010|CNPJ|IND_ATIV|INFO_COMPL|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "I010"
    - CNPJ: obrigatório, número de inscrição da pessoa jurídica no CNPJ (14 dígitos)
      - Deve ser validado o dígito verificador (DV)
      - O estabelecimento informado deve estar cadastrado no Registro 0140
    - IND_ATIV: obrigatório, indicador de operações realizadas no período
      - Valores válidos: [01, 02, 03, 04, 05, 06]
    - INFO_COMPL: opcional, informação complementar
    
    Nota: Este registro tem o objetivo de identificar o estabelecimento da pessoa jurídica
    a que se referem as operações informadas no Registro filho I100. Só devem ser escriturados
    no Registro I010 os estabelecimentos da pessoa jurídica que efetivamente tenham realizado
    operações passíveis de escrituração neste bloco.
    
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
    # Remove primeiro e último se vazios (formato padrão SPED: |I010|...|)
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
    if reg != "I010":
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
    cnpj = obter_campo(1)
    ind_ativ = obter_campo(2)
    info_compl = obter_campo(3)
    
    # Validações básicas dos campos obrigatórios
    
    # CNPJ: obrigatório, número de inscrição da pessoa jurídica no CNPJ (14 dígitos)
    # Remove formatação para validar
    cnpj_limpo = cnpj.replace(".", "").replace("/", "").replace("-", "").replace(" ", "")
    if not cnpj or len(cnpj_limpo) != 14 or not _validar_cnpj(cnpj):
        return None
    
    # IND_ATIV: obrigatório, valores válidos [01, 02, 03, 04, 05, 06]
    ind_ativ_validos = ["01", "02", "03", "04", "05", "06"]
    if not ind_ativ or ind_ativ not in ind_ativ_validos:
        return None
    
    # INFO_COMPL: opcional, informação complementar
    # Não há validação específica além de ser texto livre
    
    # Função auxiliar para formatar CNPJ
    def fmt_cnpj(cnpj_str):
        if not cnpj_str:
            return ""
        cnpj_limpo = cnpj_str.replace(".", "").replace("/", "").replace("-", "").replace(" ", "")
        if len(cnpj_limpo) == 14:
            # Formata CNPJ: 00.000.000/0000-00
            return f"{cnpj_limpo[:2]}.{cnpj_limpo[2:5]}.{cnpj_limpo[5:8]}/{cnpj_limpo[8:12]}-{cnpj_limpo[12:]}"
        return cnpj_str
    
    # Descrições dos campos
    descricoes_ind_ativ = {
        "01": "Exclusivamente operações de Instituições Financeiras e Assemelhadas",
        "02": "Exclusivamente operações de Seguros Privados",
        "03": "Exclusivamente operações de Previdência Complementar",
        "04": "Exclusivamente operações de Capitalização",
        "05": "Exclusivamente operações de Planos de Assistência à Saúde",
        "06": "Realizou operações referentes a mais de um dos indicadores acima"
    }
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "CNPJ": {
            "titulo": "Número de inscrição da pessoa jurídica no CNPJ",
            "valor": cnpj,
            "valor_formatado": fmt_cnpj(cnpj)
        },
        "IND_ATIV": {
            "titulo": "Indicador de operações realizadas no período",
            "valor": ind_ativ,
            "descricao": descricoes_ind_ativ.get(ind_ativ, "")
        },
        "INFO_COMPL": {
            "titulo": "Informação Complementar",
            "valor": info_compl
        }
    }
    
    return resultado


def validar_i010(linhas):
    """
    Valida uma ou mais linhas do registro I010 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |I010|CNPJ|IND_ATIV|INFO_COMPL|
        
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
        resultado = _processar_linha_i010(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
