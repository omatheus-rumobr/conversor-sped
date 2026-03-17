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


def _processar_linha_f700(linha):
    """
    Processa uma única linha do registro F700 e retorna um dicionário.
    
    Formato:
      |F700|IND_ORI_DED|IND_NAT_DED|VL_DED_PIS|VL_DED_COFINS|VL_BC_OPER|CNPJ|INF_COMP|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "F700"
    - IND_ORI_DED: obrigatório, valores válidos [01, 02, 03, 04, 99]
    - IND_NAT_DED: obrigatório, valores válidos [0, 1]
    - VL_DED_PIS: obrigatório, numérico com 2 decimais
    - VL_DED_COFINS: obrigatório, numérico com 2 decimais
    - VL_BC_OPER: opcional, numérico com 2 decimais
    - CNPJ: opcional, 14 dígitos com validação de DV
      - Não é obrigatório quando IND_ORI_DED = "01"
    - INF_COMP: opcional, máximo 90 caracteres
    
    Nota: Neste registro devem ser informadas as deduções diversas previstas na legislação tributária,
    inclusive os créditos que não sejam específicos do regime não-cumulativo, passíveis de dedução na
    determinação da contribuição social a recolher, nos registros M200 (PIS/Pasep) e M600 (Cofins).
    A chave deste registro é composta pelos campos IND_ORI_DED + IND_NAT_DED + CNPJ, ou seja, não poderá
    existir dois ou mais registros F700 com os mesmos valores nestes campos.
    
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
    # Remove primeiro e último se vazios (formato padrão SPED: |F700|...|)
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
    if reg != "F700":
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
    
    # Extrai todos os campos (8 campos no total)
    ind_ori_ded = obter_campo(1)
    ind_nat_ded = obter_campo(2)
    vl_ded_pis = obter_campo(3)
    vl_ded_cofins = obter_campo(4)
    vl_bc_oper = obter_campo(5)
    cnpj = obter_campo(6)
    inf_comp = obter_campo(7)
    
    # Validações básicas dos campos obrigatórios
    
    # IND_ORI_DED: obrigatório, valores válidos [01, 02, 03, 04, 99]
    ind_ori_ded_validos = ["01", "02", "03", "04", "99"]
    if not ind_ori_ded or ind_ori_ded not in ind_ori_ded_validos:
        return None
    
    # IND_NAT_DED: obrigatório, valores válidos [0, 1]
    ind_nat_ded_validos = ["0", "1"]
    if not ind_nat_ded or ind_nat_ded not in ind_nat_ded_validos:
        return None
    
    # VL_DED_PIS: obrigatório, numérico com 2 decimais
    ok1, val1, _ = validar_valor_numerico(vl_ded_pis, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok1:
        return None
    
    # VL_DED_COFINS: obrigatório, numérico com 2 decimais
    ok2, val2, _ = validar_valor_numerico(vl_ded_cofins, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok2:
        return None
    
    # VL_BC_OPER: opcional, numérico com 2 decimais
    ok3, val3, _ = validar_valor_numerico(vl_bc_oper, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok3:
        return None
    
    # CNPJ: opcional, mas deve ser válido se preenchido
    # Não é obrigatório quando IND_ORI_DED = "01"
    if cnpj:
        # Remove formatação para validar
        cnpj_limpo = cnpj.replace(".", "").replace("/", "").replace("-", "").replace(" ", "")
        if len(cnpj_limpo) != 14 or not _validar_cnpj(cnpj):
            return None
    
    # INF_COMP: opcional, máximo 90 caracteres
    if inf_comp and len(inf_comp) > 90:
        return None
    
    # Função auxiliar para formatar valores monetários
    def fmt_valor(v):
        if v is None:
            return ""
        return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    # Função auxiliar para formatar CNPJ
    def fmt_cnpj(cnpj_str):
        if not cnpj_str:
            return ""
        cnpj_limpo = cnpj_str.replace(".", "").replace("/", "").replace("-", "").replace(" ", "")
        if len(cnpj_limpo) == 14:
            # Formata CNPJ: 00.000.000/0000-00
            return f"{cnpj_limpo[:2]}.{cnpj_limpo[2:5]}.{cnpj_limpo[5:8]}/{cnpj_limpo[8:12]}-{cnpj_limpo[12:]}"
        return cnpj_str
    
    # Descrições dos campos
    descricoes_ind_ori_ded = {
        "01": "Créditos Presumidos - Medicamentos",
        "02": "Créditos Admitidos no Regime Cumulativo – Bebidas Frias",
        "03": "Contribuição Paga pelo Substituto Tributário - ZFM",
        "04": "Substituição Tributária – Não Ocorrência do Fato Gerador Presumido",
        "99": "Outras Deduções"
    }
    
    descricoes_ind_nat_ded = {
        "0": "Dedução de Natureza Não Cumulativa",
        "1": "Dedução de Natureza Cumulativa"
    }
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "IND_ORI_DED": {
            "titulo": "Indicador de Origem de Deduções Diversas",
            "valor": ind_ori_ded,
            "descricao": descricoes_ind_ori_ded.get(ind_ori_ded, "")
        },
        "IND_NAT_DED": {
            "titulo": "Indicador da Natureza da Dedução",
            "valor": ind_nat_ded,
            "descricao": descricoes_ind_nat_ded.get(ind_nat_ded, "")
        },
        "VL_DED_PIS": {
            "titulo": "Valor a Deduzir - PIS/PASEP",
            "valor": vl_ded_pis,
            "valor_formatado": fmt_valor(val1)
        },
        "VL_DED_COFINS": {
            "titulo": "Valor a Deduzir – Cofins",
            "valor": vl_ded_cofins,
            "valor_formatado": fmt_valor(val2)
        },
        "VL_BC_OPER": {
            "titulo": "Valor da Base de Cálculo da Operação que ensejou o Valor a Deduzir informado nos Campos 04 e 05",
            "valor": vl_bc_oper,
            "valor_formatado": fmt_valor(val3) if vl_bc_oper else ""
        },
        "CNPJ": {
            "titulo": "CNPJ da Pessoa Jurídica relacionada à Operação que ensejou o Valor a Deduzir informado nos Campos 04 e 05",
            "valor": cnpj,
            "valor_formatado": fmt_cnpj(cnpj) if cnpj else ""
        },
        "INF_COMP": {
            "titulo": "Informações Complementares do Documento/Operação que ensejou o Valor a Deduzir informado nos Campos 04 e 05",
            "valor": inf_comp
        }
    }
    
    return resultado


def validar_f700(linhas):
    """
    Valida uma ou mais linhas do registro F700 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |F700|IND_ORI_DED|IND_NAT_DED|VL_DED_PIS|VL_DED_COFINS|VL_BC_OPER|CNPJ|INF_COMP|
        
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
        resultado = _processar_linha_f700(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
