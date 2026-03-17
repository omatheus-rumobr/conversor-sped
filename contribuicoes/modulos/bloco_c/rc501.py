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


def _processar_linha_c501(linha):
    """
    Processa uma única linha do registro C501 e retorna um dicionário.
    
    Formato:
      |C501|CST_PIS|VL_ITEM|NAT_BC_CRED|VL_BC_PIS|ALIQ_PIS|VL_PIS|COD_CTA|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "C501"
    - CST_PIS: obrigatório, código da situação tributária referente ao PIS/PASEP (2 dígitos)
      - Valores válidos: [50, 51, 52, 53, 54, 55, 56, 60, 61, 62, 63, 64, 65, 66, 70, 71, 72, 73, 74, 75, 98, 99]
    - VL_ITEM: obrigatório, valor total dos itens (numérico, 2 decimais, positivo)
    - NAT_BC_CRED: opcional, código da base de cálculo do crédito (2 caracteres)
      - Valores válidos: [01, 02, 04, 13]
    - VL_BC_PIS: obrigatório, valor da base de cálculo do PIS/PASEP (numérico, 2 decimais)
    - ALIQ_PIS: obrigatório, alíquota do PIS/PASEP em percentual (numérico, 4 decimais)
    - VL_PIS: obrigatório, valor do PIS/PASEP (numérico, 2 decimais)
      - Validação: deve corresponder ao valor da base de cálculo (VL_BC_PIS) multiplicado pela alíquota (ALIQ_PIS), dividido por 100
    - COD_CTA: opcional, código da conta analítica contábil (255 caracteres)
      - Obrigatório para fatos geradores a partir de novembro de 2017, exceto se dispensado de escrituração contábil
    
    Nota: Este registro detalha as informações relativas à apuração do crédito de PIS/Pasep, referentes ao documento
    fiscal escriturado no Registro Pai C500. Deve ser escriturado um registro C501 para cada item cuja operação
    dê direito a crédito, pelo seu valor total ou parcial.
    
    Caso em relação a um mesmo item venha a ocorrer tratamentos tributários diversos (mais de um CST), deve a
    pessoa jurídica informar um registro C501 para cada CST.
    
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
    # Remove primeiro e último se vazios (formato padrão SPED: |C501|...|)
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
    if reg != "C501":
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
    
    # Extrai todos os campos (8 campos no total)
    cst_pis = obter_campo(1)
    vl_item = obter_campo(2)
    nat_bc_cred = obter_campo(3)
    vl_bc_pis = obter_campo(4)
    aliq_pis = obter_campo(5)
    vl_pis = obter_campo(6)
    cod_cta = obter_campo(7)
    
    # Validações básicas dos campos obrigatórios
    
    # CST_PIS: obrigatório, código da situação tributária PIS (valores válidos)
    cst_pis_validos = ["50", "51", "52", "53", "54", "55", "56", "60", "61", "62", "63", "64", "65", "66", "70", "71", "72", "73", "74", "75", "98", "99"]
    if not cst_pis or cst_pis not in cst_pis_validos:
        return None
    
    # VL_ITEM: obrigatório, valor total dos itens (numérico, 2 decimais, positivo)
    ok_vl_item, val_vl_item, _ = validar_valor_numerico(vl_item, decimais=2, obrigatorio=True, positivo=True)
    if not ok_vl_item:
        return None
    
    # NAT_BC_CRED: opcional, código da base de cálculo do crédito (2 caracteres)
    nat_bc_cred_validos = ["01", "02", "04", "13"]
    if nat_bc_cred and nat_bc_cred not in nat_bc_cred_validos:
        return None
    
    # VL_BC_PIS: obrigatório, valor da base de cálculo do PIS/PASEP (numérico, 2 decimais)
    ok_vl_bc_pis, val_vl_bc_pis, _ = validar_valor_numerico(vl_bc_pis, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok_vl_bc_pis:
        return None
    
    # ALIQ_PIS: obrigatório, alíquota do PIS em percentual (numérico, 4 decimais)
    ok_aliq_pis, val_aliq_pis, _ = validar_valor_numerico(aliq_pis, decimais=4, obrigatorio=True, nao_negativo=True)
    if not ok_aliq_pis:
        return None
    
    # VL_PIS: obrigatório, valor do PIS (numérico, 2 decimais)
    ok_vl_pis, val_vl_pis, _ = validar_valor_numerico(vl_pis, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok_vl_pis:
        return None
    
    # Validação de cálculo do VL_PIS
    # VL_PIS = VL_BC_PIS * (ALIQ_PIS / 100)
    vl_pis_calculado = val_vl_bc_pis * (val_aliq_pis / 100.0)
    # Tolerância de 0.01 para diferenças de arredondamento
    if abs(val_vl_pis - vl_pis_calculado) > 0.01:
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
        "50": "Operação com Direito a Crédito - Vinculada Exclusivamente a Receita Tributada no Mercado Interno",
        "51": "Operação com Direito a Crédito – Vinculada Exclusivamente a Receita Não Tributada no Mercado Interno",
        "52": "Operação com Direito a Crédito - Vinculada Exclusivamente a Receita de Exportação",
        "53": "Operação com Direito a Crédito - Vinculada a Receitas Tributadas e Não-Tributadas no Mercado Interno",
        "54": "Operação com Direito a Crédito - Vinculada a Receitas Tributadas no Mercado Interno e de Exportação",
        "55": "Operação com Direito a Crédito - Vinculada a Receitas Não-Tributadas no Mercado Interno e de Exportação",
        "56": "Operação com Direito a Crédito - Vinculada a Receitas Tributadas e Não-Tributadas no Mercado Interno, e de Exportação",
        "60": "Crédito Presumido - Operação de Aquisição Vinculada Exclusivamente a Receita Tributada no Mercado Interno",
        "61": "Crédito Presumido - Operação de Aquisição Vinculada Exclusivamente a Receita Não-Tributada no Mercado Interno",
        "62": "Crédito Presumido - Operação de Aquisição Vinculada Exclusivamente a Receita de Exportação",
        "63": "Crédito Presumido - Operação de Aquisição Vinculada a Receitas Tributadas e Não-Tributadas no Mercado Interno",
        "64": "Crédito Presumido - Operação de Aquisição Vinculada a Receitas Tributadas no Mercado Interno e de Exportação",
        "65": "Crédito Presumido - Operação de Aquisição Vinculada a Receitas Não-Tributadas no Mercado Interno e de Exportação",
        "66": "Crédito Presumido - Operação de Aquisição Vinculada a Receitas Tributadas e Não-Tributadas no Mercado Interno, e de Exportação",
        "70": "Operação de Aquisição sem Direito a Crédito",
        "71": "Operação de Aquisição com Isenção",
        "72": "Operação de Aquisição com Suspensão",
        "73": "Operação de Aquisição a Alíquota Zero",
        "74": "Operação de Aquisição sem Incidência da Contribuição",
        "75": "Operação de Aquisição por Substituição Tributária",
        "98": "Outras Operações de Entrada",
        "99": "Outras Operações"
    }
    
    # Descrições dos campos NAT_BC_CRED
    descricoes_nat_bc_cred = {
        "01": "Aquisição de bens para revenda",
        "02": "Aquisição de bens utilizados como insumo",
        "04": "Energia elétrica utilizada nos estabelecimentos da pessoa jurídica",
        "13": "Outras operações com direito a crédito"
    }
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg,
            "descricao": "Texto fixo contendo 'C501'"
        },
        "CST_PIS": {
            "titulo": "Código da Situação Tributária referente ao PIS/PASEP",
            "valor": cst_pis,
            "descricao": descricoes_cst.get(cst_pis, "")
        },
        "VL_ITEM": {
            "titulo": "Valor total dos itens",
            "valor": vl_item,
            "valor_formatado": fmt_valor(val_vl_item)
        },
        "NAT_BC_CRED": {
            "titulo": "Código da Base de Cálculo do Crédito",
            "valor": nat_bc_cred,
            "descricao": descricoes_nat_bc_cred.get(nat_bc_cred, "")
        },
        "VL_BC_PIS": {
            "titulo": "Valor da base de cálculo do PIS/PASEP",
            "valor": vl_bc_pis,
            "valor_formatado": fmt_valor(val_vl_bc_pis)
        },
        "ALIQ_PIS": {
            "titulo": "Alíquota do PIS/PASEP (em percentual)",
            "valor": aliq_pis,
            "valor_formatado": fmt_valor_decimais(val_aliq_pis, 4) if aliq_pis else ""
        },
        "VL_PIS": {
            "titulo": "Valor do PIS/PASEP",
            "valor": vl_pis,
            "valor_formatado": fmt_valor(val_vl_pis)
        },
        "COD_CTA": {
            "titulo": "Código da conta analítica contábil debitada/creditada",
            "valor": cod_cta
        }
    }
    
    return resultado


def validar_c501(linhas):
    """
    Valida uma ou mais linhas do registro C501 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |C501|CST_PIS|VL_ITEM|NAT_BC_CRED|VL_BC_PIS|ALIQ_PIS|VL_PIS|COD_CTA|
        
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
        resultado = _processar_linha_c501(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
