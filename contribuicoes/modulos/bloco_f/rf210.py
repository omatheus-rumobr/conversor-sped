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


def _processar_linha_f210(linha):
    """
    Processa uma única linha do registro F210 e retorna um dicionário.
    
    Formato:
      |F210|VL_CUS_ORC|VL_EXC|VL_CUS_ORC_AJU|VL_BC_CRED|CST_PIS|ALIQ_PIS|VL_CRED_PIS_UTIL|CST_COFINS|ALIQ_COFINS|VL_CRED_COFINS_UTIL|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "F210"
    - VL_CUS_ORC: obrigatório, numérico com 2 decimais
    - VL_EXC: obrigatório, numérico com 2 decimais
    - VL_CUS_ORC_AJU: obrigatório, numérico com 2 decimais
      - Deve ser = VL_CUS_ORC - VL_EXC (validação)
    - VL_BC_CRED: obrigatório, numérico com 2 decimais
    - CST_PIS: obrigatório, 2 dígitos
    - ALIQ_PIS: opcional, numérico com 8 dígitos e 4 decimais (percentual)
      - Valor esperado: 1,65% (mas é opcional)
    - VL_CRED_PIS_UTIL: opcional, numérico com 2 decimais
      - Deve ser = VL_BC_CRED * ALIQ_PIS / 100 (validação, se ambos preenchidos)
    - CST_COFINS: obrigatório, 2 dígitos
    - ALIQ_COFINS: opcional, numérico com 8 dígitos e 4 decimais (percentual)
      - Valor esperado: 7,6% (mas é opcional)
    - VL_CRED_COFINS_UTIL: opcional, numérico com 2 decimais
      - Deve ser = VL_BC_CRED * ALIQ_COFINS / 100 (validação, se ambos preenchidos)
    
    Nota: Neste registro a pessoa jurídica procederá à escrituração dos créditos referentes ao custo orçado
    para a conclusão da obra ou melhoramento, vinculado à unidade imobiliária vendida em construção.
    Os créditos referentes ao custo orçado da unidade imobiliária vendida, conforme definido pela legislação
    tributária, deve ser objeto de utilização (desconto da contribuição apurada) pela pessoa jurídica somente
    a partir da efetivação da venda e na proporção da receita relativa à venda da unidade imobiliária, à medida
    do recebimento. O Registro F210 é de preenchimento opcional. Será preenchido apenas quando o campo IND_OPER,
    do Registro F200, for igual a 03 ou 04, representativo de crédito vinculado a venda de unidade imobiliária
    não concluída.
    
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
    # Remove primeiro e último se vazios (formato padrão SPED: |F210|...|)
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
    if reg != "F210":
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
    
    # Extrai todos os campos (11 campos no total)
    vl_cus_orc = obter_campo(1)
    vl_exc = obter_campo(2)
    vl_cus_orc_aju = obter_campo(3)
    vl_bc_cred = obter_campo(4)
    cst_pis = obter_campo(5)
    aliq_pis = obter_campo(6)
    vl_cred_pis_util = obter_campo(7)
    cst_cofins = obter_campo(8)
    aliq_cofins = obter_campo(9)
    vl_cred_cofins_util = obter_campo(10)
    
    # Validações básicas dos campos obrigatórios
    
    # VL_CUS_ORC: obrigatório, numérico com 2 decimais
    ok1, val1, _ = validar_valor_numerico(vl_cus_orc, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok1:
        return None
    
    # VL_EXC: obrigatório, numérico com 2 decimais
    ok2, val2, _ = validar_valor_numerico(vl_exc, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok2:
        return None
    
    # VL_CUS_ORC_AJU: obrigatório, numérico com 2 decimais
    ok3, val3, _ = validar_valor_numerico(vl_cus_orc_aju, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok3:
        return None
    
    # Validação: VL_CUS_ORC_AJU deve ser = VL_CUS_ORC - VL_EXC
    vl_cus_orc_aju_calculado = round(val1 - val2, 2)
    # Permite pequena diferença devido a arredondamentos (tolerância de 0.01)
    if abs(val3 - vl_cus_orc_aju_calculado) > 0.01:
        return None
    
    # VL_BC_CRED: obrigatório, numérico com 2 decimais
    ok4, val4, _ = validar_valor_numerico(vl_bc_cred, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok4:
        return None
    
    # CST_PIS: obrigatório, 2 dígitos
    if not cst_pis or len(cst_pis) != 2 or not cst_pis.isdigit():
        return None
    
    # ALIQ_PIS: opcional, numérico com 8 dígitos e 4 decimais (percentual)
    # Normaliza vírgula para ponto
    aliq_pis_normalizada = aliq_pis.replace(",", ".") if aliq_pis else ""
    ok5, val5, _ = validar_valor_numerico(aliq_pis_normalizada, decimais=4, obrigatorio=False, nao_negativo=True)
    if not ok5:
        return None
    # Valida se tem no máximo 8 dígitos na parte inteira
    if aliq_pis_normalizada:
        partes_aliq = aliq_pis_normalizada.split(".")
        if len(partes_aliq[0]) > 8:
            return None
    
    # VL_CRED_PIS_UTIL: opcional, numérico com 2 decimais
    ok6, val6, _ = validar_valor_numerico(vl_cred_pis_util, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok6:
        return None
    
    # Validação: VL_CRED_PIS_UTIL deve ser = VL_BC_CRED * ALIQ_PIS / 100 (se ambos preenchidos)
    if aliq_pis_normalizada and vl_cred_pis_util:
        vl_cred_pis_util_calculado = round((val4 * val5) / 100, 2)
        # Permite pequena diferença devido a arredondamentos (tolerância de 0.01)
        if abs(val6 - vl_cred_pis_util_calculado) > 0.01:
            return None
    
    # CST_COFINS: obrigatório, 2 dígitos
    if not cst_cofins or len(cst_cofins) != 2 or not cst_cofins.isdigit():
        return None
    
    # ALIQ_COFINS: opcional, numérico com 8 dígitos e 4 decimais (percentual)
    # Normaliza vírgula para ponto
    aliq_cofins_normalizada = aliq_cofins.replace(",", ".") if aliq_cofins else ""
    ok7, val7, _ = validar_valor_numerico(aliq_cofins_normalizada, decimais=4, obrigatorio=False, nao_negativo=True)
    if not ok7:
        return None
    # Valida se tem no máximo 8 dígitos na parte inteira
    if aliq_cofins_normalizada:
        partes_aliq = aliq_cofins_normalizada.split(".")
        if len(partes_aliq[0]) > 8:
            return None
    
    # VL_CRED_COFINS_UTIL: opcional, numérico com 2 decimais
    ok8, val8, _ = validar_valor_numerico(vl_cred_cofins_util, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok8:
        return None
    
    # Validação: VL_CRED_COFINS_UTIL deve ser = VL_BC_CRED * ALIQ_COFINS / 100 (se ambos preenchidos)
    if aliq_cofins_normalizada and vl_cred_cofins_util:
        vl_cred_cofins_util_calculado = round((val4 * val7) / 100, 2)
        # Permite pequena diferença devido a arredondamentos (tolerância de 0.01)
        if abs(val8 - vl_cred_cofins_util_calculado) > 0.01:
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
        "VL_CUS_ORC": {
            "titulo": "Valor Total do Custo Orçado para Conclusão da Unidade Vendida",
            "valor": vl_cus_orc,
            "valor_formatado": fmt_valor(val1)
        },
        "VL_EXC": {
            "titulo": "Valores Referentes a Pagamentos a Pessoas Físicas, Encargos Trabalhistas, Sociais e Previdenciários e à aquisição de bens e serviços não sujeitos ao pagamento das contribuições",
            "valor": vl_exc,
            "valor_formatado": fmt_valor(val2)
        },
        "VL_CUS_ORC_AJU": {
            "titulo": "Valor da Base de Calculo do Crédito sobre o Custo Orçado Ajustado (Campo 02 – 03)",
            "valor": vl_cus_orc_aju,
            "valor_formatado": fmt_valor(val3)
        },
        "VL_BC_CRED": {
            "titulo": "Valor da Base de Cálculo do Crédito sobre o Custo Orçado referente ao mês da escrituração, proporcionalizada em função da receita recebida no mês",
            "valor": vl_bc_cred,
            "valor_formatado": fmt_valor(val4)
        },
        "CST_PIS": {
            "titulo": "Código da Situação Tributária referente ao PIS/PASEP, conforme a Tabela indicada no item 4.3.3",
            "valor": cst_pis
        },
        "ALIQ_PIS": {
            "titulo": "Alíquota do PIS/PASEP (em percentual)",
            "valor": aliq_pis,
            "valor_formatado": fmt_percentual(val5) if aliq_pis else ""
        },
        "VL_CRED_PIS_UTIL": {
            "titulo": "Valor do Crédito sobre o custo orçado a ser utilizado no período da escrituração - PIS/PASEP (Campo 05 x 07)",
            "valor": vl_cred_pis_util,
            "valor_formatado": fmt_valor(val6) if vl_cred_pis_util else ""
        },
        "CST_COFINS": {
            "titulo": "Código da Situação Tributária referente a COFINS, conforme a Tabela indicada no item 4.3.4",
            "valor": cst_cofins
        },
        "ALIQ_COFINS": {
            "titulo": "Alíquota da COFINS (em percentual)",
            "valor": aliq_cofins,
            "valor_formatado": fmt_percentual(val7) if aliq_cofins else ""
        },
        "VL_CRED_COFINS_UTIL": {
            "titulo": "Valor do Crédito sobre o custo orçado a ser utilizado no período da escrituração - COFINS (Campo 05 x 10)",
            "valor": vl_cred_cofins_util,
            "valor_formatado": fmt_valor(val8) if vl_cred_cofins_util else ""
        }
    }
    
    return resultado


def validar_f210(linhas):
    """
    Valida uma ou mais linhas do registro F210 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |F210|VL_CUS_ORC|VL_EXC|VL_CUS_ORC_AJU|VL_BC_CRED|CST_PIS|ALIQ_PIS|VL_CRED_PIS_UTIL|CST_COFINS|ALIQ_COFINS|VL_CRED_COFINS_UTIL|
        
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
        resultado = _processar_linha_f210(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
