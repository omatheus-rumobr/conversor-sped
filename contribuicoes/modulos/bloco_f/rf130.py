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


def _processar_linha_f130(linha):
    """
    Processa uma única linha do registro F130 e retorna um dicionário.
    
    Formato:
      |F130|NAT_BC_CRED|IDENT_BEM_IMOB|IND_ORIG_CRED|IND_UTIL_BEM_IMOB|MES_OPER_AQUIS|VL_OPER_AQUIS|PARC_OPER_NAO_BC_CRED|VL_BC_CRED|IND_NR_PARC|CST_PIS|VL_BC_PIS|ALIQ_PIS|VL_PIS|CST_COFINS|VL_BC_COFINS|ALIQ_COFINS|VL_COFINS|COD_CTA|COD_CCUS|DESC_BEM_IMOB|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "F130"
    - NAT_BC_CRED: obrigatório, valor fixo "10"
    - IDENT_BEM_IMOB: obrigatório, valores válidos [01, 02, 03, 04, 05, 06, 99]
    - IND_ORIG_CRED: opcional, valores válidos [0, 1]
    - IND_UTIL_BEM_IMOB: obrigatório, valores válidos [1, 2, 3, 9]
    - MES_OPER_AQUIS: opcional, 6 dígitos (mês/ano de aquisição)
    - VL_OPER_AQUIS: obrigatório, numérico com 2 decimais
    - PARC_OPER_NAO_BC_CRED: opcional, numérico com 2 decimais
    - VL_BC_CRED: obrigatório, numérico com 2 decimais
      - Deve ser = VL_OPER_AQUIS - PARC_OPER_NAO_BC_CRED (validação)
    - IND_NR_PARC: obrigatório, valores válidos [1, 2, 3, 4, 5, 9]
    - CST_PIS: obrigatório, 2 dígitos
    - VL_BC_PIS: opcional, numérico com 2 decimais
      - Deve ser = VL_BC_CRED / número de meses (validação)
    - ALIQ_PIS: opcional, numérico com 8 dígitos e 4 decimais (percentual)
    - VL_PIS: opcional, numérico com 2 decimais
      - Deve corresponder a VL_BC_PIS * ALIQ_PIS / 100 (validação)
    - CST_COFINS: obrigatório, 2 dígitos
    - VL_BC_COFINS: opcional, numérico com 2 decimais
      - Deve ser = VL_BC_CRED / número de meses (validação)
    - ALIQ_COFINS: opcional, numérico com 8 dígitos e 4 decimais (percentual)
    - VL_COFINS: opcional, numérico com 2 decimais
      - Deve corresponder a VL_BC_COFINS * ALIQ_COFINS / 100 (validação)
    - COD_CTA: opcional, máximo 255 caracteres
    - COD_CCUS: opcional, máximo 255 caracteres
    - DESC_BEM_IMOB: opcional, sem limite de tamanho
    
    Nota: Registro específico para a escrituração dos créditos determinados com base no valor de aquisição
    de bens incorporados ao Ativo Imobilizado da pessoa jurídica, adquiridos para utilização na produção
    de bens destinados à venda, ou na prestação de serviços.
    
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
    # Remove primeiro e último se vazios (formato padrão SPED: |F130|...|)
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
    if reg != "F130":
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
    
    # Extrai todos os campos (21 campos no total)
    nat_bc_cred = obter_campo(1)
    ident_bem_imob = obter_campo(2)
    ind_orig_cred = obter_campo(3)
    ind_util_bem_imob = obter_campo(4)
    mes_oper_aquis = obter_campo(5)
    vl_oper_aquis = obter_campo(6)
    parc_oper_nao_bc_cred = obter_campo(7)
    vl_bc_cred = obter_campo(8)
    ind_nr_parc = obter_campo(9)
    cst_pis = obter_campo(10)
    vl_bc_pis = obter_campo(11)
    aliq_pis = obter_campo(12)
    vl_pis = obter_campo(13)
    cst_cofins = obter_campo(14)
    vl_bc_cofins = obter_campo(15)
    aliq_cofins = obter_campo(16)
    vl_cofins = obter_campo(17)
    cod_cta = obter_campo(18)
    cod_ccus = obter_campo(19)
    desc_bem_imob = obter_campo(20)
    
    # Validações básicas dos campos obrigatórios
    
    # NAT_BC_CRED: obrigatório, valor fixo "10"
    if not nat_bc_cred or nat_bc_cred != "10":
        return None
    
    # IDENT_BEM_IMOB: obrigatório, valores válidos [01, 02, 03, 04, 05, 06, 99]
    ident_bem_imob_validos = ["01", "02", "03", "04", "05", "06", "99"]
    if not ident_bem_imob or ident_bem_imob not in ident_bem_imob_validos:
        return None
    
    # IND_ORIG_CRED: opcional, valores válidos [0, 1]
    if ind_orig_cred and ind_orig_cred not in ["0", "1"]:
        return None
    
    # IND_UTIL_BEM_IMOB: obrigatório, valores válidos [1, 2, 3, 9]
    ind_util_bem_imob_validos = ["1", "2", "3", "9"]
    if not ind_util_bem_imob or ind_util_bem_imob not in ind_util_bem_imob_validos:
        return None
    
    # MES_OPER_AQUIS: opcional, 6 dígitos (mês/ano de aquisição)
    if mes_oper_aquis:
        if not mes_oper_aquis.isdigit() or len(mes_oper_aquis) != 6:
            return None
        mes = int(mes_oper_aquis[:2])
        if mes < 1 or mes > 12:
            return None
    
    # VL_OPER_AQUIS: obrigatório, numérico com 2 decimais
    ok1, val1, _ = validar_valor_numerico(vl_oper_aquis, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok1:
        return None
    
    # PARC_OPER_NAO_BC_CRED: opcional, numérico com 2 decimais
    ok2, val2, _ = validar_valor_numerico(parc_oper_nao_bc_cred, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok2:
        return None
    
    # VL_BC_CRED: obrigatório, numérico com 2 decimais
    ok3, val3, _ = validar_valor_numerico(vl_bc_cred, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok3:
        return None
    
    # Validação: VL_BC_CRED deve ser = VL_OPER_AQUIS - PARC_OPER_NAO_BC_CRED
    vl_bc_cred_calculado = round(val1 - val2, 2)
    # Permite pequena diferença devido a arredondamentos (tolerância de 0.01)
    if abs(val3 - vl_bc_cred_calculado) > 0.01:
        return None
    
    # IND_NR_PARC: obrigatório, valores válidos [1, 2, 3, 4, 5, 9]
    ind_nr_parc_validos = ["1", "2", "3", "4", "5", "9"]
    if not ind_nr_parc or ind_nr_parc not in ind_nr_parc_validos:
        return None
    
    # Mapeia IND_NR_PARC para número de meses
    meses_por_indicador = {
        "1": 1,   # Integral (Mês de Aquisição)
        "2": 12,  # 12 Meses
        "3": 24,  # 24 Meses
        "4": 48,  # 48 Meses
        "5": 6,   # 6 Meses (Embalagens de bebidas frias)
        "9": None # Outra periodicidade definida em Lei (não sabemos o número exato)
    }
    num_meses = meses_por_indicador.get(ind_nr_parc)
    
    # CST_PIS: obrigatório, 2 dígitos
    if not cst_pis or len(cst_pis) != 2 or not cst_pis.isdigit():
        return None
    
    # VL_BC_PIS: opcional, numérico com 2 decimais
    ok4, val4, _ = validar_valor_numerico(vl_bc_pis, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok4:
        return None
    
    # Validação: VL_BC_PIS deve ser = VL_BC_CRED / número de meses (quando IND_NR_PARC != 9)
    if vl_bc_pis and num_meses:
        vl_bc_pis_calculado = round(val3 / num_meses, 2)
        # Permite pequena diferença devido a arredondamentos (tolerância de 0.01)
        if abs(val4 - vl_bc_pis_calculado) > 0.01:
            return None
    
    # ALIQ_PIS: opcional, numérico com 8 dígitos e 4 decimais (percentual)
    ok5, val5, _ = validar_valor_numerico(aliq_pis, decimais=4, obrigatorio=False, nao_negativo=True)
    if not ok5:
        return None
    # Verifica se tem no máximo 8 dígitos na parte inteira
    if aliq_pis:
        partes_aliq = aliq_pis.split(".")
        parte_inteira = partes_aliq[0]
        if len(parte_inteira) > 8:
            return None
    
    # VL_PIS: opcional, numérico com 2 decimais
    ok6, val6, _ = validar_valor_numerico(vl_pis, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok6:
        return None
    
    # Validação: VL_PIS deve corresponder a VL_BC_PIS * ALIQ_PIS / 100
    if vl_bc_pis and aliq_pis and vl_pis:
        vl_pis_calculado = round((val4 * val5) / 100, 2)
        # Permite pequena diferença devido a arredondamentos (tolerância de 0.01)
        if abs(val6 - vl_pis_calculado) > 0.01:
            return None
    
    # CST_COFINS: obrigatório, 2 dígitos
    if not cst_cofins or len(cst_cofins) != 2 or not cst_cofins.isdigit():
        return None
    
    # VL_BC_COFINS: opcional, numérico com 2 decimais
    ok7, val7, _ = validar_valor_numerico(vl_bc_cofins, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok7:
        return None
    
    # Validação: VL_BC_COFINS deve ser = VL_BC_CRED / número de meses (quando IND_NR_PARC != 9)
    if vl_bc_cofins and num_meses:
        vl_bc_cofins_calculado = round(val3 / num_meses, 2)
        # Permite pequena diferença devido a arredondamentos (tolerância de 0.01)
        if abs(val7 - vl_bc_cofins_calculado) > 0.01:
            return None
    
    # ALIQ_COFINS: opcional, numérico com 8 dígitos e 4 decimais (percentual)
    ok8, val8, _ = validar_valor_numerico(aliq_cofins, decimais=4, obrigatorio=False, nao_negativo=True)
    if not ok8:
        return None
    # Verifica se tem no máximo 8 dígitos na parte inteira
    if aliq_cofins:
        partes_aliq_cofins = aliq_cofins.split(".")
        parte_inteira_cofins = partes_aliq_cofins[0]
        if len(parte_inteira_cofins) > 8:
            return None
    
    # VL_COFINS: opcional, numérico com 2 decimais
    ok9, val9, _ = validar_valor_numerico(vl_cofins, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok9:
        return None
    
    # Validação: VL_COFINS deve corresponder a VL_BC_COFINS * ALIQ_COFINS / 100
    if vl_bc_cofins and aliq_cofins and vl_cofins:
        vl_cofins_calculado = round((val7 * val8) / 100, 2)
        # Permite pequena diferença devido a arredondamentos (tolerância de 0.01)
        if abs(val9 - vl_cofins_calculado) > 0.01:
            return None
    
    # COD_CTA: opcional, máximo 255 caracteres
    if cod_cta and len(cod_cta) > 255:
        return None
    
    # COD_CCUS: opcional, máximo 255 caracteres
    if cod_ccus and len(cod_ccus) > 255:
        return None
    
    # DESC_BEM_IMOB: opcional, sem limite de tamanho (não precisa validar tamanho)
    
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
    
    # Função auxiliar para formatar mês/ano
    def fmt_mes_ano(mes_ano_str):
        if mes_ano_str and len(mes_ano_str) == 6:
            return f"{mes_ano_str[:2]}/{mes_ano_str[2:6]}"
        return mes_ano_str
    
    # Descrições dos campos
    descricoes_nat_bc_cred = {
        "10": "Crédito com Base no Valor de Aquisição/Contribuição"
    }
    
    descricoes_ident_bem_imob = {
        "01": "Edificações e Benfeitorias",
        "02": "Edificações e Benfeitorias em Imóveis de Terceiros",
        "03": "Instalações",
        "04": "Máquinas",
        "05": "Equipamentos",
        "06": "Veículos",
        "99": "Outros bens incorporados ao Ativo Imobilizado"
    }
    
    descricoes_ind_orig_cred = {
        "0": "Aquisição no Mercado Interno",
        "1": "Aquisição no Mercado Externo (Importação)"
    }
    
    descricoes_ind_util_bem_imob = {
        "1": "Produção de Bens Destinados a Venda",
        "2": "Prestação de Serviços",
        "3": "Locação a Terceiros",
        "9": "Outros"
    }
    
    descricoes_ind_nr_parc = {
        "1": "Integral (Mês de Aquisição)",
        "2": "12 Meses",
        "3": "24 Meses",
        "4": "48 Meses",
        "5": "6 Meses (Embalagens de bebidas frias)",
        "9": "Outra periodicidade definida em Lei"
    }
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "NAT_BC_CRED": {
            "titulo": "Código da Base de Cálculo do Crédito sobre Bens Incorporados ao Ativo Imobilizado, conforme a Tabela indicada no item 4.3.7",
            "valor": nat_bc_cred,
            "descricao": descricoes_nat_bc_cred.get(nat_bc_cred, "")
        },
        "IDENT_BEM_IMOB": {
            "titulo": "Identificação dos bens ou grupo de bens incorporados ao Ativo Imobilizado",
            "valor": ident_bem_imob,
            "descricao": descricoes_ident_bem_imob.get(ident_bem_imob, "")
        },
        "IND_ORIG_CRED": {
            "titulo": "Indicador da origem do bem incorporado ao ativo imobilizado, gerador de crédito",
            "valor": ind_orig_cred,
            "descricao": descricoes_ind_orig_cred.get(ind_orig_cred, "") if ind_orig_cred else ""
        },
        "IND_UTIL_BEM_IMOB": {
            "titulo": "Indicador da Utilização dos Bens Incorporados ao Ativo Imobilizado",
            "valor": ind_util_bem_imob,
            "descricao": descricoes_ind_util_bem_imob.get(ind_util_bem_imob, "")
        },
        "MES_OPER_AQUIS": {
            "titulo": "Mês/Ano de Aquisição dos Bens Incorporados ao Ativo Imobilizado, com apuração de crédito com base no valor de aquisição",
            "valor": mes_oper_aquis,
            "valor_formatado": fmt_mes_ano(mes_oper_aquis) if mes_oper_aquis else ""
        },
        "VL_OPER_AQUIS": {
            "titulo": "Valor de Aquisição dos Bens Incorporados ao Ativo Imobilizado – Crédito com base no valor de aquisição",
            "valor": vl_oper_aquis,
            "valor_formatado": fmt_valor(val1)
        },
        "PARC_OPER_NAO_BC_CRED": {
            "titulo": "Parcela do Valor de Aquisição a excluir da base de cálculo de Crédito",
            "valor": parc_oper_nao_bc_cred,
            "valor_formatado": fmt_valor(val2) if parc_oper_nao_bc_cred else ""
        },
        "VL_BC_CRED": {
            "titulo": "Valor da Base de Cálculo do Crédito sobre Bens Incorporados ao Ativo Imobilizado (07 – 08)",
            "valor": vl_bc_cred,
            "valor_formatado": fmt_valor(val3)
        },
        "IND_NR_PARC": {
            "titulo": "Indicador do Número de Parcelas a serem apropriadas (Crédito sobre Valor de Aquisição)",
            "valor": ind_nr_parc,
            "descricao": descricoes_ind_nr_parc.get(ind_nr_parc, "")
        },
        "CST_PIS": {
            "titulo": "Código da Situação Tributária referente ao PIS/PASEP, conforme a Tabela indicada no item 4.3.3",
            "valor": cst_pis
        },
        "VL_BC_PIS": {
            "titulo": "Base de cálculo Mensal do Crédito de PIS/PASEP, conforme indicador informado no campo 10",
            "valor": vl_bc_pis,
            "valor_formatado": fmt_valor(val4) if vl_bc_pis else ""
        },
        "ALIQ_PIS": {
            "titulo": "Alíquota do PIS/PASEP",
            "valor": aliq_pis,
            "valor_formatado": fmt_percentual(val5) if aliq_pis else ""
        },
        "VL_PIS": {
            "titulo": "Valor do Crédito de PIS/PASEP",
            "valor": vl_pis,
            "valor_formatado": fmt_valor(val6) if vl_pis else ""
        },
        "CST_COFINS": {
            "titulo": "Código da Situação Tributária referente a COFINS, conforme a Tabela indicada no item 4.3.4",
            "valor": cst_cofins
        },
        "VL_BC_COFINS": {
            "titulo": "Base de Cálculo Mensal do Crédito da COFINS, conforme indicador informado no campo 10",
            "valor": vl_bc_cofins,
            "valor_formatado": fmt_valor(val7) if vl_bc_cofins else ""
        },
        "ALIQ_COFINS": {
            "titulo": "Alíquota da COFINS",
            "valor": aliq_cofins,
            "valor_formatado": fmt_percentual(val8) if aliq_cofins else ""
        },
        "VL_COFINS": {
            "titulo": "Valor do crédito da COFINS",
            "valor": vl_cofins,
            "valor_formatado": fmt_valor(val9) if vl_cofins else ""
        },
        "COD_CTA": {
            "titulo": "Código da conta analítica contábil debitada/creditada",
            "valor": cod_cta
        },
        "COD_CCUS": {
            "titulo": "Código do Centro de Custos",
            "valor": cod_ccus
        },
        "DESC_BEM_IMOB": {
            "titulo": "Descrição complementar do bem ou grupo de bens, com crédito apurado com base no valor de aquisição",
            "valor": desc_bem_imob
        }
    }
    
    return resultado


def validar_f130(linhas):
    """
    Valida uma ou mais linhas do registro F130 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |F130|NAT_BC_CRED|IDENT_BEM_IMOB|IND_ORIG_CRED|IND_UTIL_BEM_IMOB|MES_OPER_AQUIS|VL_OPER_AQUIS|PARC_OPER_NAO_BC_CRED|VL_BC_CRED|IND_NR_PARC|CST_PIS|VL_BC_PIS|ALIQ_PIS|VL_PIS|CST_COFINS|VL_BC_COFINS|ALIQ_COFINS|VL_COFINS|COD_CTA|COD_CCUS|DESC_BEM_IMOB|
        
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
        resultado = _processar_linha_f130(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
