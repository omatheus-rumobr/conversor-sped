import re
import json
from datetime import datetime


def _processar_linha_c100(linha):
    """
    Processa uma única linha do registro C100 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |C100|IND_OPER|IND_EMIT|...|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |C100|...|)
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
    if reg != "C100":
        return None
    
    # Função auxiliar para obter campo ou string vazia
    def obter_campo(indice):
        if indice < len(partes):
            valor = partes[indice].strip()
            return valor if valor else ""
        return ""
    
    # Extrai todos os campos (29 campos no total)
    ind_oper = obter_campo(1)
    ind_emit = obter_campo(2)
    cod_part = obter_campo(3)
    cod_mod = obter_campo(4)
    cod_sit = obter_campo(5)
    ser = obter_campo(6)
    num_doc = obter_campo(7)
    chv_nfe = obter_campo(8)
    dt_doc = obter_campo(9)
    dt_e_s = obter_campo(10)
    vl_doc = obter_campo(11)
    ind_pgto = obter_campo(12)
    vl_desc = obter_campo(13)
    vl_abat_nt = obter_campo(14)
    vl_merc = obter_campo(15)
    ind_frt = obter_campo(16)
    vl_frt = obter_campo(17)
    vl_seg = obter_campo(18)
    vl_out_da = obter_campo(19)
    vl_bc_icms = obter_campo(20)
    vl_icms = obter_campo(21)
    vl_bc_icms_st = obter_campo(22)
    vl_icms_st = obter_campo(23)
    vl_ipi = obter_campo(24)
    vl_pis = obter_campo(25)
    vl_cofins = obter_campo(26)
    vl_pis_st = obter_campo(27)
    vl_cofins_st = obter_campo(28)
    
    # Validações básicas dos campos obrigatórios
    # IND_OPER: [0, 1]
    if ind_oper and ind_oper not in ["0", "1"]:
        return None
    
    # IND_EMIT: [0, 1]
    if ind_emit and ind_emit not in ["0", "1"]:
        return None
    
    # Validação: se IND_EMIT = 1, então IND_OPER deve ser 0
    if ind_emit == "1" and ind_oper != "0":
        return None
    
    # COD_MOD: [01, 1B, 04, 55, 65]
    if cod_mod and cod_mod not in ["01", "1B", "04", "55", "65"]:
        return None
    
    # COD_SIT: [00, 01, 02, 03, 04, 05, 06, 07, 08]
    if cod_sit and cod_sit not in ["00", "01", "02", "03", "04", "05", "06", "07", "08"]:
        return None
    
    # Validação: COD_SIT 04 e 05 somente para NF-e ou NFC-e
    if cod_sit in ["04", "05"]:
        if cod_mod not in ["55", "65"]:
            return None
    
    # NUM_DOC: deve ser maior que 0
    if num_doc:
        try:
            if int(num_doc) <= 0:
                return None
        except ValueError:
            return None
    
    # IND_PGTO: [0, 1, 2, 9]
    if ind_pgto and ind_pgto not in ["0", "1", "2", "9"]:
        return None
    
    # IND_FRT: [0, 1, 2, 9] ou [0, 1, 2, 3, 4, 9] a partir de 01/01/2018
    if ind_frt and ind_frt not in ["0", "1", "2", "3", "4", "9"]:
        return None
    
    # Validação de formato de data (ddmmaaaa)
    def validar_data(data_str):
        if not data_str:
            return True  # Campo opcional
        if len(data_str) != 8 or not data_str.isdigit():
            return False
        try:
            dia = int(data_str[0:2])
            mes = int(data_str[2:4])
            ano = int(data_str[4:8])
            datetime(ano, mes, dia)
            return True
        except (ValueError, IndexError):
            return False
    
    # Valida formato das datas
    if dt_doc and not validar_data(dt_doc):
        return None
    if dt_e_s and not validar_data(dt_e_s):
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
    
    # Valida valores monetários
    valores = [vl_doc, vl_desc, vl_abat_nt, vl_merc, vl_frt, vl_seg, vl_out_da,
               vl_bc_icms, vl_icms, vl_bc_icms_st, vl_icms_st, vl_ipi,
               vl_pis, vl_cofins, vl_pis_st, vl_cofins_st]
    for valor in valores:
        if valor and not validar_valor(valor):
            return None
    
    # Monta o dicionário com título e valor
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "IND_OPER": {
            "titulo": "Indicador do Tipo de Operação",
            "valor": ind_oper
        },
        "IND_EMIT": {
            "titulo": "Indicador do Emitente do Documento Fiscal",
            "valor": ind_emit
        },
        "COD_PART": {
            "titulo": "Código do Participante",
            "valor": cod_part
        },
        "COD_MOD": {
            "titulo": "Código do Modelo do Documento Fiscal",
            "valor": cod_mod
        },
        "COD_SIT": {
            "titulo": "Código da Situação do Documento Fiscal",
            "valor": cod_sit
        },
        "SER": {
            "titulo": "Série do Documento Fiscal",
            "valor": ser
        },
        "NUM_DOC": {
            "titulo": "Número do Documento Fiscal",
            "valor": num_doc
        },
        "CHV_NFE": {
            "titulo": "Chave da Nota Fiscal Eletrônica",
            "valor": chv_nfe
        },
        "DT_DOC": {
            "titulo": "Data da Emissão do Documento Fiscal",
            "valor": dt_doc
        },
        "DT_E_S": {
            "titulo": "Data da Entrada ou da Saída",
            "valor": dt_e_s
        },
        "VL_DOC": {
            "titulo": "Valor Total do Documento Fiscal",
            "valor": vl_doc
        },
        "IND_PGTO": {
            "titulo": "Indicador do Tipo de Pagamento",
            "valor": ind_pgto
        },
        "VL_DESC": {
            "titulo": "Valor Total do Desconto",
            "valor": vl_desc
        },
        "VL_ABAT_NT": {
            "titulo": "Abatimento Não Tributado e Não Comercial",
            "valor": vl_abat_nt
        },
        "VL_MERC": {
            "titulo": "Valor Total das Mercadorias e Serviços",
            "valor": vl_merc
        },
        "IND_FRT": {
            "titulo": "Indicador do Tipo do Frete",
            "valor": ind_frt
        },
        "VL_FRT": {
            "titulo": "Valor do Frete",
            "valor": vl_frt
        },
        "VL_SEG": {
            "titulo": "Valor do Seguro",
            "valor": vl_seg
        },
        "VL_OUT_DA": {
            "titulo": "Valor de Outras Despesas Acessórias",
            "valor": vl_out_da
        },
        "VL_BC_ICMS": {
            "titulo": "Valor da Base de Cálculo do ICMS",
            "valor": vl_bc_icms
        },
        "VL_ICMS": {
            "titulo": "Valor do ICMS",
            "valor": vl_icms
        },
        "VL_BC_ICMS_ST": {
            "titulo": "Valor da Base de Cálculo do ICMS Substituição Tributária",
            "valor": vl_bc_icms_st
        },
        "VL_ICMS_ST": {
            "titulo": "Valor do ICMS Retido por Substituição Tributária",
            "valor": vl_icms_st
        },
        "VL_IPI": {
            "titulo": "Valor Total do IPI",
            "valor": vl_ipi
        },
        "VL_PIS": {
            "titulo": "Valor Total do PIS",
            "valor": vl_pis
        },
        "VL_COFINS": {
            "titulo": "Valor Total da COFINS",
            "valor": vl_cofins
        },
        "VL_PIS_ST": {
            "titulo": "Valor Total do PIS Retido por Substituição Tributária",
            "valor": vl_pis_st
        },
        "VL_COFINS_ST": {
            "titulo": "Valor Total da COFINS Retido por Substituição Tributária",
            "valor": vl_cofins_st
        }
    }
    
    return resultado


def validar_c100(linhas):
    """
    Valida e processa uma ou múltiplas linhas do registro C100 (Nota Fiscal) do SPED.
    
    Este registro deve ser gerado para cada documento fiscal código 01, 1B, 04, 55 e 65 (saída),
    registrando a entrada ou saída de produtos ou outras situações que envolvam a emissão 
    dos documentos fiscais mencionados.
    
    Args:
        linhas: Pode ser:
                - Uma string com uma linha do SPED
                - Uma lista de strings (cada string é uma linha)
                - Uma string com múltiplas linhas separadas por \\n
                Formato: |C100|IND_OPER|IND_EMIT|...|
        
    Returns:
        str: JSON com um array contendo os campos validados de cada linha processada.
             Retorna um array vazio [] se nenhuma linha válida for encontrada.
             Retorna None se o input for inválido.
        
    Validações principais:
        - Campo REG deve ser exatamente "C100"
        - IND_OPER: [0, 1]
        - IND_EMIT: [0, 1] e se for 1, IND_OPER deve ser 0
        - COD_MOD: [01, 1B, 04, 55, 65]
        - COD_SIT: [00, 01, 02, 03, 04, 05, 06, 07, 08]
        - NUM_DOC: deve ser maior que 0
        - IND_PGTO: [0, 1, 2, 9]
        - IND_FRT: [0, 1, 2, 9] ou [0, 1, 2, 3, 4, 9] a partir de 01/01/2018
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
        resultado = _processar_linha_c100(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    # Retorna JSON com array de resultados
    return json.dumps(resultados, ensure_ascii=False, indent=2)