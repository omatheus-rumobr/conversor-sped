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


def _processar_linha_f150(linha):
    """
    Processa uma única linha do registro F150 e retorna um dicionário.
    
    Formato:
      |F150|NAT_BC_CRED|VL_TOT_EST|EST_IMP|VL_BC_EST|VL_BC_MEN_EST|CST_PIS|ALIQ_PIS|VL_CRED_PIS|CST_COFINS|ALIQ_COFINS|VL_CRED_COFINS|DESC_EST|COD_CTA|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "F150"
    - NAT_BC_CRED: obrigatório, valor fixo "18"
    - VL_TOT_EST: obrigatório, numérico com 2 decimais
    - EST_IMP: opcional, numérico com 2 decimais
    - VL_BC_EST: obrigatório, numérico com 2 decimais
      - Deve ser = VL_TOT_EST - EST_IMP (validação)
    - VL_BC_MEN_EST: obrigatório, numérico com 2 decimais
      - Deve ser = VL_BC_EST / 12 (validação)
    - CST_PIS: obrigatório, valores válidos [50, 51, 52, 53, 54, 55, 56]
    - ALIQ_PIS: obrigatório, valor fixo "0,65" ou "0.65" (0.65%)
    - VL_CRED_PIS: obrigatório, numérico com 2 decimais
      - Deve ser = VL_BC_MEN_EST * ALIQ_PIS / 100 (validação)
    - CST_COFINS: obrigatório, valores válidos [50, 51, 52, 53, 54, 55, 56]
    - ALIQ_COFINS: obrigatório, valor fixo "3,0" ou "3.0" (3.0%)
    - VL_CRED_COFINS: obrigatório, numérico com 2 decimais
      - Deve ser = VL_BC_MEN_EST * ALIQ_COFINS / 100 (validação)
    - DESC_EST: opcional, máximo 100 caracteres
    - COD_CTA: opcional, máximo 255 caracteres
    
    Nota: Deve ser objeto de escrituração neste registro o crédito sobre o estoque de abertura de bens
    adquiridos para revenda (exceto os tributados no regime de substituição tributária e no regime
    monofásico) ou de bens a serem utilizados como insumo na prestação de serviços e na produção ou
    fabricação de bens ou produtos destinados à venda, adquiridos de pessoa jurídica domiciliada no País,
    existentes na data de início da incidência no regime não-cumulativo das contribuições sociais.
    
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
    # Remove primeiro e último se vazios (formato padrão SPED: |F150|...|)
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
    if reg != "F150":
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
    nat_bc_cred = obter_campo(1)
    vl_tot_est = obter_campo(2)
    est_imp = obter_campo(3)
    vl_bc_est = obter_campo(4)
    vl_bc_men_est = obter_campo(5)
    cst_pis = obter_campo(6)
    aliq_pis = obter_campo(7)
    vl_cred_pis = obter_campo(8)
    cst_cofins = obter_campo(9)
    aliq_cofins = obter_campo(10)
    vl_cred_cofins = obter_campo(11)
    desc_est = obter_campo(12)
    cod_cta = obter_campo(13)
    
    # Validações básicas dos campos obrigatórios
    
    # NAT_BC_CRED: obrigatório, valor fixo "18"
    if not nat_bc_cred or nat_bc_cred != "18":
        return None
    
    # VL_TOT_EST: obrigatório, numérico com 2 decimais
    ok1, val1, _ = validar_valor_numerico(vl_tot_est, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok1:
        return None
    
    # EST_IMP: opcional, numérico com 2 decimais
    ok2, val2, _ = validar_valor_numerico(est_imp, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok2:
        return None
    
    # VL_BC_EST: obrigatório, numérico com 2 decimais
    ok3, val3, _ = validar_valor_numerico(vl_bc_est, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok3:
        return None
    
    # Validação: VL_BC_EST deve ser = VL_TOT_EST - EST_IMP
    vl_bc_est_calculado = round(val1 - val2, 2)
    # Permite pequena diferença devido a arredondamentos (tolerância de 0.01)
    if abs(val3 - vl_bc_est_calculado) > 0.01:
        return None
    
    # VL_BC_MEN_EST: obrigatório, numérico com 2 decimais
    ok4, val4, _ = validar_valor_numerico(vl_bc_men_est, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok4:
        return None
    
    # Validação: VL_BC_MEN_EST deve ser = VL_BC_EST / 12
    vl_bc_men_est_calculado = round(val3 / 12, 2)
    # Permite pequena diferença devido a arredondamentos (tolerância de 0.01)
    if abs(val4 - vl_bc_men_est_calculado) > 0.01:
        return None
    
    # CST_PIS: obrigatório, valores válidos [50, 51, 52, 53, 54, 55, 56]
    cst_pis_validos = ["50", "51", "52", "53", "54", "55", "56"]
    if not cst_pis or len(cst_pis) != 2 or cst_pis not in cst_pis_validos:
        return None
    
    # ALIQ_PIS: obrigatório, valor fixo "0,65" ou "0.65" (0.65%)
    # Normaliza vírgula para ponto
    aliq_pis_normalizada = aliq_pis.replace(",", ".") if aliq_pis else ""
    ok5, val5, _ = validar_valor_numerico(aliq_pis_normalizada, decimais=4, obrigatorio=True, nao_negativo=True)
    if not ok5:
        return None
    # Valida se é aproximadamente 0.65 (tolerância de 0.0001)
    if abs(val5 - 0.65) > 0.0001:
        return None
    
    # VL_CRED_PIS: obrigatório, numérico com 2 decimais
    ok6, val6, _ = validar_valor_numerico(vl_cred_pis, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok6:
        return None
    
    # Validação: VL_CRED_PIS deve ser = VL_BC_MEN_EST * ALIQ_PIS / 100
    vl_cred_pis_calculado = round((val4 * val5) / 100, 2)
    # Permite pequena diferença devido a arredondamentos (tolerância de 0.01)
    if abs(val6 - vl_cred_pis_calculado) > 0.01:
        return None
    
    # CST_COFINS: obrigatório, valores válidos [50, 51, 52, 53, 54, 55, 56]
    cst_cofins_validos = ["50", "51", "52", "53", "54", "55", "56"]
    if not cst_cofins or len(cst_cofins) != 2 or cst_cofins not in cst_cofins_validos:
        return None
    
    # ALIQ_COFINS: obrigatório, valor fixo "3,0" ou "3.0" (3.0%)
    # Normaliza vírgula para ponto
    aliq_cofins_normalizada = aliq_cofins.replace(",", ".") if aliq_cofins else ""
    ok7, val7, _ = validar_valor_numerico(aliq_cofins_normalizada, decimais=4, obrigatorio=True, nao_negativo=True)
    if not ok7:
        return None
    # Valida se é aproximadamente 3.0 (tolerância de 0.0001)
    if abs(val7 - 3.0) > 0.0001:
        return None
    
    # VL_CRED_COFINS: obrigatório, numérico com 2 decimais
    ok8, val8, _ = validar_valor_numerico(vl_cred_cofins, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok8:
        return None
    
    # Validação: VL_CRED_COFINS deve ser = VL_BC_MEN_EST * ALIQ_COFINS / 100
    vl_cred_cofins_calculado = round((val4 * val7) / 100, 2)
    # Permite pequena diferença devido a arredondamentos (tolerância de 0.01)
    if abs(val8 - vl_cred_cofins_calculado) > 0.01:
        return None
    
    # DESC_EST: opcional, máximo 100 caracteres
    if desc_est and len(desc_est) > 100:
        return None
    
    # COD_CTA: opcional, máximo 255 caracteres
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
    descricoes_nat_bc_cred = {
        "18": "Crédito sobre Estoque de Abertura"
    }
    
    descricoes_cst_pis = {
        "50": "Operação com Direito a Crédito - Vinculada Exclusivamente a Receita Tributada no Mercado Interno",
        "51": "Operação com Direito a Crédito – Vinculada Exclusivamente a Receita Não Tributada no Mercado Interno",
        "52": "Operação com Direito a Crédito - Vinculada Exclusivamente a Receita de Exportação",
        "53": "Operação com Direito a Crédito - Vinculada a Receitas Tributadas e Não-Tributadas no Mercado Interno",
        "54": "Operação com Direito a Crédito - Vinculada a Receitas Tributadas no Mercado Interno e de Exportação",
        "55": "Operação com Direito a Crédito - Vinculada a Receitas Não-Tributadas no Mercado Interno e de Exportação",
        "56": "Operação com Direito a Crédito - Vinculada a Receitas Tributadas e Não-Tributadas no Mercado Interno, e de Exportação"
    }
    
    descricoes_cst_cofins = {
        "50": "Operação com Direito a Crédito - Vinculada Exclusivamente a Receita Tributada no Mercado Interno",
        "51": "Operação com Direito a Crédito – Vinculada Exclusivamente a Receita Não Tributada no Mercado Interno",
        "52": "Operação com Direito a Crédito - Vinculada Exclusivamente a Receita de Exportação",
        "53": "Operação com Direito a Crédito - Vinculada a Receitas Tributadas e Não-Tributadas no Mercado Interno",
        "54": "Operação com Direito a Crédito - Vinculada a Receitas Tributadas no Mercado Interno e de Exportação",
        "55": "Operação com Direito a Crédito - Vinculada a Receitas Não-Tributadas no Mercado Interno e de Exportação",
        "56": "Operação com Direito a Crédito - Vinculada a Receitas Tributadas e Não-Tributadas no Mercado Interno, e de Exportação"
    }
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "NAT_BC_CRED": {
            "titulo": "Código da Base de Cálculo do Crédito sobre Estoque de Abertura, conforme a Tabela indicada no item 4.3.7",
            "valor": nat_bc_cred,
            "descricao": descricoes_nat_bc_cred.get(nat_bc_cred, "")
        },
        "VL_TOT_EST": {
            "titulo": "Valor Total do Estoque de Abertura",
            "valor": vl_tot_est,
            "valor_formatado": fmt_valor(val1)
        },
        "EST_IMP": {
            "titulo": "Parcela do estoque de abertura referente a bens, produtos e mercadorias importados, ou adquiridas no mercado interno sem direito ao crédito",
            "valor": est_imp,
            "valor_formatado": fmt_valor(val2) if est_imp else ""
        },
        "VL_BC_EST": {
            "titulo": "Valor da Base de Cálculo do Crédito sobre o Estoque de Abertura (03 – 04)",
            "valor": vl_bc_est,
            "valor_formatado": fmt_valor(val3)
        },
        "VL_BC_MEN_EST": {
            "titulo": "Valor da Base de Cálculo Mensal do Crédito sobre o Estoque de Abertura (1/12 avos do campo 05)",
            "valor": vl_bc_men_est,
            "valor_formatado": fmt_valor(val4)
        },
        "CST_PIS": {
            "titulo": "Código da Situação Tributária referente ao PIS/PASEP, conforme a Tabela indicada no item 4.3.3",
            "valor": cst_pis,
            "descricao": descricoes_cst_pis.get(cst_pis, "")
        },
        "ALIQ_PIS": {
            "titulo": "Alíquota do PIS/PASEP (em percentual)",
            "valor": aliq_pis,
            "valor_formatado": fmt_percentual(val5)
        },
        "VL_CRED_PIS": {
            "titulo": "Valor Mensal do Crédito Presumido Apurado para o Período - PIS/PASEP (06 x 08)",
            "valor": vl_cred_pis,
            "valor_formatado": fmt_valor(val6)
        },
        "CST_COFINS": {
            "titulo": "Código da Situação Tributária referente a COFINS, conforme a Tabela indicada no item 4.3.4",
            "valor": cst_cofins,
            "descricao": descricoes_cst_cofins.get(cst_cofins, "")
        },
        "ALIQ_COFINS": {
            "titulo": "Alíquota da COFINS (em percentual)",
            "valor": aliq_cofins,
            "valor_formatado": fmt_percentual(val7)
        },
        "VL_CRED_COFINS": {
            "titulo": "Valor Mensal do Crédito Presumido Apurado para o Período - COFINS (06 x 11)",
            "valor": vl_cred_cofins,
            "valor_formatado": fmt_valor(val8)
        },
        "DESC_EST": {
            "titulo": "Descrição do estoque",
            "valor": desc_est
        },
        "COD_CTA": {
            "titulo": "Código da conta analítica contábil debitada/creditada",
            "valor": cod_cta
        }
    }
    
    return resultado


def validar_f150(linhas):
    """
    Valida uma ou mais linhas do registro F150 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |F150|NAT_BC_CRED|VL_TOT_EST|EST_IMP|VL_BC_EST|VL_BC_MEN_EST|CST_PIS|ALIQ_PIS|VL_CRED_PIS|CST_COFINS|ALIQ_COFINS|VL_CRED_COFINS|DESC_EST|COD_CTA|
        
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
        resultado = _processar_linha_f150(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
