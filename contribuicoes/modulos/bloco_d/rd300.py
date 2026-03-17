import json
from datetime import datetime


def _validar_data(data_str):
    """
    Valida se a data está no formato ddmmaaaa e se é uma data válida.
    
    Args:
        data_str: String com data no formato ddmmaaaa
        
    Returns:
        tuple: (True/False, datetime object ou None)
    """
    if not data_str or len(data_str) != 8 or not data_str.isdigit():
        return False, None
    
    try:
        dia = int(data_str[:2])
        mes = int(data_str[2:4])
        ano = int(data_str[4:8])
        data_obj = datetime(ano, mes, dia)
        return True, data_obj
    except ValueError:
        return False, None


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


def _processar_linha_d300(linha):
    """
    Processa uma única linha do registro D300 e retorna um dicionário.
    
    Formato:
      |D300|COD_MOD|SER|SUB|NUM_DOC_INI|NUM_DOC_FIN|CFOP|DT_REF|VL_DOC|VL_DESC|CST_PIS|VL_BC_PIS|ALIQ_PIS|VL_PIS|CST_COFINS|VL_BC_COFINS|ALIQ_COFINS|VL_COFINS|COD_CTA|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "D300"
    - COD_MOD: obrigatório, valores válidos [13, 14, 15, 16, 18]
    - SER: opcional, máximo 4 caracteres
    - SUB: opcional, máximo 3 caracteres (numérico)
    - NUM_DOC_INI: opcional, máximo 6 dígitos, se informado deve ser > 0, e deve ser <= NUM_DOC_FIN
    - NUM_DOC_FIN: opcional, máximo 6 dígitos, se informado deve ser > 0, e deve ser >= NUM_DOC_INI
    - CFOP: obrigatório, 4 dígitos
    - DT_REF: obrigatório, formato ddmmaaaa, data válida
    - VL_DOC: obrigatório, numérico com 2 decimais
    - VL_DESC: opcional, numérico com 2 decimais
    - CST_PIS: obrigatório, 2 dígitos (valores válidos: [01, 02, 06, 07, 08, 09, 49, 99])
    - VL_BC_PIS: opcional, numérico com 2 decimais
    - ALIQ_PIS: opcional, numérico com 8 dígitos e 4 decimais (percentual)
    - VL_PIS: opcional, numérico com 2 decimais
      - Deve corresponder a VL_BC_PIS * ALIQ_PIS / 100 (validação)
    - CST_COFINS: obrigatório, 2 dígitos (valores válidos: [01, 02, 06, 07, 08, 09, 49, 99])
    - VL_BC_COFINS: opcional, numérico com 2 decimais
    - ALIQ_COFINS: opcional, numérico com 8 dígitos e 4 decimais (percentual)
    - VL_COFINS: opcional, numérico com 2 decimais
      - Deve corresponder a VL_BC_COFINS * ALIQ_COFINS / 100 (validação)
    - COD_CTA: opcional, máximo 255 caracteres
    
    Nota: Escriturar neste registro a consolidação diária dos documentos fiscais válidos, códigos 13, 14, 15, 16 e 18,
    referentes aos serviços de transportes no período da escrituração.
    
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
    # Remove primeiro e último se vazios (formato padrão SPED: |D300|...|)
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
    if reg != "D300":
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
    
    # Extrai todos os campos (19 campos no total)
    cod_mod = obter_campo(1)
    ser = obter_campo(2)
    sub = obter_campo(3)
    num_doc_ini = obter_campo(4)
    num_doc_fin = obter_campo(5)
    cfop = obter_campo(6)
    dt_ref = obter_campo(7)
    vl_doc = obter_campo(8)
    vl_desc = obter_campo(9)
    cst_pis = obter_campo(10)
    vl_bc_pis = obter_campo(11)
    aliq_pis = obter_campo(12)
    vl_pis = obter_campo(13)
    cst_cofins = obter_campo(14)
    vl_bc_cofins = obter_campo(15)
    aliq_cofins = obter_campo(16)
    vl_cofins = obter_campo(17)
    cod_cta = obter_campo(18)
    
    # Validações básicas dos campos obrigatórios
    
    # COD_MOD: obrigatório, valores válidos [13, 14, 15, 16, 18]
    cod_mod_validos = ["13", "14", "15", "16", "18"]
    if not cod_mod or cod_mod not in cod_mod_validos:
        return None
    
    # SER: opcional, máximo 4 caracteres
    if ser and len(ser) > 4:
        return None
    
    # SUB: opcional, máximo 3 caracteres (numérico)
    if sub:
        if len(sub) > 3 or not sub.isdigit():
            return None
    
    # NUM_DOC_INI: opcional, máximo 6 dígitos, se informado deve ser > 0
    num_doc_ini_int = None
    if num_doc_ini:
        if not num_doc_ini.isdigit() or len(num_doc_ini) > 6:
            return None
        num_doc_ini_int = int(num_doc_ini)
        if num_doc_ini_int <= 0:
            return None
    
    # NUM_DOC_FIN: opcional, máximo 6 dígitos, se informado deve ser > 0
    num_doc_fin_int = None
    if num_doc_fin:
        if not num_doc_fin.isdigit() or len(num_doc_fin) > 6:
            return None
        num_doc_fin_int = int(num_doc_fin)
        if num_doc_fin_int <= 0:
            return None
    
    # Validação: NUM_DOC_INI deve ser <= NUM_DOC_FIN (se ambos informados)
    if num_doc_ini_int is not None and num_doc_fin_int is not None:
        if num_doc_ini_int > num_doc_fin_int:
            return None
    
    # CFOP: obrigatório, 4 dígitos
    if not cfop or not cfop.isdigit() or len(cfop) != 4:
        return None
    
    # DT_REF: obrigatório, formato ddmmaaaa, data válida
    dt_ref_valido, dt_ref_obj = _validar_data(dt_ref)
    if not dt_ref_valido:
        return None
    
    # VL_DOC: obrigatório, numérico com 2 decimais
    ok1, val1, _ = validar_valor_numerico(vl_doc, decimais=2, obrigatorio=True)
    if not ok1:
        return None
    
    # VL_DESC: opcional, numérico com 2 decimais
    ok2, val2, _ = validar_valor_numerico(vl_desc, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok2:
        return None
    
    # CST_PIS: obrigatório, 2 dígitos, valores válidos [01, 02, 06, 07, 08, 09, 49, 99]
    cst_pis_validos = ["01", "02", "06", "07", "08", "09", "49", "99"]
    if not cst_pis or len(cst_pis) != 2 or cst_pis not in cst_pis_validos:
        return None
    
    # VL_BC_PIS: opcional, numérico com 2 decimais
    ok3, val3, _ = validar_valor_numerico(vl_bc_pis, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok3:
        return None
    
    # ALIQ_PIS: opcional, numérico com 8 dígitos e 4 decimais (percentual)
    ok4, val4, _ = validar_valor_numerico(aliq_pis, decimais=4, obrigatorio=False, nao_negativo=True)
    if not ok4:
        return None
    if aliq_pis:
        partes_aliq = aliq_pis.split(".")
        parte_inteira = partes_aliq[0]
        if len(parte_inteira) > 8:
            return None
    
    # VL_PIS: opcional, numérico com 2 decimais
    ok5, val5, _ = validar_valor_numerico(vl_pis, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok5:
        return None
    
    # Validação: VL_PIS deve corresponder a VL_BC_PIS * ALIQ_PIS / 100
    if vl_bc_pis and aliq_pis and vl_pis:
        vl_pis_calculado = round((val3 * val4) / 100, 2)
        if abs(val5 - vl_pis_calculado) > 0.01:
            return None
    
    # CST_COFINS: obrigatório, 2 dígitos, valores válidos [01, 02, 06, 07, 08, 09, 49, 99]
    cst_cofins_validos = ["01", "02", "06", "07", "08", "09", "49", "99"]
    if not cst_cofins or len(cst_cofins) != 2 or cst_cofins not in cst_cofins_validos:
        return None
    
    # VL_BC_COFINS: opcional, numérico com 2 decimais
    ok6, val6, _ = validar_valor_numerico(vl_bc_cofins, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok6:
        return None
    
    # ALIQ_COFINS: opcional, numérico com 8 dígitos e 4 decimais (percentual)
    ok7, val7, _ = validar_valor_numerico(aliq_cofins, decimais=4, obrigatorio=False, nao_negativo=True)
    if not ok7:
        return None
    if aliq_cofins:
        partes_aliq_cofins = aliq_cofins.split(".")
        parte_inteira_cofins = partes_aliq_cofins[0]
        if len(parte_inteira_cofins) > 8:
            return None
    
    # VL_COFINS: opcional, numérico com 2 decimais
    ok8, val8, _ = validar_valor_numerico(vl_cofins, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok8:
        return None
    
    # Validação: VL_COFINS deve corresponder a VL_BC_COFINS * ALIQ_COFINS / 100
    if vl_bc_cofins and aliq_cofins and vl_cofins:
        vl_cofins_calculado = round((val6 * val7) / 100, 2)
        if abs(val8 - vl_cofins_calculado) > 0.01:
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
    
    # Função auxiliar para formatar data
    def fmt_data(dt):
        if dt:
            return dt.strftime("%d/%m/%Y")
        return ""
    
    # Descrições dos campos
    descricoes_cod_mod = {
        "13": "Bilhete Consolidado de Passagem Rodoviário",
        "14": "Bilhete Consolidado de Passagem Aquaviário",
        "15": "Bilhete Consolidado de Passagem e Nota de Bagagem",
        "16": "Bilhete Consolidado de Passagem Ferroviário",
        "18": "Resumo de Movimento Diário"
    }
    
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
    
    descricoes_cst_cofins = {
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
        "COD_MOD": {
            "titulo": "Código do modelo do documento fiscal, conforme a Tabela 4.1.1",
            "valor": cod_mod,
            "descricao": descricoes_cod_mod.get(cod_mod, "")
        },
        "SER": {
            "titulo": "Série do documento fiscal",
            "valor": ser
        },
        "SUB": {
            "titulo": "Subsérie do documento fiscal",
            "valor": sub
        },
        "NUM_DOC_INI": {
            "titulo": "Número do primeiro documento fiscal emitido no período (mesmo modelo, série e subsérie)",
            "valor": num_doc_ini
        },
        "NUM_DOC_FIN": {
            "titulo": "Número do último documento fiscal emitido no período (mesmo modelo, série e subsérie)",
            "valor": num_doc_fin
        },
        "CFOP": {
            "titulo": "Código Fiscal de Operação e Prestação conforme tabela indicada no item 4.2.2",
            "valor": cfop
        },
        "DT_REF": {
            "titulo": "Data do dia de referência do resumo diário",
            "valor": dt_ref,
            "valor_formatado": fmt_data(dt_ref_obj)
        },
        "VL_DOC": {
            "titulo": "Valor total dos documentos fiscais emitidos",
            "valor": vl_doc,
            "valor_formatado": fmt_valor(val1)
        },
        "VL_DESC": {
            "titulo": "Valor total dos descontos",
            "valor": vl_desc,
            "valor_formatado": fmt_valor(val2) if vl_desc else ""
        },
        "CST_PIS": {
            "titulo": "Código da Situação Tributária referente ao PIS/PASEP",
            "valor": cst_pis,
            "descricao": descricoes_cst_pis.get(cst_pis, "")
        },
        "VL_BC_PIS": {
            "titulo": "Valor da base de cálculo do PIS/PASEP",
            "valor": vl_bc_pis,
            "valor_formatado": fmt_valor(val3) if vl_bc_pis else ""
        },
        "ALIQ_PIS": {
            "titulo": "Alíquota do PIS/PASEP (em percentual)",
            "valor": aliq_pis,
            "valor_formatado": fmt_percentual(val4) if aliq_pis else ""
        },
        "VL_PIS": {
            "titulo": "Valor do PIS/PASEP",
            "valor": vl_pis,
            "valor_formatado": fmt_valor(val5) if vl_pis else ""
        },
        "CST_COFINS": {
            "titulo": "Código da Situação Tributária referente a COFINS",
            "valor": cst_cofins,
            "descricao": descricoes_cst_cofins.get(cst_cofins, "")
        },
        "VL_BC_COFINS": {
            "titulo": "Valor da base de cálculo da COFINS",
            "valor": vl_bc_cofins,
            "valor_formatado": fmt_valor(val6) if vl_bc_cofins else ""
        },
        "ALIQ_COFINS": {
            "titulo": "Alíquota da COFINS (em percentual)",
            "valor": aliq_cofins,
            "valor_formatado": fmt_percentual(val7) if aliq_cofins else ""
        },
        "VL_COFINS": {
            "titulo": "Valor da COFINS",
            "valor": vl_cofins,
            "valor_formatado": fmt_valor(val8) if vl_cofins else ""
        },
        "COD_CTA": {
            "titulo": "Código da conta analítica contábil debitada/creditada",
            "valor": cod_cta
        }
    }
    
    return resultado


def validar_d300(linhas):
    """
    Valida uma ou mais linhas do registro D300 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |D300|COD_MOD|SER|SUB|NUM_DOC_INI|NUM_DOC_FIN|CFOP|DT_REF|VL_DOC|VL_DESC|CST_PIS|VL_BC_PIS|ALIQ_PIS|VL_PIS|CST_COFINS|VL_BC_COFINS|ALIQ_COFINS|VL_COFINS|COD_CTA|
        
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
        resultado = _processar_linha_d300(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
