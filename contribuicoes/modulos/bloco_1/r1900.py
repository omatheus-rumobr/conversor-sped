import json


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


def validar_valor_numerico(valor_str, decimais=2, obrigatorio=False, positivo=False, nao_negativo=False, inteiro=False):
    """
    Valida um valor numérico com precisão decimal específica.

    Args:
        valor_str: String com o valor numérico
        decimais: Número máximo de casas decimais permitidas
        obrigatorio: Se True, o campo não pode estar vazio
        positivo: Se True, o valor deve ser maior que 0
        nao_negativo: Se True, o valor deve ser maior ou igual a 0
        inteiro: Se True, o valor deve ser um número inteiro

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

        # Verifica se é inteiro quando necessário
        if inteiro and valor_float != int(valor_float):
            return False, None, "Valor deve ser um número inteiro"

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


def _processar_linha_1900(linha):
    """
    Processa uma única linha do registro 1900 e retorna um dicionário.
    
    Formato:
      |1900|CNPJ|COD_MOD|SER|SUB_SER|COD_SIT|VL_TOT_REC|QUANT_DOC|CST_PIS|CST_COFINS|CFOP|INF_COMPL|COD_CTA|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "1900"
    - CNPJ: obrigatório, 14 dígitos, com validação de DV
      - Deve estar cadastrado no Registro 0140 (validação em camada superior)
    - COD_MOD: obrigatório, 2 caracteres
      - Código do modelo do documento fiscal conforme Tabela 4.1.1, ou 98 (NF de Prestação de Serviços - ISSQN), ou 99 (Outros Documentos)
    - SER: opcional, máximo 4 caracteres
    - SUB_SER: opcional, máximo 20 caracteres
    - COD_SIT: opcional, valores válidos [00, 02, 99]
    - VL_TOT_REC: obrigatório, numérico com 2 decimais, não negativo
    - QUANT_DOC: opcional, numérico inteiro, não negativo
    - CST_PIS: opcional, 2 dígitos, valores válidos [01, 02, 03, 04, 05, 06, 07, 08, 09, 49, 99]
    - CST_COFINS: opcional, 2 dígitos, valores válidos [01, 02, 03, 04, 05, 06, 07, 08, 09, 49, 99]
    - CFOP: opcional, 4 dígitos (validação na Tabela CFOP em camada superior)
    - INF_COMPL: opcional, texto livre
    - COD_CTA: opcional, máximo 255 caracteres
    
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
    # Remove primeiro e último se vazios (formato padrão SPED: |1900|...|)
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
    if reg != "1900":
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
    
    # Extrai todos os campos (13 campos no total)
    cnpj = obter_campo(1)
    cod_mod = obter_campo(2)
    ser = obter_campo(3)
    sub_ser = obter_campo(4)
    cod_sit = obter_campo(5)
    vl_tot_rec = obter_campo(6)
    quant_doc = obter_campo(7)
    cst_pis = obter_campo(8)
    cst_cofins = obter_campo(9)
    cfop = obter_campo(10)
    inf_compl = obter_campo(11)
    cod_cta = obter_campo(12)
    
    # Validações básicas dos campos obrigatórios
    
    # CNPJ: obrigatório, 14 dígitos, com validação de DV
    if not cnpj or not _validar_cnpj(cnpj):
        return None
    
    # COD_MOD: obrigatório, 2 caracteres
    if not cod_mod or len(cod_mod) > 2:
        return None
    
    # SER: opcional, máximo 4 caracteres
    if ser and len(ser) > 4:
        return None
    
    # SUB_SER: opcional, máximo 20 caracteres
    if sub_ser and len(sub_ser) > 20:
        return None
    
    # COD_SIT: opcional, valores válidos [00, 02, 99]
    if cod_sit and cod_sit not in ["00", "02", "99"]:
        return None
    
    # VL_TOT_REC: obrigatório, numérico com 2 decimais, não negativo
    ok1, val1, _ = validar_valor_numerico(vl_tot_rec, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok1:
        return None
    
    # QUANT_DOC: opcional, numérico inteiro, não negativo
    ok2, val2, _ = validar_valor_numerico(quant_doc, decimais=0, obrigatorio=False, nao_negativo=True, inteiro=True)
    if not ok2:
        return None
    
    # CST_PIS: opcional, 2 dígitos, valores válidos [01, 02, 03, 04, 05, 06, 07, 08, 09, 49, 99]
    valores_validos_cst = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "49", "99"]
    if cst_pis and (len(cst_pis) != 2 or cst_pis not in valores_validos_cst):
        return None
    
    # CST_COFINS: opcional, 2 dígitos, valores válidos [01, 02, 03, 04, 05, 06, 07, 08, 09, 49, 99]
    if cst_cofins and (len(cst_cofins) != 2 or cst_cofins not in valores_validos_cst):
        return None
    
    # CFOP: opcional, 4 dígitos
    if cfop and (len(cfop) != 4 or not cfop.isdigit()):
        return None
    
    # COD_CTA: opcional, máximo 255 caracteres
    if cod_cta and len(cod_cta) > 255:
        return None
    
    # Função auxiliar para formatar CNPJ
    def fmt_cnpj(cnpj_str):
        if cnpj_str and len(cnpj_str) == 14:
            return f"{cnpj_str[:2]}.{cnpj_str[2:5]}.{cnpj_str[5:8]}/{cnpj_str[8:12]}-{cnpj_str[12:14]}"
        return cnpj_str
    
    # Função auxiliar para formatar valores monetários
    def fmt_valor(v):
        return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    # Função auxiliar para formatar quantidade (inteiro)
    def fmt_quantidade(v):
        if v is not None:
            return f"{int(v):,}".replace(",", ".")
        return ""
    
    # Monta o resultado
    descricoes_cod_sit = {
        "00": "Documento regular",
        "02": "Documento cancelado",
        "99": "Outros"
    }
    
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
    
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "CNPJ": {
            "titulo": "CNPJ do estabelecimento da pessoa jurídica, emitente dos documentos geradores de receita",
            "valor": cnpj,
            "valor_formatado": fmt_cnpj(cnpj)
        },
        "COD_MOD": {
            "titulo": "Código do modelo do documento fiscal conforme a Tabela 4.1.1, ou: 98 – Nota Fiscal de Prestação de Serviços (ISSQN) 99 – Outros Documentos",
            "valor": cod_mod
        },
        "SER": {
            "titulo": "Série do documento fiscal",
            "valor": ser
        },
        "SUB_SER": {
            "titulo": "Subserie do documento fiscal",
            "valor": sub_ser
        },
        "COD_SIT": {
            "titulo": "Código da situação do documento fiscal",
            "valor": cod_sit,
            "descricao": descricoes_cod_sit.get(cod_sit, "") if cod_sit else ""
        },
        "VL_TOT_REC": {
            "titulo": "Valor total da receita, conforme os documentos emitidos no período, representativos da venda de bens e serviços",
            "valor": vl_tot_rec,
            "valor_formatado": fmt_valor(val1)
        },
        "QUANT_DOC": {
            "titulo": "Quantidade total de documentos emitidos no período",
            "valor": quant_doc,
            "valor_formatado": fmt_quantidade(val2) if quant_doc else ""
        },
        "CST_PIS": {
            "titulo": "Código da Situação Tributária do PIS/Pasep",
            "valor": cst_pis,
            "descricao": descricoes_cst.get(cst_pis, "") if cst_pis else ""
        },
        "CST_COFINS": {
            "titulo": "Código da Situação Tributária da Cofins",
            "valor": cst_cofins,
            "descricao": descricoes_cst.get(cst_cofins, "") if cst_cofins else ""
        },
        "CFOP": {
            "titulo": "Código fiscal de operação e prestação",
            "valor": cfop
        },
        "INF_COMPL": {
            "titulo": "Informações complementares",
            "valor": inf_compl
        },
        "COD_CTA": {
            "titulo": "Código da conta analítica contábil representativa da receita",
            "valor": cod_cta
        }
    }
    
    return resultado


def validar_1900(linhas):
    """
    Valida uma ou mais linhas do registro 1900 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |1900|CNPJ|COD_MOD|SER|SUB_SER|COD_SIT|VL_TOT_REC|QUANT_DOC|CST_PIS|CST_COFINS|CFOP|INF_COMPL|COD_CTA|
        
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
        resultado = _processar_linha_1900(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
