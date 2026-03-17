import re
import json
from datetime import datetime


def _processar_linha_1710(linha):
    """
    Processa uma única linha do registro 1710 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |1710|NUM_DOC_INI|NUM_DOC_FIN|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |1710|...|)
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
    if reg != "1710":
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
    num_doc_ini = obter_campo(1)
    num_doc_fin = obter_campo(2)
    
    # Validações dos campos obrigatórios
    
    # NUM_DOC_INI: obrigatório, numérico, até 12 dígitos
    if not num_doc_ini:
        return None
    if not num_doc_ini.isdigit() or len(num_doc_ini) > 12:
        return None
    
    # NUM_DOC_FIN: obrigatório, numérico, até 12 dígitos
    if not num_doc_fin:
        return None
    if not num_doc_fin.isdigit() or len(num_doc_fin) > 12:
        return None
    
    # Validação: NUM_DOC_FIN deve ser maior ou igual a NUM_DOC_INI
    # Quando cancelamento não for contínuo, NUM_DOC_INI pode ser igual a NUM_DOC_FIN
    try:
        num_doc_ini_int = int(num_doc_ini)
        num_doc_fin_int = int(num_doc_fin)
        if num_doc_fin_int < num_doc_ini_int:
            return None
    except ValueError:
        return None
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "NUM_DOC_INI": {
            "titulo": "Número do dispositivo autorizado (inutilizado) inicial",
            "valor": num_doc_ini
        },
        "NUM_DOC_FIN": {
            "titulo": "Número do dispositivo autorizado (inutilizado) final",
            "valor": num_doc_fin
        }
    }
    
    return resultado


def validar_1710(linhas):
    """
    Valida uma ou mais linhas do registro 1710 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |1710|NUM_DOC_INI|NUM_DOC_FIN|
        
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
        resultado = _processar_linha_1710(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
