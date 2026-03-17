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


def _float_menor_igual(a, b, tolerancia=0.01):
    """Compara se a <= b com tolerância."""
    if a is None or b is None:
        return False
    return a <= b + tolerancia


def _processar_linha_0145(linha):
    """
    Processa uma única linha do registro 0145 e retorna um dicionário.
    
    Formato:
      |0145|COD_INC_TRIB|VL_REC_TOT|VL_REC_ATIV|VL_REC_DEMAIS_ATIV|INFO_COMPL|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "0145"
    - COD_INC_TRIB: obrigatório, valores válidos [1, 2]
    - VL_REC_TOT: obrigatório, numérico com 2 decimais, não negativo
    - VL_REC_ATIV: obrigatório, numérico com 2 decimais, não negativo
    - VL_REC_DEMAIS_ATIV: opcional, numérico com 2 decimais, não negativo
    - INFO_COMPL: opcional, informação complementar
    - Validação: VL_REC_ATIV + VL_REC_DEMAIS_ATIV <= VL_REC_TOT
    
    Nota: Este registro é obrigatório para pessoa jurídica que tenha auferido receita
    das atividades de serviços ou da fabricação de produtos relacionados nos art. 7º e 8º
    da Lei nº 12.546/2011. Esta validação deve ser feita em uma camada superior.
    
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
    # Remove primeiro e último se vazios (formato padrão SPED: |0145|...|)
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
    if reg != "0145":
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
    
    # Extrai todos os campos (6 campos no total)
    cod_inc_trib = obter_campo(1)
    vl_rec_tot = obter_campo(2)
    vl_rec_ativ = obter_campo(3)
    vl_rec_demais_ativ = obter_campo(4)
    info_compl = obter_campo(5)
    
    # Validações básicas dos campos obrigatórios
    
    # COD_INC_TRIB: obrigatório, valores válidos [1, 2]
    if not cod_inc_trib or cod_inc_trib not in ["1", "2"]:
        return None
    
    # VL_REC_TOT: obrigatório, numérico com 2 decimais, não negativo
    ok1, val1, _ = validar_valor_numerico(vl_rec_tot, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok1:
        return None
    
    # VL_REC_ATIV: obrigatório, numérico com 2 decimais, não negativo
    ok2, val2, _ = validar_valor_numerico(vl_rec_ativ, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok2:
        return None
    
    # VL_REC_DEMAIS_ATIV: opcional, numérico com 2 decimais, não negativo
    ok3, val3, _ = validar_valor_numerico(vl_rec_demais_ativ, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok3:
        return None
    
    # Se não foi informado, considera zero
    if val3 is None:
        val3 = 0.0
    
    # Validação: VL_REC_ATIV + VL_REC_DEMAIS_ATIV <= VL_REC_TOT
    soma_parcial = val2 + val3
    if not _float_menor_igual(soma_parcial, val1):
        return None
    
    # Função auxiliar para formatar valores monetários
    def fmt_valor(v):
        return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    # Monta o resultado
    descricoes_inc_trib = {
        "1": "Contribuição Previdenciária apurada no período, exclusivamente com base na Receita Bruta",
        "2": "Contribuição Previdenciária apurada no período, com base na Receita Bruta e com base nas Remunerações pagas"
    }
    
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "COD_INC_TRIB": {
            "titulo": "Código indicador da incidência tributária no período",
            "valor": cod_inc_trib,
            "descricao": descricoes_inc_trib.get(cod_inc_trib, "")
        },
        "VL_REC_TOT": {
            "titulo": "Valor da Receita Bruta Total da Pessoa Jurídica no Período",
            "valor": vl_rec_tot,
            "valor_formatado": fmt_valor(val1)
        },
        "VL_REC_ATIV": {
            "titulo": "Valor da Receita Bruta da(s) Atividade(s) Sujeita(s) à Contribuição Previdenciária sobre a Receita Bruta",
            "valor": vl_rec_ativ,
            "valor_formatado": fmt_valor(val2)
        }
    }
    
    # VL_REC_DEMAIS_ATIV: opcional
    if vl_rec_demais_ativ:
        resultado["VL_REC_DEMAIS_ATIV"] = {
            "titulo": "Valor da Receita Bruta da(s) Atividade(s) não Sujeita(s) à Contribuição Previdenciária sobre a Receita Bruta",
            "valor": vl_rec_demais_ativ,
            "valor_formatado": fmt_valor(val3)
        }
    else:
        resultado["VL_REC_DEMAIS_ATIV"] = {
            "titulo": "Valor da Receita Bruta da(s) Atividade(s) não Sujeita(s) à Contribuição Previdenciária sobre a Receita Bruta",
            "valor": "",
            "valor_formatado": fmt_valor(0.0)
        }
    
    # INFO_COMPL: opcional
    if info_compl:
        resultado["INFO_COMPL"] = {
            "titulo": "Informação complementar",
            "valor": info_compl
        }
    else:
        resultado["INFO_COMPL"] = {
            "titulo": "Informação complementar",
            "valor": ""
        }
    
    return resultado


def validar_0145(linhas):
    """
    Valida uma ou mais linhas do registro 0145 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |0145|COD_INC_TRIB|VL_REC_TOT|VL_REC_ATIV|VL_REC_DEMAIS_ATIV|INFO_COMPL|
        
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
        resultado = _processar_linha_0145(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
