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


def _processar_linha_d105(linha):
    """
    Processa uma única linha do registro D105 e retorna um dicionário.
    
    Formato:
      |D105|IND_NAT_FRT|VL_ITEM|CST_COFINS|NAT_BC_CRED|VL_BC_COFINS|ALIQ_COFINS|VL_COFINS|COD_CTA|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "D105"
    - IND_NAT_FRT: obrigatório, valores válidos [0, 1, 2, 3, 4, 5, 9]
    - VL_ITEM: obrigatório, numérico com 2 decimais
    - CST_COFINS: obrigatório, 2 dígitos, código da situação tributária
      - Valores válidos: [50, 51, 52, 53, 54, 55, 56, 60, 61, 62, 63, 64, 65, 66, 70, 71, 72, 73, 74, 75, 98, 99]
    - NAT_BC_CRED: opcional, 2 caracteres (código conforme Tabela 4.3.7)
    - VL_BC_COFINS: opcional, numérico com 2 decimais
    - ALIQ_COFINS: opcional, numérico com 8 dígitos e 4 decimais (percentual)
    - VL_COFINS: opcional, numérico com 2 decimais
      - Deve corresponder a VL_BC_COFINS * ALIQ_COFINS / 100 (validação)
    - COD_CTA: opcional, máximo 255 caracteres
      - Obrigatório a partir de novembro/2017, exceto se dispensado de ECD (validação em camada superior)
    
    Nota: Serão escrituradas neste registro as informações referentes à incidência, base de cálculo,
    alíquota e valor do crédito de Cofins, básicos ou presumidos, referente às operações de transporte
    contratadas ou subcontratadas, conforme previsto na legislação.
    
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
    # Remove primeiro e último se vazios (formato padrão SPED: |D105|...|)
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
    if reg != "D105":
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
    
    # Extrai todos os campos (9 campos no total)
    ind_nat_frt = obter_campo(1)
    vl_item = obter_campo(2)
    cst_cofins = obter_campo(3)
    nat_bc_cred = obter_campo(4)
    vl_bc_cofins = obter_campo(5)
    aliq_cofins = obter_campo(6)
    vl_cofins = obter_campo(7)
    cod_cta = obter_campo(8)
    
    # Validações básicas dos campos obrigatórios
    
    # IND_NAT_FRT: obrigatório, valores válidos [0, 1, 2, 3, 4, 5, 9]
    ind_nat_frt_validos = ["0", "1", "2", "3", "4", "5", "9"]
    if not ind_nat_frt or ind_nat_frt not in ind_nat_frt_validos:
        return None
    
    # VL_ITEM: obrigatório, numérico com 2 decimais
    ok1, val1, _ = validar_valor_numerico(vl_item, decimais=2, obrigatorio=True)
    if not ok1:
        return None
    
    # CST_COFINS: obrigatório, 2 dígitos, valores válidos
    cst_cofins_validos = ["50", "51", "52", "53", "54", "55", "56", "60", "61", "62", "63", "64", "65", "66", "70", "71", "72", "73", "74", "75", "98", "99"]
    if not cst_cofins or len(cst_cofins) != 2 or cst_cofins not in cst_cofins_validos:
        return None
    
    # NAT_BC_CRED: opcional, 2 caracteres
    if nat_bc_cred and len(nat_bc_cred) > 2:
        return None
    
    # VL_BC_COFINS: opcional, numérico com 2 decimais
    ok2, val2, _ = validar_valor_numerico(vl_bc_cofins, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok2:
        return None
    
    # ALIQ_COFINS: opcional, numérico com 8 dígitos e 4 decimais (percentual)
    # Formato: N(008,4) - até 8 dígitos na parte inteira e 4 decimais
    ok3, val3, _ = validar_valor_numerico(aliq_cofins, decimais=4, obrigatorio=False, nao_negativo=True)
    if not ok3:
        return None
    # Verifica se tem no máximo 8 dígitos na parte inteira
    if aliq_cofins:
        partes_aliq = aliq_cofins.split(".")
        parte_inteira = partes_aliq[0]
        if len(parte_inteira) > 8:
            return None
    
    # VL_COFINS: opcional, numérico com 2 decimais
    ok4, val4, _ = validar_valor_numerico(vl_cofins, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok4:
        return None
    
    # Validação: VL_COFINS deve corresponder a VL_BC_COFINS * ALIQ_COFINS / 100
    if vl_bc_cofins and aliq_cofins and vl_cofins:
        vl_cofins_calculado = round((val2 * val3) / 100, 2)
        # Permite pequena diferença devido a arredondamentos (tolerância de 0.01)
        if abs(val4 - vl_cofins_calculado) > 0.01:
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
    descricoes_ind_nat_frt = {
        "0": "Operações de vendas, com ônus suportado pelo estabelecimento vendedor",
        "1": "Operações de vendas, com ônus suportado pelo adquirente",
        "2": "Operações de compras (bens para revenda, matérias-prima e outros produtos, geradores de crédito)",
        "3": "Operações de compras (bens para revenda, matérias-prima e outros produtos, não geradores de crédito)",
        "4": "Transferência de produtos acabados entre estabelecimentos da pessoa jurídica",
        "5": "Transferência de produtos em elaboração entre estabelecimentos da pessoa jurídica",
        "9": "Outras"
    }
    
    descricoes_cst_cofins = {
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
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "IND_NAT_FRT": {
            "titulo": "Indicador da Natureza do Frete Contratado",
            "valor": ind_nat_frt,
            "descricao": descricoes_ind_nat_frt.get(ind_nat_frt, "")
        },
        "VL_ITEM": {
            "titulo": "Valor total dos itens",
            "valor": vl_item,
            "valor_formatado": fmt_valor(val1)
        },
        "CST_COFINS": {
            "titulo": "Código da Situação Tributária referente a COFINS",
            "valor": cst_cofins,
            "descricao": descricoes_cst_cofins.get(cst_cofins, "")
        },
        "NAT_BC_CRED": {
            "titulo": "Código da base de Cálculo do Crédito, conforme a Tabela indicada no item 4.3.7",
            "valor": nat_bc_cred
        },
        "VL_BC_COFINS": {
            "titulo": "Valor da base de cálculo da COFINS",
            "valor": vl_bc_cofins,
            "valor_formatado": fmt_valor(val2) if vl_bc_cofins else ""
        },
        "ALIQ_COFINS": {
            "titulo": "Alíquota da COFINS (em percentual)",
            "valor": aliq_cofins,
            "valor_formatado": fmt_percentual(val3) if aliq_cofins else ""
        },
        "VL_COFINS": {
            "titulo": "Valor da COFINS",
            "valor": vl_cofins,
            "valor_formatado": fmt_valor(val4) if vl_cofins else ""
        },
        "COD_CTA": {
            "titulo": "Código da conta analítica contábil debitada/creditada",
            "valor": cod_cta
        }
    }
    
    return resultado


def validar_d105(linhas):
    """
    Valida uma ou mais linhas do registro D105 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |D105|IND_NAT_FRT|VL_ITEM|CST_COFINS|NAT_BC_CRED|VL_BC_COFINS|ALIQ_COFINS|VL_COFINS|COD_CTA|
        
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
        resultado = _processar_linha_d105(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
