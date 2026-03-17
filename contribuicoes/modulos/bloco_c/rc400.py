import json


def _processar_linha_c400(linha):
    """
    Processa uma única linha do registro C400 e retorna um dicionário.
    
    Formato:
      |C400|COD_MOD|ECF_MOD|ECF_FAB|ECF_CX|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "C400"
    - COD_MOD: obrigatório, código do modelo do documento fiscal (2 caracteres)
      - Valores válidos: [02, 2D]
    - ECF_MOD: obrigatório, modelo do equipamento (20 caracteres)
    - ECF_FAB: obrigatório, número de série de fabricação do ECF (21 caracteres)
    - ECF_CX: obrigatório, número do caixa atribuído ao ECF (3 dígitos)
      - Um mesmo valor do campo ECF_CX não pode ser usado por dois equipamentos ECF ao mesmo tempo
      - Validação: não podem ser informados dois ou mais registros C400 com a mesma combinação de valores
        dos campos COD_MOD, ECF_MOD e ECF_FAB (validação em camada superior)
    
    Nota: Este registro tem por objetivo identificar os equipamentos de ECF e deve ser informado por todos
    os contribuintes que utilizem tais equipamentos na emissão de documentos fiscais.
    
    As operações de vendas com emissão de documento fiscal (códigos 02 e 2D) por ECF podem ser escrituradas
    na EFD-Contribuições, de forma consolidada (Registro C490) ou por ECF (C400), a critério da pessoa jurídica.
    
    Caso a pessoa jurídica opte por escriturar as operações de vendas por ECF, de forma consolidada, no
    Registro C490, não precisa proceder à escrituração do Registro C400 (e registros filhos).
    
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
    # Remove primeiro e último se vazios (formato padrão SPED: |C400|...|)
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
    if reg != "C400":
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
    
    # Extrai todos os campos (5 campos no total)
    cod_mod = obter_campo(1)
    ecf_mod = obter_campo(2)
    ecf_fab = obter_campo(3)
    ecf_cx = obter_campo(4)
    
    # Validações básicas dos campos obrigatórios
    
    # COD_MOD: obrigatório, valores válidos [02, 2D]
    cod_mod_validos = ["02", "2D"]
    if not cod_mod or cod_mod not in cod_mod_validos:
        return None
    
    # ECF_MOD: obrigatório, modelo do equipamento (20 caracteres)
    if not ecf_mod or len(ecf_mod) > 20:
        return None
    
    # ECF_FAB: obrigatório, número de série de fabricação do ECF (21 caracteres)
    if not ecf_fab or len(ecf_fab) > 21:
        return None
    
    # ECF_CX: obrigatório, número do caixa atribuído ao ECF (3 dígitos)
    if not ecf_cx or not ecf_cx.isdigit() or len(ecf_cx) > 3:
        return None
    
    # Descrições dos campos COD_MOD
    descricoes_cod_mod = {
        "02": "Nota Fiscal de Venda a Consumidor",
        "2D": "Cupom Fiscal emitido por ECF"
    }
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "COD_MOD": {
            "titulo": "Código do modelo do documento fiscal, conforme a Tabela 4.1.1",
            "valor": cod_mod,
            "descricao": descricoes_cod_mod.get(cod_mod, "")
        },
        "ECF_MOD": {
            "titulo": "Modelo do equipamento",
            "valor": ecf_mod
        },
        "ECF_FAB": {
            "titulo": "Número de série de fabricação do ECF",
            "valor": ecf_fab
        },
        "ECF_CX": {
            "titulo": "Número do caixa atribuído ao ECF",
            "valor": ecf_cx
        }
    }
    
    return resultado


def validar_c400(linhas):
    """
    Valida uma ou mais linhas do registro C400 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |C400|COD_MOD|ECF_MOD|ECF_FAB|ECF_CX|
        
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
        resultado = _processar_linha_c400(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
