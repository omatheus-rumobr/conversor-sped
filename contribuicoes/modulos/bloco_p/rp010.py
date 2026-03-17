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


def _processar_linha_p010(linha):
    """
    Processa uma única linha do registro P010 e retorna um dicionário.
    
    Formato:
      |P010|CNPJ|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "P010"
    - CNPJ: obrigatório, número de inscrição do estabelecimento no CNPJ (14 dígitos)
      - Deve ser validado o dígito verificador (DV)
      - O estabelecimento informado deve estar cadastrado no Registro 0140
      - Deverá ter preenchido o respectivo registro filho "0145"
    
    Nota: Este registro tem o objetivo de identificar o estabelecimento da pessoa jurídica
    a que se referem as operações informadas neste bloco. Só devem ser escriturados no Registro
    P010 os estabelecimentos que efetivamente tenham auferido receitas sujeitas à incidência da
    Contribuição Previdenciária sobre a Receita Bruta.
    
    O estabelecimento que não realizou operações passíveis de registro nesse bloco, no período
    da escrituração, não deve ser identificado no Registro P010.
    
    Para cada estabelecimento cadastrado em "P010", deve ser informado nos registros de nível
    inferior (Registros Filho P100 e/ou P110) as informações necessárias para a apuração da
    Contribuição Previdenciária sobre Receitas.
    
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
    # Remove primeiro e último se vazios (formato padrão SPED: |P010|...|)
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
    if reg != "P010":
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
    
    # Extrai todos os campos (2 campos no total)
    cnpj = obter_campo(1)
    
    # Validações básicas dos campos obrigatórios
    
    # CNPJ: obrigatório, número de inscrição do estabelecimento no CNPJ (14 dígitos)
    # Remove formatação para validar
    cnpj_limpo = cnpj.replace(".", "").replace("/", "").replace("-", "").replace(" ", "")
    if not cnpj or len(cnpj_limpo) != 14 or not _validar_cnpj(cnpj):
        return None
    
    # Função auxiliar para formatar CNPJ
    def fmt_cnpj(cnpj_str):
        if not cnpj_str:
            return ""
        cnpj_limpo = cnpj_str.replace(".", "").replace("/", "").replace("-", "").replace(" ", "")
        if len(cnpj_limpo) == 14:
            # Formata CNPJ: 00.000.000/0000-00
            return f"{cnpj_limpo[:2]}.{cnpj_limpo[2:5]}.{cnpj_limpo[5:8]}/{cnpj_limpo[8:12]}-{cnpj_limpo[12:]}"
        return cnpj_str
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "CNPJ": {
            "titulo": "Número de inscrição do estabelecimento no CNPJ",
            "valor": cnpj,
            "valor_formatado": fmt_cnpj(cnpj)
        }
    }
    
    return resultado


def validar_p010(linhas):
    """
    Valida uma ou mais linhas do registro P010 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |P010|CNPJ|
        
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
        resultado = _processar_linha_p010(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
