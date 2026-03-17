import re
import json
from datetime import datetime


def _processar_linha_c111(linha):
    """
    Processa uma única linha do registro C111 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |C111|NUM_PROC|IND_PROC|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |C111|...|)
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
    if reg != "C111":
        return None
    
    # Função auxiliar para obter campo ou string vazia
    def obter_campo(indice):
        if indice < len(partes):
            valor = partes[indice].strip()
            return valor if valor else ""
        return ""
    
    # Extrai todos os campos (3 campos no total)
    num_proc = obter_campo(1)
    ind_proc = obter_campo(2)
    
    # Validação do campo NUM_PROC: obrigatório, máximo 60 caracteres
    if not num_proc:
        return None
    
    if len(num_proc) > 60:
        return None
    
    # Validação do campo IND_PROC: valores válidos [0, 1, 2, 3, 9]
    if not ind_proc or ind_proc not in ["0", "1", "2", "3", "9"]:
        return None
    
    # Monta o dicionário com título e valor
    descricoes_ind_proc = {
        "0": "SEFAZ",
        "1": "Justiça Federal",
        "2": "Justiça Estadual",
        "3": "SECEX/SRF",
        "9": "Outros"
    }
    
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "NUM_PROC": {
            "titulo": "Identificação do Processo ou Ato Concessório",
            "valor": num_proc
        },
        "IND_PROC": {
            "titulo": "Indicador da Origem do Processo",
            "valor": ind_proc,
            "descricao": descricoes_ind_proc.get(ind_proc, "")
        }
    }
    
    return resultado


def validar_c111(linhas):
    """
    Valida e processa uma ou múltiplas linhas do registro C111 (Processo Referenciado) do SPED.
    
    Este registro deve ser apresentado, obrigatoriamente, quando no campo "Informações Complementares" da nota
    fiscal constar a discriminação de processos referenciados no documento fiscal.
    
    Args:
        linhas: Pode ser:
                - Uma string com uma linha do SPED
                - Uma lista de strings (cada string é uma linha)
                - Uma string com múltiplas linhas separadas por \\n
                Formato: |C111|NUM_PROC|IND_PROC|
        
    Returns:
        str: JSON com um array contendo os campos validados de cada linha processada.
             Retorna um array vazio [] se nenhuma linha válida for encontrada.
             Retorna None se o input for inválido.
        
    Validações principais:
        - Campo REG deve ser exatamente "C111"
        - NUM_PROC: obrigatório, identificação do processo ou ato concessório (máximo 60 caracteres)
        - IND_PROC: obrigatório, valores válidos [0, 1, 2, 3, 9]
          - 0: SEFAZ
          - 1: Justiça Federal
          - 2: Justiça Estadual
          - 3: SECEX/SRF
          - 9: Outros
        - Não podem ser informados dois ou mais registros com o mesmo conteúdo no campo NUM_PROC para um mesmo registro C110
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
        resultado = _processar_linha_c111(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    # Retorna JSON com array de resultados
    return json.dumps(resultados, ensure_ascii=False, indent=2)