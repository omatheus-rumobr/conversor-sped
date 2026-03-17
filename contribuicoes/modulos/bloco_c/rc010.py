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


def _processar_linha_c010(linha):
    """
    Processa uma única linha do registro C010 e retorna um dicionário.
    
    Formato:
      |C010|CNPJ|IND_ESCRI|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "C010"
    - CNPJ: obrigatório, número de inscrição do estabelecimento no CNPJ (14 dígitos, com validação de DV)
      - O estabelecimento informado neste registro deve estar cadastrado no Registro 0140 (validação em camada superior)
    - IND_ESCRI: opcional, indicador da apuração das contribuições e créditos (1 dígito)
      - Valores válidos: [1, 2]
      - 1: Apuração com base nos registros de consolidação das operações por NF-e (C180 e C190) e por ECF (C490)
      - 2: Apuração com base no registro individualizado de NF-e (C100 e C170) e de ECF (C400)
    
    Nota: Este registro tem o objetivo de identificar o estabelecimento da pessoa jurídica a que se referem
    as operações e documentos fiscais informados neste bloco. Só devem ser escriturados no Registro C010 os
    estabelecimentos que efetivamente tenham realizado aquisição, venda ou devolução de mercadorias, bens e
    produtos, mediante emissão de documento fiscal definido pela legislação do ICMS e do IPI, que devam ser
    escrituradas no Bloco C.
    
    O estabelecimento que não realizou operações passíveis de registro nesse bloco, no período da escrituração,
    não deve ser identificado no Registro C010.
    
    Para cada estabelecimento cadastrado em "C010", deve ser informado nos registros de nível inferior
    (Registros Filho) as operações próprias de prestação ou de contratação de serviços, mediante emissão de
    documento fiscal, no mercado interno ou externo.
    
    Este campo deve ser preenchido se no arquivo de registros da escrituração importado pelo PVA, constar em
    relação às operações documentadas por Nota Fiscal Eletrônica – NF-e, código 55, tanto registros individualizados
    por documento fiscal (C100) como registros consolidados dos documentos fiscais (C180 e/ou C190).
    
    Deve igualmente ser preenchido se no arquivo da escrituração constar, em relação às operações emitidas por
    equipamento Emissor de Cupom Fiscal – ECF, tanto registros individualizados por ECF (C400) como registros
    consolidados de documentos fiscais emitidos por ECF (C490).
    
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
    # Remove primeiro e último se vazios (formato padrão SPED: |C010|...|)
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
    if reg != "C010":
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
    
    # Extrai todos os campos (3 campos no total)
    cnpj = obter_campo(1)
    ind_escri = obter_campo(2)
    
    # Validações básicas dos campos obrigatórios
    
    # CNPJ: obrigatório, 14 dígitos, com validação de DV
    if not cnpj or not _validar_cnpj(cnpj):
        return None
    
    # IND_ESCRI: opcional, valores válidos [1, 2]
    if ind_escri:
        ind_escri_validos = ["1", "2"]
        if ind_escri not in ind_escri_validos:
            return None
    
    # Função auxiliar para formatar CNPJ
    def fmt_cnpj(cnpj_str):
        if cnpj_str and len(cnpj_str) == 14:
            return f"{cnpj_str[:2]}.{cnpj_str[2:5]}.{cnpj_str[5:8]}/{cnpj_str[8:12]}-{cnpj_str[12:14]}"
        return cnpj_str
    
    # Descrições do campo IND_ESCRI
    descricoes_ind_escri = {
        "1": "Apuração com base nos registros de consolidação das operações por NF-e (C180 e C190) e por ECF (C490)",
        "2": "Apuração com base no registro individualizado de NF-e (C100 e C170) e de ECF (C400)"
    }
    
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
    
    # Adiciona IND_ESCRI apenas se preenchido
    if ind_escri:
        resultado["IND_ESCRI"] = {
            "titulo": "Indicador da apuração das contribuições e créditos, na escrituração das operações por NF-e e ECF, no período",
            "valor": ind_escri,
            "descricao": descricoes_ind_escri.get(ind_escri, "")
        }
    
    return resultado


def validar_c010(linhas):
    """
    Valida uma ou mais linhas do registro C010 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |C010|CNPJ|IND_ESCRI|
        
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
        resultado = _processar_linha_c010(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
