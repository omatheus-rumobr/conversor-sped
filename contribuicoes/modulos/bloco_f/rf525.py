import json


def _validar_cpf(cpf):
    """
    Valida o formato básico do CPF (11 dígitos).
    Valida também o dígito verificador (DV).
    """
    if not cpf:
        return False
    
    # Remove formatação
    cpf_limpo = cpf.replace(".", "").replace("-", "").replace(" ", "")
    
    if not cpf_limpo.isdigit() or len(cpf_limpo) != 11:
        return False
    
    # Validação do dígito verificador
    # Verifica se todos os dígitos são iguais (CPF inválido)
    if len(set(cpf_limpo)) == 1:
        return False
    
    # Calcula primeiro dígito verificador
    multiplicadores1 = [10, 9, 8, 7, 6, 5, 4, 3, 2]
    soma = sum(int(cpf_limpo[i]) * multiplicadores1[i] for i in range(9))
    resto = soma % 11
    dv1 = 0 if resto < 2 else 11 - resto
    
    if int(cpf_limpo[9]) != dv1:
        return False
    
    # Calcula segundo dígito verificador
    multiplicadores2 = [11, 10, 9, 8, 7, 6, 5, 4, 3, 2]
    soma = sum(int(cpf_limpo[i]) * multiplicadores2[i] for i in range(10))
    resto = soma % 11
    dv2 = 0 if resto < 2 else 11 - resto
    
    if int(cpf_limpo[10]) != dv2:
        return False
    
    return True


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


def _validar_cpf_cnpj(cpf_cnpj):
    """
    Valida se é um CPF (11 dígitos) ou CNPJ (14 dígitos) válido.
    """
    if not cpf_cnpj:
        return False
    
    # Remove formatação
    cpf_cnpj_limpo = cpf_cnpj.replace(".", "").replace("/", "").replace("-", "").replace(" ", "")
    
    if len(cpf_cnpj_limpo) == 11:
        return _validar_cpf(cpf_cnpj)
    elif len(cpf_cnpj_limpo) == 14:
        return _validar_cnpj(cpf_cnpj)
    else:
        return False


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


def _processar_linha_f525(linha):
    """
    Processa uma única linha do registro F525 e retorna um dicionário.
    
    Formato:
      |F525|VL_REC|IND_REC|CNPJ_CPF|NUM_DOC|COD_ITEM|VL_REC_DET|CST_PIS|CST_COFINS|INFO_COMPL|COD_CTA|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "F525"
    - VL_REC: obrigatório, numérico com 2 decimais
    - IND_REC: obrigatório, valores válidos [01, 02, 03, 04, 05, 99]
    - CNPJ_CPF: opcional, 14 caracteres (CNPJ ou CPF)
      - Deve ser preenchido se IND_REC = 01 ou 02
    - NUM_DOC: opcional, máximo 60 caracteres
      - Deve ser preenchido se IND_REC = 03 ou 04
    - COD_ITEM: opcional, máximo 60 caracteres
      - Deve ser preenchido se IND_REC = 05
    - VL_REC_DET: obrigatório, numérico com 2 decimais
    - CST_PIS: opcional, 2 dígitos
    - CST_COFINS: opcional, 2 dígitos
    - INFO_COMPL: opcional, sem limite de tamanho
    - COD_CTA: opcional, máximo 255 caracteres
    
    Nota: Registro obrigatório para a pessoa jurídica submetida ao regime de tributação com base no
    lucro presumido, optante pela apuração das contribuições sociais pelo regime de caixa. Tem por
    objetivo relacionar a composição de todas as receitas recebidas pela pessoa jurídica no período
    da escrituração, sujeitas ou não ao pagamento da contribuição social.
    
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
    # Remove primeiro e último se vazios (formato padrão SPED: |F525|...|)
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
    if reg != "F525":
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
    vl_rec = obter_campo(1)
    ind_rec = obter_campo(2)
    cnpj_cpf = obter_campo(3)
    num_doc = obter_campo(4)
    cod_item = obter_campo(5)
    vl_rec_det = obter_campo(6)
    cst_pis = obter_campo(7)
    cst_cofins = obter_campo(8)
    info_compl = obter_campo(9)
    cod_cta = obter_campo(10)
    
    # Validações básicas dos campos obrigatórios
    
    # VL_REC: obrigatório, numérico com 2 decimais
    ok1, val1, _ = validar_valor_numerico(vl_rec, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok1:
        return None
    
    # IND_REC: obrigatório, valores válidos [01, 02, 03, 04, 05, 99]
    ind_rec_validos = ["01", "02", "03", "04", "05", "99"]
    if not ind_rec or ind_rec not in ind_rec_validos:
        return None
    
    # CNPJ_CPF: opcional, mas deve ser preenchido se IND_REC = 01 ou 02
    if ind_rec in ["01", "02"]:
        if not cnpj_cpf:
            return None
        # Remove formatação para validar
        cnpj_cpf_limpo = cnpj_cpf.replace(".", "").replace("/", "").replace("-", "").replace(" ", "")
        if len(cnpj_cpf_limpo) not in [11, 14] or not _validar_cpf_cnpj(cnpj_cpf):
            return None
    elif cnpj_cpf:
        # Se IND_REC não for 01 ou 02, mas CNPJ_CPF estiver preenchido, valida o formato
        cnpj_cpf_limpo = cnpj_cpf.replace(".", "").replace("/", "").replace("-", "").replace(" ", "")
        if len(cnpj_cpf_limpo) not in [11, 14] or not _validar_cpf_cnpj(cnpj_cpf):
            return None
    
    # NUM_DOC: opcional, máximo 60 caracteres
    # Deve ser preenchido se IND_REC = 03 ou 04
    if ind_rec in ["03", "04"]:
        if not num_doc:
            return None
    if num_doc and len(num_doc) > 60:
        return None
    
    # COD_ITEM: opcional, máximo 60 caracteres
    # Deve ser preenchido se IND_REC = 05
    if ind_rec == "05":
        if not cod_item:
            return None
    if cod_item and len(cod_item) > 60:
        return None
    
    # VL_REC_DET: obrigatório, numérico com 2 decimais
    ok2, val2, _ = validar_valor_numerico(vl_rec_det, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok2:
        return None
    
    # CST_PIS: opcional, 2 dígitos
    if cst_pis and (len(cst_pis) != 2 or not cst_pis.isdigit()):
        return None
    
    # CST_COFINS: opcional, 2 dígitos
    if cst_cofins and (len(cst_cofins) != 2 or not cst_cofins.isdigit()):
        return None
    
    # INFO_COMPL: opcional, sem limite de tamanho (não precisa validar)
    
    # COD_CTA: opcional, máximo 255 caracteres
    if cod_cta and len(cod_cta) > 255:
        return None
    
    # Função auxiliar para formatar valores monetários
    def fmt_valor(v):
        if v is None:
            return ""
        return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    # Função auxiliar para formatar CPF/CNPJ
    def fmt_cpf_cnpj(cpf_cnpj_str):
        if not cpf_cnpj_str:
            return ""
        cpf_cnpj_limpo = cpf_cnpj_str.replace(".", "").replace("/", "").replace("-", "").replace(" ", "")
        if len(cpf_cnpj_limpo) == 11:
            # Formata CPF: 000.000.000-00
            return f"{cpf_cnpj_limpo[:3]}.{cpf_cnpj_limpo[3:6]}.{cpf_cnpj_limpo[6:9]}-{cpf_cnpj_limpo[9:]}"
        elif len(cpf_cnpj_limpo) == 14:
            # Formata CNPJ: 00.000.000/0000-00
            return f"{cpf_cnpj_limpo[:2]}.{cpf_cnpj_limpo[2:5]}.{cpf_cnpj_limpo[5:8]}/{cpf_cnpj_limpo[8:12]}-{cpf_cnpj_limpo[12:]}"
        return cpf_cnpj_str
    
    # Descrições dos campos
    descricoes_ind_rec = {
        "01": "Clientes",
        "02": "Administradora de cartão de débito/crédito",
        "03": "Título de crédito - Duplicata, nota promissória, cheque, etc.",
        "04": "Documento fiscal",
        "05": "Item vendido (produtos e serviços)",
        "99": "Outros (Detalhar no campo 10 – Informação Complementar)"
    }
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "VL_REC": {
            "titulo": "Valor total da receita recebida, correspondente ao indicador informado no campo 03 (IND_REC)",
            "valor": vl_rec,
            "valor_formatado": fmt_valor(val1)
        },
        "IND_REC": {
            "titulo": "Indicador da composição da receita recebida no período (Campo 02)",
            "valor": ind_rec,
            "descricao": descricoes_ind_rec.get(ind_rec, "")
        },
        "CNPJ_CPF": {
            "titulo": "CNPJ/CPF do participante (cliente/pessoa física ou jurídica pagadora) ou da administradora de cartões (vendas por cartão de débito ou de crédito), no caso de detalhamento da receita recebida conforme os indicadores \"01\" ou \"02\", respectivamente",
            "valor": cnpj_cpf,
            "valor_formatado": fmt_cpf_cnpj(cnpj_cpf) if cnpj_cpf else ""
        },
        "NUM_DOC": {
            "titulo": "Número do título de crédito ou do documento fiscal, no caso de detalhamento da receita recebida conforme os indicadores \"03\" ou \"04\", respectivamente",
            "valor": num_doc
        },
        "COD_ITEM": {
            "titulo": "Código do item (campo 02 do Registro 0200), no caso de detalhamento da receita recebida por item vendido, conforme o indicador \"05\"",
            "valor": cod_item
        },
        "VL_REC_DET": {
            "titulo": "Valor da receita detalhada, correspondente ao conteúdo informado no campo 04, 05, 06 ou 10",
            "valor": vl_rec_det,
            "valor_formatado": fmt_valor(val2)
        },
        "CST_PIS": {
            "titulo": "Código da Situação Tributária do PIS/Pasep",
            "valor": cst_pis
        },
        "CST_COFINS": {
            "titulo": "Código da Situação Tributária da Cofins",
            "valor": cst_cofins
        },
        "INFO_COMPL": {
            "titulo": "Informação complementar",
            "valor": info_compl
        },
        "COD_CTA": {
            "titulo": "Código da conta analítica contábil representativa da receita recebida",
            "valor": cod_cta
        }
    }
    
    return resultado


def validar_f525(linhas):
    """
    Valida uma ou mais linhas do registro F525 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |F525|VL_REC|IND_REC|CNPJ_CPF|NUM_DOC|COD_ITEM|VL_REC_DET|CST_PIS|CST_COFINS|INFO_COMPL|COD_CTA|
        
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
        resultado = _processar_linha_f525(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
