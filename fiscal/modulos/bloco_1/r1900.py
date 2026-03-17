import re
import json
from datetime import datetime


def _processar_linha_1900(linha):
    """
    Processa uma única linha do registro 1900 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |1900|IND_APUR_ICMS|DESCR_COMPL_OUT_APUR|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |1900|...|)
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
    if reg != "1900":
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
    ind_apur_icms = obter_campo(1)
    descr_compl_out_apur = obter_campo(2)
    
    # Validações dos campos obrigatórios
    
    # IND_APUR_ICMS: obrigatório, valores válidos: ["3","4","5","6","7","8"]
    ind_apur_icms_validos = ["3", "4", "5", "6", "7", "8"]
    if ind_apur_icms not in ind_apur_icms_validos:
        return None
    
    # DESCR_COMPL_OUT_APUR: obrigatório (não pode estar vazio)
    if not descr_compl_out_apur:
        return None
    
    # Mapeamento de códigos para descrições
    ind_apur_icms_desc = {
        "3": "APURAÇÃO 1",
        "4": "APURAÇÃO 2",
        "5": "APURAÇÃO 3",
        "6": "APURAÇÃO 4",
        "7": "APURAÇÃO 5",
        "8": "APURAÇÃO 6"
    }
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "IND_APUR_ICMS": {
            "titulo": "Indicador de outra apuração do ICMS",
            "valor": ind_apur_icms,
            "descricao": ind_apur_icms_desc.get(ind_apur_icms, "")
        },
        "DESCR_COMPL_OUT_APUR": {
            "titulo": "Descrição complementar de Outra Apuração do ICMS",
            "valor": descr_compl_out_apur
        }
    }
    
    return resultado


def validar_1900(linhas):
    """
    Valida uma ou mais linhas do registro 1900 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |1900|IND_APUR_ICMS|DESCR_COMPL_OUT_APUR|
        
    Returns:
        String JSON com array de objetos contendo os campos validados.
        Cada objeto tem a estrutura {"CAMPO": {"titulo": "...", "valor": "...", "descricao": "..."}}.
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
        resultado = _processar_linha_1900(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
