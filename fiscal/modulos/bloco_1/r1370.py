import re
import json
from datetime import datetime


def _processar_linha_1370(linha):
    """
    Processa uma única linha do registro 1370 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |1370|NUM_BICO|COD_ITEM|NUM_TANQUE|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |1370|...|)
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
    if reg != "1370":
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
    
    # Extrai todos os campos (4 campos no total)
    num_bico = obter_campo(1)
    cod_item = obter_campo(2)
    num_tanque = obter_campo(3)
    
    # Validações básicas dos campos obrigatórios
    # NUM_BICO: obrigatório, numérico, até 3 dígitos
    if not num_bico:
        return None
    try:
        num_bico_int = int(num_bico)
        if num_bico_int < 0 or len(num_bico) > 3:
            return None
    except ValueError:
        return None
    
    # COD_ITEM: obrigatório, até 60 caracteres
    if not cod_item or len(cod_item) > 60:
        return None
    
    # NUM_TANQUE: obrigatório, até 3 caracteres
    if not num_tanque or len(num_tanque) > 3:
        return None
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "NUM_BICO": {
            "titulo": "Número sequencial do bico ligado a bomba",
            "valor": num_bico
        },
        "COD_ITEM": {
            "titulo": "Código do Produto, constante do registro 0200",
            "valor": cod_item
        },
        "NUM_TANQUE": {
            "titulo": "Tanque que armazena o combustível",
            "valor": num_tanque
        }
    }
    
    return resultado


def validar_1370_fiscal(linhas):
    """
    Valida uma ou mais linhas do registro 1370 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |1370|NUM_BICO|COD_ITEM|NUM_TANQUE|
        
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
        resultado = _processar_linha_1370(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
