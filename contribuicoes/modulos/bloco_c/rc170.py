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


def _processar_linha_c170(linha):
    """
    Processa uma única linha do registro C170 e retorna um dicionário.
    
    Formato:
      |C170|NUM_ITEM|COD_ITEM|DESCR_COMPL|QTD|UNID|VL_ITEM|VL_DESC|IND_MOV|CST_ICMS|CFOP|COD_NAT|VL_BC_ICMS|ALIQ_ICMS|VL_ICMS|VL_BC_ICMS_ST|ALIQ_ST|VL_ICMS_ST|IND_APUR|CST_IPI|COD_ENQ|VL_BC_IPI|ALIQ_IPI|VL_IPI|CST_PIS|VL_BC_PIS|ALIQ_PIS|QUANT_BC_PIS|ALIQ_PIS_QUANT|VL_PIS|CST_COFINS|VL_BC_COFINS|ALIQ_COFINS|QUANT_BC_COFINS|ALIQ_COFINS_QUANT|VL_COFINS|COD_CTA|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "C170"
    - NUM_ITEM: obrigatório, número sequencial do item no documento fiscal (3 dígitos, maior que 0)
    - COD_ITEM: obrigatório, código do item (60 caracteres)
      - Validação: deve existir no registro 0200 (validação em camada superior)
    - DESCR_COMPL: opcional, descrição complementar do item (texto livre)
    - QTD: opcional, quantidade do item (numérico, 5 decimais, maior que 0 quando preenchido)
    - UNID: opcional, unidade do item (6 caracteres)
      - Validação: deve existir no registro 0190 (validação em camada superior)
    - VL_ITEM: obrigatório, valor total do item (numérico, 2 decimais, positivo)
    - VL_DESC: opcional, valor do desconto comercial (numérico, 2 decimais, não negativo)
    - IND_MOV: opcional, movimentação física do item (1 dígito)
      - Valores válidos: [0, 1]
      - 0: SIM
      - 1: NÃO
    - CST_ICMS: opcional, código da situação tributária referente ao ICMS (3 dígitos)
    - CFOP: obrigatório, código fiscal de operação e prestação (4 dígitos)
      - Validação: deve existir na Tabela de CFOP (validação em camada superior)
    - COD_NAT: opcional, código da natureza da operação (10 caracteres)
      - Validação: deve existir no registro 0400 (validação em camada superior)
    - VL_BC_ICMS: opcional, valor da base de cálculo do ICMS (numérico, 2 decimais)
    - ALIQ_ICMS: opcional, alíquota do ICMS (numérico, 6 dígitos, 2 decimais)
    - VL_ICMS: opcional, valor do ICMS creditado/debitado (numérico, 2 decimais)
    - VL_BC_ICMS_ST: opcional, valor da base de cálculo referente à substituição tributária (numérico, 2 decimais)
    - ALIQ_ST: opcional, alíquota do ICMS da substituição tributária (numérico, 6 dígitos, 2 decimais)
    - VL_ICMS_ST: opcional, valor do ICMS referente à substituição tributária (numérico, 2 decimais)
    - IND_APUR: opcional, indicador de período de apuração do IPI (1 dígito)
      - Valores válidos: [0, 1]
      - 0: Mensal
      - 1: Decendial
    - CST_IPI: opcional, código da situação tributária referente ao IPI (2 caracteres)
    - COD_ENQ: opcional, código de enquadramento legal do IPI (3 caracteres)
    - VL_BC_IPI: opcional, valor da base de cálculo do IPI (numérico, 2 decimais)
    - ALIQ_IPI: opcional, alíquota do IPI (numérico, 6 dígitos, 2 decimais)
    - VL_IPI: opcional, valor do IPI creditado/debitado (numérico, 2 decimais)
    - CST_PIS: obrigatório, código da situação tributária referente ao PIS (2 dígitos)
    - VL_BC_PIS: opcional, valor da base de cálculo do PIS/PASEP (numérico, 2 decimais)
    - ALIQ_PIS: opcional, alíquota do PIS em percentual (numérico, 8 dígitos, 4 decimais)
    - QUANT_BC_PIS: opcional, quantidade - base de cálculo PIS/PASEP (numérico, 3 decimais)
    - ALIQ_PIS_QUANT: opcional, alíquota do PIS/PASEP em reais (numérico, 4 decimais)
    - VL_PIS: opcional, valor do PIS/PASEP (numérico, 2 decimais)
      - Validação: deve corresponder ao valor da base de cálculo (campo 26 ou 28) multiplicado pela alíquota (campo 27 ou 29)
    - CST_COFINS: obrigatório, código da situação tributária referente ao COFINS (2 dígitos)
    - VL_BC_COFINS: opcional, valor da base de cálculo da COFINS (numérico, 2 decimais)
    - ALIQ_COFINS: opcional, alíquota da COFINS em percentual (numérico, 8 dígitos, 4 decimais)
    - QUANT_BC_COFINS: opcional, quantidade - base de cálculo COFINS (numérico, 3 decimais)
    - ALIQ_COFINS_QUANT: opcional, alíquota da COFINS em reais (numérico, 4 decimais)
    - VL_COFINS: opcional, valor da COFINS (numérico, 2 decimais)
      - Validação: deve corresponder ao valor da base de cálculo (campo 32 ou 34) multiplicado pela alíquota (campo 33 ou 35)
    - COD_CTA: opcional, código da conta analítica contábil (255 caracteres)
      - Obrigatório para fatos geradores a partir de novembro de 2017, exceto se dispensado de escrituração contábil
    
    Nota: Registro obrigatório para discriminar os itens da nota fiscal (mercadorias e/ou serviços constantes
    em notas conjugadas), inclusive em operações de entrada de mercadorias acompanhada de Nota Fiscal Eletrônica
    (NF-e) de emissão de terceiros.
    
    Não podem ser informados para um mesmo documento fiscal, dois ou mais registros com o mesmo conteúdo
    no campo NUM_ITEM (validação em camada superior).
    
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
    # Remove primeiro e último se vazios (formato padrão SPED: |C170|...|)
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
    if reg != "C170":
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
    
    # Extrai todos os campos (37 campos no total)
    num_item = obter_campo(1)
    cod_item = obter_campo(2)
    descr_compl = obter_campo(3)
    qtd = obter_campo(4)
    unid = obter_campo(5)
    vl_item = obter_campo(6)
    vl_desc = obter_campo(7)
    ind_mov = obter_campo(8)
    cst_icms = obter_campo(9)
    cfop = obter_campo(10)
    cod_nat = obter_campo(11)
    vl_bc_icms = obter_campo(12)
    aliq_icms = obter_campo(13)
    vl_icms = obter_campo(14)
    vl_bc_icms_st = obter_campo(15)
    aliq_st = obter_campo(16)
    vl_icms_st = obter_campo(17)
    ind_apur = obter_campo(18)
    cst_ipi = obter_campo(19)
    cod_enq = obter_campo(20)
    vl_bc_ipi = obter_campo(21)
    aliq_ipi = obter_campo(22)
    vl_ipi = obter_campo(23)
    cst_pis = obter_campo(24)
    vl_bc_pis = obter_campo(25)
    aliq_pis = obter_campo(26)
    quant_bc_pis = obter_campo(27)
    aliq_pis_quant = obter_campo(28)
    vl_pis = obter_campo(29)
    cst_cofins = obter_campo(30)
    vl_bc_cofins = obter_campo(31)
    aliq_cofins = obter_campo(32)
    quant_bc_cofins = obter_campo(33)
    aliq_cofins_quant = obter_campo(34)
    vl_cofins = obter_campo(35)
    cod_cta = obter_campo(36)
    
    # Validações básicas dos campos obrigatórios
    
    # NUM_ITEM: obrigatório, número sequencial do item (3 dígitos, maior que 0)
    if not num_item or not num_item.isdigit() or len(num_item) > 3:
        return None
    try:
        num_item_int = int(num_item)
        if num_item_int <= 0:
            return None
    except ValueError:
        return None
    
    # COD_ITEM: obrigatório, código do item (60 caracteres)
    if not cod_item or len(cod_item) > 60:
        return None
    
    # QTD: opcional, quantidade do item (numérico, 5 decimais, maior que 0 quando preenchido)
    ok_qtd, val_qtd, _ = validar_valor_numerico(qtd, decimais=5, obrigatorio=False, positivo=True)
    if not ok_qtd:
        return None
    
    # UNID: opcional, unidade do item (6 caracteres)
    if unid and len(unid) > 6:
        return None
    
    # VL_ITEM: obrigatório, valor total do item (numérico, 2 decimais, positivo)
    ok_vl_item, val_vl_item, _ = validar_valor_numerico(vl_item, decimais=2, obrigatorio=True, positivo=True)
    if not ok_vl_item:
        return None
    
    # VL_DESC: opcional, valor do desconto (numérico, 2 decimais, não negativo)
    ok_vl_desc, val_vl_desc, _ = validar_valor_numerico(vl_desc, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok_vl_desc:
        return None
    
    # IND_MOV: opcional, movimentação física (valores válidos [0, 1])
    if ind_mov:
        ind_mov_validos = ["0", "1"]
        if ind_mov not in ind_mov_validos:
            return None
    
    # CST_ICMS: opcional, código da situação tributária ICMS (3 dígitos)
    if cst_icms and (not cst_icms.isdigit() or len(cst_icms) > 3):
        return None
    
    # CFOP: obrigatório, código fiscal de operação (4 dígitos)
    if not cfop or not cfop.isdigit() or len(cfop) != 4:
        return None
    
    # COD_NAT: opcional, código da natureza da operação (10 caracteres)
    if cod_nat and len(cod_nat) > 10:
        return None
    
    # VL_BC_ICMS: opcional, base de cálculo do ICMS (numérico, 2 decimais)
    ok_vl_bc_icms, val_vl_bc_icms, _ = validar_valor_numerico(vl_bc_icms, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok_vl_bc_icms:
        return None
    
    # ALIQ_ICMS: opcional, alíquota do ICMS (numérico, 6 dígitos, 2 decimais)
    ok_aliq_icms, val_aliq_icms, _ = validar_valor_numerico(aliq_icms, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok_aliq_icms:
        return None
    
    # VL_ICMS: opcional, valor do ICMS (numérico, 2 decimais)
    ok_vl_icms, val_vl_icms, _ = validar_valor_numerico(vl_icms, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok_vl_icms:
        return None
    
    # VL_BC_ICMS_ST: opcional, base de cálculo ICMS ST (numérico, 2 decimais)
    ok_vl_bc_icms_st, val_vl_bc_icms_st, _ = validar_valor_numerico(vl_bc_icms_st, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok_vl_bc_icms_st:
        return None
    
    # ALIQ_ST: opcional, alíquota do ICMS ST (numérico, 6 dígitos, 2 decimais)
    ok_aliq_st, val_aliq_st, _ = validar_valor_numerico(aliq_st, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok_aliq_st:
        return None
    
    # VL_ICMS_ST: opcional, valor do ICMS ST (numérico, 2 decimais)
    ok_vl_icms_st, val_vl_icms_st, _ = validar_valor_numerico(vl_icms_st, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok_vl_icms_st:
        return None
    
    # IND_APUR: opcional, indicador de período de apuração do IPI (valores válidos [0, 1])
    if ind_apur:
        ind_apur_validos = ["0", "1"]
        if ind_apur not in ind_apur_validos:
            return None
    
    # CST_IPI: opcional, código da situação tributária IPI (2 caracteres)
    if cst_ipi and len(cst_ipi) > 2:
        return None
    
    # COD_ENQ: opcional, código de enquadramento legal do IPI (3 caracteres)
    if cod_enq and len(cod_enq) > 3:
        return None
    
    # VL_BC_IPI: opcional, base de cálculo do IPI (numérico, 2 decimais)
    ok_vl_bc_ipi, val_vl_bc_ipi, _ = validar_valor_numerico(vl_bc_ipi, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok_vl_bc_ipi:
        return None
    
    # ALIQ_IPI: opcional, alíquota do IPI (numérico, 6 dígitos, 2 decimais)
    ok_aliq_ipi, val_aliq_ipi, _ = validar_valor_numerico(aliq_ipi, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok_aliq_ipi:
        return None
    
    # VL_IPI: opcional, valor do IPI (numérico, 2 decimais)
    ok_vl_ipi, val_vl_ipi, _ = validar_valor_numerico(vl_ipi, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok_vl_ipi:
        return None
    
    # CST_PIS: obrigatório, código da situação tributária PIS (2 dígitos)
    if not cst_pis or len(cst_pis) > 2:
        return None
    
    # VL_BC_PIS: opcional, base de cálculo do PIS em valor (numérico, 2 decimais)
    ok_vl_bc_pis, val_vl_bc_pis, _ = validar_valor_numerico(vl_bc_pis, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok_vl_bc_pis:
        return None
    
    # ALIQ_PIS: opcional, alíquota do PIS em percentual (numérico, 8 dígitos, 4 decimais)
    ok_aliq_pis, val_aliq_pis, _ = validar_valor_numerico(aliq_pis, decimais=4, obrigatorio=False, nao_negativo=True)
    if not ok_aliq_pis:
        return None
    
    # QUANT_BC_PIS: opcional, quantidade - base de cálculo PIS (numérico, 3 decimais)
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
        # Se tem base de cálculo em valor, calcula com base e alíquota percentual
        elif vl_bc_pis and aliq_pis:
            vl_pis_calculado = val_vl_bc_pis * (val_aliq_pis / 100.0)
            # Tolerância de 0.01 para diferenças de arredondamento
            if abs(val_vl_pis - vl_pis_calculado) > 0.01:
                return None
    
    # CST_COFINS: obrigatório, código da situação tributária COFINS (2 dígitos)
    if not cst_cofins or len(cst_cofins) > 2:
        return None
    
    # VL_BC_COFINS: opcional, base de cálculo da COFINS em valor (numérico, 2 decimais)
    ok_vl_bc_cofins, val_vl_bc_cofins, _ = validar_valor_numerico(vl_bc_cofins, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok_vl_bc_cofins:
        return None
    
    # ALIQ_COFINS: opcional, alíquota da COFINS em percentual (numérico, 8 dígitos, 4 decimais)
    ok_aliq_cofins, val_aliq_cofins, _ = validar_valor_numerico(aliq_cofins, decimais=4, obrigatorio=False, nao_negativo=True)
    if not ok_aliq_cofins:
        return None
    
    # QUANT_BC_COFINS: opcional, quantidade - base de cálculo COFINS (numérico, 3 decimais)
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
        # Se tem base de cálculo em valor, calcula com base e alíquota percentual
        elif vl_bc_cofins and aliq_cofins:
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
    
    # Descrições dos campos
    descricoes_ind_mov = {
        "0": "SIM",
        "1": "NÃO"
    }
    
    descricoes_ind_apur = {
        "0": "Mensal",
        "1": "Decendial"
    }
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "NUM_ITEM": {
            "titulo": "Número seqüencial do item no documento fiscal",
            "valor": num_item
        },
        "COD_ITEM": {
            "titulo": "Código do item (campo 02 do Registro 0200)",
            "valor": cod_item
        },
        "DESCR_COMPL": {
            "titulo": "Descrição complementar do item como adotado no documento fiscal",
            "valor": descr_compl
        },
        "QTD": {
            "titulo": "Quantidade do item",
            "valor": qtd,
            "valor_formatado": fmt_valor_decimais(val_qtd, 5) if qtd else ""
        },
        "UNID": {
            "titulo": "Unidade do item (Campo 02 do registro 0190)",
            "valor": unid
        },
        "VL_ITEM": {
            "titulo": "Valor total do item (mercadorias ou serviços)",
            "valor": vl_item,
            "valor_formatado": fmt_valor(val_vl_item)
        },
        "VL_DESC": {
            "titulo": "Valor do desconto comercial / exclusão da base de cálculo do PIS/PASEP e da COFINS",
            "valor": vl_desc,
            "valor_formatado": fmt_valor(val_vl_desc)
        },
        "IND_MOV": {
            "titulo": "Movimentação física do ITEM/PRODUTO",
            "valor": ind_mov,
            "descricao": descricoes_ind_mov.get(ind_mov, "") if ind_mov else ""
        },
        "CST_ICMS": {
            "titulo": "Código da Situação Tributária referente ao ICMS, conforme a Tabela indicada no item 4.3.1",
            "valor": cst_icms
        },
        "CFOP": {
            "titulo": "Código Fiscal de Operação e Prestação",
            "valor": cfop
        },
        "COD_NAT": {
            "titulo": "Código da natureza da operação (campo 02 do Registro 0400)",
            "valor": cod_nat
        },
        "VL_BC_ICMS": {
            "titulo": "Valor da base de cálculo do ICMS",
            "valor": vl_bc_icms,
            "valor_formatado": fmt_valor(val_vl_bc_icms)
        },
        "ALIQ_ICMS": {
            "titulo": "Alíquota do ICMS",
            "valor": aliq_icms,
            "valor_formatado": fmt_valor(val_aliq_icms) if aliq_icms else ""
        },
        "VL_ICMS": {
            "titulo": "Valor do ICMS creditado/debitado",
            "valor": vl_icms,
            "valor_formatado": fmt_valor(val_vl_icms)
        },
        "VL_BC_ICMS_ST": {
            "titulo": "Valor da base de cálculo referente à substituição tributária",
            "valor": vl_bc_icms_st,
            "valor_formatado": fmt_valor(val_vl_bc_icms_st)
        },
        "ALIQ_ST": {
            "titulo": "Alíquota do ICMS da substituição tributária na unidade da federação de destino",
            "valor": aliq_st,
            "valor_formatado": fmt_valor(val_aliq_st) if aliq_st else ""
        },
        "VL_ICMS_ST": {
            "titulo": "Valor do ICMS referente à substituição tributária",
            "valor": vl_icms_st,
            "valor_formatado": fmt_valor(val_vl_icms_st)
        },
        "IND_APUR": {
            "titulo": "Indicador de período de apuração do IPI",
            "valor": ind_apur,
            "descricao": descricoes_ind_apur.get(ind_apur, "") if ind_apur else ""
        },
        "CST_IPI": {
            "titulo": "Código da Situação Tributária referente ao IPI, conforme a Tabela indicada no item 4.3.2",
            "valor": cst_ipi
        },
        "COD_ENQ": {
            "titulo": "Código de enquadramento legal do IPI, conforme tabela indicada no item 4.5.3",
            "valor": cod_enq
        },
        "VL_BC_IPI": {
            "titulo": "Valor da base de cálculo do IPI",
            "valor": vl_bc_ipi,
            "valor_formatado": fmt_valor(val_vl_bc_ipi)
        },
        "ALIQ_IPI": {
            "titulo": "Alíquota do IPI",
            "valor": aliq_ipi,
            "valor_formatado": fmt_valor(val_aliq_ipi) if aliq_ipi else ""
        },
        "VL_IPI": {
            "titulo": "Valor do IPI creditado/debitado",
            "valor": vl_ipi,
            "valor_formatado": fmt_valor(val_vl_ipi)
        },
        "CST_PIS": {
            "titulo": "Código da Situação Tributária referente ao PIS",
            "valor": cst_pis
        },
        "VL_BC_PIS": {
            "titulo": "Valor da base de cálculo do PIS/PASEP",
            "valor": vl_bc_pis,
            "valor_formatado": fmt_valor(val_vl_bc_pis)
        },
        "ALIQ_PIS": {
            "titulo": "Alíquota do PIS (em percentual)",
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
        "CST_COFINS": {
            "titulo": "Código da Situação Tributária referente ao COFINS",
            "valor": cst_cofins
        },
        "VL_BC_COFINS": {
            "titulo": "Valor da base de cálculo da COFINS",
            "valor": vl_bc_cofins,
            "valor_formatado": fmt_valor(val_vl_bc_cofins)
        },
        "ALIQ_COFINS": {
            "titulo": "Alíquota da COFINS (em percentual)",
            "valor": aliq_cofins,
            "valor_formatado": fmt_valor_decimais(val_aliq_cofins, 4) if aliq_cofins else ""
        },
        "QUANT_BC_COFINS": {
            "titulo": "Quantidade – Base de cálculo COFINS",
            "valor": quant_bc_cofins,
            "valor_formatado": fmt_valor_decimais(val_quant_bc_cofins, 3) if quant_bc_cofins else ""
        },
        "ALIQ_COFINS_QUANT": {
            "titulo": "Alíquota da COFINS (em reais)",
            "valor": aliq_cofins_quant,
            "valor_formatado": fmt_valor_decimais(val_aliq_cofins_quant, 4) if aliq_cofins_quant else ""
        },
        "VL_COFINS": {
            "titulo": "Valor da COFINS",
            "valor": vl_cofins,
            "valor_formatado": fmt_valor(val_vl_cofins)
        },
        "COD_CTA": {
            "titulo": "Código da conta analítica contábil debitada/creditada",
            "valor": cod_cta
        }
    }
    
    return resultado


def validar_c170(linhas):
    """
    Valida uma ou mais linhas do registro C170 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |C170|NUM_ITEM|COD_ITEM|DESCR_COMPL|QTD|UNID|VL_ITEM|VL_DESC|IND_MOV|CST_ICMS|CFOP|COD_NAT|VL_BC_ICMS|ALIQ_ICMS|VL_ICMS|VL_BC_ICMS_ST|ALIQ_ST|VL_ICMS_ST|IND_APUR|CST_IPI|COD_ENQ|VL_BC_IPI|ALIQ_IPI|VL_IPI|CST_PIS|VL_BC_PIS|ALIQ_PIS|QUANT_BC_PIS|ALIQ_PIS_QUANT|VL_PIS|CST_COFINS|VL_BC_COFINS|ALIQ_COFINS|QUANT_BC_COFINS|ALIQ_COFINS_QUANT|VL_COFINS|COD_CTA|
        
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
        resultado = _processar_linha_c170(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
