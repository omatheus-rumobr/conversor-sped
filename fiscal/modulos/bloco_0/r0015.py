import re
import json
from datetime import datetime


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


def _processar_linha_0015(linha):
    """
    Processa uma única linha do registro 0015 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |0015|UF_ST|IE_ST|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |0015|...|)
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
    if reg != "0015":
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
    
    # Extrai todos os campos (3 campos no total)
    uf_st = obter_campo(1)
    ie_st = obter_campo(2)
    
    # Validações básicas dos campos obrigatórios
    # UF_ST: obrigatório, deve ser sigla válida de UF
    if not uf_st or not _validar_uf(uf_st):
        return None
    
    # IE_ST: obrigatório, até 14 caracteres
    # Validação: valida a Inscrição Estadual, considerando a UF informada
    # Como não temos acesso ao algoritmo de validação específico de cada UF,
    # validamos apenas o formato básico (até 14 caracteres, não vazio)
    if not ie_st or len(ie_st) > 14:
        return None
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "UF_ST": {
            "titulo": "Sigla da Unidade da Federação do Contribuinte Substituído",
            "valor": uf_st.upper()
        },
        "IE_ST": {
            "titulo": "Inscrição Estadual do Contribuinte Substituto",
            "valor": ie_st
        }
    }
    
    return resultado


def validar_0015(linhas):
    """
    Valida uma ou mais linhas do registro 0015 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |0015|UF_ST|IE_ST|
        
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
        resultado = _processar_linha_0015(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
