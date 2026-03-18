import re
import json
from datetime import datetime


def _processar_linha_c170(linha):
    """
    Processa uma única linha do registro C170 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |C170|NUM_ITEM|COD_ITEM|...| (38 campos)
        
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
    reg = partes[0].strip().upper() if partes else ""
    
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
    
    # Extrai todos os campos (38 campos no total)
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
    aliq_pis_reais = obter_campo(28)
    vl_pis = obter_campo(29)
    cst_cofins = obter_campo(30)
    vl_bc_cofins = obter_campo(31)
    aliq_cofins = obter_campo(32)
    quant_bc_cofins = obter_campo(33)
    aliq_cofins_reais = obter_campo(34)
    vl_cofins = obter_campo(35)
    cod_cta = obter_campo(36)
    vl_abat_nt = obter_campo(37)
    
    # Validações básicas dos campos obrigatórios
    # NUM_ITEM: obrigatório, numérico
    if not num_item:
        return None
    try:
        int(num_item)
    except ValueError:
        return None
    
    # COD_ITEM: obrigatório
    if not cod_item:
        return None
    
    # QTD: obrigatório, numérico, maior que 0 (exceto para COD_SIT 6 ou 7)
    if not qtd:
        return None
    try:
        qtd_float = float(qtd.replace(",", "."))
        if qtd_float < 0:
            return None
        # Para COD_SIT 6 ou 7, pode ser 0, mas isso seria validado no C100
        # Por padrão, deve ser maior que 0
        if qtd_float == 0:
            # Aceita 0, mas pode ser validado posteriormente
            pass
    except ValueError:
        return None
    
    # UNID: obrigatório
    if not unid:
        return None
    
    # VL_ITEM: obrigatório, numérico
    if not vl_item:
        return None
    try:
        float(vl_item.replace(",", "."))
    except ValueError:
        return None
    
    # IND_MOV: obrigatório, valores válidos [0, 1]
    if not ind_mov or ind_mov not in ["0", "1"]:
        return None
    
    # CST_ICMS: obrigatório, numérico de 3 dígitos
    if not cst_icms:
        return None
    try:
        int(cst_icms)
        if len(cst_icms) > 3:
            return None
    except ValueError:
        return None
    
    # CFOP: obrigatório, numérico de 4 dígitos
    if not cfop:
        return None
    try:
        int(cfop)
        if len(cfop) != 4:
            return None
    except ValueError:
        return None
    
    # Validação de valores numéricos (devem ser números válidos se preenchidos)
    def validar_valor(valor_str):
        if not valor_str:
            return True  # Campo opcional
        try:
            float(valor_str.replace(",", "."))
            return True
        except ValueError:
            return False
    
    # Valida valores monetários opcionais
    valores_monetarios = [vl_desc, vl_bc_icms, vl_icms, vl_bc_icms_st, vl_icms_st,
                          vl_bc_ipi, vl_ipi, vl_bc_pis, vl_pis, vl_bc_cofins, vl_cofins,
                          vl_abat_nt]
    for valor in valores_monetarios:
        if valor and not validar_valor(valor):
            return None
    
    # Valida alíquotas (podem ter mais casas decimais)
    aliqs = [aliq_icms, aliq_st, aliq_ipi, aliq_pis, aliq_pis_reais, aliq_cofins, aliq_cofins_reais]
    for aliq in aliqs:
        if aliq and not validar_valor(aliq):
            return None
    
    # Valida quantidades
    quantidades = [quant_bc_pis, quant_bc_cofins]
    for quant in quantidades:
        if quant and not validar_valor(quant):
            return None
    
    # IND_APUR: se preenchido, valores válidos [0, 1]
    if ind_apur and ind_apur not in ["0", "1"]:
        return None
    
    # Monta o dicionário com título e valor
    descricoes_ind_mov = {
        "0": "SIM",
        "1": "NÃO"
    }
    
    descricoes_ind_apur = {
        "0": "Mensal",
        "1": "Decendial"
    }
    
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "NUM_ITEM": {
            "titulo": "Número Sequencial do Item no Documento Fiscal",
            "valor": num_item
        },
        "COD_ITEM": {
            "titulo": "Código do Item",
            "valor": cod_item
        },
        "DESCR_COMPL": {
            "titulo": "Descrição Complementar do Item",
            "valor": descr_compl
        },
        "QTD": {
            "titulo": "Quantidade do Item",
            "valor": qtd
        },
        "UNID": {
            "titulo": "Unidade do Item",
            "valor": unid
        },
        "VL_ITEM": {
            "titulo": "Valor Total do Item (Mercadorias ou Serviços)",
            "valor": vl_item
        },
        "VL_DESC": {
            "titulo": "Valor do Desconto Comercial",
            "valor": vl_desc
        },
        "IND_MOV": {
            "titulo": "Movimentação Física do ITEM/PRODUTO",
            "valor": ind_mov,
            "descricao": descricoes_ind_mov.get(ind_mov, "")
        },
        "CST_ICMS": {
            "titulo": "Código da Situação Tributária referente ao ICMS",
            "valor": cst_icms
        },
        "CFOP": {
            "titulo": "Código Fiscal de Operação e Prestação",
            "valor": cfop
        },
        "COD_NAT": {
            "titulo": "Código da Natureza da Operação",
            "valor": cod_nat
        },
        "VL_BC_ICMS": {
            "titulo": "Valor da Base de Cálculo do ICMS",
            "valor": vl_bc_icms
        },
        "ALIQ_ICMS": {
            "titulo": "Alíquota do ICMS",
            "valor": aliq_icms
        },
        "VL_ICMS": {
            "titulo": "Valor do ICMS Creditado/Debitado",
            "valor": vl_icms
        },
        "VL_BC_ICMS_ST": {
            "titulo": "Valor da Base de Cálculo referente à Substituição Tributária",
            "valor": vl_bc_icms_st
        },
        "ALIQ_ST": {
            "titulo": "Alíquota do ICMS da Substituição Tributária na UF de Destino",
            "valor": aliq_st
        },
        "VL_ICMS_ST": {
            "titulo": "Valor do ICMS referente à Substituição Tributária",
            "valor": vl_icms_st
        },
        "IND_APUR": {
            "titulo": "Indicador de Período de Apuração do IPI",
            "valor": ind_apur,
            "descricao": descricoes_ind_apur.get(ind_apur, "") if ind_apur else ""
        },
        "CST_IPI": {
            "titulo": "Código da Situação Tributária referente ao IPI",
            "valor": cst_ipi
        },
        "COD_ENQ": {
            "titulo": "Código de Enquadramento Legal do IPI",
            "valor": cod_enq
        },
        "VL_BC_IPI": {
            "titulo": "Valor da Base de Cálculo do IPI",
            "valor": vl_bc_ipi
        },
        "ALIQ_IPI": {
            "titulo": "Alíquota do IPI",
            "valor": aliq_ipi
        },
        "VL_IPI": {
            "titulo": "Valor do IPI Creditado/Debitado",
            "valor": vl_ipi
        },
        "CST_PIS": {
            "titulo": "Código da Situação Tributária referente ao PIS",
            "valor": cst_pis
        },
        "VL_BC_PIS": {
            "titulo": "Valor da Base de Cálculo do PIS",
            "valor": vl_bc_pis
        },
        "ALIQ_PIS": {
            "titulo": "Alíquota do PIS (em percentual)",
            "valor": aliq_pis
        },
        "QUANT_BC_PIS": {
            "titulo": "Quantidade – Base de Cálculo PIS",
            "valor": quant_bc_pis
        },
        "ALIQ_PIS_REAIS": {
            "titulo": "Alíquota do PIS (em reais)",
            "valor": aliq_pis_reais
        },
        "VL_PIS": {
            "titulo": "Valor do PIS",
            "valor": vl_pis
        },
        "CST_COFINS": {
            "titulo": "Código da Situação Tributária referente ao COFINS",
            "valor": cst_cofins
        },
        "VL_BC_COFINS": {
            "titulo": "Valor da Base de Cálculo da COFINS",
            "valor": vl_bc_cofins
        },
        "ALIQ_COFINS": {
            "titulo": "Alíquota do COFINS (em percentual)",
            "valor": aliq_cofins
        },
        "QUANT_BC_COFINS": {
            "titulo": "Quantidade – Base de Cálculo COFINS",
            "valor": quant_bc_cofins
        },
        "ALIQ_COFINS_REAIS": {
            "titulo": "Alíquota da COFINS (em reais)",
            "valor": aliq_cofins_reais
        },
        "VL_COFINS": {
            "titulo": "Valor da COFINS",
            "valor": vl_cofins
        },
        "COD_CTA": {
            "titulo": "Código da Conta Analítica Contábil Debitada/Creditada",
            "valor": cod_cta
        },
        "VL_ABAT_NT": {
            "titulo": "Valor do Abatimento Não Tributado e Não Comercial",
            "valor": vl_abat_nt
        }
    }
    
    return resultado


def validar_c170_fiscal(linhas):
    """
    Valida e processa uma ou múltiplas linhas do registro C170 (Itens do Documento) do SPED.
    
    Registro obrigatório para discriminar os itens da nota fiscal (mercadorias e/ou serviços constantes em notas
    conjugadas), inclusive em operações de entrada de mercadorias acompanhadas de Nota Fiscal Eletrônica (NF-e) de emissão de
    terceiros.
    
    Args:
        linhas: Pode ser:
                - Uma string com uma linha do SPED
                - Uma lista de strings (cada string é uma linha)
                - Uma string com múltiplas linhas separadas por \\n
                Formato: |C170|NUM_ITEM|COD_ITEM|DESCR_COMPL|QTD|UNID|VL_ITEM|...| (38 campos)
        
    Returns:
        str: JSON com um array contendo os campos validados de cada linha processada.
             Retorna um array vazio [] se nenhuma linha válida for encontrada.
             Retorna None se o input for inválido.
        
    Validações principais:
        - Campo REG deve ser exatamente "C170"
        - NUM_ITEM: obrigatório, numérico
        - COD_ITEM: obrigatório
        - QTD: obrigatório, numérico, maior ou igual a 0
        - UNID: obrigatório
        - VL_ITEM: obrigatório, numérico
        - IND_MOV: obrigatório, valores válidos [0, 1]
        - CST_ICMS: obrigatório, código de situação tributária
        - CFOP: obrigatório, código fiscal de operação (4 dígitos)
        - Demais campos: opcionais, mas validados quando preenchidos
    """
    if linhas is None:
        return None
    
    # Lista para armazenar as linhas a processar
    linhas_para_processar = []
    
    # Se for uma lista, processa cada item
    if isinstance(linhas, list):
        linhas_para_processar = linhas
    # Se for uma string, verifica se tem múltiplas linhas
    elif isinstance(linhas, str):
        # Se contém \n, divide em linhas
        if '\n' in linhas:
            linhas_para_processar = linhas.split('\n')
        else:
            # String única
            linhas_para_processar = [linhas]
    else:
        return None
    
    # Lista para armazenar os resultados válidos
    resultados = []
    
    # Processa cada linha
    for linha in linhas_para_processar:
        resultado = _processar_linha_c170(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    # Retorna JSON com array de resultados
    return json.dumps(resultados, ensure_ascii=False, indent=2)