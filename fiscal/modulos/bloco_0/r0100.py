import re
import json
from datetime import datetime


def _validar_cnpj(cnpj):
    """
    Valida o formato básico do CNPJ (14 dígitos).
    Não valida o dígito verificador completo, apenas o formato.
    """
    if not cnpj:
        return False
    # Remove formatação
    cnpj_limpo = cnpj.replace(".", "").replace("/", "").replace("-", "").replace(" ", "")
    if not cnpj_limpo.isdigit() or len(cnpj_limpo) != 14:
        return False
    return True


def _validar_cpf(cpf):
    """
    Valida o formato básico do CPF (11 dígitos).
    Não valida o dígito verificador completo, apenas o formato.
    """
    if not cpf:
        return False
    # Remove formatação
    cpf_limpo = cpf.replace(".", "").replace("-", "").replace(" ", "")
    if not cpf_limpo.isdigit() or len(cpf_limpo) != 11:
        return False
    return True


def _validar_email(email):
    """
    Valida formato básico de email.
    
    Args:
        email: String com endereço de email
        
    Returns:
        bool: True se formato válido, False caso contrário
    """
    if not email:
        return False
    
    # Padrão básico de email: texto@texto.texto
    padrao_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(padrao_email, email))


def _validar_cep(cep):
    """
    Valida formato do CEP (8 dígitos).
    
    Args:
        cep: String com CEP
        
    Returns:
        bool: True se formato válido, False caso contrário
    """
    if not cep:
        return False
    
    # Remove formatação
    cep_limpo = cep.replace(".", "").replace("-", "").replace(" ", "")
    if not cep_limpo.isdigit() or len(cep_limpo) != 8:
        return False
    return True


def _processar_linha_0100(linha):
    """
    Processa uma única linha do registro 0100 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |0100|NOME|CPF|CRC|CNPJ|CEP|END|NUM|COMPL|BAIRRO|FONE|FAX|EMAIL|COD_MUN|
        
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
    
    # CPF: obrigatório, formato válido (11 dígitos)
    if not cpf or not _validar_cpf(cpf):
        return None
    
    # CRC: obrigatório, até 15 caracteres
    if not crc or len(crc) > 15:
        return None
    
    # CNPJ: opcional condicional, se informado deve ter formato válido (14 dígitos)
    if cnpj and not _validar_cnpj(cnpj):
        return None
    
    # CEP: opcional condicional, se informado deve ter formato válido (8 dígitos)
    if cep and not _validar_cep(cep):
        return None
    
    # END: opcional condicional, até 60 caracteres
    if end and len(end) > 60:
        return None
    
    # NUM: opcional condicional, até 10 caracteres
    if num and len(num) > 10:
        return None
    
    # COMPL: opcional condicional, até 60 caracteres
    if compl and len(compl) > 60:
        return None
    
    # BAIRRO: opcional condicional, até 60 caracteres
    if bairro and len(bairro) > 60:
        return None
    
    # FONE: opcional condicional, 11 caracteres
    if fone and len(fone) > 11:
        return None
    
    # FAX: opcional condicional, 11 caracteres
    if fax and len(fax) > 11:
        return None
    
    # EMAIL: obrigatório, formato válido
    if not email or not _validar_email(email):
        return None
    
    # COD_MUN: obrigatório, 7 dígitos
    if not cod_mun or not cod_mun.isdigit() or len(cod_mun) != 7:
        return None
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "NOME": {
            "titulo": "Nome do Contabilista",
            "valor": nome
        },
        "CPF": {
            "titulo": "Número de Inscrição no CPF",
            "valor": cpf
        },
        "CRC": {
            "titulo": "Número de Inscrição no Conselho Regional de Contabilidade",
            "valor": crc
        }
    }
    
    # CNPJ é opcional
    if cnpj:
        resultado["CNPJ"] = {
            "titulo": "Número de Inscrição do Escritório de Contabilidade no CNPJ",
            "valor": cnpj
        }
    else:
        resultado["CNPJ"] = {
            "titulo": "Número de Inscrição do Escritório de Contabilidade no CNPJ",
            "valor": ""
        }
    
    # CEP é opcional
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
    
    # END é opcional
    if end:
        resultado["END"] = {
            "titulo": "Logradouro e Endereço do Imóvel",
            "valor": end
        }
    else:
        resultado["END"] = {
            "titulo": "Logradouro e Endereço do Imóvel",
            "valor": ""
        }
    
    # NUM é opcional
    if num:
        resultado["NUM"] = {
            "titulo": "Número do Imóvel",
            "valor": num
        }
    else:
        resultado["NUM"] = {
            "titulo": "Número do Imóvel",
            "valor": ""
        }
    
    # COMPL é opcional
    if compl:
        resultado["COMPL"] = {
            "titulo": "Dados Complementares do Endereço",
            "valor": compl
        }
    else:
        resultado["COMPL"] = {
            "titulo": "Dados Complementares do Endereço",
            "valor": ""
        }
    
    # BAIRRO é opcional
    if bairro:
        resultado["BAIRRO"] = {
            "titulo": "Bairro em que o Imóvel está Situado",
            "valor": bairro
        }
    else:
        resultado["BAIRRO"] = {
            "titulo": "Bairro em que o Imóvel está Situado",
            "valor": ""
        }
    
    # FONE é opcional
    if fone:
        resultado["FONE"] = {
            "titulo": "Número do Telefone (DDD+FONE)",
            "valor": fone
        }
    else:
        resultado["FONE"] = {
            "titulo": "Número do Telefone (DDD+FONE)",
            "valor": ""
        }
    
    # FAX é opcional
    if fax:
        resultado["FAX"] = {
            "titulo": "Número do Fax",
            "valor": fax
        }
    else:
        resultado["FAX"] = {
            "titulo": "Número do Fax",
            "valor": ""
        }
    
    resultado["EMAIL"] = {
        "titulo": "Endereço do Correio Eletrônico",
        "valor": email
    }
    
    resultado["COD_MUN"] = {
        "titulo": "Código do Município",
        "valor": cod_mun
    }
    
    return resultado


def validar_0100_fiscal(linhas):
    """
    Valida uma ou mais linhas do registro 0100 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |0100|NOME|CPF|CRC|CNPJ|CEP|END|NUM|COMPL|BAIRRO|FONE|FAX|EMAIL|COD_MUN|
        
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
