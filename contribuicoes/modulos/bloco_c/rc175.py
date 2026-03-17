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


def _processar_linha_c175(linha):
    """
    Processa uma única linha do registro C175 e retorna um dicionário.
    
    Formato:
      |C175|CFOP|VL_OPR|VL_DESC|CST_PIS|VL_BC_PIS|ALIQ_PIS|QUANT_BC_PIS|ALIQ_PIS_QUANT|VL_PIS|CST_COFINS|VL_BC_COFINS|ALIQ_COFINS|QUANT_BC_COFINS|ALIQ_COFINS_QUANT|VL_COFINS|COD_CTA|INFO_COMPL|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "C175"
    - CFOP: obrigatório, código fiscal de operação e prestação (4 dígitos)
      - Validação: deve existir na Tabela de CFOP (validação em camada superior)
      - Na escrituração analítica das NFC-e, só poderão ser informados CFOP iniciados com 5 (validação em camada superior)
    - VL_OPR: obrigatório, valor da operação (numérico, 2 decimais, positivo)
    - VL_DESC: opcional, valor do desconto comercial (numérico, 2 decimais, não negativo)
    - CST_PIS: opcional, código da situação tributária referente ao PIS/PASEP (2 dígitos)
      - Valores válidos: [01, 02, 03, 04, 05, 06, 07, 08, 09, 49, 99]
    - VL_BC_PIS: opcional, valor da base de cálculo do PIS/PASEP em valor (numérico, 2 decimais)
    - ALIQ_PIS: opcional, alíquota do PIS/PASEP em percentual (numérico, 4 decimais)
    - QUANT_BC_PIS: opcional, base de cálculo PIS/PASEP em quantidade (numérico, 3 decimais)
    - ALIQ_PIS_QUANT: opcional, alíquota do PIS em reais (numérico, 4 decimais)
    - VL_PIS: opcional, valor do PIS/PASEP (numérico, 2 decimais)
      - Validação: deve corresponder ao valor da base de cálculo (campo 06 ou 08) multiplicado pela alíquota (campo 07 ou 09)
      - No caso de aplicação da alíquota do campo 07, o resultado deverá ser dividido por 100
    - CST_COFINS: obrigatório, código da situação tributária referente ao COFINS (2 dígitos)
      - Valores válidos: [01, 02, 03, 04, 05, 06, 07, 08, 09, 49, 99]
    - VL_BC_COFINS: opcional, valor da base de cálculo da COFINS (numérico, 2 decimais)
    - ALIQ_COFINS: opcional, alíquota da COFINS em percentual (numérico, 4 decimais)
    - QUANT_BC_COFINS: opcional, base de cálculo COFINS em quantidade (numérico, 3 decimais)
    - ALIQ_COFINS_QUANT: opcional, alíquota da COFINS em reais (numérico, 4 decimais)
    - VL_COFINS: opcional, valor da COFINS (numérico, 2 decimais)
      - Validação: deve corresponder ao valor da base de cálculo (campo 12 ou 14) multiplicado pela alíquota (campo 13 ou 15)
      - No caso de aplicação da alíquota do campo 13, o resultado deverá ser dividido por 100
    - COD_CTA: opcional, código da conta analítica contábil (255 caracteres)
      - Obrigatório para fatos geradores a partir de novembro de 2017, exceto se dispensado de escrituração contábil
    - INFO_COMPL: opcional, informação complementar (texto livre)
    
    Nota: Registro analítico do documento (Código 65 - NFC-e). Este registro tem por objetivo representar
    a escrituração da NFC-e, código 65, os documentos fiscais totalizados por CST PIS, CST Cofins, CFOP,
    alíquota de PIS e alíquota da Cofins.
    
    Não podem ser informados dois ou mais registros com a mesma combinação de valores dos campos: CFOP,
    CST (PIS/Pasep e Cofins) e alíquotas (PIS/Pasep e Cofins) (validação em camada superior).
    
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
    # Remove primeiro e último se vazios (formato padrão SPED: |C175|...|)
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
    if reg != "C175":
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
    cfop = obter_campo(1)
    vl_opr = obter_campo(2)
    vl_desc = obter_campo(3)
    cst_pis = obter_campo(4)
    vl_bc_pis = obter_campo(5)
    aliq_pis = obter_campo(6)
    quant_bc_pis = obter_campo(7)
    aliq_pis_quant = obter_campo(8)
    vl_pis = obter_campo(9)
    cst_cofins = obter_campo(10)
    vl_bc_cofins = obter_campo(11)
    aliq_cofins = obter_campo(12)
    quant_bc_cofins = obter_campo(13)
    aliq_cofins_quant = obter_campo(14)
    vl_cofins = obter_campo(15)
    cod_cta = obter_campo(16)
    info_compl = obter_campo(17)
    
    # Validações básicas dos campos obrigatórios
    
    # CFOP: obrigatório, código fiscal de operação (4 dígitos)
    if not cfop or not cfop.isdigit() or len(cfop) != 4:
        return None
    
    # VL_OPR: obrigatório, valor da operação (numérico, 2 decimais, positivo)
    ok_vl_opr, val_vl_opr, _ = validar_valor_numerico(vl_opr, decimais=2, obrigatorio=True, positivo=True)
    if not ok_vl_opr:
        return None
    
    # VL_DESC: opcional, valor do desconto (numérico, 2 decimais, não negativo)
    ok_vl_desc, val_vl_desc, _ = validar_valor_numerico(vl_desc, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok_vl_desc:
        return None
    
    # CST_PIS: opcional, código da situação tributária PIS (valores válidos)
    if cst_pis:
        cst_pis_validos = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "49", "99"]
        if cst_pis not in cst_pis_validos:
            return None
    
    # VL_BC_PIS: opcional, base de cálculo do PIS em valor (numérico, 2 decimais)
    ok_vl_bc_pis, val_vl_bc_pis, _ = validar_valor_numerico(vl_bc_pis, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok_vl_bc_pis:
        return None
    
    # ALIQ_PIS: opcional, alíquota do PIS em percentual (numérico, 4 decimais)
    ok_aliq_pis, val_aliq_pis, _ = validar_valor_numerico(aliq_pis, decimais=4, obrigatorio=False, nao_negativo=True)
    if not ok_aliq_pis:
        return None
    
    # QUANT_BC_PIS: opcional, base de cálculo PIS em quantidade (numérico, 3 decimais)
    ok_quant_bc_pis, val_quant_bc_pis, _ = validar_valor_numerico(quant_bc_pis, decimais=3, obrigatorio=False, positivo=True)
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
    if vl_pis:
        # Se tem quantidade base, calcula com quantidade e alíquota em reais
        if quant_bc_pis and aliq_pis_quant:
            vl_pis_calculado = val_quant_bc_pis * val_aliq_pis_quant
            # Tolerância de 0.01 para diferenças de arredondamento
            if abs(val_vl_pis - vl_pis_calculado) > 0.01:
                return None
        # Se tem base de cálculo em valor, calcula com base e alíquota percentual (dividido por 100)
        elif vl_bc_pis and aliq_pis:
            vl_pis_calculado = val_vl_bc_pis * (val_aliq_pis / 100.0)
            # Tolerância de 0.01 para diferenças de arredondamento
            if abs(val_vl_pis - vl_pis_calculado) > 0.01:
                return None
    
    # CST_COFINS: obrigatório, código da situação tributária COFINS (valores válidos)
    cst_cofins_validos = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "49", "99"]
    if not cst_cofins or cst_cofins not in cst_cofins_validos:
        return None
    
    # VL_BC_COFINS: opcional, base de cálculo da COFINS (numérico, 2 decimais)
    ok_vl_bc_cofins, val_vl_bc_cofins, _ = validar_valor_numerico(vl_bc_cofins, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok_vl_bc_cofins:
        return None
    
    # ALIQ_COFINS: opcional, alíquota da COFINS em percentual (numérico, 4 decimais)
    ok_aliq_cofins, val_aliq_cofins, _ = validar_valor_numerico(aliq_cofins, decimais=4, obrigatorio=False, nao_negativo=True)
    if not ok_aliq_cofins:
        return None
    
    # QUANT_BC_COFINS: opcional, base de cálculo COFINS em quantidade (numérico, 3 decimais)
    ok_quant_bc_cofins, val_quant_bc_cofins, _ = validar_valor_numerico(quant_bc_cofins, decimais=3, obrigatorio=False, positivo=True)
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
    if vl_cofins:
        # Se tem quantidade base, calcula com quantidade e alíquota em reais
        if quant_bc_cofins and aliq_cofins_quant:
            vl_cofins_calculado = val_quant_bc_cofins * val_aliq_cofins_quant
            # Tolerância de 0.01 para diferenças de arredondamento
            if abs(val_vl_cofins - vl_cofins_calculado) > 0.01:
                return None
        # Se tem base de cálculo em valor, calcula com base e alíquota percentual (dividido por 100)
        elif vl_bc_cofins and aliq_cofins:
            vl_cofins_calculado = val_vl_bc_cofins * (val_aliq_cofins / 100.0)
            # Tolerância de 0.01 para diferenças de arredondamento
            if abs(val_vl_cofins - vl_cofins_calculado) > 0.01:
                return None
    
    # COD_CTA: opcional, código da conta analítica contábil (255 caracteres)
    if cod_cta and len(cod_cta) > 255:
        return None
    
    # INFO_COMPL: opcional, informação complementar (texto livre)
    # Não há validação específica além de ser texto livre
    
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
        "CFOP": {
            "titulo": "Código fiscal de operação e prestação",
            "valor": cfop
        },
        "VL_OPR": {
            "titulo": "Valor da operação na combinação de CFOP, CST e alíquotas, correspondente ao somatório do valor das mercadorias e produtos constantes no documento",
            "valor": vl_opr,
            "valor_formatado": fmt_valor(val_vl_opr)
        },
        "VL_DESC": {
            "titulo": "Valor do desconto comercial / exclusão da base de cálculo do PIS/PASEP e da COFINS",
            "valor": vl_desc,
            "valor_formatado": fmt_valor(val_vl_desc)
        },
        "CST_PIS": {
            "titulo": "Código da Situação Tributária referente ao PIS/PASEP, conforme a Tabela indicada no item 4.3.3",
            "valor": cst_pis,
            "descricao": descricoes_cst.get(cst_pis, "") if cst_pis else ""
        },
        "VL_BC_PIS": {
            "titulo": "Valor da base de cálculo do PIS/PASEP (em valor)",
            "valor": vl_bc_pis,
            "valor_formatado": fmt_valor(val_vl_bc_pis)
        },
        "ALIQ_PIS": {
            "titulo": "Alíquota do PIS/PASEP (em percentual)",
            "valor": aliq_pis,
            "valor_formatado": fmt_valor_decimais(val_aliq_pis, 4) if aliq_pis else ""
        },
        "QUANT_BC_PIS": {
            "titulo": "Base de cálculo PIS/PASEP (em quantidade)",
            "valor": quant_bc_pis,
            "valor_formatado": fmt_valor_decimais(val_quant_bc_pis, 3) if quant_bc_pis else ""
        },
        "ALIQ_PIS_QUANT": {
            "titulo": "Alíquota do PIS (em reais)",
            "valor": aliq_pis_quant,
            "valor_formatado": fmt_valor_decimais(val_aliq_pis_quant, 4) if aliq_pis_quant else ""
        },
        "VL_PIS": {
            "titulo": "Valor do PIS/PASEP",
            "valor": vl_pis,
            "valor_formatado": fmt_valor(val_vl_pis)
        },
        "CST_COFINS": {
            "titulo": "Código da Situação Tributária referente a Cofins, conforme a Tabela indicada no item 4.3.4",
            "valor": cst_cofins,
            "descricao": descricoes_cst.get(cst_cofins, "")
        },
        "VL_BC_COFINS": {
            "titulo": "Valor da base de cálculo da Cofins",
            "valor": vl_bc_cofins,
            "valor_formatado": fmt_valor(val_vl_bc_cofins)
        },
        "ALIQ_COFINS": {
            "titulo": "Alíquota da Cofins (em percentual)",
            "valor": aliq_cofins,
            "valor_formatado": fmt_valor_decimais(val_aliq_cofins, 4) if aliq_cofins else ""
        },
        "QUANT_BC_COFINS": {
            "titulo": "Base de cálculo COFINS (em quantidade)",
            "valor": quant_bc_cofins,
            "valor_formatado": fmt_valor_decimais(val_quant_bc_cofins, 3) if quant_bc_cofins else ""
        },
        "ALIQ_COFINS_QUANT": {
            "titulo": "Alíquota da COFINS (em reais)",
            "valor": aliq_cofins_quant,
            "valor_formatado": fmt_valor_decimais(val_aliq_cofins_quant, 4) if aliq_cofins_quant else ""
        },
        "VL_COFINS": {
            "titulo": "Valor da Cofins",
            "valor": vl_cofins,
            "valor_formatado": fmt_valor(val_vl_cofins)
        },
        "COD_CTA": {
            "titulo": "Código da conta analítica contábil debitada/creditada",
            "valor": cod_cta
        },
        "INFO_COMPL": {
            "titulo": "Informação complementar",
            "valor": info_compl
        }
    }
    
    return resultado


def validar_c175(linhas):
    """
    Valida uma ou mais linhas do registro C175 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |C175|CFOP|VL_OPR|VL_DESC|CST_PIS|VL_BC_PIS|ALIQ_PIS|QUANT_BC_PIS|ALIQ_PIS_QUANT|VL_PIS|CST_COFINS|VL_BC_COFINS|ALIQ_COFINS|QUANT_BC_COFINS|ALIQ_COFINS_QUANT|VL_COFINS|COD_CTA|INFO_COMPL|
        
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
        resultado = _processar_linha_c175(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
