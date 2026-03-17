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


def _processar_linha_c880(linha):
    """
    Processa uma única linha do registro C880 e retorna um dicionário.
    
    Formato:
      |C880|COD_ITEM|CFOP|VL_ITEM|VL_DESC|CST_PIS|QUANT_BC_PIS|ALIQ_PIS_QUANT|VL_PIS|CST_COFINS|QUANT_BC_COFINS|ALIQ_COFINS_QUANT|VL_COFINS|COD_CTA|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "C880"
    - COD_ITEM: opcional, código do item (60 caracteres)
      - Validação: deve existir no registro 0200 (validação em camada superior)
    - CFOP: obrigatório, código fiscal de operação e prestação (4 dígitos)
      - Validação: deve existir na Tabela de CFOP (validação em camada superior)
    - VL_ITEM: obrigatório, valor total dos itens (numérico, 2 decimais, positivo)
    - VL_DESC: opcional, valor da exclusão/desconto comercial dos itens (numérico, 2 decimais, não negativo)
    - CST_PIS: obrigatório, código da situação tributária referente ao PIS/PASEP (2 dígitos)
      - Valores válidos: [03, 05, 06, 07, 08, 09, 49, 99]
    - QUANT_BC_PIS: opcional, base de cálculo em quantidade - PIS/PASEP (numérico, 3 decimais)
    - ALIQ_PIS_QUANT: opcional, alíquota do PIS/PASEP em reais (numérico, 4 decimais)
    - VL_PIS: opcional, valor do PIS/PASEP (numérico, 2 decimais)
      - Validação: deve corresponder ao valor da base de cálculo em quantidade (QUANT_BC_PIS) multiplicado pela alíquota em reais (ALIQ_PIS_QUANT)
    - CST_COFINS: obrigatório, código da situação tributária referente a COFINS (2 dígitos)
      - Valores válidos: [03, 05, 06, 07, 08, 09, 49, 99]
    - QUANT_BC_COFINS: opcional, base de cálculo em quantidade - COFINS (numérico, 3 decimais)
    - ALIQ_COFINS_QUANT: opcional, alíquota da COFINS em reais (numérico, 4 decimais)
    - VL_COFINS: opcional, valor da COFINS (numérico, 2 decimais)
      - Validação: deve corresponder ao valor da base de cálculo em quantidade (QUANT_BC_COFINS) multiplicado pela alíquota em reais (ALIQ_COFINS_QUANT)
    - COD_CTA: opcional, código da conta analítica contábil (255 caracteres)
    
    Nota: Este registro tem por objetivo representar a escrituração consolidada das vendas diárias por equipamento
    SAT-CF-e, segmentado por CST (CST PIS/Pasep e CST Cofins) ou por item, correspondente a receitas tributadas
    por quantidade de produtos vendidos.
    
    Na escrituração de suas operações diárias de cada equipamento SAT-CF-e, por item vendido, deve ser gerado um
    registro para cada item, conforme o código de item cadastrado no Registro 0200.
    
    No caso de ocorrência de venda com CST distintos, deve ser gerado um registro para cada CST. Como também,
    no caso de a operação tributável incidir a alíquotas distintas.
    
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
    # Remove primeiro e último se vazios (formato padrão SPED: |C880|...|)
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
    if reg != "C880":
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
    
    # Extrai todos os campos (14 campos no total)
    cod_item = obter_campo(1)
    cfop = obter_campo(2)
    vl_item = obter_campo(3)
    vl_desc = obter_campo(4)
    cst_pis = obter_campo(5)
    quant_bc_pis = obter_campo(6)
    aliq_pis_quant = obter_campo(7)
    vl_pis = obter_campo(8)
    cst_cofins = obter_campo(9)
    quant_bc_cofins = obter_campo(10)
    aliq_cofins_quant = obter_campo(11)
    vl_cofins = obter_campo(12)
    cod_cta = obter_campo(13)
    
    # Validações básicas dos campos obrigatórios
    
    # COD_ITEM: opcional, código do item (60 caracteres)
    if cod_item and len(cod_item) > 60:
        return None
    
    # CFOP: obrigatório, código fiscal de operação e prestação (4 dígitos)
    if not cfop or (not cfop.isdigit() or len(cfop) != 4):
        return None
    
    # VL_ITEM: obrigatório, valor total dos itens (numérico, 2 decimais, positivo)
    ok_vl_item, val_vl_item, _ = validar_valor_numerico(vl_item, decimais=2, obrigatorio=True, positivo=True)
    if not ok_vl_item:
        return None
    
    # VL_DESC: opcional, valor da exclusão/desconto comercial dos itens (numérico, 2 decimais, não negativo)
    ok_vl_desc, val_vl_desc, _ = validar_valor_numerico(vl_desc, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok_vl_desc:
        return None
    
    # CST_PIS: obrigatório, código da situação tributária PIS (valores válidos)
    cst_pis_validos = ["03", "05", "06", "07", "08", "09", "49", "99"]
    if not cst_pis or cst_pis not in cst_pis_validos:
        return None
    
    # QUANT_BC_PIS: opcional, base de cálculo em quantidade - PIS/PASEP (numérico, 3 decimais)
    ok_quant_bc_pis, val_quant_bc_pis, _ = validar_valor_numerico(quant_bc_pis, decimais=3, obrigatorio=False, nao_negativo=True)
    if not ok_quant_bc_pis:
        return None
    
    # ALIQ_PIS_QUANT: opcional, alíquota do PIS em reais (numérico, 4 decimais)
    ok_aliq_pis_quant, val_aliq_pis_quant, _ = validar_valor_numerico(aliq_pis_quant, decimais=4, obrigatorio=False, nao_negativo=True)
    if not ok_aliq_pis_quant:
        return None
    
    # VL_PIS: opcional, valor do PIS (numérico, 2 decimais)
    ok_vl_pis, val_vl_pis, _ = validar_valor_numerico(vl_pis, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok_vl_pis:
        return None
    
    # Validação de cálculo do VL_PIS
    if vl_pis and quant_bc_pis and aliq_pis_quant:
        # VL_PIS = QUANT_BC_PIS * ALIQ_PIS_QUANT
        vl_pis_calculado = val_quant_bc_pis * val_aliq_pis_quant
        # Tolerância de 0.01 para diferenças de arredondamento
        if abs(val_vl_pis - vl_pis_calculado) > 0.01:
            return None
    
    # CST_COFINS: obrigatório, código da situação tributária COFINS (valores válidos)
    cst_cofins_validos = ["03", "05", "06", "07", "08", "09", "49", "99"]
    if not cst_cofins or cst_cofins not in cst_cofins_validos:
        return None
    
    # QUANT_BC_COFINS: opcional, base de cálculo em quantidade - COFINS (numérico, 3 decimais)
    ok_quant_bc_cofins, val_quant_bc_cofins, _ = validar_valor_numerico(quant_bc_cofins, decimais=3, obrigatorio=False, nao_negativo=True)
    if not ok_quant_bc_cofins:
        return None
    
    # ALIQ_COFINS_QUANT: opcional, alíquota da COFINS em reais (numérico, 4 decimais)
    ok_aliq_cofins_quant, val_aliq_cofins_quant, _ = validar_valor_numerico(aliq_cofins_quant, decimais=4, obrigatorio=False, nao_negativo=True)
    if not ok_aliq_cofins_quant:
        return None
    
    # VL_COFINS: opcional, valor da COFINS (numérico, 2 decimais)
    ok_vl_cofins, val_vl_cofins, _ = validar_valor_numerico(vl_cofins, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok_vl_cofins:
        return None
    
    # Validação de cálculo do VL_COFINS
    if vl_cofins and quant_bc_cofins and aliq_cofins_quant:
        # VL_COFINS = QUANT_BC_COFINS * ALIQ_COFINS_QUANT
        vl_cofins_calculado = val_quant_bc_cofins * val_aliq_cofins_quant
        # Tolerância de 0.01 para diferenças de arredondamento
        if abs(val_vl_cofins - vl_cofins_calculado) > 0.01:
            return None
    
    # COD_CTA: opcional, código da conta analítica contábil (255 caracteres)
    if cod_cta and len(cod_cta) > 255:
        return None
    
    # Função auxiliar para formatar valores monetários
    def fmt_valor(v):
        if v is None:
            return ""
        return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    # Função auxiliar para formatar valores com mais decimais
    def fmt_valor_decimais(v, decimais):
        if v is None:
            return ""
        formato = f"{{:,.{decimais}f}}"
        return formato.format(v).replace(",", "X").replace(".", ",").replace("X", ".")
    
    # Descrições dos campos CST
    descricoes_cst = {
        "03": "Operação Tributável com Alíquota por Unidade de Medida de Produto",
        "05": "Operação Tributável por Substituição Tributária",
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
            "valor": reg,
            "descricao": "Texto fixo contendo 'C880'"
        },
        "COD_ITEM": {
            "titulo": "Código do item (campo 02 do Registro 0200)",
            "valor": cod_item
        },
        "CFOP": {
            "titulo": "Código fiscal de operação e prestação",
            "valor": cfop
        },
        "VL_ITEM": {
            "titulo": "Valor total dos itens",
            "valor": vl_item,
            "valor_formatado": fmt_valor(val_vl_item)
        },
        "VL_DESC": {
            "titulo": "Valor da exclusão/desconto comercial dos itens",
            "valor": vl_desc,
            "valor_formatado": fmt_valor(val_vl_desc)
        },
        "CST_PIS": {
            "titulo": "Código da Situação Tributária referente ao PIS/PASEP",
            "valor": cst_pis,
            "descricao": descricoes_cst.get(cst_pis, "")
        },
        "QUANT_BC_PIS": {
            "titulo": "Base de cálculo em quantidade - PIS/PASEP",
            "valor": quant_bc_pis,
            "valor_formatado": fmt_valor_decimais(val_quant_bc_pis, 3) if quant_bc_pis else ""
        },
        "ALIQ_PIS_QUANT": {
            "titulo": "Alíquota do PIS/PASEP (em reais)",
            "valor": aliq_pis_quant,
            "valor_formatado": fmt_valor_decimais(val_aliq_pis_quant, 4) if aliq_pis_quant else ""
        },
        "VL_PIS": {
            "titulo": "Valor do PIS/PASEP",
            "valor": vl_pis,
            "valor_formatado": fmt_valor(val_vl_pis)
        },
        "CST_COFINS": {
            "titulo": "Código da Situação Tributária referente a COFINS",
            "valor": cst_cofins,
            "descricao": descricoes_cst.get(cst_cofins, "")
        },
        "QUANT_BC_COFINS": {
            "titulo": "Base de cálculo em quantidade – COFINS",
            "valor": quant_bc_cofins,
            "valor_formatado": fmt_valor_decimais(val_quant_bc_cofins, 3) if quant_bc_cofins else ""
        },
        "ALIQ_COFINS_QUANT": {
            "titulo": "Alíquota da COFINS (em reais)",
            "valor": aliq_cofins_quant,
            "valor_formatado": fmt_valor_decimais(val_aliq_cofins_quant, 4) if aliq_cofins_quant else ""
        },
        "VL_COFINS": {
            "titulo": "Valor da COFINS",
            "valor": vl_cofins,
            "valor_formatado": fmt_valor(val_vl_cofins)
        },
        "COD_CTA": {
            "titulo": "Código da conta analítica contábil debitada/creditada",
            "valor": cod_cta
        }
    }
    
    return resultado


def validar_c880(linhas):
    """
    Valida uma ou mais linhas do registro C880 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |C880|COD_ITEM|CFOP|VL_ITEM|VL_DESC|CST_PIS|QUANT_BC_PIS|ALIQ_PIS_QUANT|VL_PIS|CST_COFINS|QUANT_BC_COFINS|ALIQ_COFINS_QUANT|VL_COFINS|COD_CTA|
        
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
        resultado = _processar_linha_c880(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
