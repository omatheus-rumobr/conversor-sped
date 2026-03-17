import re
import json
from datetime import datetime


def _processar_linha_c110(linha):
    """
    Processa uma única linha do registro C110 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |C110|COD_INF|TXT_COMPL|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |C110|...|)
    if partes and not partes[0]:
        partes = partes[1:]
    if partes and not partes[-1]:
        partes = partes[:-1]
    
    # Verifica se tem pelo menos o campo REG
    if len(partes) < 1:
        return None
    
    # Extrai o campo REG
    reg = partes[0].strip().upper() if partes else ""
    
    # Validação do campo REG
    if reg != "C110":
        return None
    
    # Função auxiliar para obter campo ou string vazia
    def obter_campo(indice):
        if indice < len(partes):
            valor = partes[indice].strip()
            return valor if valor else ""
        return ""
    
    # Extrai todos os campos (3 campos no total)
    cod_inf = obter_campo(1)
    txt_compl = obter_campo(2)
    
    # Validação do campo COD_INF: obrigatório, deve estar preenchido
    if not cod_inf:
        return None
    
    # Validação básica: COD_INF deve ter no máximo 6 caracteres (conforme documentação)
    if len(cod_inf) > 6:
        return None
    
    # Monta o dicionário com título e valor
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "COD_INF": {
            "titulo": "Código da Informação Complementar do Documento Fiscal",
            "valor": cod_inf
        },
        "TXT_COMPL": {
            "titulo": "Descrição Complementar do Código de Referência",
            "valor": txt_compl
        }
    }
    
    return resultado


def validar_c110(linhas):
    """
    Valida e processa uma ou múltiplas linhas do registro C110 (Informação Complementar da Nota Fiscal) do SPED.
    
    Este registro tem por objetivo identificar os dados contidos no campo Informações Complementares da Nota Fiscal,
    que sejam de interesse do fisco, conforme dispõe a legislação.
    
    Args:
        linhas: Pode ser:
                - Uma string com uma linha do SPED
                - Uma lista de strings (cada string é uma linha)
                - Uma string com múltiplas linhas separadas por \\n
                Formato: |C110|COD_INF|TXT_COMPL|
        
    Returns:
        str: JSON com um array contendo os campos validados de cada linha processada.
             Retorna um array vazio [] se nenhuma linha válida for encontrada.
             Retorna None se o input for inválido.
        
    Validações principais:
        - Campo REG deve ser exatamente "C110"
        - COD_INF: obrigatório, código da informação complementar (campo 02 do Registro 0450)
        - TXT_COMPL: opcional, descrição complementar do código de referência
        - Não podem ser informados para um mesmo documento fiscal, dois ou mais registros com o mesmo conteúdo no campo COD_INF
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
        resultado = _processar_linha_c110(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    # Retorna JSON com array de resultados
    return json.dumps(resultados, ensure_ascii=False, indent=2)