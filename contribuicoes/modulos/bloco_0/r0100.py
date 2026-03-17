import json
import re


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


def _validar_email(email):
    """
    Valida formato básico de email.
    """
    if not email:
        return False
    
    # Padrão básico de email
    padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(padrao, email))


def _processar_linha_0100(linha):
    """
    Processa uma única linha do registro 0100 e retorna um dicionário.
    
    Formato:
      |0100|NOME|CPF|CRC|CNPJ|CEP|END|NUM|COMPL|BAIRRO|FONE|FAX|EMAIL|COD_MUN|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "0100"
    - NOME: obrigatório, até 100 caracteres
    - CPF: obrigatório, 11 dígitos, sem formatação, validar DV
    - CRC: obrigatório, até 15 caracteres
    - CNPJ: opcional, 14 dígitos, sem formatação, validar DV se informado
    - CEP: opcional, 8 dígitos
    - END: opcional, até 60 caracteres
    - NUM: opcional
    - COMPL: opcional, até 60 caracteres
    - BAIRRO: opcional, até 60 caracteres
    - FONE: opcional, até 11 caracteres
    - FAX: opcional, até 11 caracteres
    - EMAIL: opcional, formato de email válido
    - COD_MUN: opcional, 7 dígitos, deve existir na tabela IBGE (validação externa)
    
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
    # Remove primeiro e último se vazios (formato padrão SPED: |0100|...|)
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
    if reg != "0100":
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
    
    # Extrai todos os campos (14 campos no total)
    nome = obter_campo(1)
    cpf = obter_campo(2)
    crc = obter_campo(3)
    cnpj = obter_campo(4)
    cep = obter_campo(5)
    end = obter_campo(6)
    num = obter_campo(7)
    compl = obter_campo(8)
    bairro = obter_campo(9)
    fone = obter_campo(10)
    fax = obter_campo(11)
    email = obter_campo(12)
    cod_mun = obter_campo(13)
    
    # Validações básicas dos campos obrigatórios
    
    # NOME: obrigatório, até 100 caracteres
    if not nome or len(nome) > 100:
        return None
    
    # CPF: obrigatório, 11 dígitos, sem formatação, validar DV
    if not cpf:
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
    
    # CRC: obrigatório, até 15 caracteres
    if not crc or len(crc) > 15:
        return None
    
    # CNPJ: opcional, se informado deve ser válido (14 dígitos, sem formatação, validar DV)
    if cnpj:
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
    
    # CEP: opcional, se informado deve ter 8 dígitos
    if cep:
        cep_limpo = cep.replace("-", "").replace(" ", "")
        if not cep_limpo.isdigit() or len(cep_limpo) != 8:
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
    
    # FONE: opcional, até 11 caracteres
    if fone and len(fone) > 11:
        return None
    
    # FAX: opcional, até 11 caracteres
    if fax and len(fax) > 11:
        return None
    
    # EMAIL: opcional, formato de email válido
    if email and not _validar_email(email):
        return None
    
    # COD_MUN: opcional, 7 dígitos
    if cod_mun:
        if not cod_mun.isdigit() or len(cod_mun) != 7:
            return None
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "NOME": {
            "titulo": "Nome do contabilista",
            "valor": nome
        },
        "CPF": {
            "titulo": "Número de inscrição do contabilista no CPF",
            "valor": cpf
        },
        "CRC": {
            "titulo": "Número de inscrição do contabilista no Conselho Regional de Contabilidade",
            "valor": crc
        }
    }
    
    # CNPJ: opcional
    if cnpj:
        resultado["CNPJ"] = {
            "titulo": "Número de inscrição do escritório de contabilidade no CNPJ",
            "valor": cnpj
        }
    else:
        resultado["CNPJ"] = {
            "titulo": "Número de inscrição do escritório de contabilidade no CNPJ",
            "valor": ""
        }
    
    # CEP: opcional
    if cep:
        resultado["CEP"] = {
            "titulo": "Código de Endereçamento Postal",
            "valor": cep
        }
    else:
        resultado["CEP"] = {
            "titulo": "Código de Endereçamento Postal",
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
    
    # FONE: opcional
    if fone:
        resultado["FONE"] = {
            "titulo": "Número do telefone",
            "valor": fone
        }
    else:
        resultado["FONE"] = {
            "titulo": "Número do telefone",
            "valor": ""
        }
    
    # FAX: opcional
    if fax:
        resultado["FAX"] = {
            "titulo": "Número do fax",
            "valor": fax
        }
    else:
        resultado["FAX"] = {
            "titulo": "Número do fax",
            "valor": ""
        }
    
    # EMAIL: opcional
    if email:
        resultado["EMAIL"] = {
            "titulo": "Endereço do correio eletrônico",
            "valor": email
        }
    else:
        resultado["EMAIL"] = {
            "titulo": "Endereço do correio eletrônico",
            "valor": ""
        }
    
    # COD_MUN: opcional
    if cod_mun:
        resultado["COD_MUN"] = {
            "titulo": "Código do município, conforme tabela IBGE",
            "valor": cod_mun
        }
    else:
        resultado["COD_MUN"] = {
            "titulo": "Código do município, conforme tabela IBGE",
            "valor": ""
        }
    
    return resultado


def validar_0100(linhas):
    """
    Valida uma ou mais linhas do registro 0100 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |0100|NOME|CPF|CRC|CNPJ|CEP|END|NUM|COMPL|BAIRRO|FONE|FAX|EMAIL|COD_MUN|
        
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
        resultado = _processar_linha_0100(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
