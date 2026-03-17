import re
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
    if not valor_str:
        if obrigatorio:
            return False, None, f"Campo obrigatório não preenchido"
        return True, 0.0, None
    
    try:
        valor_float = float(valor_str)
        
        # Verifica precisão decimal
        partes_decimal = valor_str.split('.')
        if len(partes_decimal) == 2 and len(partes_decimal[1]) > decimais:
            return False, None, f"Valor com mais de {decimais} casas decimais"
        
        # Validações de sinal
        if positivo and valor_float <= 0:
            return False, None, "Valor deve ser maior que zero"
        if nao_negativo and valor_float < 0:
            return False, None, "Valor não pode ser negativo"
        
        return True, valor_float, None
    except ValueError:
        return False, None, "Valor não é numérico válido"


def _processar_linha_1500(linha):
    """
    Processa uma única linha do registro 1500 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |1500|IND_OPER|IND_EMIT|COD_PART|...|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |1500|...|)
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
    if reg != "1500":
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
    
    # Extrai todos os campos (27 campos no total)
    ind_oper = obter_campo(1)
    ind_emit = obter_campo(2)
    cod_part = obter_campo(3)
    cod_mod = obter_campo(4)
    cod_sit = obter_campo(5)
    ser = obter_campo(6)
    sub = obter_campo(7)
    cod_cons = obter_campo(8)
    num_doc = obter_campo(9)
    dt_doc = obter_campo(10)
    dt_e_s = obter_campo(11)
    vl_doc = obter_campo(12)
    vl_desc = obter_campo(13)
    vl_forn = obter_campo(14)
    vl_serv_nt = obter_campo(15)
    vl_terc = obter_campo(16)
    vl_da = obter_campo(17)
    vl_bc_icms = obter_campo(18)
    vl_icms = obter_campo(19)
    vl_bc_icms_st = obter_campo(20)
    vl_icms_st = obter_campo(21)
    cod_inf = obter_campo(22)
    vl_pis = obter_campo(23)
    vl_cofins = obter_campo(24)
    tp_ligacao = obter_campo(25)
    cod_grupo_tensao = obter_campo(26)
    
    # Validações dos campos obrigatórios
    
    # IND_OPER: obrigatório, valores válidos: [1]
    if ind_oper != "1":
        return None
    
    # IND_EMIT: obrigatório, valores válidos: [0]
    if ind_emit != "0":
        return None
    
    # COD_PART: obrigatório, até 60 caracteres
    if not cod_part or len(cod_part) > 60:
        return None
    
    # COD_MOD: obrigatório, valores válidos: [06]
    if cod_mod != "06":
        return None
    
    # COD_SIT: obrigatório, valores válidos: [00, 01, 06, 07, 08]
    cod_sit_validos = ["00", "01", "06", "07", "08"]
    if cod_sit not in cod_sit_validos:
        return None
    
    # Verifica se é exceção (COD_SIT = "06", "07" ou "08")
    # Nestes casos, apenas alguns campos são obrigatórios
    is_excecao = cod_sit in ["06", "07", "08"]
    
    # SER: obrigatório condicional (exceto em exceções)
    if not is_excecao and not ser:
        return None
    if ser and len(ser) > 4:
        return None
    
    # SUB: obrigatório condicional (exceto em exceções), numérico até 3 dígitos
    if not is_excecao and not sub:
        return None
    if sub:
        if not sub.isdigit() or len(sub) > 3:
            return None
    
    # COD_CONS: obrigatório (exceto em exceções), valores válidos: [01, 02, 03, 04, 05, 06, 07, 08]
    if not is_excecao:
        cod_cons_validos = ["01", "02", "03", "04", "05", "06", "07", "08"]
        if not cod_cons or cod_cons not in cod_cons_validos:
            return None
    else:
        # Em exceções, COD_CONS é opcional, mas se preenchido deve ser válido
        if cod_cons:
            cod_cons_validos = ["01", "02", "03", "04", "05", "06", "07", "08"]
            if cod_cons not in cod_cons_validos:
                return None
    
    # NUM_DOC: obrigatório, numérico, maior que 0
    if not num_doc:
        return None
    try:
        num_doc_int = int(num_doc)
        if num_doc_int <= 0:
            return None
    except ValueError:
        return None
    
    # DT_DOC: obrigatório, formato DDMMAAAA
    if not dt_doc:
        return None
    dt_doc_valida, dt_doc_obj = _validar_data(dt_doc)
    if not dt_doc_valida:
        return None
    
    # DT_E_S: obrigatório (exceto em exceções), formato DDMMAAAA
    if not is_excecao:
        if not dt_e_s:
            return None
        dt_e_s_valida, dt_e_s_obj = _validar_data(dt_e_s)
        if not dt_e_s_valida:
            return None
    else:
        # Em exceções, DT_E_S é opcional, mas se preenchido deve ser válido
        if dt_e_s:
            dt_e_s_valida, dt_e_s_obj = _validar_data(dt_e_s)
            if not dt_e_s_valida:
                return None
    
    # VL_DOC: obrigatório (exceto em exceções), numérico com 2 decimais, maior que 0
    if not is_excecao:
        if not vl_doc:
            return None
        vl_doc_valido, vl_doc_float, vl_doc_erro = validar_valor_numerico(vl_doc, decimais=2, obrigatorio=True, positivo=True)
        if not vl_doc_valido:
            return None
    else:
        # Em exceções, VL_DOC é opcional, mas se preenchido deve ser válido
        if vl_doc:
            vl_doc_valido, vl_doc_float, vl_doc_erro = validar_valor_numerico(vl_doc, decimais=2, positivo=True)
            if not vl_doc_valido:
                return None
    
    # VL_DESC: obrigatório condicional, numérico com 2 decimais
    if vl_desc:
        vl_desc_valido, vl_desc_float, vl_desc_erro = validar_valor_numerico(vl_desc, decimais=2, nao_negativo=True)
        if not vl_desc_valido:
            return None
    
    # VL_FORN: obrigatório (exceto em exceções), numérico com 2 decimais, maior que 0
    if not is_excecao:
        if not vl_forn:
            return None
        vl_forn_valido, vl_forn_float, vl_forn_erro = validar_valor_numerico(vl_forn, decimais=2, obrigatorio=True, positivo=True)
        if not vl_forn_valido:
            return None
    else:
        # Em exceções, VL_FORN é opcional, mas se preenchido deve ser válido
        if vl_forn:
            vl_forn_valido, vl_forn_float, vl_forn_erro = validar_valor_numerico(vl_forn, decimais=2, positivo=True)
            if not vl_forn_valido:
                return None
    
    # VL_SERV_NT: obrigatório condicional, numérico com 2 decimais
    if vl_serv_nt:
        vl_serv_nt_valido, vl_serv_nt_float, vl_serv_nt_erro = validar_valor_numerico(vl_serv_nt, decimais=2, nao_negativo=True)
        if not vl_serv_nt_valido:
            return None
    
    # VL_TERC: obrigatório condicional, numérico com 2 decimais
    if vl_terc:
        vl_terc_valido, vl_terc_float, vl_terc_erro = validar_valor_numerico(vl_terc, decimais=2, nao_negativo=True)
        if not vl_terc_valido:
            return None
    
    # VL_DA: obrigatório condicional, numérico com 2 decimais
    if vl_da:
        vl_da_valido, vl_da_float, vl_da_erro = validar_valor_numerico(vl_da, decimais=2, nao_negativo=True)
        if not vl_da_valido:
            return None
    
    # VL_BC_ICMS: obrigatório condicional, numérico com 2 decimais
    if vl_bc_icms:
        vl_bc_icms_valido, vl_bc_icms_float, vl_bc_icms_erro = validar_valor_numerico(vl_bc_icms, decimais=2, nao_negativo=True)
        if not vl_bc_icms_valido:
            return None
    
    # VL_ICMS: obrigatório condicional, numérico com 2 decimais
    if vl_icms:
        vl_icms_valido, vl_icms_float, vl_icms_erro = validar_valor_numerico(vl_icms, decimais=2, nao_negativo=True)
        if not vl_icms_valido:
            return None
    
    # VL_BC_ICMS_ST: obrigatório condicional, numérico com 2 decimais
    if vl_bc_icms_st:
        vl_bc_icms_st_valido, vl_bc_icms_st_float, vl_bc_icms_st_erro = validar_valor_numerico(vl_bc_icms_st, decimais=2, nao_negativo=True)
        if not vl_bc_icms_st_valido:
            return None
    
    # VL_ICMS_ST: obrigatório condicional, numérico com 2 decimais
    if vl_icms_st:
        vl_icms_st_valido, vl_icms_st_float, vl_icms_st_erro = validar_valor_numerico(vl_icms_st, decimais=2, nao_negativo=True)
        if not vl_icms_st_valido:
            return None
    
    # COD_INF: obrigatório condicional, até 6 caracteres
    if cod_inf:
        if len(cod_inf) > 6:
            return None
    
    # VL_PIS: obrigatório condicional, numérico com 2 decimais
    if vl_pis:
        vl_pis_valido, vl_pis_float, vl_pis_erro = validar_valor_numerico(vl_pis, decimais=2, nao_negativo=True)
        if not vl_pis_valido:
            return None
    
    # VL_COFINS: obrigatório condicional, numérico com 2 decimais
    if vl_cofins:
        vl_cofins_valido, vl_cofins_float, vl_cofins_erro = validar_valor_numerico(vl_cofins, decimais=2, nao_negativo=True)
        if not vl_cofins_valido:
            return None
    
    # TP_LIGACAO: obrigatório condicional, valores válidos: [1, 2, 3]
    if tp_ligacao:
        if tp_ligacao not in ["1", "2", "3"]:
            return None
    
    # COD_GRUPO_TENSAO: obrigatório condicional, valores válidos: [01, 02, 03, 04, 05, 06, 07, 08, 09, 10, 11, 12, 13, 14]
    if cod_grupo_tensao:
        cod_grupo_tensao_validos = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14"]
        if cod_grupo_tensao not in cod_grupo_tensao_validos:
            return None
    
    # Formatação de valores monetários para exibição
    def formatar_valor(valor_str):
        if not valor_str:
            return ""
        try:
            valor_float = float(valor_str)
            return f"{valor_float:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        except ValueError:
            return valor_str
    
    # Mapeamento de códigos para descrições
    cod_cons_desc = {
        "01": "Comercial",
        "02": "Consumo Próprio",
        "03": "Iluminação Pública",
        "04": "Industrial",
        "05": "Poder Público",
        "06": "Residencial",
        "07": "Rural",
        "08": "Serviço Público"
    }
    
    cod_sit_desc = {
        "00": "Documento regular",
        "01": "Documento regular extemporâneo",
        "06": "Documento fiscal complementar",
        "07": "Documento fiscal complementar extemporâneo",
        "08": "Documento fiscal emitido com base em regime especial ou norma específica"
    }
    
    tp_ligacao_desc = {
        "1": "Monofásico",
        "2": "Bifásico",
        "3": "Trifásico"
    }
    
    cod_grupo_tensao_desc = {
        "01": "A1 - Alta Tensão (230kV ou mais)",
        "02": "A2 - Alta Tensão (88 a 138kV)",
        "03": "A3 - Alta Tensão (69kV)",
        "04": "A3a - Alta Tensão (30kV a 44kV)",
        "05": "A4 - Alta Tensão (2,3kV a 25kV)",
        "06": "AS - Alta Tensão Subterrâneo",
        "07": "B1 - Residencial",
        "08": "B1 - Residencial Baixa Renda",
        "09": "B2 - Rural",
        "10": "B2 - Cooperativa de Eletrificação Rural",
        "11": "B2 - Serviço Público de Irrigação",
        "12": "B3 - Demais Classes",
        "13": "B4a - Iluminação Pública - rede de distribuição",
        "14": "B4b - Iluminação Pública - bulbo de lâmpada"
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
            "descricao": "Saída" if ind_oper == "1" else ""
        },
        "IND_EMIT": {
            "titulo": "Indicador do emitente do documento fiscal",
            "valor": ind_emit,
            "descricao": "Emissão própria" if ind_emit == "0" else ""
        },
        "COD_PART": {
            "titulo": "Código do participante (campo 02 do Registro 0150)",
            "valor": cod_part
        },
        "COD_MOD": {
            "titulo": "Código do modelo do documento fiscal, conforme a Tabela 4.1.1",
            "valor": cod_mod,
            "descricao": "06 - Nota Fiscal/Conta de Energia Elétrica"
        },
        "COD_SIT": {
            "titulo": "Código da situação do documento fiscal, conforme a Tabela 4.1.2",
            "valor": cod_sit,
            "descricao": cod_sit_desc.get(cod_sit, "")
        },
        "SER": {
            "titulo": "Série do documento fiscal",
            "valor": ser if ser else ""
        },
        "SUB": {
            "titulo": "Subsérie do documento fiscal",
            "valor": sub if sub else ""
        },
        "COD_CONS": {
            "titulo": "Código de classe de consumo de energia elétrica",
            "valor": cod_cons,
            "descricao": cod_cons_desc.get(cod_cons, "")
        },
        "NUM_DOC": {
            "titulo": "Número do documento fiscal",
            "valor": num_doc
        },
        "DT_DOC": {
            "titulo": "Data da emissão do documento fiscal",
            "valor": dt_doc,
            "valor_formatado": f"{dt_doc[:2]}/{dt_doc[2:4]}/{dt_doc[4:8]}" if dt_doc else ""
        },
        "DT_E_S": {
            "titulo": "Data da entrada ou da saída",
            "valor": dt_e_s,
            "valor_formatado": f"{dt_e_s[:2]}/{dt_e_s[2:4]}/{dt_e_s[4:8]}" if dt_e_s else ""
        },
        "VL_DOC": {
            "titulo": "Valor total do documento fiscal",
            "valor": vl_doc,
            "valor_formatado": formatar_valor(vl_doc)
        },
        "VL_DESC": {
            "titulo": "Valor total do desconto",
            "valor": vl_desc if vl_desc else "",
            "valor_formatado": formatar_valor(vl_desc) if vl_desc else ""
        },
        "VL_FORN": {
            "titulo": "Valor total fornecido/consumido",
            "valor": vl_forn,
            "valor_formatado": formatar_valor(vl_forn)
        },
        "VL_SERV_NT": {
            "titulo": "Valor total dos serviços não-tributados pelo ICMS",
            "valor": vl_serv_nt if vl_serv_nt else "",
            "valor_formatado": formatar_valor(vl_serv_nt) if vl_serv_nt else ""
        },
        "VL_TERC": {
            "titulo": "Valor total cobrado em nome de terceiros",
            "valor": vl_terc if vl_terc else "",
            "valor_formatado": formatar_valor(vl_terc) if vl_terc else ""
        },
        "VL_DA": {
            "titulo": "Valor total de despesas acessórias indicadas no documento fiscal",
            "valor": vl_da if vl_da else "",
            "valor_formatado": formatar_valor(vl_da) if vl_da else ""
        },
        "VL_BC_ICMS": {
            "titulo": "Valor acumulado da base de cálculo do ICMS",
            "valor": vl_bc_icms if vl_bc_icms else "",
            "valor_formatado": formatar_valor(vl_bc_icms) if vl_bc_icms else ""
        },
        "VL_ICMS": {
            "titulo": "Valor acumulado do ICMS",
            "valor": vl_icms if vl_icms else "",
            "valor_formatado": formatar_valor(vl_icms) if vl_icms else ""
        },
        "VL_BC_ICMS_ST": {
            "titulo": "Valor acumulado da base de cálculo do ICMS substituição tributária",
            "valor": vl_bc_icms_st if vl_bc_icms_st else "",
            "valor_formatado": formatar_valor(vl_bc_icms_st) if vl_bc_icms_st else ""
        },
        "VL_ICMS_ST": {
            "titulo": "Valor acumulado do ICMS retido por substituição tributária",
            "valor": vl_icms_st if vl_icms_st else "",
            "valor_formatado": formatar_valor(vl_icms_st) if vl_icms_st else ""
        },
        "COD_INF": {
            "titulo": "Código da informação complementar do documento fiscal (campo 02 do Registro 0450)",
            "valor": cod_inf if cod_inf else ""
        },
        "VL_PIS": {
            "titulo": "Valor do PIS",
            "valor": vl_pis if vl_pis else "",
            "valor_formatado": formatar_valor(vl_pis) if vl_pis else ""
        },
        "VL_COFINS": {
            "titulo": "Valor da COFINS",
            "valor": vl_cofins if vl_cofins else "",
            "valor_formatado": formatar_valor(vl_cofins) if vl_cofins else ""
        },
        "TP_LIGACAO": {
            "titulo": "Código de tipo de Ligação",
            "valor": tp_ligacao if tp_ligacao else "",
            "descricao": tp_ligacao_desc.get(tp_ligacao, "") if tp_ligacao else ""
        },
        "COD_GRUPO_TENSAO": {
            "titulo": "Código de grupo de tensão",
            "valor": cod_grupo_tensao if cod_grupo_tensao else "",
            "descricao": cod_grupo_tensao_desc.get(cod_grupo_tensao, "") if cod_grupo_tensao else ""
        }
    }
    
    return resultado


def validar_1500(linhas):
    """
    Valida uma ou mais linhas do registro 1500 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |1500|IND_OPER|IND_EMIT|COD_PART|...|
        
    Returns:
        String JSON com array de objetos contendo os campos validados.
        Cada objeto tem a estrutura {"CAMPO": {"titulo": "...", "valor": "...", "valor_formatado": "...", "descricao": "..."}}.
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
        resultado = _processar_linha_1500(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
