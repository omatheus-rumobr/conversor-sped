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


def _validar_periodo_mmaaaa(periodo_str):
    """
    Valida se o período está no formato mmaaaa e se é um período válido.
    
    Args:
        periodo_str: String com período no formato mmaaaa
        
    Returns:
        tuple: (True/False, (mes, ano) ou None)
    """
    if not periodo_str or len(periodo_str) != 6 or not periodo_str.isdigit():
        return False, None
    
    try:
        mes = int(periodo_str[:2])
        ano = int(periodo_str[2:6])
        
        if mes < 1 or mes > 12:
            return False, None
        
        return True, (mes, ano)
    except ValueError:
        return False, None


def _validar_cnpj(cnpj):
    """
    Valida o formato básico do CNPJ (14 dígitos).
    Valida também o dígito verificador (DV).
    """
    if not cnpj:
        return False
    
    # Remove formatação
    cnpj_limpo = cnpj.replace(".", "").replace("/", "").replace("-", "").replace(" ", "")
    
    if not cnpj_limpo.isdigit() or len(cnpj_limpo) != 14:
        return False
    
    # Validação do dígito verificador
    # Verifica se todos os dígitos são iguais (CNPJ inválido)
    if len(set(cnpj_limpo)) == 1:
        return False
    
    # Calcula primeiro dígito verificador
    multiplicadores1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma = sum(int(cnpj_limpo[i]) * multiplicadores1[i] for i in range(12))
    resto = soma % 11
    dv1 = 0 if resto < 2 else 11 - resto
    
    if int(cnpj_limpo[12]) != dv1:
        return False
    
    # Calcula segundo dígito verificador
    multiplicadores2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma = sum(int(cnpj_limpo[i]) * multiplicadores2[i] for i in range(13))
    resto = soma % 11
    dv2 = 0 if resto < 2 else 11 - resto
    
    if int(cnpj_limpo[13]) != dv2:
        return False
    
    return True


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


def _processar_linha_1101(linha, per_apu_escrit=None):
    """
    Processa uma única linha do registro 1101 e retorna um dicionário.
    
    Formato:
      |1101|COD_PART|COD_ITEM|COD_MOD|SER|SUB_SER|NUM_DOC|DT_OPER|CHV_NFE|VL_OPER|CFOP|NAT_BC_CRED|IND_ORIG_CRED|CST_PIS|VL_BC_PIS|ALIQ_PIS|VL_PIS|COD_CTA|COD_CCUS|DESC_COMPL|PER_ESCRIT|CNPJ|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "1101"
    - COD_PART: opcional, até 60 caracteres (deve existir no registro 0150)
    - COD_ITEM: opcional, até 60 caracteres (deve existir no registro 0200)
    - COD_MOD: opcional, 2 caracteres (código conforme Tabela 4.1.1)
    - SER: opcional, até 4 caracteres
    - SUB_SER: opcional, até 3 caracteres
    - NUM_DOC: opcional, até 9 dígitos
    - DT_OPER: obrigatório, formato ddmmaaaa, data válida
    - CHV_NFE: opcional, 44 dígitos
    - VL_OPER: obrigatório, numérico com 2 decimais, > 0
    - CFOP: opcional, 4 dígitos
    - NAT_BC_CRED: obrigatório, 2 caracteres (código conforme Tabela 4.3.7)
    - IND_ORIG_CRED: obrigatório, valores válidos [0, 1]
    - CST_PIS: obrigatório, 2 dígitos (código conforme Tabela 4.3.3)
    - VL_BC_PIS: obrigatório, numérico com 3 decimais, não negativo
    - ALIQ_PIS: obrigatório, numérico com 4 decimais, não negativo
    - VL_PIS: obrigatório, numérico com 2 decimais, não negativo
    - COD_CTA: opcional, até 255 caracteres
    - COD_CCUS: opcional, até 255 caracteres
    - DESC_COMPL: opcional
    - PER_ESCRIT: opcional, formato mmaaaa, período válido, anterior ao período da escrituração atual
    - CNPJ: obrigatório, 14 dígitos, validar DV (deve existir no registro 0140)
    
    Nota: Este registro é utilizado para créditos extemporâneos referentes a períodos anteriores.
    A partir de agosto de 2013, este registro não é mais validado pelo PVA para períodos de apuração
    a partir de agosto de 2013, mas ainda pode ser utilizado para períodos anteriores.
    As validações de que COD_PART deve existir no 0150, COD_ITEM deve existir no 0200, COD_MOD deve
    existir na Tabela 4.1.1, NAT_BC_CRED deve existir na Tabela 4.3.7, CST_PIS deve existir na Tabela 4.3.3,
    e CNPJ deve existir no 0140 devem ser feitas em uma camada superior.
    
    Args:
        linha: String com uma linha do SPED
        per_apu_escrit: Período de apuração da escrituração atual (mmaaaa) - opcional, para validação
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |1101|...|)
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
    if reg != "1101":
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
    
    # Extrai todos os campos (22 campos no total)
    cod_part = obter_campo(1)
    cod_item = obter_campo(2)
    cod_mod = obter_campo(3)
    ser = obter_campo(4)
    sub_ser = obter_campo(5)
    num_doc = obter_campo(6)
    dt_oper = obter_campo(7)
    chv_nfe = obter_campo(8)
    vl_oper = obter_campo(9)
    cfop = obter_campo(10)
    nat_bc_cred = obter_campo(11)
    ind_orig_cred = obter_campo(12)
    cst_pis = obter_campo(13)
    vl_bc_pis = obter_campo(14)
    aliq_pis = obter_campo(15)
    vl_pis = obter_campo(16)
    cod_cta = obter_campo(17)
    cod_ccus = obter_campo(18)
    desc_compl = obter_campo(19)
    per_escrit = obter_campo(20)
    cnpj = obter_campo(21)
    
    # Validações básicas dos campos obrigatórios
    
    # COD_PART: opcional, até 60 caracteres
    if cod_part and len(cod_part) > 60:
        return None
    
    # COD_ITEM: opcional, até 60 caracteres
    if cod_item and len(cod_item) > 60:
        return None
    
    # COD_MOD: opcional, 2 caracteres
    if cod_mod and len(cod_mod) != 2:
        return None
    
    # SER: opcional, até 4 caracteres
    if ser and len(ser) > 4:
        return None
    
    # SUB_SER: opcional, até 3 caracteres
    if sub_ser and len(sub_ser) > 3:
        return None
    
    # NUM_DOC: opcional, até 9 dígitos
    if num_doc and (len(num_doc) > 9 or not num_doc.isdigit()):
        return None
    
    # DT_OPER: obrigatório, formato ddmmaaaa, data válida
    dt_oper_valida, dt_oper_obj = _validar_data(dt_oper)
    if not dt_oper_valida:
        return None
    
    # CHV_NFE: opcional, 44 dígitos
    if chv_nfe and (len(chv_nfe) != 44 or not chv_nfe.isdigit()):
        return None
    
    # VL_OPER: obrigatório, numérico com 2 decimais, > 0
    ok1, val1, _ = validar_valor_numerico(vl_oper, decimais=2, obrigatorio=True, positivo=True)
    if not ok1:
        return None
    
    # CFOP: opcional, 4 dígitos
    if cfop and (len(cfop) != 4 or not cfop.isdigit()):
        return None
    
    # NAT_BC_CRED: obrigatório, 2 caracteres
    if not nat_bc_cred or len(nat_bc_cred) != 2:
        return None
    
    # IND_ORIG_CRED: obrigatório, valores válidos [0, 1]
    if not ind_orig_cred or ind_orig_cred not in ["0", "1"]:
        return None
    
    # CST_PIS: obrigatório, 2 dígitos
    if not cst_pis or len(cst_pis) != 2 or not cst_pis.isdigit():
        return None
    
    # VL_BC_PIS: obrigatório, numérico com 3 decimais, não negativo
    ok2, val2, _ = validar_valor_numerico(vl_bc_pis, decimais=3, obrigatorio=True, nao_negativo=True)
    if not ok2:
        return None
    
    # ALIQ_PIS: obrigatório, numérico com 4 decimais, não negativo
    ok3, val3, _ = validar_valor_numerico(aliq_pis, decimais=4, obrigatorio=True, nao_negativo=True)
    if not ok3:
        return None
    
    # VL_PIS: obrigatório, numérico com 2 decimais, não negativo
    ok4, val4, _ = validar_valor_numerico(vl_pis, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok4:
        return None
    
    # COD_CTA: opcional, até 255 caracteres
    if cod_cta and len(cod_cta) > 255:
        return None
    
    # COD_CCUS: opcional, até 255 caracteres
    if cod_ccus and len(cod_ccus) > 255:
        return None
    
    # PER_ESCRIT: opcional, formato mmaaaa, período válido, anterior ao período da escrituração atual
    per_escrit_valido = False
    per_escrit_tuplo = None
    if per_escrit:
        per_escrit_valido, per_escrit_tuplo = _validar_periodo_mmaaaa(per_escrit)
        if not per_escrit_valido:
            return None
        
        # PER_ESCRIT deve ser anterior ao período da escrituração atual (quando informado)
        if per_apu_escrit:
            ok_escrit, per_escrit_tuplo_atual = _validar_periodo_mmaaaa(per_apu_escrit)
            if ok_escrit and per_escrit_tuplo:
                mes_escrit_reg, ano_escrit_reg = per_escrit_tuplo
                mes_escrit_atual, ano_escrit_atual = per_escrit_tuplo_atual
                if ano_escrit_reg > ano_escrit_atual or (ano_escrit_reg == ano_escrit_atual and mes_escrit_reg >= mes_escrit_atual):
                    return None
    
    # CNPJ: obrigatório, 14 dígitos, validar DV
    if not cnpj or not _validar_cnpj(cnpj):
        return None
    
    # Função auxiliar para formatar data
    def fmt_data(d):
        return d.strftime("%d/%m/%Y") if d else ""
    
    # Função auxiliar para formatar período
    def fmt_periodo(p):
        if p:
            mes, ano = p
            return f"{mes:02d}/{ano}"
        return ""
    
    # Função auxiliar para formatar valores monetários
    def fmt_valor(v):
        return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    # Função auxiliar para formatar valores com 3 decimais
    def fmt_valor_3dec(v):
        return f"{v:,.3f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    # Função auxiliar para formatar valores com 4 decimais
    def fmt_valor_4dec(v):
        return f"{v:,.4f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    # Monta o resultado
    descricoes_ind_orig_cred = {
        "0": "Operação no Mercado Interno",
        "1": "Operação de Importação"
    }
    
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "DT_OPER": {
            "titulo": "Data da Operação",
            "valor": dt_oper,
            "valor_formatado": fmt_data(dt_oper_obj)
        },
        "VL_OPER": {
            "titulo": "Valor da Operação",
            "valor": vl_oper,
            "valor_formatado": fmt_valor(val1)
        },
        "NAT_BC_CRED": {
            "titulo": "Código da Base de Cálculo do Crédito, conforme a Tabela indicada no item 4.3.7",
            "valor": nat_bc_cred
        },
        "IND_ORIG_CRED": {
            "titulo": "Indicador da origem do crédito",
            "valor": ind_orig_cred,
            "descricao": descricoes_ind_orig_cred.get(ind_orig_cred, "")
        },
        "CST_PIS": {
            "titulo": "Código da Situação Tributária referente ao PIS/PASEP",
            "valor": cst_pis
        },
        "VL_BC_PIS": {
            "titulo": "Base de Cálculo do Crédito de PIS/PASEP (em valor ou em quantidade)",
            "valor": vl_bc_pis,
            "valor_formatado": fmt_valor_3dec(val2)
        },
        "ALIQ_PIS": {
            "titulo": "Alíquota do PIS/PASEP (em percentual ou em reais)",
            "valor": aliq_pis,
            "valor_formatado": fmt_valor_4dec(val3)
        },
        "VL_PIS": {
            "titulo": "Valor do Crédito de PIS/PASEP",
            "valor": vl_pis,
            "valor_formatado": fmt_valor(val4)
        },
        "CNPJ": {
            "titulo": "CNPJ do estabelecimento gerador do crédito extemporâneo",
            "valor": cnpj
        }
    }
    
    # COD_PART: opcional
    if cod_part:
        resultado["COD_PART"] = {
            "titulo": "Código do participante (Campo 02 do Registro 0150)",
            "valor": cod_part
        }
    else:
        resultado["COD_PART"] = {
            "titulo": "Código do participante (Campo 02 do Registro 0150)",
            "valor": ""
        }
    
    # COD_ITEM: opcional
    if cod_item:
        resultado["COD_ITEM"] = {
            "titulo": "Código do item (campo 02 do Registro 0200)",
            "valor": cod_item
        }
    else:
        resultado["COD_ITEM"] = {
            "titulo": "Código do item (campo 02 do Registro 0200)",
            "valor": ""
        }
    
    # COD_MOD: opcional
    if cod_mod:
        resultado["COD_MOD"] = {
            "titulo": "Código do modelo do documento fiscal, conforme a Tabela 4.1.1",
            "valor": cod_mod
        }
    else:
        resultado["COD_MOD"] = {
            "titulo": "Código do modelo do documento fiscal, conforme a Tabela 4.1.1",
            "valor": ""
        }
    
    # SER: opcional
    if ser:
        resultado["SER"] = {
            "titulo": "Série do documento fiscal",
            "valor": ser
        }
    else:
        resultado["SER"] = {
            "titulo": "Série do documento fiscal",
            "valor": ""
        }
    
    # SUB_SER: opcional
    if sub_ser:
        resultado["SUB_SER"] = {
            "titulo": "Subsérie do documento fiscal",
            "valor": sub_ser
        }
    else:
        resultado["SUB_SER"] = {
            "titulo": "Subsérie do documento fiscal",
            "valor": ""
        }
    
    # NUM_DOC: opcional
    if num_doc:
        resultado["NUM_DOC"] = {
            "titulo": "Número do documento fiscal",
            "valor": num_doc
        }
    else:
        resultado["NUM_DOC"] = {
            "titulo": "Número do documento fiscal",
            "valor": ""
        }
    
    # CHV_NFE: opcional
    if chv_nfe:
        resultado["CHV_NFE"] = {
            "titulo": "Chave da Nota Fiscal Eletrônica",
            "valor": chv_nfe
        }
    else:
        resultado["CHV_NFE"] = {
            "titulo": "Chave da Nota Fiscal Eletrônica",
            "valor": ""
        }
    
    # CFOP: opcional
    if cfop:
        resultado["CFOP"] = {
            "titulo": "Código fiscal de operação e prestação",
            "valor": cfop
        }
    else:
        resultado["CFOP"] = {
            "titulo": "Código fiscal de operação e prestação",
            "valor": ""
        }
    
    # COD_CTA: opcional
    if cod_cta:
        resultado["COD_CTA"] = {
            "titulo": "Código da conta analítica contábil debitada/creditada",
            "valor": cod_cta
        }
    else:
        resultado["COD_CTA"] = {
            "titulo": "Código da conta analítica contábil debitada/creditada",
            "valor": ""
        }
    
    # COD_CCUS: opcional
    if cod_ccus:
        resultado["COD_CCUS"] = {
            "titulo": "Código do Centro de Custos",
            "valor": cod_ccus
        }
    else:
        resultado["COD_CCUS"] = {
            "titulo": "Código do Centro de Custos",
            "valor": ""
        }
    
    # DESC_COMPL: opcional
    if desc_compl:
        resultado["DESC_COMPL"] = {
            "titulo": "Descrição complementar do Documento/Operação",
            "valor": desc_compl
        }
    else:
        resultado["DESC_COMPL"] = {
            "titulo": "Descrição complementar do Documento/Operação",
            "valor": ""
        }
    
    # PER_ESCRIT: opcional
    if per_escrit:
        resultado["PER_ESCRIT"] = {
            "titulo": "Mês/Ano da Escrituração em que foi registrado o documento/operação",
            "valor": per_escrit,
            "valor_formatado": fmt_periodo(per_escrit_tuplo)
        }
    else:
        resultado["PER_ESCRIT"] = {
            "titulo": "Mês/Ano da Escrituração em que foi registrado o documento/operação",
            "valor": "",
            "valor_formatado": ""
        }
    
    return resultado


def validar_1101(linhas, per_apu_escrit=None):
    """
    Valida uma ou mais linhas do registro 1101 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |1101|COD_PART|COD_ITEM|COD_MOD|SER|SUB_SER|NUM_DOC|DT_OPER|CHV_NFE|VL_OPER|CFOP|NAT_BC_CRED|IND_ORIG_CRED|CST_PIS|VL_BC_PIS|ALIQ_PIS|VL_PIS|COD_CTA|COD_CCUS|DESC_COMPL|PER_ESCRIT|CNPJ|
        per_apu_escrit: Período de apuração da escrituração atual (mmaaaa) - opcional, para validação
        
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
        resultado = _processar_linha_1101(linha, per_apu_escrit=per_apu_escrit)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
