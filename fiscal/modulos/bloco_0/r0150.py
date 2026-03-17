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


def _processar_linha_0150(linha):
    """
    Processa uma única linha do registro 0150 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |0150|COD_PART|NOME|COD_PAIS|CNPJ|CPF|IE|COD_MUN|SUFRAMA|END|NUM|COMPL|BAIRRO|
        
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
    # COD_PART: obrigatório
    if not cod_part:
        return None
    
    # NOME: obrigatório
    if not nome:
        return None
    
    # COD_PAIS: obrigatório, pode ser 4 ou 5 dígitos
    if not cod_pais:
        return None
    # Remove zeros à esquerda para normalizar
    cod_pais_limpo = cod_pais.lstrip('0')
    if not cod_pais_limpo.isdigit():
        return None
    # Aceita 4 ou 5 dígitos (com ou sem zero à esquerda)
    if len(cod_pais) < 4 or len(cod_pais) > 5:
        return None
    
    # Verifica se é Brasil (01058 ou 1058)
    cod_pais_normalizado = cod_pais.lstrip('0')
    is_brasil = cod_pais_normalizado == "1058" or cod_pais == "01058" or cod_pais == "1058"
    
    # Validação: CNPJ ou CPF deve ser preenchido (obrigatoriamente um deles)
    # Se for Brasil, pelo menos um deve estar preenchido
    if is_brasil:
        if not cnpj and not cpf:
            return None
        # CNPJ e CPF são mutuamente excludentes
        if cnpj and cpf:
            return None
        # Valida formato se preenchido
        if cnpj and not _validar_cnpj(cnpj):
            return None
        if cpf and not _validar_cpf(cpf):
            return None
    else:
        # Se não for Brasil, CNPJ e CPF não devem ser preenchidos
        if cnpj or cpf:
            return None
    
    # COD_MUN: obrigatório se COD_PAIS = 01058 ou 1058 (Brasil)
    if is_brasil:
        if not cod_mun:
            return None
        # Valida formato: 7 dígitos
        if not cod_mun.isdigit() or len(cod_mun) != 7:
            return None
    else:
        # Se não for Brasil, pode estar vazio ou ser 9999999
        if cod_mun and cod_mun != "9999999":
            # Se preenchido e não for 9999999, valida formato
            if not cod_mun.isdigit() or len(cod_mun) != 7:
                return None
    
    # END: obrigatório
    if not end:
        return None
    
    # Validação básica de SUFRAMA (se preenchido, deve ter formato válido)
    if suframa:
        # SUFRAMA tem 9 caracteres e dígito verificador
        suframa_limpo = suframa.replace("-", "").replace(" ", "")
        if not suframa_limpo.isdigit() or len(suframa_limpo) != 9:
            return None
    
    # Monta o dicionário com título e valor
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "COD_PART": {
            "titulo": "Código de Identificação do Participante no Arquivo",
            "valor": cod_part
        },
        "NOME": {
            "titulo": "Nome Pessoal ou Empresarial do Participante",
            "valor": nome
        },
        "COD_PAIS": {
            "titulo": "Código do País do Participante",
            "valor": cod_pais
        },
        "CNPJ": {
            "titulo": "CNPJ do Participante",
            "valor": cnpj
        },
        "CPF": {
            "titulo": "CPF do Participante",
            "valor": cpf
        },
        "IE": {
            "titulo": "Inscrição Estadual do Participante",
            "valor": ie
        },
        "COD_MUN": {
            "titulo": "Código do Município (IBGE)",
            "valor": cod_mun
        },
        "SUFRAMA": {
            "titulo": "Número de Inscrição do Participante na SUFRAMA",
            "valor": suframa
        },
        "END": {
            "titulo": "Logradouro e Endereço do Imóvel",
            "valor": end
        },
        "NUM": {
            "titulo": "Número do Imóvel",
            "valor": num
        },
        "COMPL": {
            "titulo": "Dados Complementares do Endereço",
            "valor": compl
        },
        "BAIRRO": {
            "titulo": "Bairro em que o Imóvel está Situado",
            "valor": bairro
        }
    }
    
    return resultado


def validar_0150(linhas):
    """
    Valida e processa uma ou múltiplas linhas do registro 0150 (Tabela de Cadastro do Participante) do SPED.
    
    Registro utilizado para informações cadastrais das pessoas físicas ou jurídicas envolvidas nas transações comerciais
    com o estabelecimento, no período.
    
    Args:
        linhas: Pode ser:
                - Uma string com uma linha do SPED
                - Uma lista de strings (cada string é uma linha)
                - Uma string com múltiplas linhas separadas por \\n
                Formato: |0150|COD_PART|NOME|COD_PAIS|CNPJ|CPF|IE|COD_MUN|SUFRAMA|END|NUM|COMPL|BAIRRO|
        
    Returns:
        str: JSON com um array contendo os campos validados de cada linha processada.
             Retorna um array vazio [] se nenhuma linha válida for encontrada.
             Retorna None se o input for inválido.
        
    Validações principais:
        - Campo REG deve ser exatamente "0150"
        - COD_PART: obrigatório
        - NOME: obrigatório
        - COD_PAIS: obrigatório, código do país (4 ou 5 dígitos)
        - CNPJ ou CPF: obrigatoriamente um deles deve ser preenchido (se COD_PAIS = 01058 ou 1058)
        - CNPJ e CPF são mutuamente excludentes
        - COD_MUN: obrigatório se COD_PAIS = 01058 ou 1058 (Brasil), 7 dígitos
        - END: obrigatório
        - Demais campos: opcionais, mas validados quando preenchidos
    """
    if linhas is None:
        return None
    
    # Lista para armazenar as linhas a processar
    linhas_para_processar = []
    
    # Se for uma lista, processa cada item
    if isinstance(linhas, list):
        linhas_para_processar = linhas
    # Se for uma string, verifica se tem múltiplas linhas
    elif isinstance(linhas, str):
        # Se contém \n, divide em linhas
        if '\n' in linhas:
            linhas_para_processar = linhas.split('\n')
        else:
            # String única
            linhas_para_processar = [linhas]
    else:
        return None
    
    # Lista para armazenar os resultados válidos
    resultados = []
    
    # Processa cada linha
    for linha in linhas_para_processar:
        resultado = _processar_linha_0150(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    # Retorna JSON com array de resultados
    return json.dumps(resultados, ensure_ascii=False, indent=2)