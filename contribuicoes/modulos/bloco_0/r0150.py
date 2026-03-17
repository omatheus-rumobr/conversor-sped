import json


def _validar_cpf(cpf):
    """
    Valida o formato básico do CPF (11 dígitos).
    Valida também o dígito verificador (DV).
    """
    if not cpf:
        return False
    
    # Remove formatação
    cpf_limpo = cpf.replace(".", "").replace("-", "").replace(" ", "")
    
    if not cpf_limpo.isdigit() or len(cpf_limpo) != 11:
        return False
    
    # Validação do dígito verificador
    # Verifica se todos os dígitos são iguais (CPF inválido)
    if len(set(cpf_limpo)) == 1:
        return False
    
    # Calcula primeiro dígito verificador
    multiplicadores1 = [10, 9, 8, 7, 6, 5, 4, 3, 2]
    soma = sum(int(cpf_limpo[i]) * multiplicadores1[i] for i in range(9))
    resto = soma % 11
    dv1 = 0 if resto < 2 else 11 - resto
    
    if int(cpf_limpo[9]) != dv1:
        return False
    
    # Calcula segundo dígito verificador
    multiplicadores2 = [11, 10, 9, 8, 7, 6, 5, 4, 3, 2]
    soma = sum(int(cpf_limpo[i]) * multiplicadores2[i] for i in range(10))
    resto = soma % 11
    dv2 = 0 if resto < 2 else 11 - resto
    
    if int(cpf_limpo[10]) != dv2:
        return False
    
    return True


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


def _normalizar_cod_pais(cod_pais):
    """
    Normaliza o código do país para 5 dígitos.
    Aceita códigos com 4 ou 5 dígitos (desprezando zero à esquerda).
    """
    if not cod_pais:
        return None
    
    cod_pais_limpo = cod_pais.strip()
    
    # Remove zeros à esquerda e depois adiciona zeros à esquerda até ter 5 dígitos
    if cod_pais_limpo.isdigit():
        cod_pais_int = int(cod_pais_limpo)
        return f"{cod_pais_int:05d}"
    
    return None


def _eh_brasil(cod_pais):
    """
    Verifica se o código do país é Brasil (01058 ou 1058).
    """
    cod_normalizado = _normalizar_cod_pais(cod_pais)
    return cod_normalizado == "01058"


def _processar_linha_0150(linha):
    """
    Processa uma única linha do registro 0150 e retorna um dicionário.
    
    Formato:
      |0150|COD_PART|NOME|COD_PAIS|CNPJ|CPF|IE|COD_MUN|SUFRAMA|END|NUM|COMPL|BAIRRO|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "0150"
    - COD_PART: obrigatório, até 60 caracteres
    - NOME: obrigatório, até 100 caracteres
    - COD_PAIS: obrigatório, 4 ou 5 dígitos, deve existir na tabela de países (validação externa)
    - CNPJ: opcional, 14 dígitos, sem formatação, validar DV
      - Não deve ser preenchido se COD_PAIS diferente de Brasil
      - Mutuamente excludente com CPF
      - Obrigatório se COD_PAIS = Brasil e CPF não informado
    - CPF: opcional, 11 dígitos, sem formatação, validar DV
      - Não deve ser preenchido se COD_PAIS diferente de Brasil
      - Mutuamente excludente com CNPJ
      - Obrigatório se COD_PAIS = Brasil e CNPJ não informado
    - IE: opcional, até 14 caracteres
    - COD_MUN: opcional, 7 dígitos, obrigatório se COD_PAIS = Brasil
      - Deve existir na tabela IBGE (validação externa)
    - SUFRAMA: opcional, 9 caracteres, validar DV se informado
    - END: opcional, até 60 caracteres
    - NUM: opcional
    - COMPL: opcional, até 60 caracteres
    - BAIRRO: opcional, até 60 caracteres
    
    Nota: Este registro é obrigatório para participantes informados nos registros dos Blocos A, C, D ou F,
    exceto quando identificados diretamente pelo CNPJ ou CPF nos registros.
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
    # Remove primeiro e último se vazios (formato padrão SPED: |0150|...|)
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
    if reg != "0150":
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
    
    # Extrai todos os campos (13 campos no total)
    cod_part = obter_campo(1)
    nome = obter_campo(2)
    cod_pais = obter_campo(3)
    cnpj = obter_campo(4)
    cpf = obter_campo(5)
    ie = obter_campo(6)
    cod_mun = obter_campo(7)
    suframa = obter_campo(8)
    end = obter_campo(9)
    num = obter_campo(10)
    compl = obter_campo(11)
    bairro = obter_campo(12)
    
    # Validações básicas dos campos obrigatórios
    
    # COD_PART: obrigatório, até 60 caracteres
    if not cod_part or len(cod_part) > 60:
        return None
    
    # NOME: obrigatório, até 100 caracteres
    if not nome or len(nome) > 100:
        return None
    
    # COD_PAIS: obrigatório, 4 ou 5 dígitos
    if not cod_pais:
        return None
    
    cod_pais_normalizado = _normalizar_cod_pais(cod_pais)
    if not cod_pais_normalizado:
        return None
    
    eh_brasil_flag = _eh_brasil(cod_pais)
    
    # CNPJ: opcional, mas regras especiais para Brasil
    cnpj_valido = False
    if cnpj:
        # Não deve ser preenchido se COD_PAIS diferente de Brasil
        if not eh_brasil_flag:
            return None
        
        # Remove formatação para validação
        cnpj_limpo = cnpj.replace(".", "").replace("/", "").replace("-", "").replace(" ", "")
        
        # Deve ter exatamente 14 dígitos numéricos
        if not cnpj_limpo.isdigit() or len(cnpj_limpo) != 14:
            return None
        
        # Verifica se o valor original tinha formatação (não permitido)
        if cnpj != cnpj_limpo:
            return None
        
        # Valida DV do CNPJ
        if not _validar_cnpj(cnpj_limpo):
            return None
        
        cnpj_valido = True
    
    # CPF: opcional, mas regras especiais para Brasil
    cpf_valido = False
    if cpf:
        # Não deve ser preenchido se COD_PAIS diferente de Brasil
        if not eh_brasil_flag:
            return None
        
        # Remove formatação para validação
        cpf_limpo = cpf.replace(".", "").replace("-", "").replace(" ", "")
        
        # Deve ter exatamente 11 dígitos numéricos
        if not cpf_limpo.isdigit() or len(cpf_limpo) != 11:
            return None
        
        # Verifica se o valor original tinha formatação (não permitido)
        if cpf != cpf_limpo:
            return None
        
        # Valida DV do CPF
        if not _validar_cpf(cpf_limpo):
            return None
        
        cpf_valido = True
    
    # CNPJ e CPF são mutuamente excludentes
    if cnpj_valido and cpf_valido:
        return None
    
    # Se COD_PAIS = Brasil, obrigatoriamente um dos campos (CNPJ ou CPF) deve ser preenchido
    if eh_brasil_flag and not cnpj_valido and not cpf_valido:
        return None
    
    # IE: opcional, até 14 caracteres
    if ie and len(ie) > 14:
        return None
    
    # COD_MUN: obrigatório se COD_PAIS = Brasil, opcional caso contrário
    if eh_brasil_flag:
        if not cod_mun or not cod_mun.isdigit() or len(cod_mun) != 7:
            return None
    elif cod_mun:
        # Se não for Brasil, pode estar vazio ou preenchido com 9999999
        if cod_mun != "9999999" and (not cod_mun.isdigit() or len(cod_mun) != 7):
            return None
    
    # SUFRAMA: opcional, se informado deve ter 9 caracteres e DV válido
    if suframa:
        if not _validar_suframa(suframa):
            return None
    
    # END: opcional, até 60 caracteres
    if end and len(end) > 60:
        return None
    
    # NUM: opcional, sem validação específica
    
    # COMPL: opcional, até 60 caracteres
    if compl and len(compl) > 60:
        return None
    
    # BAIRRO: opcional, até 60 caracteres
    if bairro and len(bairro) > 60:
        return None
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "COD_PART": {
            "titulo": "Código de identificação do participante no arquivo",
            "valor": cod_part
        },
        "NOME": {
            "titulo": "Nome pessoal ou empresarial do participante",
            "valor": nome
        },
        "COD_PAIS": {
            "titulo": "Código do país do participante, conforme a tabela indicada no item 3.2.1",
            "valor": cod_pais_normalizado
        }
    }
    
    # CNPJ: opcional
    if cnpj:
        resultado["CNPJ"] = {
            "titulo": "CNPJ do participante",
            "valor": cnpj
        }
    else:
        resultado["CNPJ"] = {
            "titulo": "CNPJ do participante",
            "valor": ""
        }
    
    # CPF: opcional
    if cpf:
        resultado["CPF"] = {
            "titulo": "CPF do participante",
            "valor": cpf
        }
    else:
        resultado["CPF"] = {
            "titulo": "CPF do participante",
            "valor": ""
        }
    
    # IE: opcional
    if ie:
        resultado["IE"] = {
            "titulo": "Inscrição Estadual do participante",
            "valor": ie
        }
    else:
        resultado["IE"] = {
            "titulo": "Inscrição Estadual do participante",
            "valor": ""
        }
    
    # COD_MUN: opcional (obrigatório se Brasil)
    if cod_mun:
        resultado["COD_MUN"] = {
            "titulo": "Código do município, conforme a tabela IBGE",
            "valor": cod_mun
        }
    else:
        resultado["COD_MUN"] = {
            "titulo": "Código do município, conforme a tabela IBGE",
            "valor": ""
        }
    
    # SUFRAMA: opcional
    if suframa:
        resultado["SUFRAMA"] = {
            "titulo": "Número de inscrição do participante na Suframa",
            "valor": suframa
        }
    else:
        resultado["SUFRAMA"] = {
            "titulo": "Número de inscrição do participante na Suframa",
            "valor": ""
        }
    
    # END: opcional
    if end:
        resultado["END"] = {
            "titulo": "Logradouro e endereço do imóvel",
            "valor": end
        }
    else:
        resultado["END"] = {
            "titulo": "Logradouro e endereço do imóvel",
            "valor": ""
        }
    
    # NUM: opcional
    if num:
        resultado["NUM"] = {
            "titulo": "Número do imóvel",
            "valor": num
        }
    else:
        resultado["NUM"] = {
            "titulo": "Número do imóvel",
            "valor": ""
        }
    
    # COMPL: opcional
    if compl:
        resultado["COMPL"] = {
            "titulo": "Dados complementares do endereço",
            "valor": compl
        }
    else:
        resultado["COMPL"] = {
            "titulo": "Dados complementares do endereço",
            "valor": ""
        }
    
    # BAIRRO: opcional
    if bairro:
        resultado["BAIRRO"] = {
            "titulo": "Bairro em que o imóvel está situado",
            "valor": bairro
        }
    else:
        resultado["BAIRRO"] = {
            "titulo": "Bairro em que o imóvel está situado",
            "valor": ""
        }
    
    return resultado


def validar_0150(linhas):
    """
    Valida uma ou mais linhas do registro 0150 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |0150|COD_PART|NOME|COD_PAIS|CNPJ|CPF|IE|COD_MUN|SUFRAMA|END|NUM|COMPL|BAIRRO|
        
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
        resultado = _processar_linha_0150(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
