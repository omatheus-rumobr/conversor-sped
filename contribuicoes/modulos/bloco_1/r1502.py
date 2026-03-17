import json


def validar_valor_numerico(valor_str, decimais=2, obrigatorio=False, positivo=False, nao_negativo=False):
    """
    Valida um valor numérico com precisão decimal específica.

    Args:
        valor_str: String com o valor numérico
        decimais: Número máximo de casas decimais permitidas
        obrigatorio: Se True, o campo não pode estar vazio
        positivo: Se True, o valor deve ser maior que 0
        nao_negativo: Se True, o valor deve ser maior ou igual a 0

    Returns:
        tuple: (True/False, valor float ou None, mensagem de erro ou None)
    """
    if valor_str is None:
        valor_str = ""

    if not valor_str:
        if obrigatorio:
            return False, None, "Campo obrigatório não preenchido"
        return True, 0.0, None

    try:
        valor_float = float(valor_str)

        # Verifica precisão decimal (quando houver ponto decimal)
        partes_decimal = valor_str.split(".")
        if len(partes_decimal) == 2 and len(partes_decimal[1]) > decimais:
            return False, None, f"Valor com mais de {decimais} casas decimais"

        if positivo and valor_float <= 0:
            return False, None, "Valor deve ser maior que zero"
        if nao_negativo and valor_float < 0:
            return False, None, "Valor não pode ser negativo"

        return True, valor_float, None
    except ValueError:
        return False, None, "Valor não é numérico válido"


def _processar_linha_1502(linha, cod_cred_1500=None, vl_cofins_1501=None):
    """
    Processa uma única linha do registro 1502 e retorna um dicionário.
    
    Formato:
      |1502|VL_CRED_COFINS_TRIB_MI|VL_CRED_COFINS_NT_MI|VL_CRED_COFINS_EXP|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "1502"
    - VL_CRED_COFINS_TRIB_MI: opcional, numérico com 2 decimais, não negativo
      - Só deve ser preenchido se COD_CRED do registro 1500 iniciar com "1"
    - VL_CRED_COFINS_NT_MI: opcional, numérico com 2 decimais, não negativo
      - Só deve ser preenchido se COD_CRED do registro 1500 iniciar com "2"
    - VL_CRED_COFINS_EXP: opcional, numérico com 2 decimais, não negativo
      - Só deve ser preenchido se COD_CRED do registro 1500 iniciar com "3"
    
    Nota: Este registro deve ser preenchido quando CST_COFINS do registro 1501 for referente
    a operações com direito a crédito (códigos 53, 54, 55, 56, 63, 64, 65 ou 66).
    As validações condicionais relacionadas ao COD_CRED do registro 1500 devem ser feitas
    em uma camada superior que tenha acesso a esse registro.
    A validação de que a soma dos valores deve ser igual ao VL_COFINS do registro 1501 deve
    ser feita em uma camada superior.
    
    Args:
        linha: String com uma linha do SPED
        cod_cred_1500: Código do crédito do registro 1500 (opcional, para validação condicional)
        vl_cofins_1501: Valor do crédito COFINS do registro 1501 (opcional, para validação de soma)
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |1502|...|)
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
    if reg != "1502":
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
    vl_cred_cofins_trib_mi = obter_campo(1)
    vl_cred_cofins_nt_mi = obter_campo(2)
    vl_cred_cofins_exp = obter_campo(3)
    
    # Validações básicas dos campos
    
    # VL_CRED_COFINS_TRIB_MI: opcional, numérico com 2 decimais, não negativo
    ok1, val1, _ = validar_valor_numerico(vl_cred_cofins_trib_mi, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok1:
        return None
    if val1 is None:
        val1 = 0.0
    
    # VL_CRED_COFINS_NT_MI: opcional, numérico com 2 decimais, não negativo
    ok2, val2, _ = validar_valor_numerico(vl_cred_cofins_nt_mi, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok2:
        return None
    if val2 is None:
        val2 = 0.0
    
    # VL_CRED_COFINS_EXP: opcional, numérico com 2 decimais, não negativo
    ok3, val3, _ = validar_valor_numerico(vl_cred_cofins_exp, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok3:
        return None
    if val3 is None:
        val3 = 0.0
    
    # Validações condicionais relacionadas ao COD_CRED do registro 1500
    # Estas validações são feitas apenas se cod_cred_1500 for informado
    if cod_cred_1500:
        cod_cred_str = str(cod_cred_1500).strip()
        if cod_cred_str:
            primeiro_digito = cod_cred_str[0] if len(cod_cred_str) > 0 else ""
            
            # VL_CRED_COFINS_TRIB_MI só deve ser preenchido se COD_CRED iniciar com "1"
            if primeiro_digito != "1" and val1 > 0:
                return None
            
            # VL_CRED_COFINS_NT_MI só deve ser preenchido se COD_CRED iniciar com "2"
            if primeiro_digito != "2" and val2 > 0:
                return None
            
            # VL_CRED_COFINS_EXP só deve ser preenchido se COD_CRED iniciar com "3"
            if primeiro_digito != "3" and val3 > 0:
                return None
    
    # Validação: pelo menos um dos campos deve ter valor > 0
    if val1 == 0.0 and val2 == 0.0 and val3 == 0.0:
        return None
    
    # Função auxiliar para formatar valores monetários
    def fmt_valor(v):
        return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        }
    }
    
    # VL_CRED_COFINS_TRIB_MI: opcional
    if vl_cred_cofins_trib_mi:
        resultado["VL_CRED_COFINS_TRIB_MI"] = {
            "titulo": "Parcela do Crédito de COFINS, vinculada a Receita Tributada no Mercado Interno",
            "valor": vl_cred_cofins_trib_mi,
            "valor_formatado": fmt_valor(val1)
        }
    else:
        resultado["VL_CRED_COFINS_TRIB_MI"] = {
            "titulo": "Parcela do Crédito de COFINS, vinculada a Receita Tributada no Mercado Interno",
            "valor": "",
            "valor_formatado": ""
        }
    
    # VL_CRED_COFINS_NT_MI: opcional
    if vl_cred_cofins_nt_mi:
        resultado["VL_CRED_COFINS_NT_MI"] = {
            "titulo": "Parcela do Crédito de COFINS, vinculada a Receita Não Tributada no Mercado Interno",
            "valor": vl_cred_cofins_nt_mi,
            "valor_formatado": fmt_valor(val2)
        }
    else:
        resultado["VL_CRED_COFINS_NT_MI"] = {
            "titulo": "Parcela do Crédito de COFINS, vinculada a Receita Não Tributada no Mercado Interno",
            "valor": "",
            "valor_formatado": ""
        }
    
    # VL_CRED_COFINS_EXP: opcional
    if vl_cred_cofins_exp:
        resultado["VL_CRED_COFINS_EXP"] = {
            "titulo": "Parcela do Crédito de COFINS, vinculada a Receita de Exportação",
            "valor": vl_cred_cofins_exp,
            "valor_formatado": fmt_valor(val3)
        }
    else:
        resultado["VL_CRED_COFINS_EXP"] = {
            "titulo": "Parcela do Crédito de COFINS, vinculada a Receita de Exportação",
            "valor": "",
            "valor_formatado": ""
        }
    
    return resultado


def validar_1502(linhas, cod_cred_1500=None, vl_cofins_1501=None):
    """
    Valida uma ou mais linhas do registro 1502 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |1502|VL_CRED_COFINS_TRIB_MI|VL_CRED_COFINS_NT_MI|VL_CRED_COFINS_EXP|
        cod_cred_1500: Código do crédito do registro 1500 (opcional, para validação condicional)
        vl_cofins_1501: Valor do crédito COFINS do registro 1501 (opcional, para validação de soma)
        
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
        resultado = _processar_linha_1502(linha, cod_cred_1500=cod_cred_1500, vl_cofins_1501=vl_cofins_1501)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
