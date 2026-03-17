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


def _processar_linha_d201(linha):
    """
    Processa uma única linha do registro D201 e retorna um dicionário.
    
    Formato:
      |D201|CST_PIS|VL_ITEM|VL_BC_PIS|ALIQ_PIS|VL_PIS|COD_CTA|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "D201"
    - CST_PIS: obrigatório, 2 dígitos, código da situação tributária
      - Valores válidos: [01, 02, 06, 07, 08, 09, 49, 99]
    - VL_ITEM: obrigatório, numérico com 2 decimais
    - VL_BC_PIS: opcional, numérico com 2 decimais
    - ALIQ_PIS: opcional, numérico com 8 dígitos e 4 decimais (percentual)
    - VL_PIS: opcional, numérico com 2 decimais
      - Deve corresponder a VL_BC_PIS * ALIQ_PIS / 100 (validação)
    - COD_CTA: opcional, máximo 255 caracteres
      - Obrigatório a partir de novembro/2017, exceto se dispensado de ECD (validação em camada superior)
    
    Nota: Serão escrituradas neste registro as informações referentes à incidência, base de cálculo,
    alíquota e valor do PIS/Pasep, referente às operações de transporte consolidadas em D200.
    
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
    # Remove primeiro e último se vazios (formato padrão SPED: |D201|...|)
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
    if reg != "D201":
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
    
    # Extrai todos os campos (7 campos no total)
    cst_pis = obter_campo(1)
    vl_item = obter_campo(2)
    vl_bc_pis = obter_campo(3)
    aliq_pis = obter_campo(4)
    vl_pis = obter_campo(5)
    cod_cta = obter_campo(6)
    
    # Validações básicas dos campos obrigatórios
    
    # CST_PIS: obrigatório, 2 dígitos, valores válidos [01, 02, 06, 07, 08, 09, 49, 99]
    cst_pis_validos = ["01", "02", "06", "07", "08", "09", "49", "99"]
    if not cst_pis or len(cst_pis) != 2 or cst_pis not in cst_pis_validos:
        return None
    
    # VL_ITEM: obrigatório, numérico com 2 decimais
    ok1, val1, _ = validar_valor_numerico(vl_item, decimais=2, obrigatorio=True)
    if not ok1:
        return None
    
    # VL_BC_PIS: opcional, numérico com 2 decimais
    ok2, val2, _ = validar_valor_numerico(vl_bc_pis, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok2:
        return None
    
    # ALIQ_PIS: opcional, numérico com 8 dígitos e 4 decimais (percentual)
    # Formato: N(008,4) - até 8 dígitos na parte inteira e 4 decimais
    ok3, val3, _ = validar_valor_numerico(aliq_pis, decimais=4, obrigatorio=False, nao_negativo=True)
    if not ok3:
        return None
    # Verifica se tem no máximo 8 dígitos na parte inteira
    if aliq_pis:
        partes_aliq = aliq_pis.split(".")
        parte_inteira = partes_aliq[0]
        if len(parte_inteira) > 8:
            return None
    
    # VL_PIS: opcional, numérico com 2 decimais
    ok4, val4, _ = validar_valor_numerico(vl_pis, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok4:
        return None
    
    # Validação: VL_PIS deve corresponder a VL_BC_PIS * ALIQ_PIS / 100
    if vl_bc_pis and aliq_pis and vl_pis:
        vl_pis_calculado = round((val2 * val3) / 100, 2)
        # Permite pequena diferença devido a arredondamentos (tolerância de 0.01)
        if abs(val4 - vl_pis_calculado) > 0.01:
            return None
    
    # COD_CTA: opcional, máximo 255 caracteres
    # Nota: Obrigatório a partir de novembro/2017, exceto se dispensado de ECD (validação em camada superior)
    if cod_cta and len(cod_cta) > 255:
        return None
    
    # Função auxiliar para formatar valores monetários
    def fmt_valor(v):
        if v is None:
            return ""
        return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    # Função auxiliar para formatar percentual
    def fmt_percentual(v):
        if v is None:
            return ""
        return f"{v:,.4f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    # Descrições dos campos
    descricoes_cst_pis = {
        "01": "Operação Tributável com Alíquota Básica",
        "02": "Operação Tributável com Alíquota Diferenciada",
        "06": "Operação Tributável a Alíquota Zero",
        "07": "Operação Isenta da Contribuição",
        "08": "Operação sem Incidência da Contribuição",
        "09": "Operação com Suspensão da Contribuição",
        "49": "Outras Operações de Saída",
        "99": "Outras Operações"
    }
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "CST_PIS": {
            "titulo": "Código da Situação Tributária referente ao PIS/PASEP",
            "valor": cst_pis,
            "descricao": descricoes_cst_pis.get(cst_pis, "")
        },
        "VL_ITEM": {
            "titulo": "Valor total dos itens",
            "valor": vl_item,
            "valor_formatado": fmt_valor(val1)
        },
        "VL_BC_PIS": {
            "titulo": "Valor da base de cálculo do PIS/PASEP",
            "valor": vl_bc_pis,
            "valor_formatado": fmt_valor(val2) if vl_bc_pis else ""
        },
        "ALIQ_PIS": {
            "titulo": "Alíquota do PIS/PASEP (em percentual)",
            "valor": aliq_pis,
            "valor_formatado": fmt_percentual(val3) if aliq_pis else ""
        },
        "VL_PIS": {
            "titulo": "Valor do PIS/PASEP",
            "valor": vl_pis,
            "valor_formatado": fmt_valor(val4) if vl_pis else ""
        },
        "COD_CTA": {
            "titulo": "Código da conta analítica contábil debitada/creditada",
            "valor": cod_cta
        }
    }
    
    return resultado


def validar_d201(linhas):
    """
    Valida uma ou mais linhas do registro D201 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |D201|CST_PIS|VL_ITEM|VL_BC_PIS|ALIQ_PIS|VL_PIS|COD_CTA|
        
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
        resultado = _processar_linha_d201(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
