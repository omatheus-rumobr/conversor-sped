import re
import json
from datetime import datetime


def _processar_linha_0005(linha):
    """
    Processa uma única linha do registro 0005 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |0005|FANTASIA|CEP|END|NUM|COMPL|BAIRRO|FONE|FAX|EMAIL|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |0005|...|)
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
    if reg != "0005":
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
    
    # Extrai todos os campos (10 campos no total)
    fantasia = obter_campo(1)
    cep = obter_campo(2)
    end = obter_campo(3)
    num = obter_campo(4)
    compl = obter_campo(5)
    bairro = obter_campo(6)
    fone = obter_campo(7)
    fax = obter_campo(8)
    email = obter_campo(9)
    
    # Validações básicas dos campos obrigatórios
    # FANTASIA: obrigatório
    if not fantasia:
        return None
    
    # CEP: obrigatório, 8 dígitos numéricos
    if not cep:
        return None
    # Remove formatação do CEP (hífens, pontos, etc.)
    cep_limpo = cep.replace("-", "").replace(".", "").replace(" ", "")
    if not cep_limpo.isdigit() or len(cep_limpo) != 8:
        return None
    
    # END: obrigatório
    if not end:
        return None
    
    # BAIRRO: obrigatório
    if not bairro:
        return None
    
    # Validação básica de email (se preenchido)
    def validar_email(email_str):
        if not email_str:
            return True  # Campo opcional
        # Validação básica: deve conter @ e pelo menos um ponto após o @
        if "@" in email_str and "." in email_str.split("@")[1]:
            return True
        return False
    
    if email and not validar_email(email):
        return None
    
    # Monta o dicionário com título e valor
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "FANTASIA": {
            "titulo": "Nome de Fantasia",
            "valor": fantasia
        },
        "CEP": {
            "titulo": "Código de Endereçamento Postal",
            "valor": cep
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
        },
        "FONE": {
            "titulo": "Número do Telefone (DDD+FONE)",
            "valor": fone
        },
        "FAX": {
            "titulo": "Número do Fax",
            "valor": fax
        },
        "EMAIL": {
            "titulo": "Endereço do Correio Eletrônico",
            "valor": email
        }
    }
    
    return resultado


def validar_0005_fiscal(linhas):
    """
    Valida e processa uma ou múltiplas linhas do registro 0005 (Dados Complementares da Entidade) do SPED.
    
    Registro obrigatório utilizado para complementar as informações de identificação do informante do arquivo.
    
    Args:
        linhas: Pode ser:
                - Uma string com uma linha do SPED
                - Uma lista de strings (cada string é uma linha)
                - Uma string com múltiplas linhas separadas por \\n
                Formato: |0005|FANTASIA|CEP|END|NUM|COMPL|BAIRRO|FONE|FAX|EMAIL|
        
    Returns:
        str: JSON com um array contendo os campos validados de cada linha processada.
             Retorna um array vazio [] se nenhuma linha válida for encontrada.
             Retorna None se o input for inválido.
        
    Validações principais:
        - Campo REG deve ser exatamente "0005"
        - FANTASIA: obrigatório, nome de fantasia
        - CEP: obrigatório, código de endereçamento postal (8 dígitos)
        - END: obrigatório, logradouro e endereço
        - NUM: opcional, número do imóvel
        - COMPL: opcional, dados complementares do endereço
        - BAIRRO: obrigatório, bairro
        - FONE: opcional, número do telefone
        - FAX: opcional, número do fax
        - EMAIL: opcional, endereço de email (validado se preenchido)
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
        resultado = _processar_linha_0005(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    # Retorna JSON com array de resultados
    return json.dumps(resultados, ensure_ascii=False, indent=2)