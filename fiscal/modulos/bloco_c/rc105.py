import re
import json
from datetime import datetime


# Lista de siglas válidas de UF brasileiras
UFS_VALIDAS = [
    'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA',
    'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN',
    'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
]


def _processar_linha_c105(linha):
    """
    Processa uma única linha do registro C105 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |C105|OPER|UF|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |C105|...|)
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
    if reg != "C105":
        return None
    
    # Função auxiliar para obter campo ou string vazia
    def obter_campo(indice):
        if indice < len(partes):
            valor = partes[indice].strip()
            return valor if valor else ""
        return ""
    
    # Extrai todos os campos (3 campos no total)
    oper = obter_campo(1)
    uf = obter_campo(2)
    
    # Validação do campo OPER: [0, 1, 2]
    if not oper or oper not in ["0", "1", "2"]:
        return None
    
    # Validação do campo UF: deve ser uma sigla válida de UF
    if not uf:
        return None
    
    uf_upper = uf.upper()
    if uf_upper not in UFS_VALIDAS:
        return None
    
    # Monta o dicionário com título e valor
    descricoes_oper = {
        "0": "Combustíveis e Lubrificantes",
        "1": "Leasing de veículos ou faturamento direto",
        "2": "Recusa de recebimento"
    }
    
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "OPER": {
            "titulo": "Indicador do Tipo de Operação",
            "valor": oper,
            "descricao": descricoes_oper.get(oper, "")
        },
        "UF": {
            "titulo": "Sigla da UF de Destino do ICMS ST",
            "valor": uf_upper
        }
    }
    
    return resultado


def validar_c105_fiscal(linhas):
    """
    Valida e processa uma ou múltiplas linhas do registro C105 (Operações com ICMS ST Recolhido para UF
    Diversa do Destinatário do Documento Fiscal) do SPED.
    
    Este registro tem por objetivo identificar a UF destinatária do recolhimento do ICMS ST, quando esta for
    diversa da UF do destinatário do produto.
    
    Args:
        linhas: Pode ser:
                - Uma string com uma linha do SPED
                - Uma lista de strings (cada string é uma linha)
                - Uma string com múltiplas linhas separadas por \\n
                Formato: |C105|OPER|UF|
        
    Returns:
        str: JSON com um array contendo os campos validados de cada linha processada.
             Retorna um array vazio [] se nenhuma linha válida for encontrada.
             Retorna None se o input for inválido.
        
    Validações principais:
        - Campo REG deve ser exatamente "C105"
        - OPER: valores válidos [0, 1, 2]
          - 0: Combustíveis e Lubrificantes
          - 1: Leasing de veículos ou faturamento direto
          - 2: Recusa de recebimento
        - UF: deve ser uma sigla válida de unidade da federação brasileira
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
        resultado = _processar_linha_c105(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    # Retorna JSON com array de resultados
    return json.dumps(resultados, ensure_ascii=False, indent=2)