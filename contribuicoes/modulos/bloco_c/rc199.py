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


def _processar_linha_c199(linha):
    """
    Processa uma única linha do registro C199 e retorna um dicionário.
    
    Formato:
      |C199|COD_DOC_IMP|NUM_DOC_IMP|VL_PIS_IMP|VL_COFINS_IMP|NUM_ACDRAW|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "C199"
    - COD_DOC_IMP: obrigatório, documento de importação (1 dígito)
      - Valores válidos: [0, 1, 2]
      - 0: Declaração de Importação
      - 1: Declaração Simplificada de Importação
      - 2: Declaração Única de Importação (a partir de 01/2019)
    - NUM_DOC_IMP: obrigatório, número do documento de importação (15 caracteres)
    - VL_PIS_IMP: opcional, valor pago de PIS na importação (numérico, 2 decimais, não negativo)
      - Informar o valor recolhido de PIS/Pasep – Importação, relacionado ao documento informado
      - No caso de haver mais de um recolhimento, informar o somatório dos valores pagos
    - VL_COFINS_IMP: opcional, valor pago de COFINS na importação (numérico, 2 decimais, não negativo)
      - Informar o valor recolhido de Cofins – Importação, relacionado ao documento informado
      - No caso de haver mais de um recolhimento, informar o somatório dos valores pagos
    - NUM_ACDRAW: opcional, número do Ato Concessório do regime Drawback (20 caracteres)
    
    Nota: Este registro tem por objetivo informar detalhes das operações de importação, que estejam sendo
    documentadas de forma consolidada no registro C190 (registro consolidado das aquisições por NF-e,
    código 55), quando no Campo 03 dos registros C191 e C195 conste CST_PIS ou CST_COFINS gerador de
    crédito (CST 50 a 56) e, no Campo 04, conste CFOP próprio de operações de importação (CFOP iniciado em 3).
    
    Caso a pessoa jurídica tenha importado mercadorias, bens e produtos de pessoa física ou jurídica
    domiciliada no exterior, com direito a crédito na forma prevista na Lei nº 10.865, de 2004, deve
    preencher o Registro "C199" para validar a apuração do crédito.
    
    Devem ser informados neste registro os pagamentos de PIS/Pasep-Importação e de Cofins-Importação,
    referente ao serviço contratado com direito a crédito, uma vez que de acordo com a legislação em
    referência, o direito à apuração de crédito aplica-se apenas em relação às contribuições efetivamente
    pagas na importação de bens e serviços (art. 15 da Lei nº 10.865, de 2004).
    
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
    # Remove primeiro e último se vazios (formato padrão SPED: |C199|...|)
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
    if reg != "C199":
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
    cod_doc_imp = obter_campo(1)
    num_doc_imp = obter_campo(2)
    vl_pis_imp = obter_campo(3)
    vl_cofins_imp = obter_campo(4)
    num_acdraw = obter_campo(5)
    
    # Validações básicas dos campos obrigatórios
    
    # COD_DOC_IMP: obrigatório, valores válidos [0, 1, 2]
    cod_doc_imp_validos = ["0", "1", "2"]
    if not cod_doc_imp or cod_doc_imp not in cod_doc_imp_validos:
        return None
    
    # NUM_DOC_IMP: obrigatório, número do documento de importação (15 caracteres)
    if not num_doc_imp or len(num_doc_imp) > 15:
        return None
    
    # VL_PIS_IMP: opcional, valor pago de PIS na importação (numérico, 2 decimais, não negativo)
    ok_vl_pis_imp, val_vl_pis_imp, _ = validar_valor_numerico(vl_pis_imp, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok_vl_pis_imp:
        return None
    
    # VL_COFINS_IMP: opcional, valor pago de COFINS na importação (numérico, 2 decimais, não negativo)
    ok_vl_cofins_imp, val_vl_cofins_imp, _ = validar_valor_numerico(vl_cofins_imp, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok_vl_cofins_imp:
        return None
    
    # NUM_ACDRAW: opcional, número do Ato Concessório do regime Drawback (20 caracteres)
    if num_acdraw and len(num_acdraw) > 20:
        return None
    
    # Função auxiliar para formatar valores monetários
    def fmt_valor(v):
        if v is None:
            return ""
        return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    # Descrições dos campos
    descricoes_cod_doc_imp = {
        "0": "Declaração de Importação",
        "1": "Declaração Simplificada de Importação",
        "2": "Declaração Única de Importação"
    }
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "COD_DOC_IMP": {
            "titulo": "Documento de importação",
            "valor": cod_doc_imp,
            "descricao": descricoes_cod_doc_imp.get(cod_doc_imp, "")
        },
        "NUM_DOC_IMP": {
            "titulo": "Número do documento de Importação",
            "valor": num_doc_imp
        },
        "VL_PIS_IMP": {
            "titulo": "Valor pago de PIS na importação",
            "valor": vl_pis_imp,
            "valor_formatado": fmt_valor(val_vl_pis_imp)
        },
        "VL_COFINS_IMP": {
            "titulo": "Valor pago de COFINS na importação",
            "valor": vl_cofins_imp,
            "valor_formatado": fmt_valor(val_vl_cofins_imp)
        },
        "NUM_ACDRAW": {
            "titulo": "Número do Ato Concessório do regime Drawback",
            "valor": num_acdraw
        }
    }
    
    return resultado


def validar_c199(linhas):
    """
    Valida uma ou mais linhas do registro C199 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |C199|COD_DOC_IMP|NUM_DOC_IMP|VL_PIS_IMP|VL_COFINS_IMP|NUM_ACDRAW|
        
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
        resultado = _processar_linha_c199(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
