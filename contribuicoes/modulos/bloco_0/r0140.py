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


def _validar_suframa(suframa):
    """
    Valida o formato básico da inscrição SUFRAMA (9 caracteres).
    Valida também o dígito verificador (DV) usando módulo 11.
    """
    if not suframa:
        return False
    
    # Remove formatação
    suframa_limpo = suframa.replace(".", "").replace("-", "").replace(" ", "")
    
    if not suframa_limpo.isdigit() or len(suframa_limpo) != 9:
        return False
    
    # Validação do dígito verificador (módulo 11)
    # Os 8 primeiros dígitos são o número base
    # O 9º dígito é o DV
    numero_base = suframa_limpo[:8]
    dv_informado = int(suframa_limpo[8])
    
    multiplicadores = [2, 3, 4, 5, 6, 7, 8, 9]
    soma = sum(int(numero_base[i]) * multiplicadores[i] for i in range(8))
    resto = soma % 11
    
    # Se resto for 0 ou 1, DV é 0; caso contrário, DV é 11 - resto
    dv_calculado = 0 if resto < 2 else 11 - resto
    
    return dv_informado == dv_calculado


def _validar_uf(uf):
    """
    Valida se a UF é uma sigla válida do Brasil.
    
    Args:
        uf: String com sigla da UF
        
    Returns:
        bool: True se válida, False caso contrário
    """
    ufs_validas = [
        'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA',
        'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN',
        'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
    ]
    return uf.upper() in ufs_validas


def _processar_linha_0140(linha):
    """
    Processa uma única linha do registro 0140 e retorna um dicionário.
    
    Formato:
      |0140|COD_EST|NOME|CNPJ|UF|IE|COD_MUN|IM|SUFRAMA|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "0140"
    - COD_EST: opcional, até 60 caracteres
    - NOME: obrigatório, até 100 caracteres
    - CNPJ: obrigatório, 14 dígitos, sem formatação, validar DV
    - UF: obrigatório, sigla válida
    - IE: opcional, até 14 caracteres
    - COD_MUN: obrigatório, 7 dígitos, deve existir na tabela IBGE (validação externa)
    - IM: opcional, inscrição municipal
    - SUFRAMA: opcional, 9 caracteres, validar DV se informado
    
    Nota: Este registro é obrigatório para o estabelecimento matriz.
    Para demais estabelecimentos, é obrigatório apenas se auferiram receitas,
    realizaram operações geradoras de créditos ou sofreram retenções na fonte.
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
    # Remove primeiro e último se vazios (formato padrão SPED: |0140|...|)
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
    if reg != "0140":
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
    
    # Extrai todos os campos (9 campos no total)
    cod_est = obter_campo(1)
    nome = obter_campo(2)
    cnpj = obter_campo(3)
    uf = obter_campo(4)
    ie = obter_campo(5)
    cod_mun = obter_campo(6)
    im = obter_campo(7)
    suframa = obter_campo(8)
    
    # Validações básicas dos campos obrigatórios
    
    # COD_EST: opcional, até 60 caracteres
    if cod_est and len(cod_est) > 60:
        return None
    
    # NOME: obrigatório, até 100 caracteres
    if not nome or len(nome) > 100:
        return None
    
    # CNPJ: obrigatório, validar formato e DV
    if not cnpj or not _validar_cnpj(cnpj):
        return None
    
    # UF: obrigatório, deve ser sigla válida
    if not uf or not _validar_uf(uf):
        return None
    
    # IE: opcional, até 14 caracteres
    if ie and len(ie) > 14:
        return None
    
    # COD_MUN: obrigatório, 7 dígitos
    if not cod_mun or not cod_mun.isdigit() or len(cod_mun) != 7:
        return None
    
    # IM: opcional, sem validação específica de formato
    
    # SUFRAMA: opcional, se informado deve ter 9 caracteres e DV válido
    if suframa:
        if not _validar_suframa(suframa):
            return None
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "NOME": {
            "titulo": "Nome empresarial do estabelecimento",
            "valor": nome
        },
        "CNPJ": {
            "titulo": "Número de inscrição do estabelecimento no CNPJ",
            "valor": cnpj
        },
        "UF": {
            "titulo": "Sigla da unidade da federação do estabelecimento",
            "valor": uf
        },
        "COD_MUN": {
            "titulo": "Código do município do domicílio fiscal do estabelecimento, conforme a tabela IBGE",
            "valor": cod_mun
        }
    }
    
    # COD_EST: opcional
    if cod_est:
        resultado["COD_EST"] = {
            "titulo": "Código de identificação do estabelecimento",
            "valor": cod_est
        }
    else:
        resultado["COD_EST"] = {
            "titulo": "Código de identificação do estabelecimento",
            "valor": ""
        }
    
    # IE: opcional
    if ie:
        resultado["IE"] = {
            "titulo": "Inscrição Estadual do estabelecimento, se contribuinte de ICMS",
            "valor": ie
        }
    else:
        resultado["IE"] = {
            "titulo": "Inscrição Estadual do estabelecimento, se contribuinte de ICMS",
            "valor": ""
        }
    
    # IM: opcional
    if im:
        resultado["IM"] = {
            "titulo": "Inscrição Municipal do estabelecimento, se contribuinte do ISS",
            "valor": im
        }
    else:
        resultado["IM"] = {
            "titulo": "Inscrição Municipal do estabelecimento, se contribuinte do ISS",
            "valor": ""
        }
    
    # SUFRAMA: opcional
    if suframa:
        resultado["SUFRAMA"] = {
            "titulo": "Inscrição do estabelecimento na Suframa",
            "valor": suframa
        }
    else:
        resultado["SUFRAMA"] = {
            "titulo": "Inscrição do estabelecimento na Suframa",
            "valor": ""
        }
    
    return resultado


def validar_0140(linhas):
    """
    Valida uma ou mais linhas do registro 0140 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |0140|COD_EST|NOME|CNPJ|UF|IE|COD_MUN|IM|SUFRAMA|
        
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
        resultado = _processar_linha_0140(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
