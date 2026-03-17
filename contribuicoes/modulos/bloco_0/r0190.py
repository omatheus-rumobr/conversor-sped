import json


def _processar_linha_0190(linha):
    """
    Processa uma única linha do registro 0190 e retorna um dicionário.
    
    Formato:
      |0190|UNID|DESCR|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "0190"
    - UNID: obrigatório, até 6 caracteres
    - DESCR: obrigatório, descrição da unidade de medida
    - Validação: UNID e DESCR não podem ter o mesmo conteúdo
    
    Args:
        linha: String com uma linha do SPED
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |0190|...|)
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
    if reg != "0190":
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
    unid = obter_campo(1)
    descr = obter_campo(2)
    
    # Validações básicas dos campos obrigatórios
    
    # UNID: obrigatório, até 6 caracteres
    if not unid or len(unid) > 6:
        return None
    
    # DESCR: obrigatório
    if not descr:
        return None
    
    # Validação: UNID e DESCR não podem ter o mesmo conteúdo
    if unid.strip().upper() == descr.strip().upper():
        return None
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "UNID": {
            "titulo": "Código da unidade de medida",
            "valor": unid
        },
        "DESCR": {
            "titulo": "Descrição da unidade de medida",
            "valor": descr
        }
    }
    
    return resultado


def validar_0190(linhas):
    """
    Valida uma ou mais linhas do registro 0190 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |0190|UNID|DESCR|
        
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
        resultado = _processar_linha_0190(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
