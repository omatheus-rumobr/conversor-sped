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


def _validar_chave_nfe(chave_nfe):
    """
    Valida a chave da NF-e (44 dígitos) e o dígito verificador.
    
    Args:
        chave_nfe: String com a chave da NF-e (44 dígitos)
        
    Returns:
        bool: True se válida, False caso contrário
    """
    if not chave_nfe or len(chave_nfe) != 44 or not chave_nfe.isdigit():
        return False
    
    # Extrai os 43 primeiros dígitos e o dígito verificador (último dígito)
    chave_43 = chave_nfe[:43]
    dv_informado = int(chave_nfe[43])
    
    # Calcula o dígito verificador usando módulo 11
    soma = 0
    multiplicador = 2
    
    # Percorre os 43 dígitos de trás para frente
    for i in range(42, -1, -1):
        soma += int(chave_43[i]) * multiplicador
        multiplicador += 1
        if multiplicador > 9:
            multiplicador = 2
    
    # Calcula o resto da divisão por 11
    resto = soma % 11
    
    # Se o resto for 0 ou 1, o dígito verificador é 0
    # Caso contrário, é 11 - resto
    if resto < 2:
        dv_calculado = 0
    else:
        dv_calculado = 11 - resto
    
    return dv_calculado == dv_informado


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


def _processar_linha_c100(linha):
    """
    Processa uma única linha do registro C100 e retorna um dicionário.
    
    Formato:
      |C100|IND_OPER|IND_EMIT|COD_PART|COD_MOD|COD_SIT|SER|NUM_DOC|CHV_NFE|DT_DOC|DT_E_S|VL_DOC|IND_PGTO|VL_DESC|VL_ABAT_NT|VL_MERC|IND_FRT|VL_FRT|VL_SEG|VL_OUT_DA|VL_BC_ICMS|VL_ICMS|VL_BC_ICMS_ST|VL_ICMS_ST|VL_IPI|VL_PIS|VL_COFINS|VL_PIS_ST|VL_COFINS_ST|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "C100"
    - IND_OPER: obrigatório, indicador do tipo de operação (1 dígito)
      - Valores válidos: [0, 1]
      - 0: Entrada
      - 1: Saída
    - IND_EMIT: obrigatório, indicador do emitente do documento fiscal (1 dígito)
      - Valores válidos: [0, 1]
      - 0: Emissão própria
      - 1: Terceiros
      - Validação: se IND_EMIT = 1, então IND_OPER deve ser 0 (validação em camada superior)
    - COD_PART: obrigatório, código do participante (60 caracteres)
      - Validação: deve existir no campo COD_PART do registro 0150 (validação em camada superior)
    - COD_MOD: obrigatório, código do modelo do documento fiscal (2 caracteres)
      - Valores válidos: [01, 1B, 04, 55, 65]
    - COD_SIT: obrigatório, código da situação do documento fiscal (2 dígitos)
      - Valores válidos: [00, 01, 02, 03, 04, 05, 06, 07, 08]
      - Valores 04 e 05 só são possíveis para NF-e de emissão própria
    - SER: opcional, série do documento fiscal (3 caracteres)
      - Obrigatório com 3 posições para NF-e (COD_MOD = 55) e NFC-e (COD_MOD = 65)
      - Se não existir série para NF-e ou NFC-e, informar 000
    - NUM_DOC: obrigatório, número do documento fiscal (9 dígitos)
      - Deve ser maior que 0
    - CHV_NFE: opcional, chave da Nota Fiscal Eletrônica ou da NFC-e (44 dígitos)
      - Obrigatório para COD_MOD = 55 ou 65 quando IND_EMIT = 0
      - Validação do dígito verificador quando preenchido
    - DT_DOC: obrigatório, data de emissão do documento fiscal (ddmmaaaa)
    - DT_E_S: opcional, data de entrada ou saída (ddmmaaaa)
      - Obrigatório para operações de entrada
      - Deve ser >= DT_DOC
    - VL_DOC: obrigatório, valor total do documento fiscal (numérico, 2 decimais)
    - IND_PGTO: obrigatório, indicador do tipo de pagamento (1 dígito)
      - Valores válidos: [0, 1, 9] (ou [0, 1, 2] a partir de 01/07/2012)
      - 0: À vista
      - 1: A prazo
      - 9: Sem pagamento (ou 2: Outros a partir de 01/07/2012)
    - VL_DESC: opcional, valor total do desconto (numérico, 2 decimais)
    - VL_ABAT_NT: opcional, abatimento não tributado e não comercial (numérico, 2 decimais)
    - VL_MERC: opcional, valor total das mercadorias e serviços (numérico, 2 decimais)
    - IND_FRT: obrigatório, indicador do tipo de frete/transporte (1 dígito)
      - Valores válidos: [0, 1, 2, 3, 4, 9] (varia conforme período)
      - 0: Frete por conta do remetente (CIF) - a partir de 01/10/2017
      - 1: Frete por conta do destinatário (FOB) - a partir de 01/10/2017
      - 2: Frete por conta de terceiros
      - 3: Transporte próprio por conta do remetente - a partir de 01/10/2017
      - 4: Transporte próprio por conta do destinatário - a partir de 01/10/2017
      - 9: Sem ocorrência de transporte - a partir de 01/10/2017
    - VL_FRT: opcional, valor do frete indicado no documento fiscal (numérico, 2 decimais)
    - VL_SEG: opcional, valor do seguro indicado no documento fiscal (numérico, 2 decimais)
    - VL_OUT_DA: opcional, valor de outras despesas acessórias (numérico, 2 decimais)
    - VL_BC_ICMS: opcional, valor da base de cálculo do ICMS (numérico, 2 decimais)
    - VL_ICMS: opcional, valor do ICMS (numérico, 2 decimais)
    - VL_BC_ICMS_ST: opcional, valor da base de cálculo do ICMS substituição tributária (numérico, 2 decimais)
    - VL_ICMS_ST: opcional, valor do ICMS retido por substituição tributária (numérico, 2 decimais)
    - VL_IPI: opcional, valor total do IPI (numérico, 2 decimais)
    - VL_PIS: opcional, valor total do PIS (numérico, 2 decimais)
    - VL_COFINS: opcional, valor total da COFINS (numérico, 2 decimais)
    - VL_PIS_ST: opcional, valor total do PIS retido por substituição tributária (numérico, 2 decimais)
    - VL_COFINS_ST: opcional, valor total da COFINS retida por substituição tributária (numérico, 2 decimais)
    
    Nota: Registro com estrutura, campos e conteúdo definidos e constantes no Leiaute da Escrituração Fiscal Digital – EFD (ICMS e IPI).
    Este registro deve ser gerado para cada documento fiscal código 01, 1B, 04, 55 e 65 (NFC-e), registrando a entrada ou saída de produtos
    ou outras situações que envolvam a emissão dos documentos fiscais mencionados.
    
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
    # Remove primeiro e último se vazios (formato padrão SPED: |C100|...|)
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
    if reg != "C100":
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
    
    # IND_OPER: obrigatório, valores válidos [0, 1]
    ind_oper_validos = ["0", "1"]
    if not ind_oper or ind_oper not in ind_oper_validos:
        return None
    
    # IND_EMIT: obrigatório, valores válidos [0, 1]
    ind_emit_validos = ["0", "1"]
    if not ind_emit or ind_emit not in ind_emit_validos:
        return None
    
    # COD_PART: obrigatório, código do participante (60 caracteres)
    if not cod_part or len(cod_part) > 60:
        return None
    
    # COD_MOD: obrigatório, valores válidos [01, 1B, 04, 55, 65]
    cod_mod_validos = ["01", "1B", "04", "55", "65"]
    if not cod_mod or cod_mod not in cod_mod_validos:
        return None
    
    # COD_SIT: obrigatório, valores válidos [00, 01, 02, 03, 04, 05, 06, 07, 08]
    cod_sit_validos = ["00", "01", "02", "03", "04", "05", "06", "07", "08"]
    if not cod_sit or cod_sit not in cod_sit_validos:
        return None
    
    # Validação: valores 04 e 05 só são possíveis para NF-e de emissão própria
    if cod_sit in ["04", "05"] and ind_emit != "0":
        return None
    
    # SER: opcional, série do documento fiscal (3 caracteres)
    # Obrigatório com 3 posições para NF-e (COD_MOD = 55) e NFC-e (COD_MOD = 65)
    if cod_mod in ["55", "65"]:
        if not ser or len(ser) != 3:
            return None
    elif ser and len(ser) > 3:
        return None
    
    # NUM_DOC: obrigatório, número do documento fiscal (9 dígitos, maior que 0)
    if not num_doc or not num_doc.isdigit() or len(num_doc) > 9:
        return None
    try:
        num_doc_int = int(num_doc)
        if num_doc_int <= 0:
            return None
    except ValueError:
        return None
    
    # CHV_NFE: opcional, chave da NF-e (44 dígitos)
    # Obrigatório para COD_MOD = 55 ou 65 quando IND_EMIT = 0
    if cod_mod in ["55", "65"] and ind_emit == "0":
        if not chv_nfe:
            return None
        if not _validar_chave_nfe(chv_nfe):
            return None
    elif chv_nfe:
        # Se preenchido, deve ser válido
        if not _validar_chave_nfe(chv_nfe):
            return None
    
    # DT_DOC: obrigatório, data de emissão (ddmmaaaa)
    ok_dt_doc, dt_doc_obj = _validar_data(dt_doc)
    if not ok_dt_doc:
        return None
    
    # DT_E_S: opcional, data de entrada/saída (ddmmaaaa)
    # Obrigatório para operações de entrada
    if ind_oper == "0":  # Entrada
        ok_dt_e_s, dt_e_s_obj = _validar_data(dt_e_s)
        if not ok_dt_e_s:
            return None
        # Deve ser >= DT_DOC
        if dt_e_s_obj < dt_doc_obj:
            return None
    elif dt_e_s:
        # Se preenchido, deve ser válido e >= DT_DOC
        ok_dt_e_s, dt_e_s_obj = _validar_data(dt_e_s)
        if not ok_dt_e_s:
            return None
        if dt_e_s_obj < dt_doc_obj:
            return None
    else:
        dt_e_s_obj = None
    
    # VL_DOC: obrigatório, valor total do documento (numérico, 2 decimais)
    ok_vl_doc, val_vl_doc, _ = validar_valor_numerico(vl_doc, decimais=2, obrigatorio=True, positivo=True)
    if not ok_vl_doc:
        return None
    
    # IND_PGTO: obrigatório, valores válidos [0, 1, 9] (ou [0, 1, 2] a partir de 01/07/2012)
    ind_pgto_validos = ["0", "1", "9", "2"]
    if not ind_pgto or ind_pgto not in ind_pgto_validos:
        return None
    
    # VL_DESC: opcional, valor total do desconto (numérico, 2 decimais)
    ok_vl_desc, val_vl_desc, _ = validar_valor_numerico(vl_desc, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok_vl_desc:
        return None
    
    # VL_ABAT_NT: opcional, abatimento não tributado (numérico, 2 decimais)
    ok_vl_abat_nt, val_vl_abat_nt, _ = validar_valor_numerico(vl_abat_nt, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok_vl_abat_nt:
        return None
    
    # VL_MERC: opcional, valor total das mercadorias (numérico, 2 decimais)
    ok_vl_merc, val_vl_merc, _ = validar_valor_numerico(vl_merc, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok_vl_merc:
        return None
    
    # IND_FRT: obrigatório, valores válidos [0, 1, 2, 3, 4, 9]
    ind_frt_validos = ["0", "1", "2", "3", "4", "9"]
    if not ind_frt or ind_frt not in ind_frt_validos:
        return None
    
    # VL_FRT: opcional, valor do frete (numérico, 2 decimais)
    ok_vl_frt, val_vl_frt, _ = validar_valor_numerico(vl_frt, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok_vl_frt:
        return None
    
    # VL_SEG: opcional, valor do seguro (numérico, 2 decimais)
    ok_vl_seg, val_vl_seg, _ = validar_valor_numerico(vl_seg, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok_vl_seg:
        return None
    
    # VL_OUT_DA: opcional, outras despesas acessórias (numérico, 2 decimais)
    ok_vl_out_da, val_vl_out_da, _ = validar_valor_numerico(vl_out_da, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok_vl_out_da:
        return None
    
    # VL_BC_ICMS: opcional, base de cálculo do ICMS (numérico, 2 decimais)
    ok_vl_bc_icms, val_vl_bc_icms, _ = validar_valor_numerico(vl_bc_icms, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok_vl_bc_icms:
        return None
    
    # VL_ICMS: opcional, valor do ICMS (numérico, 2 decimais)
    ok_vl_icms, val_vl_icms, _ = validar_valor_numerico(vl_icms, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok_vl_icms:
        return None
    
    # VL_BC_ICMS_ST: opcional, base de cálculo do ICMS ST (numérico, 2 decimais)
    ok_vl_bc_icms_st, val_vl_bc_icms_st, _ = validar_valor_numerico(vl_bc_icms_st, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok_vl_bc_icms_st:
        return None
    
    # VL_ICMS_ST: opcional, valor do ICMS ST (numérico, 2 decimais)
    ok_vl_icms_st, val_vl_icms_st, _ = validar_valor_numerico(vl_icms_st, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok_vl_icms_st:
        return None
    
    # VL_IPI: opcional, valor total do IPI (numérico, 2 decimais)
    ok_vl_ipi, val_vl_ipi, _ = validar_valor_numerico(vl_ipi, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok_vl_ipi:
        return None
    
    # VL_PIS: opcional, valor total do PIS (numérico, 2 decimais)
    ok_vl_pis, val_vl_pis, _ = validar_valor_numerico(vl_pis, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok_vl_pis:
        return None
    
    # VL_COFINS: opcional, valor total da COFINS (numérico, 2 decimais)
    ok_vl_cofins, val_vl_cofins, _ = validar_valor_numerico(vl_cofins, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok_vl_cofins:
        return None
    
    # VL_PIS_ST: opcional, valor total do PIS ST (numérico, 2 decimais)
    ok_vl_pis_st, val_vl_pis_st, _ = validar_valor_numerico(vl_pis_st, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok_vl_pis_st:
        return None
    
    # VL_COFINS_ST: opcional, valor total da COFINS ST (numérico, 2 decimais)
    ok_vl_cofins_st, val_vl_cofins_st, _ = validar_valor_numerico(vl_cofins_st, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok_vl_cofins_st:
        return None
    
    # Função auxiliar para formatar valores monetários
    def fmt_valor(v):
        if v is None:
            return ""
        return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    # Função auxiliar para formatar data
    def fmt_data(data_str):
        if not data_str or len(data_str) != 8:
            return ""
        return f"{data_str[:2]}/{data_str[2:4]}/{data_str[4:]}"
    
    # Descrições dos campos
    descricoes_ind_oper = {
        "0": "Entrada",
        "1": "Saída"
    }
    
    descricoes_ind_emit = {
        "0": "Emissão própria",
        "1": "Terceiros"
    }
    
    descricoes_ind_pgto = {
        "0": "À vista",
        "1": "A prazo",
        "9": "Sem pagamento",
        "2": "Outros"
    }
    
    descricoes_ind_frt = {
        "0": "Frete por conta do remetente (CIF)",
        "1": "Frete por conta do destinatário (FOB)",
        "2": "Frete por conta de terceiros",
        "3": "Transporte próprio por conta do remetente",
        "4": "Transporte próprio por conta do destinatário",
        "9": "Sem ocorrência de transporte"
    }
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "IND_OPER": {
            "titulo": "Indicador do tipo de operação",
            "valor": ind_oper,
            "descricao": descricoes_ind_oper.get(ind_oper, "")
        },
        "IND_EMIT": {
            "titulo": "Indicador do emitente do documento fiscal",
            "valor": ind_emit,
            "descricao": descricoes_ind_emit.get(ind_emit, "")
        },
        "COD_PART": {
            "titulo": "Código do participante (campo 02 do Registro 0150)",
            "valor": cod_part
        },
        "COD_MOD": {
            "titulo": "Código do modelo do documento fiscal, conforme a Tabela 4.1.1",
            "valor": cod_mod
        },
        "COD_SIT": {
            "titulo": "Código da situação do documento fiscal, conforme a Tabela 4.1.2",
            "valor": cod_sit
        },
        "SER": {
            "titulo": "Série do documento fiscal",
            "valor": ser
        },
        "NUM_DOC": {
            "titulo": "Número do documento fiscal",
            "valor": num_doc
        },
        "CHV_NFE": {
            "titulo": "Chave da Nota Fiscal Eletrônica ou da NFC-e",
            "valor": chv_nfe
        },
        "DT_DOC": {
            "titulo": "Data da emissão do documento fiscal",
            "valor": dt_doc,
            "valor_formatado": fmt_data(dt_doc)
        },
        "DT_E_S": {
            "titulo": "Data da entrada ou da saída",
            "valor": dt_e_s,
            "valor_formatado": fmt_data(dt_e_s) if dt_e_s else ""
        },
        "VL_DOC": {
            "titulo": "Valor total do documento fiscal",
            "valor": vl_doc,
            "valor_formatado": fmt_valor(val_vl_doc)
        },
        "IND_PGTO": {
            "titulo": "Indicador do tipo de pagamento",
            "valor": ind_pgto,
            "descricao": descricoes_ind_pgto.get(ind_pgto, "")
        },
        "VL_DESC": {
            "titulo": "Valor total do desconto",
            "valor": vl_desc,
            "valor_formatado": fmt_valor(val_vl_desc)
        },
        "VL_ABAT_NT": {
            "titulo": "Abatimento não tributado e não comercial",
            "valor": vl_abat_nt,
            "valor_formatado": fmt_valor(val_vl_abat_nt)
        },
        "VL_MERC": {
            "titulo": "Valor total das mercadorias e serviços",
            "valor": vl_merc,
            "valor_formatado": fmt_valor(val_vl_merc)
        },
        "IND_FRT": {
            "titulo": "Indicador do tipo de frete/transporte",
            "valor": ind_frt,
            "descricao": descricoes_ind_frt.get(ind_frt, "")
        },
        "VL_FRT": {
            "titulo": "Valor do frete indicado no documento fiscal",
            "valor": vl_frt,
            "valor_formatado": fmt_valor(val_vl_frt)
        },
        "VL_SEG": {
            "titulo": "Valor do seguro indicado no documento fiscal",
            "valor": vl_seg,
            "valor_formatado": fmt_valor(val_vl_seg)
        },
        "VL_OUT_DA": {
            "titulo": "Valor de outras despesas acessórias",
            "valor": vl_out_da,
            "valor_formatado": fmt_valor(val_vl_out_da)
        },
        "VL_BC_ICMS": {
            "titulo": "Valor da base de cálculo do ICMS",
            "valor": vl_bc_icms,
            "valor_formatado": fmt_valor(val_vl_bc_icms)
        },
        "VL_ICMS": {
            "titulo": "Valor do ICMS",
            "valor": vl_icms,
            "valor_formatado": fmt_valor(val_vl_icms)
        },
        "VL_BC_ICMS_ST": {
            "titulo": "Valor da base de cálculo do ICMS substituição tributária",
            "valor": vl_bc_icms_st,
            "valor_formatado": fmt_valor(val_vl_bc_icms_st)
        },
        "VL_ICMS_ST": {
            "titulo": "Valor do ICMS retido por substituição tributária",
            "valor": vl_icms_st,
            "valor_formatado": fmt_valor(val_vl_icms_st)
        },
        "VL_IPI": {
            "titulo": "Valor total do IPI",
            "valor": vl_ipi,
            "valor_formatado": fmt_valor(val_vl_ipi)
        },
        "VL_PIS": {
            "titulo": "Valor total do PIS",
            "valor": vl_pis,
            "valor_formatado": fmt_valor(val_vl_pis)
        },
        "VL_COFINS": {
            "titulo": "Valor total da COFINS",
            "valor": vl_cofins,
            "valor_formatado": fmt_valor(val_vl_cofins)
        },
        "VL_PIS_ST": {
            "titulo": "Valor total do PIS retido por substituição tributária",
            "valor": vl_pis_st,
            "valor_formatado": fmt_valor(val_vl_pis_st)
        },
        "VL_COFINS_ST": {
            "titulo": "Valor total da COFINS retida por substituição tributária",
            "valor": vl_cofins_st,
            "valor_formatado": fmt_valor(val_vl_cofins_st)
        }
    }
    
    return resultado


def validar_c100(linhas):
    """
    Valida uma ou mais linhas do registro C100 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |C100|IND_OPER|IND_EMIT|COD_PART|COD_MOD|COD_SIT|SER|NUM_DOC|CHV_NFE|DT_DOC|DT_E_S|VL_DOC|IND_PGTO|VL_DESC|VL_ABAT_NT|VL_MERC|IND_FRT|VL_FRT|VL_SEG|VL_OUT_DA|VL_BC_ICMS|VL_ICMS|VL_BC_ICMS_ST|VL_ICMS_ST|VL_IPI|VL_PIS|VL_COFINS|VL_PIS_ST|VL_COFINS_ST|
        
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
        resultado = _processar_linha_c100(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
