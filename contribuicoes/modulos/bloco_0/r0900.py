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


def _float_igual(a, b, tolerancia=0.01):
    """Compara dois floats com tolerância."""
    if a is None or b is None:
        return False
    return abs(a - b) <= tolerancia


def _float_menor_igual(a, b, tolerancia=0.01):
    """Compara se a <= b com tolerância."""
    if a is None or b is None:
        return False
    return a <= b + tolerancia


def _processar_linha_0900(linha):
    """
    Processa uma única linha do registro 0900 e retorna um dicionário.
    
    Formato:
      |0900|REC_TOTAL_BLOCO_A|REC_NRB_BLOCO_A|REC_TOTAL_BLOCO_C|REC_NRB_BLOCO_C|REC_TOTAL_BLOCO_D|REC_NRB_BLOCO_D|REC_TOTAL_BLOCO_F|REC_NRB_BLOCO_F|REC_TOTAL_BLOCO_I|REC_NRB_BLOCO_I|REC_TOTAL_BLOCO_1|REC_NRB_BLOCO_1|REC_TOTAL_PERIODO|REC_TOTAL_NRB_PERÍODO|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "0900"
    - REC_TOTAL_BLOCO_A: obrigatório, numérico com 2 decimais, não negativo
    - REC_NRB_BLOCO_A: opcional, numérico com 2 decimais, não negativo, <= REC_TOTAL_BLOCO_A
    - REC_TOTAL_BLOCO_C: obrigatório, numérico com 2 decimais, não negativo
    - REC_NRB_BLOCO_C: opcional, numérico com 2 decimais, não negativo, <= REC_TOTAL_BLOCO_C
    - REC_TOTAL_BLOCO_D: obrigatório, numérico com 2 decimais, não negativo
    - REC_NRB_BLOCO_D: opcional, numérico com 2 decimais, não negativo, <= REC_TOTAL_BLOCO_D
    - REC_TOTAL_BLOCO_F: obrigatório, numérico com 2 decimais, não negativo
    - REC_NRB_BLOCO_F: opcional, numérico com 2 decimais, não negativo, <= REC_TOTAL_BLOCO_F
    - REC_TOTAL_BLOCO_I: obrigatório, numérico com 2 decimais, não negativo
    - REC_NRB_BLOCO_I: opcional, numérico com 2 decimais, não negativo, <= REC_TOTAL_BLOCO_I
    - REC_TOTAL_BLOCO_1: obrigatório, numérico com 2 decimais, não negativo
    - REC_NRB_BLOCO_1: opcional, numérico com 2 decimais, não negativo, <= REC_TOTAL_BLOCO_1
    - REC_TOTAL_PERIODO: obrigatório, numérico com 2 decimais, não negativo
      - Deve ser igual à soma dos campos 02, 04, 06, 08, 10 e 12
    - REC_TOTAL_NRB_PERÍODO: opcional, numérico com 2 decimais, não negativo
      - Deve ser igual à soma dos campos 03, 05, 07, 09, 11 e 13
      - Deve ser <= REC_TOTAL_PERIODO
    
    Nota: Este registro é obrigatório sempre que o arquivo original da EFD-Contribuições
    for transmitido após o prazo regular de entrega.
    As validações de que os valores devem ser iguais aos somatórios dos registros dos blocos
    devem ser feitas em uma camada superior.
    
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
    # Remove primeiro e último se vazios (formato padrão SPED: |0900|...|)
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
    if reg != "0900":
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
    
    # Extrai todos os campos (15 campos no total)
    rec_total_bloco_a = obter_campo(1)
    rec_nrb_bloco_a = obter_campo(2)
    rec_total_bloco_c = obter_campo(3)
    rec_nrb_bloco_c = obter_campo(4)
    rec_total_bloco_d = obter_campo(5)
    rec_nrb_bloco_d = obter_campo(6)
    rec_total_bloco_f = obter_campo(7)
    rec_nrb_bloco_f = obter_campo(8)
    rec_total_bloco_i = obter_campo(9)
    rec_nrb_bloco_i = obter_campo(10)
    rec_total_bloco_1 = obter_campo(11)
    rec_nrb_bloco_1 = obter_campo(12)
    rec_total_periodo = obter_campo(13)
    rec_total_nrb_periodo = obter_campo(14)
    
    # Validações dos campos obrigatórios (todos numéricos com 2 decimais, não negativos)
    
    # REC_TOTAL_BLOCO_A: obrigatório
    ok1, val1, _ = validar_valor_numerico(rec_total_bloco_a, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok1:
        return None
    
    # REC_NRB_BLOCO_A: opcional
    ok2, val2, _ = validar_valor_numerico(rec_nrb_bloco_a, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok2:
        return None
    if val2 is None:
        val2 = 0.0
    
    # REC_NRB_BLOCO_A <= REC_TOTAL_BLOCO_A
    if not _float_menor_igual(val2, val1):
        return None
    
    # REC_TOTAL_BLOCO_C: obrigatório
    ok3, val3, _ = validar_valor_numerico(rec_total_bloco_c, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok3:
        return None
    
    # REC_NRB_BLOCO_C: opcional
    ok4, val4, _ = validar_valor_numerico(rec_nrb_bloco_c, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok4:
        return None
    if val4 is None:
        val4 = 0.0
    
    # REC_NRB_BLOCO_C <= REC_TOTAL_BLOCO_C
    if not _float_menor_igual(val4, val3):
        return None
    
    # REC_TOTAL_BLOCO_D: obrigatório
    ok5, val5, _ = validar_valor_numerico(rec_total_bloco_d, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok5:
        return None
    
    # REC_NRB_BLOCO_D: opcional
    ok6, val6, _ = validar_valor_numerico(rec_nrb_bloco_d, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok6:
        return None
    if val6 is None:
        val6 = 0.0
    
    # REC_NRB_BLOCO_D <= REC_TOTAL_BLOCO_D
    if not _float_menor_igual(val6, val5):
        return None
    
    # REC_TOTAL_BLOCO_F: obrigatório
    ok7, val7, _ = validar_valor_numerico(rec_total_bloco_f, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok7:
        return None
    
    # REC_NRB_BLOCO_F: opcional
    ok8, val8, _ = validar_valor_numerico(rec_nrb_bloco_f, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok8:
        return None
    if val8 is None:
        val8 = 0.0
    
    # REC_NRB_BLOCO_F <= REC_TOTAL_BLOCO_F
    if not _float_menor_igual(val8, val7):
        return None
    
    # REC_TOTAL_BLOCO_I: obrigatório
    ok9, val9, _ = validar_valor_numerico(rec_total_bloco_i, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok9:
        return None
    
    # REC_NRB_BLOCO_I: opcional
    ok10, val10, _ = validar_valor_numerico(rec_nrb_bloco_i, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok10:
        return None
    if val10 is None:
        val10 = 0.0
    
    # REC_NRB_BLOCO_I <= REC_TOTAL_BLOCO_I
    if not _float_menor_igual(val10, val9):
        return None
    
    # REC_TOTAL_BLOCO_1: obrigatório
    ok11, val11, _ = validar_valor_numerico(rec_total_bloco_1, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok11:
        return None
    
    # REC_NRB_BLOCO_1: opcional
    ok12, val12, _ = validar_valor_numerico(rec_nrb_bloco_1, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok12:
        return None
    if val12 is None:
        val12 = 0.0
    
    # REC_NRB_BLOCO_1 <= REC_TOTAL_BLOCO_1
    if not _float_menor_igual(val12, val11):
        return None
    
    # REC_TOTAL_PERIODO: obrigatório
    ok13, val13, _ = validar_valor_numerico(rec_total_periodo, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok13:
        return None
    
    # REC_TOTAL_NRB_PERÍODO: opcional
    ok14, val14, _ = validar_valor_numerico(rec_total_nrb_periodo, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok14:
        return None
    if val14 is None:
        val14 = 0.0
    
    # Validação: REC_TOTAL_PERIODO deve ser igual à soma dos campos 02, 04, 06, 08, 10 e 12
    soma_total = val1 + val3 + val5 + val7 + val9 + val11
    if not _float_igual(val13, soma_total):
        return None
    
    # Validação: REC_TOTAL_NRB_PERÍODO deve ser igual à soma dos campos 03, 05, 07, 09, 11 e 13
    soma_nrb = val2 + val4 + val6 + val8 + val10 + val12
    if not _float_igual(val14, soma_nrb):
        return None
    
    # Validação: REC_TOTAL_NRB_PERÍODO <= REC_TOTAL_PERIODO
    if not _float_menor_igual(val14, val13):
        return None
    
    # Função auxiliar para formatar valores monetários
    def fmt_valor(v):
        return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "REC_TOTAL_BLOCO_A": {
            "titulo": "Receita total referente aos registros escriturados no Bloco A",
            "valor": rec_total_bloco_a,
            "valor_formatado": fmt_valor(val1)
        },
        "REC_TOTAL_BLOCO_C": {
            "titulo": "Receita total referente aos registros escriturados no Bloco C",
            "valor": rec_total_bloco_c,
            "valor_formatado": fmt_valor(val3)
        },
        "REC_TOTAL_BLOCO_D": {
            "titulo": "Receita total referente aos registros escriturados no Bloco D",
            "valor": rec_total_bloco_d,
            "valor_formatado": fmt_valor(val5)
        },
        "REC_TOTAL_BLOCO_F": {
            "titulo": "Receita total referente aos registros escriturados no Bloco F",
            "valor": rec_total_bloco_f,
            "valor_formatado": fmt_valor(val7)
        },
        "REC_TOTAL_BLOCO_I": {
            "titulo": "Receita total referente aos registros escriturados no Bloco I",
            "valor": rec_total_bloco_i,
            "valor_formatado": fmt_valor(val9)
        },
        "REC_TOTAL_BLOCO_1": {
            "titulo": "Receita total referente aos registros escriturados no Bloco 1 (RET)",
            "valor": rec_total_bloco_1,
            "valor_formatado": fmt_valor(val11)
        },
        "REC_TOTAL_PERIODO": {
            "titulo": "Receita total (Soma dos Campos 02, 04, 06, 08, 10 e 12)",
            "valor": rec_total_periodo,
            "valor_formatado": fmt_valor(val13)
        }
    }
    
    # REC_NRB_BLOCO_A: opcional
    if rec_nrb_bloco_a:
        resultado["REC_NRB_BLOCO_A"] = {
            "titulo": "Parcela da receita total escriturada no Bloco A, não classificada como receita bruta",
            "valor": rec_nrb_bloco_a,
            "valor_formatado": fmt_valor(val2)
        }
    else:
        resultado["REC_NRB_BLOCO_A"] = {
            "titulo": "Parcela da receita total escriturada no Bloco A, não classificada como receita bruta",
            "valor": "",
            "valor_formatado": fmt_valor(0.0)
        }
    
    # REC_NRB_BLOCO_C: opcional
    if rec_nrb_bloco_c:
        resultado["REC_NRB_BLOCO_C"] = {
            "titulo": "Parcela da receita total escriturada no Bloco C, não classificada como receita bruta",
            "valor": rec_nrb_bloco_c,
            "valor_formatado": fmt_valor(val4)
        }
    else:
        resultado["REC_NRB_BLOCO_C"] = {
            "titulo": "Parcela da receita total escriturada no Bloco C, não classificada como receita bruta",
            "valor": "",
            "valor_formatado": fmt_valor(0.0)
        }
    
    # REC_NRB_BLOCO_D: opcional
    if rec_nrb_bloco_d:
        resultado["REC_NRB_BLOCO_D"] = {
            "titulo": "Parcela da receita total escriturada no Bloco D, não classificada como receita bruta",
            "valor": rec_nrb_bloco_d,
            "valor_formatado": fmt_valor(val6)
        }
    else:
        resultado["REC_NRB_BLOCO_D"] = {
            "titulo": "Parcela da receita total escriturada no Bloco D, não classificada como receita bruta",
            "valor": "",
            "valor_formatado": fmt_valor(0.0)
        }
    
    # REC_NRB_BLOCO_F: opcional
    if rec_nrb_bloco_f:
        resultado["REC_NRB_BLOCO_F"] = {
            "titulo": "Parcela da receita total escriturada no Bloco F, não classificada como receita bruta",
            "valor": rec_nrb_bloco_f,
            "valor_formatado": fmt_valor(val8)
        }
    else:
        resultado["REC_NRB_BLOCO_F"] = {
            "titulo": "Parcela da receita total escriturada no Bloco F, não classificada como receita bruta",
            "valor": "",
            "valor_formatado": fmt_valor(0.0)
        }
    
    # REC_NRB_BLOCO_I: opcional
    if rec_nrb_bloco_i:
        resultado["REC_NRB_BLOCO_I"] = {
            "titulo": "Parcela da receita total escriturada no Bloco I, não classificada como receita bruta",
            "valor": rec_nrb_bloco_i,
            "valor_formatado": fmt_valor(val10)
        }
    else:
        resultado["REC_NRB_BLOCO_I"] = {
            "titulo": "Parcela da receita total escriturada no Bloco I, não classificada como receita bruta",
            "valor": "",
            "valor_formatado": fmt_valor(0.0)
        }
    
    # REC_NRB_BLOCO_1: opcional
    if rec_nrb_bloco_1:
        resultado["REC_NRB_BLOCO_1"] = {
            "titulo": "Parcela da receita total escriturada no Bloco 1, não classificada como receita bruta",
            "valor": rec_nrb_bloco_1,
            "valor_formatado": fmt_valor(val12)
        }
    else:
        resultado["REC_NRB_BLOCO_1"] = {
            "titulo": "Parcela da receita total escriturada no Bloco 1, não classificada como receita bruta",
            "valor": "",
            "valor_formatado": fmt_valor(0.0)
        }
    
    # REC_TOTAL_NRB_PERÍODO: opcional
    if rec_total_nrb_periodo:
        resultado["REC_TOTAL_NRB_PERÍODO"] = {
            "titulo": "Parcela da receita total escriturada não classificada como receita bruta (Soma dos Campos 03, 05, 07, 09, 11 e 13)",
            "valor": rec_total_nrb_periodo,
            "valor_formatado": fmt_valor(val14)
        }
    else:
        resultado["REC_TOTAL_NRB_PERÍODO"] = {
            "titulo": "Parcela da receita total escriturada não classificada como receita bruta (Soma dos Campos 03, 05, 07, 09, 11 e 13)",
            "valor": "",
            "valor_formatado": fmt_valor(0.0)
        }
    
    return resultado


def validar_0900(linhas):
    """
    Valida uma ou mais linhas do registro 0900 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |0900|REC_TOTAL_BLOCO_A|REC_NRB_BLOCO_A|REC_TOTAL_BLOCO_C|REC_NRB_BLOCO_C|REC_TOTAL_BLOCO_D|REC_NRB_BLOCO_D|REC_TOTAL_BLOCO_F|REC_NRB_BLOCO_F|REC_TOTAL_BLOCO_I|REC_NRB_BLOCO_I|REC_TOTAL_BLOCO_1|REC_NRB_BLOCO_1|REC_TOTAL_PERIODO|REC_TOTAL_NRB_PERÍODO|
        
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
        resultado = _processar_linha_0900(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
