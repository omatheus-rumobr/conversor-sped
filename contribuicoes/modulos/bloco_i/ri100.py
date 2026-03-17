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


def _processar_linha_i100(linha):
    """
    Processa uma única linha do registro I100 e retorna um dicionário.
    
    Formato:
      |I100|VL_REC|CST_PIS_COFINS|VL_TOT_DED_GER|VL_TOT_DED_ESP|VL_BC_PIS|ALIQ_PIS|VL_PIS|VL_BC_COFINS|ALIQ_COFINS|VL_COFINS|INFO_COMPL|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "I100"
    - VL_REC: obrigatório, valor total do faturamento/receita bruta no período (numérico, 2 decimais)
    - CST_PIS_COFINS: obrigatório, código de situação tributária (2 dígitos)
      - Valores válidos: [01, 02, 03, 04, 05, 06, 07, 08, 09, 49, 99]
    - VL_TOT_DED_GER: obrigatório, valor total das deduções e exclusões de caráter geral (numérico, 2 decimais)
    - VL_TOT_DED_ESP: obrigatório, valor total das deduções e exclusões de caráter específico (numérico, 2 decimais)
    - VL_BC_PIS: obrigatório, valor da base de cálculo do PIS/PASEP (numérico, 2 decimais)
    - ALIQ_PIS: obrigatório, alíquota do PIS/PASEP em percentual (8 dígitos, 2 decimais)
    - VL_PIS: obrigatório, valor do PIS/PASEP (numérico, 2 decimais)
      - Validação: VL_PIS = VL_BC_PIS * ALIQ_PIS / 100
    - VL_BC_COFINS: obrigatório, valor da base de cálculo da Cofins (numérico, 2 decimais)
    - ALIQ_COFINS: obrigatório, alíquota da COFINS em percentual (8 dígitos, 2 decimais)
    - VL_COFINS: obrigatório, valor da COFINS (numérico, 2 decimais)
      - Validação: VL_COFINS = VL_BC_COFINS * ALIQ_COFINS / 100
    - INFO_COMPL: opcional, informação complementar (texto livre)
    
    Nota: Registro específico para escrituração pelas pessoas jurídicas referidas nos §§ 6º, 8º e 9º
    do art. 3º da Lei nº 9.718, sujeitas ao regime cumulativo de apuração das contribuições, conforme
    definido nas Leis nº 10.637/2002 (PIS/Pasep) e nº 10.833/2003 (Cofins).
    
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
    # Remove primeiro e último se vazios (formato padrão SPED: |I100|...|)
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
    if reg != "I100":
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
    
    # Extrai todos os campos (12 campos no total)
    vl_rec = obter_campo(1)
    cst_pis_cofins = obter_campo(2)
    vl_tot_ded_ger = obter_campo(3)
    vl_tot_ded_esp = obter_campo(4)
    vl_bc_pis = obter_campo(5)
    aliq_pis = obter_campo(6)
    vl_pis = obter_campo(7)
    vl_bc_cofins = obter_campo(8)
    aliq_cofins = obter_campo(9)
    vl_cofins = obter_campo(10)
    info_compl = obter_campo(11)
    
    # Validações básicas dos campos obrigatórios
    
    # VL_REC: obrigatório, numérico com 2 decimais
    ok1, val1, _ = validar_valor_numerico(vl_rec, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok1:
        return None
    
    # CST_PIS_COFINS: obrigatório, valores válidos [01, 02, 03, 04, 05, 06, 07, 08, 09, 49, 99]
    cst_validos = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "49", "99"]
    if not cst_pis_cofins or len(cst_pis_cofins) != 2 or cst_pis_cofins not in cst_validos:
        return None
    
    # VL_TOT_DED_GER: obrigatório, numérico com 2 decimais
    ok2, val2, _ = validar_valor_numerico(vl_tot_ded_ger, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok2:
        return None
    
    # VL_TOT_DED_ESP: obrigatório, numérico com 2 decimais
    ok3, val3, _ = validar_valor_numerico(vl_tot_ded_esp, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok3:
        return None
    
    # VL_BC_PIS: obrigatório, numérico com 2 decimais
    ok4, val4, _ = validar_valor_numerico(vl_bc_pis, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok4:
        return None
    
    # ALIQ_PIS: obrigatório, numérico com 8 dígitos e 2 decimais (percentual)
    # Normaliza vírgula para ponto
    aliq_pis_normalizada = aliq_pis.replace(",", ".") if aliq_pis else ""
    ok5, val5, _ = validar_valor_numerico(aliq_pis_normalizada, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok5:
        return None
    # Valida se tem no máximo 8 dígitos na parte inteira
    if aliq_pis_normalizada:
        partes_aliq = aliq_pis_normalizada.split(".")
        if len(partes_aliq[0]) > 8:
            return None
    
    # VL_PIS: obrigatório, numérico com 2 decimais
    ok6, val6, _ = validar_valor_numerico(vl_pis, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok6:
        return None
    
    # Validação: VL_PIS deve corresponder a VL_BC_PIS * ALIQ_PIS / 100
    vl_pis_calculado = round((val4 * val5) / 100, 2)
    # Permite pequena diferença devido a arredondamentos (tolerância de 0.01)
    if abs(val6 - vl_pis_calculado) > 0.01:
        return None
    
    # VL_BC_COFINS: obrigatório, numérico com 2 decimais
    ok7, val7, _ = validar_valor_numerico(vl_bc_cofins, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok7:
        return None
    
    # ALIQ_COFINS: obrigatório, numérico com 8 dígitos e 2 decimais (percentual)
    # Normaliza vírgula para ponto
    aliq_cofins_normalizada = aliq_cofins.replace(",", ".") if aliq_cofins else ""
    ok8, val8, _ = validar_valor_numerico(aliq_cofins_normalizada, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok8:
        return None
    # Valida se tem no máximo 8 dígitos na parte inteira
    if aliq_cofins_normalizada:
        partes_aliq = aliq_cofins_normalizada.split(".")
        if len(partes_aliq[0]) > 8:
            return None
    
    # VL_COFINS: obrigatório, numérico com 2 decimais
    ok9, val9, _ = validar_valor_numerico(vl_cofins, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok9:
        return None
    
    # Validação: VL_COFINS deve corresponder a VL_BC_COFINS * ALIQ_COFINS / 100
    vl_cofins_calculado = round((val7 * val8) / 100, 2)
    # Permite pequena diferença devido a arredondamentos (tolerância de 0.01)
    if abs(val9 - vl_cofins_calculado) > 0.01:
        return None
    
    # INFO_COMPL: opcional, informação complementar (texto livre)
    # Não há validação específica além de ser texto livre
    
    # Função auxiliar para formatar valores monetários
    def fmt_valor(v):
        if v is None:
            return ""
        return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    # Função auxiliar para formatar percentual
    def fmt_percentual(v):
        if v is None:
            return ""
        return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") + "%"
    
    # Descrições dos campos
    descricoes_cst = {
        "01": "Operação Tributável com Alíquota Básica",
        "02": "Operação Tributável com Alíquota Diferenciada",
        "03": "Operação Tributável com Alíquota por Unidade de Medida de Produto",
        "04": "Operação Tributável Monofásica - Revenda a Alíquota Zero",
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
            "valor": reg
        },
        "VL_REC": {
            "titulo": "Valor Total do Faturamento/Receita Bruta no Período",
            "valor": vl_rec,
            "valor_formatado": fmt_valor(val1)
        },
        "CST_PIS_COFINS": {
            "titulo": "Código de Situação Tributária referente à Receita informada no Campo 02 (Tabelas 4.3.3 e 4.3.4)",
            "valor": cst_pis_cofins,
            "descricao": descricoes_cst.get(cst_pis_cofins, "")
        },
        "VL_TOT_DED_GER": {
            "titulo": "Valor Total das Deduções e Exclusões de Caráter Geral",
            "valor": vl_tot_ded_ger,
            "valor_formatado": fmt_valor(val2)
        },
        "VL_TOT_DED_ESP": {
            "titulo": "Valor Total das Deduções e Exclusões de Caráter Específico",
            "valor": vl_tot_ded_esp,
            "valor_formatado": fmt_valor(val3)
        },
        "VL_BC_PIS": {
            "titulo": "Valor da base de cálculo do PIS/PASEP",
            "valor": vl_bc_pis,
            "valor_formatado": fmt_valor(val4)
        },
        "ALIQ_PIS": {
            "titulo": "Alíquota do PIS/PASEP (em percentual)",
            "valor": aliq_pis,
            "valor_formatado": fmt_percentual(val5)
        },
        "VL_PIS": {
            "titulo": "Valor do PIS/PASEP",
            "valor": vl_pis,
            "valor_formatado": fmt_valor(val6)
        },
        "VL_BC_COFINS": {
            "titulo": "Valor da base de cálculo da Cofins",
            "valor": vl_bc_cofins,
            "valor_formatado": fmt_valor(val7)
        },
        "ALIQ_COFINS": {
            "titulo": "Alíquota da COFINS (em percentual)",
            "valor": aliq_cofins,
            "valor_formatado": fmt_percentual(val8)
        },
        "VL_COFINS": {
            "titulo": "Valor da COFINS",
            "valor": vl_cofins,
            "valor_formatado": fmt_valor(val9)
        },
        "INFO_COMPL": {
            "titulo": "Informação Complementar dos dados informados no registro",
            "valor": info_compl
        }
    }
    
    return resultado


def validar_i100(linhas):
    """
    Valida uma ou mais linhas do registro I100 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |I100|VL_REC|CST_PIS_COFINS|VL_TOT_DED_GER|VL_TOT_DED_ESP|VL_BC_PIS|ALIQ_PIS|VL_PIS|VL_BC_COFINS|ALIQ_COFINS|VL_COFINS|INFO_COMPL|
        
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
        resultado = _processar_linha_i100(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
