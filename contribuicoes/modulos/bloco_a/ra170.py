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


def _float_igual(a, b, tolerancia=0.01):
    """Compara dois floats com tolerância."""
    if a is None or b is None:
        return False
    return abs(a - b) <= tolerancia


def _processar_linha_a170(linha):
    """
    Processa uma única linha do registro A170 e retorna um dicionário.
    
    Formato:
      |A170|NUM_ITEM|COD_ITEM|DESCR_COMPL|VL_ITEM|VL_DESC|NAT_BC_CRED|IND_ORIG_CRED|CST_PIS|VL_BC_PIS|ALIQ_PIS|VL_PIS|CST_COFINS|VL_BC_COFINS|ALIQ_COFINS|VL_COFINS|COD_CTA|COD_CCUS|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "A170"
    - NUM_ITEM: obrigatório, numérico, maior que 0, sequencial
    - COD_ITEM: obrigatório, máximo 60 caracteres, deve existir no registro 0200 (validação em camada superior)
    - DESCR_COMPL: opcional, texto livre
    - VL_ITEM: obrigatório, numérico com 2 decimais
    - VL_DESC: opcional, numérico com 2 decimais
    - NAT_BC_CRED: opcional, 2 caracteres, código da base de cálculo do crédito
    - IND_ORIG_CRED: opcional, valores válidos [0, 1]
    - CST_PIS: obrigatório, 2 dígitos, código da situação tributária
    - VL_BC_PIS: opcional, numérico com 2 decimais
    - ALIQ_PIS: opcional, numérico com 2 decimais (percentual)
    - VL_PIS: opcional, numérico com 2 decimais
      - Deve ser igual a VL_BC_PIS * ALIQ_PIS / 100 (com tolerância)
    - CST_COFINS: obrigatório, 2 dígitos, código da situação tributária
    - VL_BC_COFINS: opcional, numérico com 2 decimais
    - ALIQ_COFINS: opcional, numérico com 6 caracteres, 2 decimais (percentual)
    - VL_COFINS: opcional, numérico com 2 decimais
      - Deve ser igual a VL_BC_COFINS * ALIQ_COFINS / 100 (com tolerância)
    - COD_CTA: opcional, máximo 255 caracteres
    - COD_CCUS: opcional, máximo 255 caracteres
    
    Nota: Este registro obrigatório para discriminar os itens da nota fiscal de serviço emitida pela
    pessoa jurídica ou por terceiros. Não podem ser informados para um mesmo documento fiscal, dois ou
    mais registros com o mesmo conteúdo no campo NUM_ITEM. Esta validação deve ser feita em uma camada
    superior. A validação de que COD_ITEM deve existir no registro 0200 deve ser feita em uma camada
    superior. A validação de que NAT_BC_CRED deve existir na Tabela 4.3.7 deve ser feita em uma camada
    superior. A validação de que CST_PIS e CST_COFINS devem existir nas respectivas tabelas deve ser
    feita em uma camada superior.
    
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
    # Remove primeiro e último se vazios (formato padrão SPED: |A170|...|)
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
    if reg != "A170":
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
    num_item = obter_campo(1)
    cod_item = obter_campo(2)
    descr_compl = obter_campo(3)
    vl_item = obter_campo(4)
    vl_desc = obter_campo(5)
    nat_bc_cred = obter_campo(6)
    ind_orig_cred = obter_campo(7)
    cst_pis = obter_campo(8)
    vl_bc_pis = obter_campo(9)
    aliq_pis = obter_campo(10)
    vl_pis = obter_campo(11)
    cst_cofins = obter_campo(12)
    vl_bc_cofins = obter_campo(13)
    aliq_cofins = obter_campo(14)
    vl_cofins = obter_campo(15)
    cod_cta = obter_campo(16)
    cod_ccus = obter_campo(17)
    
    # Validações básicas dos campos obrigatórios
    
    # NUM_ITEM: obrigatório, numérico, maior que 0, inteiro
    if not num_item:
        return None
    try:
        val_num_item = float(num_item)
        if val_num_item <= 0 or val_num_item != int(val_num_item):
            return None
        val_num_item = int(val_num_item)
    except ValueError:
        return None
    
    # COD_ITEM: obrigatório, máximo 60 caracteres
    if not cod_item or len(cod_item) > 60:
        return None
    
    # VL_ITEM: obrigatório, numérico com 2 decimais
    ok1, val1, _ = validar_valor_numerico(vl_item, decimais=2, obrigatorio=True)
    if not ok1:
        return None
    
    # VL_DESC: opcional, numérico com 2 decimais
    ok2, val2, _ = validar_valor_numerico(vl_desc, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok2:
        return None
    
    # NAT_BC_CRED: opcional, 2 caracteres
    if nat_bc_cred and len(nat_bc_cred) > 2:
        return None
    
    # IND_ORIG_CRED: opcional, valores válidos [0, 1]
    if ind_orig_cred and ind_orig_cred not in ["0", "1"]:
        return None
    
    # CST_PIS: obrigatório, 2 dígitos
    if not cst_pis or len(cst_pis) != 2 or not cst_pis.isdigit():
        return None
    
    # VL_BC_PIS: opcional, numérico com 2 decimais
    ok3, val3, _ = validar_valor_numerico(vl_bc_pis, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok3:
        return None
    
    # ALIQ_PIS: opcional, numérico com 2 decimais (percentual)
    ok4, val4, _ = validar_valor_numerico(aliq_pis, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok4:
        return None
    
    # VL_PIS: opcional, numérico com 2 decimais
    ok5, val5, _ = validar_valor_numerico(vl_pis, decimais=2, obrigatorio=False)
    if not ok5:
        return None
    
    # Validação: VL_PIS deve ser igual a VL_BC_PIS * ALIQ_PIS / 100 (com tolerância)
    if vl_bc_pis and aliq_pis and vl_pis:
        vl_pis_calculado = val3 * val4 / 100.0
        if not _float_igual(val5, vl_pis_calculado):
            return None
    
    # CST_COFINS: obrigatório, 2 dígitos
    if not cst_cofins or len(cst_cofins) != 2 or not cst_cofins.isdigit():
        return None
    
    # VL_BC_COFINS: opcional, numérico com 2 decimais
    ok6, val6, _ = validar_valor_numerico(vl_bc_cofins, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok6:
        return None
    
    # ALIQ_COFINS: opcional, numérico com 6 caracteres, 2 decimais (percentual)
    if aliq_cofins:
        if len(aliq_cofins) > 6:
            return None
        ok7, val7, _ = validar_valor_numerico(aliq_cofins, decimais=2, obrigatorio=False, nao_negativo=True)
        if not ok7:
            return None
    else:
        val7 = 0.0
    
    # VL_COFINS: opcional, numérico com 2 decimais
    ok8, val8, _ = validar_valor_numerico(vl_cofins, decimais=2, obrigatorio=False)
    if not ok8:
        return None
    
    # Validação: VL_COFINS deve ser igual a VL_BC_COFINS * ALIQ_COFINS / 100 (com tolerância)
    if vl_bc_cofins and aliq_cofins and vl_cofins:
        vl_cofins_calculado = val6 * val7 / 100.0
        if not _float_igual(val8, vl_cofins_calculado):
            return None
    
    # COD_CTA: opcional, máximo 255 caracteres
    if cod_cta and len(cod_cta) > 255:
        return None
    
    # COD_CCUS: opcional, máximo 255 caracteres
    if cod_ccus and len(cod_ccus) > 255:
        return None
    
    # Função auxiliar para formatar valores monetários
    def fmt_valor(v):
        return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    # Função auxiliar para formatar porcentagem
    def fmt_percentual(v):
        return f"{v:.2f}%"
    
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
        "NUM_ITEM": {
            "titulo": "Número seqüencial do item no documento fiscal",
            "valor": num_item,
            "valor_formatado": str(val_num_item)
        },
        "COD_ITEM": {
            "titulo": "Código do item (campo 02 do Registro 0200)",
            "valor": cod_item
        },
        "DESCR_COMPL": {
            "titulo": "Descrição complementar do item como adotado no documento fiscal",
            "valor": descr_compl
        },
        "VL_ITEM": {
            "titulo": "Valor total do item (mercadorias ou serviços)",
            "valor": vl_item,
            "valor_formatado": fmt_valor(val1)
        },
        "VL_DESC": {
            "titulo": "Valor do desconto comercial / exclusão da base de cálculo do PIS/PASEP e da COFINS",
            "valor": vl_desc,
            "valor_formatado": fmt_valor(val2) if vl_desc else ""
        },
        "NAT_BC_CRED": {
            "titulo": "Código da base de cálculo do crédito, conforme a Tabela indicada no item 4.3.7",
            "valor": nat_bc_cred
        },
        "IND_ORIG_CRED": {
            "titulo": "Indicador da origem do crédito",
            "valor": ind_orig_cred,
            "descricao": descricoes_ind_orig_cred.get(ind_orig_cred, "") if ind_orig_cred else ""
        },
        "CST_PIS": {
            "titulo": "Código da Situação Tributária referente ao PIS/PASEP – Tabela 4.3.3",
            "valor": cst_pis
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
            "titulo": "Código da Situação Tributária referente ao COFINS – Tabela 4.3.4",
            "valor": cst_cofins
        },
        "VL_BC_COFINS": {
            "titulo": "Valor da base de cálculo da COFINS",
            "valor": vl_bc_cofins,
            "valor_formatado": fmt_valor(val6) if vl_bc_cofins else ""
        },
        "ALIQ_COFINS": {
            "titulo": "Alíquota do COFINS (em percentual)",
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
        },
        "COD_CCUS": {
            "titulo": "Código do centro de custos",
            "valor": cod_ccus
        }
    }
    
    return resultado


def validar_a170(linhas):
    """
    Valida uma ou mais linhas do registro A170 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |A170|NUM_ITEM|COD_ITEM|DESCR_COMPL|VL_ITEM|VL_DESC|NAT_BC_CRED|IND_ORIG_CRED|CST_PIS|VL_BC_PIS|ALIQ_PIS|VL_PIS|CST_COFINS|VL_BC_COFINS|ALIQ_COFINS|VL_COFINS|COD_CTA|COD_CCUS|
        
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
        resultado = _processar_linha_a170(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
