import re
import json
from datetime import datetime


def _processar_linha_c101(linha):
    """
    Processa uma única linha do registro C101 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |C101|VL_FCP_UF_DEST|VL_ICMS_UF_DEST|VL_ICMS_UF_REM|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |C101|...|)
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
    if reg != "C101":
        return None
    
    # Função auxiliar para obter campo ou string vazia
    def obter_campo(indice):
        if indice < len(partes):
            valor = partes[indice].strip()
            return valor if valor else ""
        return ""
    
    # Extrai todos os campos (4 campos no total)
    vl_fcp_uf_dest = obter_campo(1)
    vl_icms_uf_dest = obter_campo(2)
    vl_icms_uf_rem = obter_campo(3)
    
    # Validação de valores numéricos (devem ser números válidos e obrigatórios)
    def validar_valor(valor_str):
        if not valor_str:
            return False  # Campos são obrigatórios
        try:
            float(valor_str.replace(",", "."))
            return True
        except ValueError:
            return False
    
    # Valida valores monetários (todos obrigatórios)
    if not validar_valor(vl_fcp_uf_dest):
        return None
    if not validar_valor(vl_icms_uf_dest):
        return None
    if not validar_valor(vl_icms_uf_rem):
        return None
    
    # Monta o dicionário com título e valor
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "VL_FCP_UF_DEST": {
            "titulo": "Valor Total Relativo ao Fundo de Combate à Pobreza (FCP) da UF de Destino",
            "valor": vl_fcp_uf_dest
        },
        "VL_ICMS_UF_DEST": {
            "titulo": "Valor Total do ICMS Interestadual para a UF de Destino",
            "valor": vl_icms_uf_dest
        },
        "VL_ICMS_UF_REM": {
            "titulo": "Valor Total do ICMS Interestadual para a UF do Remetente",
            "valor": vl_icms_uf_rem
        }
    }
    
    return resultado


def validar_c101(linhas):
    """
    Valida e processa uma ou múltiplas linhas do registro C101 (Informação Complementar dos Documentos Fiscais
    quando das Operações Interestaduais Destinadas a Consumidor Final Não Contribuinte EC 87/15) do SPED.
    
    Este registro tem por objetivo prestar informações complementares constantes da NF-e quando das operações
    interestaduais destinadas a consumidor final NÃO contribuinte do ICMS, segundo dispôs a Emenda Constitucional 87/2015.
    
    Args:
        linhas: Pode ser:
                - Uma string com uma linha do SPED
                - Uma lista de strings (cada string é uma linha)
                - Uma string com múltiplas linhas separadas por \\n
                Formato: |C101|VL_FCP_UF_DEST|VL_ICMS_UF_DEST|VL_ICMS_UF_REM|
        
    Returns:
        str: JSON com um array contendo os campos validados de cada linha processada.
             Retorna um array vazio [] se nenhuma linha válida for encontrada.
             Retorna None se o input for inválido.
        
    Validações principais:
        - Campo REG deve ser exatamente "C101"
        - VL_FCP_UF_DEST: obrigatório, valor numérico
        - VL_ICMS_UF_DEST: obrigatório, valor numérico
        - VL_ICMS_UF_REM: obrigatório, valor numérico
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
        resultado = _processar_linha_c101(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    # Retorna JSON com array de resultados
    return json.dumps(resultados, ensure_ascii=False, indent=2)