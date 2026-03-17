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


def _processar_linha_d350(linha, dt_fin_0000=None):
    """
    Processa uma única linha do registro D350 e retorna um dicionário.
    
    Formato:
      |D350|COD_MOD|ECF_MOD|ECF_FAB|DT_DOC|CRO|CRZ|NUM_COO_FIN|GT_FIN|VL_BRT|CST_PIS|VL_BC_PIS|ALIQ_PIS|QUANT_BC_PIS|ALIQ_PIS_QUANT|VL_PIS|CST_COFINS|VL_BC_COFINS|ALIQ_COFINS|QUANT_BC_COFINS|ALIQ_COFINS_QUANT|VL_COFINS|COD_CTA|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "D350"
    - COD_MOD: obrigatório, valores válidos [2E, 13, 14, 15, 16]
    - ECF_MOD: obrigatório, máximo 20 caracteres
    - ECF_FAB: obrigatório, máximo 21 caracteres
    - DT_DOC: obrigatório, formato ddmmaaaa, data válida, deve ser <= DT_FIN (validação em camada superior)
    - CRO: obrigatório, 3 dígitos, deve ser > 0
    - CRZ: obrigatório, 6 dígitos, deve ser > 0
    - NUM_COO_FIN: obrigatório, 6 dígitos, deve ser > 0
    - GT_FIN: obrigatório, numérico com 2 decimais
    - VL_BRT: obrigatório, numérico com 2 decimais, deve ser > 0
    - CST_PIS: obrigatório, 2 dígitos (valores válidos: [01, 02, 06, 07, 08, 09, 49, 99])
    - VL_BC_PIS: opcional, numérico com 2 decimais
    - ALIQ_PIS: opcional, numérico com 8 dígitos e 4 decimais (percentual)
    - QUANT_BC_PIS: opcional, numérico com 3 decimais
    - ALIQ_PIS_QUANT: opcional, numérico com 4 decimais (em reais)
    - VL_PIS: opcional, numérico com 2 decimais
    - CST_COFINS: obrigatório, 2 dígitos (valores válidos: [01, 02, 06, 07, 08, 09, 49, 99])
    - VL_BC_COFINS: opcional, numérico com 2 decimais
    - ALIQ_COFINS: opcional, numérico com 8 dígitos e 4 decimais (percentual)
    - QUANT_BC_COFINS: opcional, numérico com 3 decimais
    - ALIQ_COFINS_QUANT: opcional, numérico com 4 decimais (em reais)
    - VL_COFINS: opcional, numérico com 2 decimais
    - COD_CTA: opcional, máximo 255 caracteres
    
    Nota: Deve ser escriturada neste registro a consolidação diária das operações referentes serviços de transportes,
    objeto de registro nos documentos fiscais códigos 2E, 13, 14, 15 e 16, emitidos por equipamentos de ECF.
    
    Args:
        linha: String com uma linha do SPED
        dt_fin_0000: Data final da escrituração (ddmmaaaa) - opcional, para validação
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |D350|...|)
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
    if reg != "D350":
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
    
    # Extrai todos os campos (23 campos no total)
    cod_mod = obter_campo(1)
    ecf_mod = obter_campo(2)
    ecf_fab = obter_campo(3)
    dt_doc = obter_campo(4)
    cro = obter_campo(5)
    crz = obter_campo(6)
    num_coo_fin = obter_campo(7)
    gt_fin = obter_campo(8)
    vl_brt = obter_campo(9)
    cst_pis = obter_campo(10)
    vl_bc_pis = obter_campo(11)
    aliq_pis = obter_campo(12)
    quant_bc_pis = obter_campo(13)
    aliq_pis_quant = obter_campo(14)
    vl_pis = obter_campo(15)
    cst_cofins = obter_campo(16)
    vl_bc_cofins = obter_campo(17)
    aliq_cofins = obter_campo(18)
    quant_bc_cofins = obter_campo(19)
    aliq_cofins_quant = obter_campo(20)
    vl_cofins = obter_campo(21)
    cod_cta = obter_campo(22)
    
    # Validações básicas dos campos obrigatórios
    
    # COD_MOD: obrigatório, valores válidos [2E, 13, 14, 15, 16]
    cod_mod_validos = ["2E", "13", "14", "15", "16"]
    if not cod_mod or cod_mod not in cod_mod_validos:
        return None
    
    # ECF_MOD: obrigatório, máximo 20 caracteres
    if not ecf_mod or len(ecf_mod) > 20:
        return None
    
    # ECF_FAB: obrigatório, máximo 21 caracteres
    if not ecf_fab or len(ecf_fab) > 21:
        return None
    
    # DT_DOC: obrigatório, formato ddmmaaaa, data válida
    dt_doc_valido, dt_doc_obj = _validar_data(dt_doc)
    if not dt_doc_valido:
        return None
    
    # Validação: DT_DOC deve ser <= DT_FIN (quando informado)
    if dt_fin_0000:
        ok_fin, dt_fin_obj = _validar_data(dt_fin_0000)
        if ok_fin and dt_doc_obj and dt_doc_obj > dt_fin_obj:
            return None
    
    # CRO: obrigatório, 3 dígitos, deve ser > 0
    if not cro or not cro.isdigit() or len(cro) > 3:
        return None
    if int(cro) <= 0:
        return None
    
    # CRZ: obrigatório, 6 dígitos, deve ser > 0
    if not crz or not crz.isdigit() or len(crz) > 6:
        return None
    if int(crz) <= 0:
        return None
    
    # NUM_COO_FIN: obrigatório, 6 dígitos, deve ser > 0
    if not num_coo_fin or not num_coo_fin.isdigit() or len(num_coo_fin) > 6:
        return None
    if int(num_coo_fin) <= 0:
        return None
    
    # GT_FIN: obrigatório, numérico com 2 decimais
    ok1, val1, _ = validar_valor_numerico(gt_fin, decimais=2, obrigatorio=True)
    if not ok1:
        return None
    
    # VL_BRT: obrigatório, numérico com 2 decimais, deve ser > 0
    ok2, val2, _ = validar_valor_numerico(vl_brt, decimais=2, obrigatorio=True, positivo=True)
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
    
    # QUANT_BC_PIS: opcional, numérico com 3 decimais
    ok5, val5, _ = validar_valor_numerico(quant_bc_pis, decimais=3, obrigatorio=False, nao_negativo=True)
    if not ok5:
        return None
    
    # ALIQ_PIS_QUANT: opcional, numérico com 4 decimais (em reais)
    ok6, val6, _ = validar_valor_numerico(aliq_pis_quant, decimais=4, obrigatorio=False, nao_negativo=True)
    if not ok6:
        return None
    
    # VL_PIS: opcional, numérico com 2 decimais
    ok7, val7, _ = validar_valor_numerico(vl_pis, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok7:
        return None
    
    # CST_COFINS: obrigatório, 2 dígitos, valores válidos [01, 02, 06, 07, 08, 09, 49, 99]
    cst_cofins_validos = ["01", "02", "06", "07", "08", "09", "49", "99"]
    if not cst_cofins or len(cst_cofins) != 2 or cst_cofins not in cst_cofins_validos:
        return None
    
    # VL_BC_COFINS: opcional, numérico com 2 decimais
    ok8, val8, _ = validar_valor_numerico(vl_bc_cofins, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok8:
        return None
    
    # ALIQ_COFINS: opcional, numérico com 8 dígitos e 4 decimais (percentual)
    ok9, val9, _ = validar_valor_numerico(aliq_cofins, decimais=4, obrigatorio=False, nao_negativo=True)
    if not ok9:
        return None
    if aliq_cofins:
        partes_aliq_cofins = aliq_cofins.split(".")
        parte_inteira_cofins = partes_aliq_cofins[0]
        if len(parte_inteira_cofins) > 8:
            return None
    
    # QUANT_BC_COFINS: opcional, numérico com 3 decimais
    ok10, val10, _ = validar_valor_numerico(quant_bc_cofins, decimais=3, obrigatorio=False, nao_negativo=True)
    if not ok10:
        return None
    
    # ALIQ_COFINS_QUANT: opcional, numérico com 4 decimais (em reais)
    ok11, val11, _ = validar_valor_numerico(aliq_cofins_quant, decimais=4, obrigatorio=False, nao_negativo=True)
    if not ok11:
        return None
    
    # VL_COFINS: opcional, numérico com 2 decimais
    ok12, val12, _ = validar_valor_numerico(vl_cofins, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok12:
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
    
    # Função auxiliar para formatar quantidade
    def fmt_quantidade(v):
        if v is None:
            return ""
        return f"{v:,.3f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    # Função auxiliar para formatar alíquota em reais
    def fmt_aliq_reais(v):
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
        "2E": "Cupom Fiscal Emitido Por ECF",
        "13": "Bilhete Consolidado de Passagem Rodoviário",
        "14": "Bilhete Consolidado de Passagem Aquaviário",
        "15": "Bilhete Consolidado de Passagem e Nota de Bagagem",
        "16": "Bilhete Consolidado de Passagem Ferroviário"
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
        "ECF_MOD": {
            "titulo": "Modelo do equipamento",
            "valor": ecf_mod
        },
        "ECF_FAB": {
            "titulo": "Número de série de fabricação do ECF",
            "valor": ecf_fab
        },
        "DT_DOC": {
            "titulo": "Data do movimento a que se refere a Redução Z",
            "valor": dt_doc,
            "valor_formatado": fmt_data(dt_doc_obj)
        },
        "CRO": {
            "titulo": "Posição do Contador de Reinício de Operação",
            "valor": cro
        },
        "CRZ": {
            "titulo": "Posição do Contador de Redução Z",
            "valor": crz
        },
        "NUM_COO_FIN": {
            "titulo": "Número do Contador de Ordem de Operação do último documento emitido no dia. (Número do COO na Redução Z)",
            "valor": num_coo_fin
        },
        "GT_FIN": {
            "titulo": "Valor do Grande Total final",
            "valor": gt_fin,
            "valor_formatado": fmt_valor(val1)
        },
        "VL_BRT": {
            "titulo": "Valor da venda bruta",
            "valor": vl_brt,
            "valor_formatado": fmt_valor(val2)
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
        "QUANT_BC_PIS": {
            "titulo": "Quantidade – Base de cálculo PIS/PASEP",
            "valor": quant_bc_pis,
            "valor_formatado": fmt_quantidade(val5) if quant_bc_pis else ""
        },
        "ALIQ_PIS_QUANT": {
            "titulo": "Alíquota do PIS/PASEP (em reais)",
            "valor": aliq_pis_quant,
            "valor_formatado": fmt_aliq_reais(val6) if aliq_pis_quant else ""
        },
        "VL_PIS": {
            "titulo": "Valor do PIS/PASEP",
            "valor": vl_pis,
            "valor_formatado": fmt_valor(val7) if vl_pis else ""
        },
        "CST_COFINS": {
            "titulo": "Código da Situação Tributária referente a COFINS",
            "valor": cst_cofins,
            "descricao": descricoes_cst_cofins.get(cst_cofins, "")
        },
        "VL_BC_COFINS": {
            "titulo": "Valor da base de cálculo da COFINS",
            "valor": vl_bc_cofins,
            "valor_formatado": fmt_valor(val8) if vl_bc_cofins else ""
        },
        "ALIQ_COFINS": {
            "titulo": "Alíquota da COFINS (em percentual)",
            "valor": aliq_cofins,
            "valor_formatado": fmt_percentual(val9) if aliq_cofins else ""
        },
        "QUANT_BC_COFINS": {
            "titulo": "Quantidade – Base de cálculo da COFINS",
            "valor": quant_bc_cofins,
            "valor_formatado": fmt_quantidade(val10) if quant_bc_cofins else ""
        },
        "ALIQ_COFINS_QUANT": {
            "titulo": "Alíquota da COFINS (em reais)",
            "valor": aliq_cofins_quant,
            "valor_formatado": fmt_aliq_reais(val11) if aliq_cofins_quant else ""
        },
        "VL_COFINS": {
            "titulo": "Valor da COFINS",
            "valor": vl_cofins,
            "valor_formatado": fmt_valor(val12) if vl_cofins else ""
        },
        "COD_CTA": {
            "titulo": "Código da conta analítica contábil debitada/creditada",
            "valor": cod_cta
        }
    }
    
    return resultado


def validar_d350(linhas, dt_fin_0000=None):
    """
    Valida uma ou mais linhas do registro D350 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |D350|COD_MOD|ECF_MOD|ECF_FAB|DT_DOC|CRO|CRZ|NUM_COO_FIN|GT_FIN|VL_BRT|CST_PIS|VL_BC_PIS|ALIQ_PIS|QUANT_BC_PIS|ALIQ_PIS_QUANT|VL_PIS|CST_COFINS|VL_BC_COFINS|ALIQ_COFINS|QUANT_BC_COFINS|ALIQ_COFINS_QUANT|VL_COFINS|COD_CTA|
        dt_fin_0000: Data final da escrituração (ddmmaaaa) - opcional, para validação
        
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
        resultado = _processar_linha_d350(linha, dt_fin_0000)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
