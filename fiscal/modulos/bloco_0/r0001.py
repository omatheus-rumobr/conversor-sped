import re
import json
from datetime import datetime


def _processar_linha_0001(linha):
    """
    Processa uma única linha do registro 0001 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |0001|IND_MOV|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |0001|...|)
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
    if reg != "0001":
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
    ind_mov = obter_campo(1)
    
    # Validação do campo IND_MOV: valores válidos [0, 1]
    # Nota: A documentação menciona que o valor válido é [0], mas a descrição do campo indica [0, 1]
    # Vou validar ambos conforme a descrição do campo
    if not ind_mov or ind_mov not in ["0", "1"]:
        return None
    
    # Monta o dicionário com título e valor
    descricoes_ind_mov = {
        "0": "Bloco com dados informados",
        "1": "Bloco sem dados informados"
    }
    
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "IND_MOV": {
            "titulo": "Indicador de Movimento",
            "valor": ind_mov,
            "descricao": descricoes_ind_mov.get(ind_mov, "")
        }
    }
    
    return resultado


def validar_0001(linhas):
    """
    Valida e processa uma ou múltiplas linhas do registro 0001 (Abertura do Bloco 0) do SPED.
    
    Este registro deve ser gerado para abertura do bloco 0 e indica as informações previstas para este bloco.
    
    Args:
        linhas: Pode ser:
                - Uma string com uma linha do SPED
                - Uma lista de strings (cada string é uma linha)
                - Uma string com múltiplas linhas separadas por \\n
                Formato: |0001|IND_MOV|
        
    Returns:
        str: JSON com um array contendo os campos validados de cada linha processada.
             Retorna um array vazio [] se nenhuma linha válida for encontrada.
             Retorna None se o input for inválido.
        
    Validações principais:
        - Campo REG deve ser exatamente "0001"
        - IND_MOV: obrigatório, valores válidos [0, 1]
          - 0: Bloco com dados informados
          - 1: Bloco sem dados informados
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
        resultado = _processar_linha_0001(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    # Retorna JSON com array de resultados
    return json.dumps(resultados, ensure_ascii=False, indent=2)