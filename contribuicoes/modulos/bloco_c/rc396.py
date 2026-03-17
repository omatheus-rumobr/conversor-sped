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


def _processar_linha_c396(linha):
    """
    Processa uma única linha do registro C396 e retorna um dicionário.
    
    Formato:
      |C396|COD_ITEM|VL_ITEM|VL_DESC|NAT_BC_CRED|CST_PIS|VL_BC_PIS|ALIQ_PIS|VL_PIS|CST_COFINS|VL_BC_COFINS|ALIQ_COFINS|VL_COFINS|COD_CTA|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "C396"
    - COD_ITEM: obrigatório, código do item (60 caracteres)
      - Validação: deve existir no registro 0200 (validação em camada superior)
    - VL_ITEM: obrigatório, valor total do item (numérico, 2 decimais, positivo)
    - VL_DESC: opcional, valor do desconto comercial (numérico, 2 decimais, não negativo)
    - NAT_BC_CRED: obrigatório, código da base de cálculo do crédito (2 caracteres)
      - Validação: conforme Tabela indicada no item 4.3.7 (validação em camada superior)
    - CST_PIS: obrigatório, código da situação tributária referente ao PIS/PASEP (2 dígitos)
      - Validação: deve constar na Tabela de CST (validação em camada superior)
    - VL_BC_PIS: opcional, valor da base de cálculo do crédito de PIS/PASEP (numérico, 2 decimais)
    - ALIQ_PIS: opcional, alíquota do PIS/PASEP em percentual (numérico, 4 decimais)
    - VL_PIS: opcional, valor do crédito de PIS/PASEP (numérico, 2 decimais)
      - Validação: deve corresponder ao valor da base de cálculo (campo 07) multiplicado pela alíquota (campo 08)
      - No caso de aplicação da alíquota do campo 08, o resultado deverá ser dividido por 100
    - CST_COFINS: obrigatório, código da situação tributária referente ao COFINS (2 dígitos)
      - Validação: deve constar na Tabela de CST (validação em camada superior)
    - VL_BC_COFINS: opcional, valor da base de cálculo do crédito de COFINS (numérico, 2 decimais)
    - ALIQ_COFINS: opcional, alíquota da COFINS em percentual (numérico, 4 decimais)
    - VL_COFINS: opcional, valor do crédito de COFINS (numérico, 2 decimais)
      - Validação: deve corresponder ao valor da base de cálculo (campo 11) multiplicado pela alíquota (campo 12)
      - No caso de aplicação da alíquota do campo 12, o resultado deverá ser dividido por 100
    - COD_CTA: opcional, código da conta analítica contábil (255 caracteres)
      - Obrigatório para fatos geradores a partir de novembro de 2017, exceto se dispensado de escrituração contábil
    
    Nota: Deve ser informado neste registro as informações referentes aos itens das notas fiscais de vendas a
    consumidor relacionadas no Registro Pai C395, necessárias para a apuração, por item do documento fiscal,
    dos créditos de PIS/Pasep e de Cofins.
    
    Deve ser gerado um registro para cada item constante na nota fiscal de venda a consumidor relacionada em C395.
    
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
    # Remove primeiro e último se vazios (formato padrão SPED: |C396|...|)
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
    if reg != "C396":
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
    
    # Extrai todos os campos (14 campos no total)
    cod_item = obter_campo(1)
    vl_item = obter_campo(2)
    vl_desc = obter_campo(3)
    nat_bc_cred = obter_campo(4)
    cst_pis = obter_campo(5)
    vl_bc_pis = obter_campo(6)
    aliq_pis = obter_campo(7)
    vl_pis = obter_campo(8)
    cst_cofins = obter_campo(9)
    vl_bc_cofins = obter_campo(10)
    aliq_cofins = obter_campo(11)
    vl_cofins = obter_campo(12)
    cod_cta = obter_campo(13)
    
    # Validações básicas dos campos obrigatórios
    
    # COD_ITEM: obrigatório, código do item (60 caracteres)
    if not cod_item or len(cod_item) > 60:
        return None
    
    # VL_ITEM: obrigatório, valor total do item (numérico, 2 decimais, positivo)
    ok_vl_item, val_vl_item, _ = validar_valor_numerico(vl_item, decimais=2, obrigatorio=True, positivo=True)
    if not ok_vl_item:
        return None
    
    # VL_DESC: opcional, valor do desconto comercial (numérico, 2 decimais, não negativo)
    ok_vl_desc, val_vl_desc, _ = validar_valor_numerico(vl_desc, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok_vl_desc:
        return None
    
    # NAT_BC_CRED: obrigatório, código da base de cálculo do crédito (2 caracteres)
    if not nat_bc_cred or len(nat_bc_cred) != 2:
        return None
    
    # CST_PIS: obrigatório, código da situação tributária PIS (2 dígitos)
    if not cst_pis or not cst_pis.isdigit() or len(cst_pis) != 2:
        return None
    
    # VL_BC_PIS: opcional, base de cálculo do crédito de PIS (numérico, 2 decimais)
    ok_vl_bc_pis, val_vl_bc_pis, _ = validar_valor_numerico(vl_bc_pis, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok_vl_bc_pis:
        return None
    
    # ALIQ_PIS: opcional, alíquota do PIS em percentual (numérico, 4 decimais)
    ok_aliq_pis, val_aliq_pis, _ = validar_valor_numerico(aliq_pis, decimais=4, obrigatorio=False, nao_negativo=True)
    if not ok_aliq_pis:
        return None
    
    # VL_PIS: opcional, valor do crédito de PIS (numérico, 2 decimais)
    ok_vl_pis, val_vl_pis, _ = validar_valor_numerico(vl_pis, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok_vl_pis:
        return None
    
    # Validação de cálculo do VL_PIS
    if vl_pis and vl_bc_pis and aliq_pis:
        vl_pis_calculado = val_vl_bc_pis * (val_aliq_pis / 100.0)
        # Tolerância de 0.01 para diferenças de arredondamento
        if abs(val_vl_pis - vl_pis_calculado) > 0.01:
            return None
    
    # CST_COFINS: obrigatório, código da situação tributária COFINS (2 dígitos)
    if not cst_cofins or not cst_cofins.isdigit() or len(cst_cofins) != 2:
        return None
    
    # VL_BC_COFINS: opcional, base de cálculo do crédito de COFINS (numérico, 2 decimais)
    ok_vl_bc_cofins, val_vl_bc_cofins, _ = validar_valor_numerico(vl_bc_cofins, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok_vl_bc_cofins:
        return None
    
    # ALIQ_COFINS: opcional, alíquota da COFINS em percentual (numérico, 4 decimais)
    ok_aliq_cofins, val_aliq_cofins, _ = validar_valor_numerico(aliq_cofins, decimais=4, obrigatorio=False, nao_negativo=True)
    if not ok_aliq_cofins:
        return None
    
    # VL_COFINS: opcional, valor do crédito de COFINS (numérico, 2 decimais)
    ok_vl_cofins, val_vl_cofins, _ = validar_valor_numerico(vl_cofins, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok_vl_cofins:
        return None
    
    # Validação de cálculo do VL_COFINS
    if vl_cofins and vl_bc_cofins and aliq_cofins:
        vl_cofins_calculado = val_vl_bc_cofins * (val_aliq_cofins / 100.0)
        # Tolerância de 0.01 para diferenças de arredondamento
        if abs(val_vl_cofins - vl_cofins_calculado) > 0.01:
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
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "COD_ITEM": {
            "titulo": "Código do item (campo 02 do Registro 0200)",
            "valor": cod_item
        },
        "VL_ITEM": {
            "titulo": "Valor total do item (mercadorias ou serviços)",
            "valor": vl_item,
            "valor_formatado": fmt_valor(val_vl_item)
        },
        "VL_DESC": {
            "titulo": "Valor do desconto comercial do item",
            "valor": vl_desc,
            "valor_formatado": fmt_valor(val_vl_desc)
        },
        "NAT_BC_CRED": {
            "titulo": "Código da Base de Cálculo do Crédito, conforme a Tabela indicada no item 4.3.7",
            "valor": nat_bc_cred
        },
        "CST_PIS": {
            "titulo": "Código da Situação Tributária referente ao PIS/PASEP",
            "valor": cst_pis
        },
        "VL_BC_PIS": {
            "titulo": "Valor da base de cálculo do crédito de PIS/PASEP",
            "valor": vl_bc_pis,
            "valor_formatado": fmt_valor(val_vl_bc_pis)
        },
        "ALIQ_PIS": {
            "titulo": "Alíquota do PIS/PASEP (em percentual)",
            "valor": aliq_pis,
            "valor_formatado": fmt_valor_decimais(val_aliq_pis, 4) if aliq_pis else ""
        },
        "VL_PIS": {
            "titulo": "Valor do crédito de PIS/PASEP",
            "valor": vl_pis,
            "valor_formatado": fmt_valor(val_vl_pis)
        },
        "CST_COFINS": {
            "titulo": "Código da Situação Tributária referente a COFINS",
            "valor": cst_cofins
        },
        "VL_BC_COFINS": {
            "titulo": "Valor da base de cálculo do crédito de COFINS",
            "valor": vl_bc_cofins,
            "valor_formatado": fmt_valor(val_vl_bc_cofins)
        },
        "ALIQ_COFINS": {
            "titulo": "Alíquota da COFINS (em percentual)",
            "valor": aliq_cofins,
            "valor_formatado": fmt_valor_decimais(val_aliq_cofins, 4) if aliq_cofins else ""
        },
        "VL_COFINS": {
            "titulo": "Valor do crédito de COFINS",
            "valor": vl_cofins,
            "valor_formatado": fmt_valor(val_vl_cofins)
        },
        "COD_CTA": {
            "titulo": "Código da conta analítica contábil debitada/creditada",
            "valor": cod_cta
        }
    }
    
    return resultado


def validar_c396(linhas):
    """
    Valida uma ou mais linhas do registro C396 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |C396|COD_ITEM|VL_ITEM|VL_DESC|NAT_BC_CRED|CST_PIS|VL_BC_PIS|ALIQ_PIS|VL_PIS|CST_COFINS|VL_BC_COFINS|ALIQ_COFINS|VL_COFINS|COD_CTA|
        
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
        resultado = _processar_linha_c396(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
