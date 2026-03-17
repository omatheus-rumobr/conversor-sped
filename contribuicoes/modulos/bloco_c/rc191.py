import json


def _validar_cpf(cpf):
    """
    Valida o formato básico do CPF (11 dígitos).
    Valida também o dígito verificador (DV).
    """
    if not cpf:
        return False
    
    # Remove formatação
    cpf_limpo = cpf.replace(".", "").replace("/", "").replace("-", "").replace(" ", "")
    
    if not cpf_limpo.isdigit() or len(cpf_limpo) != 11:
        return False
    
    # Validação do dígito verificador
    # Verifica se todos os dígitos são iguais (CPF inválido)
    if len(set(cpf_limpo)) == 1:
        return False
    
    # Calcula primeiro dígito verificador
    soma = sum(int(cpf_limpo[i]) * (10 - i) for i in range(9))
    resto = soma % 11
    dv1 = 0 if resto < 2 else 11 - resto
    
    if int(cpf_limpo[9]) != dv1:
        return False
    
    # Calcula segundo dígito verificador
    soma = sum(int(cpf_limpo[i]) * (11 - i) for i in range(10))
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


def _processar_linha_c191(linha):
    """
    Processa uma única linha do registro C191 e retorna um dicionário.
    
    Formato:
      |C191|CNPJ_CPF_PART|CST_PIS|CFOP|VL_ITEM|VL_DESC|VL_BC_PIS|ALIQ_PIS|QUANT_BC_PIS|ALIQ_PIS_QUANT|VL_PIS|COD_CTA|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "C191"
    - CNPJ_CPF_PART: opcional, CNPJ/CPF do participante (14 caracteres)
      - Obrigatório, exceto em operações com participantes estrangeiros (importação) não cadastrados no CNPJ/CPF
      - Validação: quando preenchido, deve ser CPF (11 dígitos) ou CNPJ (14 dígitos) válido
    - CST_PIS: obrigatório, código da situação tributária referente ao PIS/PASEP (2 dígitos)
      - Valores válidos: [50, 51, 52, 53, 54, 55, 56, 60, 61, 62, 63, 64, 65, 66, 70, 71, 72, 73, 74, 75, 98, 99, 49]
    - CFOP: obrigatório, código fiscal de operação e prestação (4 dígitos)
      - Validação: deve existir na Tabela de CFOP (validação em camada superior)
    - VL_ITEM: obrigatório, valor do item (numérico, 2 decimais, positivo)
    - VL_DESC: opcional, valor do desconto comercial (numérico, 2 decimais, não negativo)
    - VL_BC_PIS: opcional, valor da base de cálculo do PIS/PASEP em valor (numérico, 2 decimais)
    - ALIQ_PIS: opcional, alíquota do PIS/PASEP em percentual (numérico, 4 decimais)
    - QUANT_BC_PIS: opcional, quantidade - base de cálculo PIS/PASEP (numérico, 3 decimais)
    - ALIQ_PIS_QUANT: opcional, alíquota do PIS/PASEP em reais (numérico, 4 decimais)
    - VL_PIS: opcional, valor do PIS/PASEP (numérico, 2 decimais)
      - Validação: deve corresponder ao valor da base de cálculo (campo 07 ou 09) multiplicado pela alíquota (campo 08 ou 10)
      - No caso de aplicação da alíquota do campo 08, o resultado deverá ser dividido por 100
    - COD_CTA: opcional, código da conta analítica contábil (255 caracteres)
      - Obrigatório para fatos geradores a partir de novembro de 2017, exceto se dispensado de escrituração contábil
    
    Nota: Registro obrigatório, para fins de detalhamento por fornecedor, CST, CFOP e Alíquotas, dos valores
    consolidados de PIS/Pasep referentes a cada item objeto de aquisição e/ou devolução, por Nota Fiscal
    Eletrônica – NF-e.
    
    Deve ser informado um registro C191 para cada CST, CFOP ou Alíquotas, referentes às aquisições e devoluções
    do item no período da escrituração.
    
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
    # Remove primeiro e último se vazios (formato padrão SPED: |C191|...|)
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
    if reg != "C191":
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
    cnpj_cpf_part = obter_campo(1)
    cst_pis = obter_campo(2)
    cfop = obter_campo(3)
    vl_item = obter_campo(4)
    vl_desc = obter_campo(5)
    vl_bc_pis = obter_campo(6)
    aliq_pis = obter_campo(7)
    quant_bc_pis = obter_campo(8)
    aliq_pis_quant = obter_campo(9)
    vl_pis = obter_campo(10)
    cod_cta = obter_campo(11)
    
    # Validações básicas dos campos obrigatórios
    
    # CNPJ_CPF_PART: opcional, CNPJ/CPF do participante (14 caracteres)
    # Obrigatório, exceto em operações com participantes estrangeiros não cadastrados no CNPJ/CPF
    # Quando preenchido, deve ser válido
    if cnpj_cpf_part:
        # Remove formatação para verificar tamanho
        cnpj_cpf_limpo = cnpj_cpf_part.replace(".", "").replace("/", "").replace("-", "").replace(" ", "")
        if len(cnpj_cpf_limpo) not in [11, 14]:
            return None
        if not _validar_cpf_cnpj(cnpj_cpf_part):
            return None
    
    # CST_PIS: obrigatório, código da situação tributária PIS (valores válidos para créditos)
    cst_pis_validos = ["50", "51", "52", "53", "54", "55", "56", "60", "61", "62", "63", "64", "65", "66", "70", "71", "72", "73", "74", "75", "98", "99", "49"]
    if not cst_pis or cst_pis not in cst_pis_validos:
        return None
    
    # CFOP: obrigatório, código fiscal de operação (4 dígitos)
    if not cfop or not cfop.isdigit() or len(cfop) != 4:
        return None
    
    # VL_ITEM: obrigatório, valor do item (numérico, 2 decimais, positivo)
    ok_vl_item, val_vl_item, _ = validar_valor_numerico(vl_item, decimais=2, obrigatorio=True, positivo=True)
    if not ok_vl_item:
        return None
    
    # VL_DESC: opcional, valor do desconto (numérico, 2 decimais, não negativo)
    ok_vl_desc, val_vl_desc, _ = validar_valor_numerico(vl_desc, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok_vl_desc:
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
    
    # COD_CTA: opcional, código da conta analítica contábil (255 caracteres)
    if cod_cta and len(cod_cta) > 255:
        return None
    
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
    
    # Função auxiliar para formatar CNPJ/CPF
    def fmt_cnpj_cpf(cnpj_cpf_str):
        if not cnpj_cpf_str:
            return ""
        cnpj_cpf_limpo = cnpj_cpf_str.replace(".", "").replace("/", "").replace("-", "").replace(" ", "")
        if len(cnpj_cpf_limpo) == 11:
            return f"{cnpj_cpf_limpo[:3]}.{cnpj_cpf_limpo[3:6]}.{cnpj_cpf_limpo[6:9]}-{cnpj_cpf_limpo[9:11]}"
        elif len(cnpj_cpf_limpo) == 14:
            return f"{cnpj_cpf_limpo[:2]}.{cnpj_cpf_limpo[2:5]}.{cnpj_cpf_limpo[5:8]}/{cnpj_cpf_limpo[8:12]}-{cnpj_cpf_limpo[12:14]}"
        return cnpj_cpf_str
    
    # Descrições dos campos CST
    descricoes_cst = {
        "50": "Operação com Direito a Crédito - Vinculada Exclusivamente a Receita Tributada no Mercado Interno",
        "51": "Operação com Direito a Crédito – Vinculada Exclusivamente a Receita Não Tributada no Mercado Interno",
        "52": "Operação com Direito a Crédito - Vinculada Exclusivamente a Receita de Exportação",
        "53": "Operação com Direito a Crédito - Vinculada a Receitas Tributadas e Não-Tributadas no Mercado Interno",
        "54": "Operação com Direito a Crédito - Vinculada a Receitas Tributadas no Mercado Interno e de Exportação",
        "55": "Operação com Direito a Crédito - Vinculada a Receitas Não-Tributadas no Mercado Interno e de Exportação",
        "56": "Operação com Direito a Crédito - Vinculada a Receitas Tributadas e Não-Tributadas no Mercado Interno, e de Exportação",
        "60": "Crédito Presumido - Operação de Aquisição Vinculada Exclusivamente a Receita Tributada no Mercado Interno",
        "61": "Crédito Presumido - Operação de Aquisição Vinculada Exclusivamente a Receita Não-Tributada no Mercado Interno",
        "62": "Crédito Presumido - Operação de Aquisição Vinculada Exclusivamente a Receita de Exportação",
        "63": "Crédito Presumido - Operação de Aquisição Vinculada a Receitas Tributadas e Não-Tributadas no Mercado Interno",
        "64": "Crédito Presumido - Operação de Aquisição Vinculada a Receitas Tributadas no Mercado Interno e de Exportação",
        "65": "Crédito Presumido - Operação de Aquisição Vinculada a Receitas Não-Tributadas no Mercado Interno e de Exportação",
        "66": "Crédito Presumido - Operação de Aquisição Vinculada a Receitas Tributadas e Não-Tributadas no Mercado Interno, e de Exportação",
        "70": "Operação de Aquisição sem Direito a Crédito",
        "71": "Operação de Aquisição com Isenção",
        "72": "Operação de Aquisição com Suspensão",
        "73": "Operação de Aquisição a Alíquota Zero",
        "74": "Operação de Aquisição sem Incidência da Contribuição",
        "75": "Operação de Aquisição por Substituição Tributária",
        "98": "Outras Operações de Entrada",
        "99": "Outras Operações",
        "49": "Outras Operações de Saída"
    }
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "CNPJ_CPF_PART": {
            "titulo": "CNPJ/CPF do Participante a que se referem as operações consolidadas neste registro (pessoa jurídica ou pessoa física vendedora/remetente)",
            "valor": cnpj_cpf_part,
            "valor_formatado": fmt_cnpj_cpf(cnpj_cpf_part) if cnpj_cpf_part else ""
        },
        "CST_PIS": {
            "titulo": "Código da Situação Tributária referente ao PIS/PASEP",
            "valor": cst_pis,
            "descricao": descricoes_cst.get(cst_pis, "")
        },
        "CFOP": {
            "titulo": "Código fiscal de operação e prestação",
            "valor": cfop
        },
        "VL_ITEM": {
            "titulo": "Valor do item",
            "valor": vl_item,
            "valor_formatado": fmt_valor(val_vl_item)
        },
        "VL_DESC": {
            "titulo": "Valor do desconto comercial / Exclusão",
            "valor": vl_desc,
            "valor_formatado": fmt_valor(val_vl_desc)
        },
        "VL_BC_PIS": {
            "titulo": "Valor da base de cálculo do PIS/PASEP",
            "valor": vl_bc_pis,
            "valor_formatado": fmt_valor(val_vl_bc_pis)
        },
        "ALIQ_PIS": {
            "titulo": "Alíquota do PIS/PASEP (em percentual)",
            "valor": aliq_pis,
            "valor_formatado": fmt_valor_decimais(val_aliq_pis, 4) if aliq_pis else ""
        },
        "QUANT_BC_PIS": {
            "titulo": "Quantidade – Base de cálculo PIS/PASEP",
            "valor": quant_bc_pis,
            "valor_formatado": fmt_valor_decimais(val_quant_bc_pis, 3) if quant_bc_pis else ""
        },
        "ALIQ_PIS_QUANT": {
            "titulo": "Alíquota do PIS/PASEP (em reais)",
            "valor": aliq_pis_quant,
            "valor_formatado": fmt_valor_decimais(val_aliq_pis_quant, 4) if aliq_pis_quant else ""
        },
        "VL_PIS": {
            "titulo": "Valor do PIS/PASEP",
            "valor": vl_pis,
            "valor_formatado": fmt_valor(val_vl_pis)
        },
        "COD_CTA": {
            "titulo": "Código da conta analítica contábil debitada/creditada",
            "valor": cod_cta
        }
    }
    
    return resultado


def validar_c191(linhas):
    """
    Valida uma ou mais linhas do registro C191 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |C191|CNPJ_CPF_PART|CST_PIS|CFOP|VL_ITEM|VL_DESC|VL_BC_PIS|ALIQ_PIS|QUANT_BC_PIS|ALIQ_PIS_QUANT|VL_PIS|COD_CTA|
        
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
        resultado = _processar_linha_c191(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
