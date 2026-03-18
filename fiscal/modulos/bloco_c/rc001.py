import re
import json


def validar_c001_fiscal(linha):
    """
    Valida e processa uma linha do registro C001 (Abertura do Bloco C) do SPED.
    
    Este registro tem por objetivo identificar a abertura do bloco C, indicando 
    se há informações sobre documentos fiscais.
    
    Args:
        linha: String com a linha do SPED no formato |C001|IND_MOV|
        
    Returns:
        dict: JSON com os campos validados contendo título e valor, ou None se inválido
        
    Validações:
        - Campo REG deve ser exatamente "C001"
        - Campo IND_MOV deve ser "0" (bloco com dados) ou "1" (bloco sem dados)
    """
    if not linha or not isinstance(linha, str):
        return None
    
    linha = linha.strip()
    
    # Remove espaços e divide por pipe
    partes = [p.strip() for p in linha.split('|') if p.strip()]
    
    # Verifica se tem pelo menos 2 partes (REG e IND_MOV)
    if len(partes) < 2:
        return None
    
    # Extrai os campos
    reg = partes[0].upper() if partes else ""
    ind_mov = partes[1] if len(partes) > 1 else ""
    
    # Validação do campo REG
    if reg != "C001":
        return None
    
    # Validação do campo IND_MOV
    if ind_mov not in ["0", "1"]:
        return None
    
    # Monta o JSON com título e valor
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "IND_MOV": {
            "titulo": "Indicador de Movimento",
            "valor": ind_mov
        }
    }
    
    return json.dumps(resultado, ensure_ascii=False, indent=2)
