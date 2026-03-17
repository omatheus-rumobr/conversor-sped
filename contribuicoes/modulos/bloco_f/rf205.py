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


def _processar_linha_f205(linha):
    """
    Processa uma única linha do registro F205 e retorna um dicionário.
    
    Formato:
      |F205|VL_CUS_INC_ACUM_ANT|VL_CUS_INC_PER_ESC|VL_CUS_INC_ACUM|VL_EXC_BC_CUS_INC_ACUM|VL_BC_CUS_INC|CST_PIS|ALIQ_PIS|VL_CRED_PIS_ACUM|VL_CRED_PIS_DESC_ANT|VL_CRED_PIS_DESC|VL_CRED_PIS_DESC_FUT|CST_COFINS|ALIQ_COFINS|VL_CRED_COFINS_ACUM|VL_CRED_COFINS_DESC_ANT|VL_CRED_COFINS_DESC|VL_CRED_COFINS_DESC_FUT|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "F205"
    - VL_CUS_INC_ACUM_ANT: obrigatório, numérico com 2 decimais
    - VL_CUS_INC_PER_ESC: obrigatório, numérico com 2 decimais
    - VL_CUS_INC_ACUM: obrigatório, numérico com 2 decimais
      - Deve ser = VL_CUS_INC_ACUM_ANT + VL_CUS_INC_PER_ESC (validação)
    - VL_EXC_BC_CUS_INC_ACUM: obrigatório, numérico com 2 decimais
    - VL_BC_CUS_INC: obrigatório, numérico com 2 decimais
      - Deve ser = VL_CUS_INC_ACUM - VL_EXC_BC_CUS_INC_ACUM (validação)
    - CST_PIS: obrigatório, 2 dígitos
    - ALIQ_PIS: obrigatório, valor fixo "1,65" ou "1.65" (1.65%)
    - VL_CRED_PIS_ACUM: obrigatório, numérico com 2 decimais
      - Deve ser = VL_BC_CUS_INC * ALIQ_PIS / 100 (validação)
    - VL_CRED_PIS_DESC_ANT: obrigatório, numérico com 2 decimais
    - VL_CRED_PIS_DESC: obrigatório, numérico com 2 decimais
    - VL_CRED_PIS_DESC_FUT: obrigatório, numérico com 2 decimais
      - Deve ser = VL_CRED_PIS_ACUM - VL_CRED_PIS_DESC_ANT - VL_CRED_PIS_DESC (validação)
    - CST_COFINS: obrigatório, 2 dígitos
    - ALIQ_COFINS: obrigatório, valor fixo "7,6" ou "7.6" (7.6%)
    - VL_CRED_COFINS_ACUM: obrigatório, numérico com 2 decimais
      - Deve ser = VL_BC_CUS_INC * ALIQ_COFINS / 100 (validação)
    - VL_CRED_COFINS_DESC_ANT: obrigatório, numérico com 2 decimais
    - VL_CRED_COFINS_DESC: obrigatório, numérico com 2 decimais
    - VL_CRED_COFINS_DESC_FUT: obrigatório, numérico com 2 decimais
      - Deve ser = VL_CRED_COFINS_ACUM - VL_CRED_COFINS_DESC_ANT - VL_CRED_COFINS_DESC (validação)
    
    Nota: Neste registro a pessoa jurídica procederá à escrituração dos créditos referentes aos custos
    vinculados à unidade imobiliária vendida, construída ou em construção. Os créditos referentes aos custos
    incorridos da unidade imobiliária vendida, conforme definido pela legislação tributária, deve ser objeto
    de utilização (desconto da contribuição apurada) pela pessoa jurídica somente a partir da efetivação da
    venda e na proporção da receita relativa à venda da unidade imobiliária, à medida do recebimento.
    
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
    # Remove primeiro e último se vazios (formato padrão SPED: |F205|...|)
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
    if reg != "F205":
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
    
    # Extrai todos os campos (18 campos no total)
    vl_cus_inc_acum_ant = obter_campo(1)
    vl_cus_inc_per_esc = obter_campo(2)
    vl_cus_inc_acum = obter_campo(3)
    vl_exc_bc_cus_inc_acum = obter_campo(4)
    vl_bc_cus_inc = obter_campo(5)
    cst_pis = obter_campo(6)
    aliq_pis = obter_campo(7)
    vl_cred_pis_acum = obter_campo(8)
    vl_cred_pis_desc_ant = obter_campo(9)
    vl_cred_pis_desc = obter_campo(10)
    vl_cred_pis_desc_fut = obter_campo(11)
    cst_cofins = obter_campo(12)
    aliq_cofins = obter_campo(13)
    vl_cred_cofins_acum = obter_campo(14)
    vl_cred_cofins_desc_ant = obter_campo(15)
    vl_cred_cofins_desc = obter_campo(16)
    vl_cred_cofins_desc_fut = obter_campo(17)
    
    # Validações básicas dos campos obrigatórios
    
    # VL_CUS_INC_ACUM_ANT: obrigatório, numérico com 2 decimais
    ok1, val1, _ = validar_valor_numerico(vl_cus_inc_acum_ant, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok1:
        return None
    
    # VL_CUS_INC_PER_ESC: obrigatório, numérico com 2 decimais
    ok2, val2, _ = validar_valor_numerico(vl_cus_inc_per_esc, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok2:
        return None
    
    # VL_CUS_INC_ACUM: obrigatório, numérico com 2 decimais
    ok3, val3, _ = validar_valor_numerico(vl_cus_inc_acum, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok3:
        return None
    
    # Validação: VL_CUS_INC_ACUM deve ser = VL_CUS_INC_ACUM_ANT + VL_CUS_INC_PER_ESC
    vl_cus_inc_acum_calculado = round(val1 + val2, 2)
    # Permite pequena diferença devido a arredondamentos (tolerância de 0.01)
    if abs(val3 - vl_cus_inc_acum_calculado) > 0.01:
        return None
    
    # VL_EXC_BC_CUS_INC_ACUM: obrigatório, numérico com 2 decimais
    ok4, val4, _ = validar_valor_numerico(vl_exc_bc_cus_inc_acum, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok4:
        return None
    
    # VL_BC_CUS_INC: obrigatório, numérico com 2 decimais
    ok5, val5, _ = validar_valor_numerico(vl_bc_cus_inc, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok5:
        return None
    
    # Validação: VL_BC_CUS_INC deve ser = VL_CUS_INC_ACUM - VL_EXC_BC_CUS_INC_ACUM
    vl_bc_cus_inc_calculado = round(val3 - val4, 2)
    # Permite pequena diferença devido a arredondamentos (tolerância de 0.01)
    if abs(val5 - vl_bc_cus_inc_calculado) > 0.01:
        return None
    
    # CST_PIS: obrigatório, 2 dígitos
    if not cst_pis or len(cst_pis) != 2 or not cst_pis.isdigit():
        return None
    
    # ALIQ_PIS: obrigatório, valor fixo "1,65" ou "1.65" (1.65%)
    # Normaliza vírgula para ponto
    aliq_pis_normalizada = aliq_pis.replace(",", ".") if aliq_pis else ""
    ok6, val6, _ = validar_valor_numerico(aliq_pis_normalizada, decimais=4, obrigatorio=True, nao_negativo=True)
    if not ok6:
        return None
    # Valida se é aproximadamente 1.65 (tolerância de 0.0001)
    if abs(val6 - 1.65) > 0.0001:
        return None
    
    # VL_CRED_PIS_ACUM: obrigatório, numérico com 2 decimais
    ok7, val7, _ = validar_valor_numerico(vl_cred_pis_acum, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok7:
        return None
    
    # Validação: VL_CRED_PIS_ACUM deve ser = VL_BC_CUS_INC * ALIQ_PIS / 100
    vl_cred_pis_acum_calculado = round((val5 * val6) / 100, 2)
    # Permite pequena diferença devido a arredondamentos (tolerância de 0.01)
    if abs(val7 - vl_cred_pis_acum_calculado) > 0.01:
        return None
    
    # VL_CRED_PIS_DESC_ANT: obrigatório, numérico com 2 decimais
    ok8, val8, _ = validar_valor_numerico(vl_cred_pis_desc_ant, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok8:
        return None
    
    # VL_CRED_PIS_DESC: obrigatório, numérico com 2 decimais
    ok9, val9, _ = validar_valor_numerico(vl_cred_pis_desc, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok9:
        return None
    
    # VL_CRED_PIS_DESC_FUT: obrigatório, numérico com 2 decimais
    ok10, val10, _ = validar_valor_numerico(vl_cred_pis_desc_fut, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok10:
        return None
    
    # Validação: VL_CRED_PIS_DESC_FUT deve ser = VL_CRED_PIS_ACUM - VL_CRED_PIS_DESC_ANT - VL_CRED_PIS_DESC
    vl_cred_pis_desc_fut_calculado = round(val7 - val8 - val9, 2)
    # Permite pequena diferença devido a arredondamentos (tolerância de 0.01)
    if abs(val10 - vl_cred_pis_desc_fut_calculado) > 0.01:
        return None
    
    # CST_COFINS: obrigatório, 2 dígitos
    if not cst_cofins or len(cst_cofins) != 2 or not cst_cofins.isdigit():
        return None
    
    # ALIQ_COFINS: obrigatório, valor fixo "7,6" ou "7.6" (7.6%)
    # Normaliza vírgula para ponto
    aliq_cofins_normalizada = aliq_cofins.replace(",", ".") if aliq_cofins else ""
    ok11, val11, _ = validar_valor_numerico(aliq_cofins_normalizada, decimais=4, obrigatorio=True, nao_negativo=True)
    if not ok11:
        return None
    # Valida se é aproximadamente 7.6 (tolerância de 0.0001)
    if abs(val11 - 7.6) > 0.0001:
        return None
    
    # VL_CRED_COFINS_ACUM: obrigatório, numérico com 2 decimais
    ok12, val12, _ = validar_valor_numerico(vl_cred_cofins_acum, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok12:
        return None
    
    # Validação: VL_CRED_COFINS_ACUM deve ser = VL_BC_CUS_INC * ALIQ_COFINS / 100
    vl_cred_cofins_acum_calculado = round((val5 * val11) / 100, 2)
    # Permite pequena diferença devido a arredondamentos (tolerância de 0.01)
    if abs(val12 - vl_cred_cofins_acum_calculado) > 0.01:
        return None
    
    # VL_CRED_COFINS_DESC_ANT: obrigatório, numérico com 2 decimais
    ok13, val13, _ = validar_valor_numerico(vl_cred_cofins_desc_ant, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok13:
        return None
    
    # VL_CRED_COFINS_DESC: obrigatório, numérico com 2 decimais
    ok14, val14, _ = validar_valor_numerico(vl_cred_cofins_desc, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok14:
        return None
    
    # VL_CRED_COFINS_DESC_FUT: obrigatório, numérico com 2 decimais
    ok15, val15, _ = validar_valor_numerico(vl_cred_cofins_desc_fut, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok15:
        return None
    
    # Validação: VL_CRED_COFINS_DESC_FUT deve ser = VL_CRED_COFINS_ACUM - VL_CRED_COFINS_DESC_ANT - VL_CRED_COFINS_DESC
    vl_cred_cofins_desc_fut_calculado = round(val12 - val13 - val14, 2)
    # Permite pequena diferença devido a arredondamentos (tolerância de 0.01)
    if abs(val15 - vl_cred_cofins_desc_fut_calculado) > 0.01:
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
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "VL_CUS_INC_ACUM_ANT": {
            "titulo": "Valor Total do Custo Incorrido da unidade imobiliária acumulado até o mês anterior ao da escrituração",
            "valor": vl_cus_inc_acum_ant,
            "valor_formatado": fmt_valor(val1)
        },
        "VL_CUS_INC_PER_ESC": {
            "titulo": "Valor Total do Custo Incorrido da unidade imobiliária no mês da escrituração",
            "valor": vl_cus_inc_per_esc,
            "valor_formatado": fmt_valor(val2)
        },
        "VL_CUS_INC_ACUM": {
            "titulo": "Valor Total do Custo Incorrido da unidade imobiliária acumulado até o mês da escrituração (Campo 02 + 03)",
            "valor": vl_cus_inc_acum,
            "valor_formatado": fmt_valor(val3)
        },
        "VL_EXC_BC_CUS_INC_ACUM": {
            "titulo": "Parcela do Custo Incorrido sem direito ao crédito da atividade imobiliária, acumulado até o período",
            "valor": vl_exc_bc_cus_inc_acum,
            "valor_formatado": fmt_valor(val4)
        },
        "VL_BC_CUS_INC": {
            "titulo": "Valor da Base de Cálculo do Crédito sobre o Custo Incorrido, acumulado até o período da escrituração (Campo 04 – 05)",
            "valor": vl_bc_cus_inc,
            "valor_formatado": fmt_valor(val5)
        },
        "CST_PIS": {
            "titulo": "Código da Situação Tributária referente ao PIS/PASEP, conforme a Tabela indicada no item 4.3.3",
            "valor": cst_pis
        },
        "ALIQ_PIS": {
            "titulo": "Alíquota do PIS/PASEP (em percentual)",
            "valor": aliq_pis,
            "valor_formatado": fmt_percentual(val6)
        },
        "VL_CRED_PIS_ACUM": {
            "titulo": "Valor Total do Crédito Acumulado sobre o custo incorrido – PIS/PASEP (Campo 06 x 08)",
            "valor": vl_cred_pis_acum,
            "valor_formatado": fmt_valor(val7)
        },
        "VL_CRED_PIS_DESC_ANT": {
            "titulo": "Parcela do crédito descontada até o período anterior da escrituração – PIS/PASEP (proporcional à receita recebida até o mês anterior)",
            "valor": vl_cred_pis_desc_ant,
            "valor_formatado": fmt_valor(val8)
        },
        "VL_CRED_PIS_DESC": {
            "titulo": "Parcela a descontar no período da escrituração – PIS/PASEP (proporcional à receita recebida no mês)",
            "valor": vl_cred_pis_desc,
            "valor_formatado": fmt_valor(val9)
        },
        "VL_CRED_PIS_DESC_FUT": {
            "titulo": "Parcela a descontar em períodos futuros – PIS/PASEP (Campo 09 – 10 – 11)",
            "valor": vl_cred_pis_desc_fut,
            "valor_formatado": fmt_valor(val10)
        },
        "CST_COFINS": {
            "titulo": "Código da Situação Tributária referente ao COFINS, conforme a Tabela indicada no item 4.3.4",
            "valor": cst_cofins
        },
        "ALIQ_COFINS": {
            "titulo": "Alíquota do COFINS (em percentual)",
            "valor": aliq_cofins,
            "valor_formatado": fmt_percentual(val11)
        },
        "VL_CRED_COFINS_ACUM": {
            "titulo": "Valor Total do Crédito Acumulado sobre o custo incorrido - COFINS (Campo 06 x 14)",
            "valor": vl_cred_cofins_acum,
            "valor_formatado": fmt_valor(val12)
        },
        "VL_CRED_COFINS_DESC_ANT": {
            "titulo": "Parcela do crédito descontada até o período anterior da escrituração – COFINS (proporcional à receita acumulada recebida até o mês anterior)",
            "valor": vl_cred_cofins_desc_ant,
            "valor_formatado": fmt_valor(val13)
        },
        "VL_CRED_COFINS_DESC": {
            "titulo": "Parcela a descontar no período da escrituração – COFINS (proporcional à receita recebida no mês)",
            "valor": vl_cred_cofins_desc,
            "valor_formatado": fmt_valor(val14)
        },
        "VL_CRED_COFINS_DESC_FUT": {
            "titulo": "Parcela a descontar em períodos futuros – COFINS (Campo 15 – 16 – 17)",
            "valor": vl_cred_cofins_desc_fut,
            "valor_formatado": fmt_valor(val15)
        }
    }
    
    return resultado


def validar_f205(linhas):
    """
    Valida uma ou mais linhas do registro F205 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |F205|VL_CUS_INC_ACUM_ANT|VL_CUS_INC_PER_ESC|VL_CUS_INC_ACUM|VL_EXC_BC_CUS_INC_ACUM|VL_BC_CUS_INC|CST_PIS|ALIQ_PIS|VL_CRED_PIS_ACUM|VL_CRED_PIS_DESC_ANT|VL_CRED_PIS_DESC|VL_CRED_PIS_DESC_FUT|CST_COFINS|ALIQ_COFINS|VL_CRED_COFINS_ACUM|VL_CRED_COFINS_DESC_ANT|VL_CRED_COFINS_DESC|VL_CRED_COFINS_DESC_FUT|
        
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
        resultado = _processar_linha_f205(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
