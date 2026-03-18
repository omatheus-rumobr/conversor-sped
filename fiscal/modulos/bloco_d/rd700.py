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


def _validar_periodo_fiscal(periodo_str):
    """
    Valida se o período fiscal está no formato mmaaaa e se é válido.
    
    Args:
        periodo_str: String com período no formato mmaaaa
        
    Returns:
        tuple: (True/False, dict com mes e ano ou None)
    """
    if not periodo_str or len(periodo_str) != 6 or not periodo_str.isdigit():
        return False, None
    
    try:
        mes = int(periodo_str[:2])
        ano = int(periodo_str[2:6])
        
        # Valida mês (1-12)
        if mes < 1 or mes > 12:
            return False, None
        
        # Valida ano (deve ser razoável, por exemplo entre 1900 e 2100)
        if ano < 1900 or ano > 2100:
            return False, None
        
        return True, {"mes": mes, "ano": ano}
    except ValueError:
        return False, None


def _validar_codigo_municipio(cod_mun_str):
    """
    Valida o código do município IBGE (7 dígitos).
    Aceita também códigos especiais: 9999999 (Exterior) e 9999998 (CT-e simplificado).
    
    Args:
        cod_mun_str: String com o código do município
        
    Returns:
        bool: True se válido, False caso contrário
    """
    if not cod_mun_str:
        return False
    
    # Códigos especiais permitidos
    if cod_mun_str in ["9999999", "9999998"]:
        return True
    
    # Deve ter 7 dígitos numéricos
    if len(cod_mun_str) != 7 or not cod_mun_str.isdigit():
        return False
    
    return True


def _validar_chave_doc_eletronico(chave):
    """
    Valida a chave do documento eletrônico (44 dígitos) e o dígito verificador.
    Usado para NFCom (COD_MOD=62).
    
    Args:
        chave: String com a chave do documento eletrônico (44 dígitos)
        
    Returns:
        bool: True se válida, False caso contrário
    """
    if not chave or len(chave) != 44 or not chave.isdigit():
        return False
    
    # Extrai os 43 primeiros dígitos e o dígito verificador (último dígito)
    chave_43 = chave[:43]
    dv_informado = int(chave[43])
    
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


def _processar_linha_d700(linha):
    """
    Processa uma única linha do registro D700 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |D700|IND_OPER|IND_EMIT|COD_PART|COD_MOD|COD_SIT|SER|NUM_DOC|DT_DOC|DT_E_S|VL_DOC|VL_DESC|VL_SERV|VL_SERV_NT|VL_TERC|VL_DA|VL_BC_ICMS|VL_ICMS|COD_INF|VL_PIS|VL_COFINS|CHV_DOCe|FIN_DOCe|TIP_FAT|COD_MOD_DOC_REF|CHV_DOCe_REF|HASH_DOC_REF|SER_DOC_REF|NUM_DOC_REF|MES_DOC_REF|COD_MUN_DEST|DED|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |D700|...|)
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
    if reg != "D700":
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
    
    # Extrai todos os campos (32 campos no total)
    ind_oper = obter_campo(1)
    ind_emit = obter_campo(2)
    cod_part = obter_campo(3)
    cod_mod = obter_campo(4)
    cod_sit = obter_campo(5)
    ser = obter_campo(6)
    num_doc = obter_campo(7)
    dt_doc = obter_campo(8)
    dt_e_s = obter_campo(9)
    vl_doc = obter_campo(10)
    vl_desc = obter_campo(11)
    vl_serv = obter_campo(12)
    vl_serv_nt = obter_campo(13)
    vl_terc = obter_campo(14)
    vl_da = obter_campo(15)
    vl_bc_icms = obter_campo(16)
    vl_icms = obter_campo(17)
    cod_inf = obter_campo(18)
    vl_pis = obter_campo(19)
    vl_cofins = obter_campo(20)
    chv_doce = obter_campo(21)
    fin_doce = obter_campo(22)
    tip_fat = obter_campo(23)
    cod_mod_doc_ref = obter_campo(24)
    chv_doce_ref = obter_campo(25)
    hash_doc_ref = obter_campo(26)
    ser_doc_ref = obter_campo(27)
    num_doc_ref = obter_campo(28)
    mes_doc_ref = obter_campo(29)
    cod_mun_dest = obter_campo(30)
    ded = obter_campo(31)
    
    # Validações dos campos obrigatórios sempre presentes
    
    # IND_OPER: obrigatório, valores válidos: ["0", "1"]
    if not ind_oper or ind_oper not in ["0", "1"]:
        return None
    
    # IND_EMIT: obrigatório, valores válidos: ["0", "1"]
    if not ind_emit or ind_emit not in ["0", "1"]:
        return None
    
    # COD_MOD: obrigatório, valor válido: "62"
    if not cod_mod or cod_mod != "62":
        return None
    
    # COD_SIT: obrigatório, valores válidos: ["00", "08"]
    if not cod_sit or cod_sit not in ["00", "08"]:
        return None
    
    # SER: obrigatório, até 3 caracteres
    if not ser or len(ser) > 3:
        return None
    
    # NUM_DOC: obrigatório, numérico, até 9 dígitos, maior que zero
    if not num_doc or not num_doc.isdigit() or len(num_doc) > 9 or int(num_doc) <= 0:
        return None
    
    # DT_DOC: obrigatório, formato ddmmaaaa
    dt_doc_valido, dt_doc_obj = _validar_data(dt_doc)
    if not dt_doc_valido:
        return None
    
    # CHV_DOCe: obrigatório, 44 dígitos, com validação de dígito verificador
    if not chv_doce or not _validar_chave_doc_eletronico(chv_doce):
        return None
    
    # FIN_DOCe: obrigatório, valores válidos: ["0", "3", "4"]
    if not fin_doce or fin_doce not in ["0", "3", "4"]:
        return None
    
    # TIP_FAT: obrigatório, valores válidos: ["0", "1", "2"]
    if not tip_fat or tip_fat not in ["0", "1", "2"]:
        return None
    
    # Validações condicionais baseadas em IND_OPER
    
    # COD_PART: obrigatório quando IND_OPER=0, não pode ser informado quando IND_OPER=1
    if ind_oper == "0":
        if not cod_part or len(cod_part) > 60:
            return None
    elif ind_oper == "1":
        if cod_part:
            return None
    
    # Exceção 1: COD_SIT = "08" (regime especial)
    # Apenas REG, IND_OPER, IND_EMIT, COD_PART (nas entradas), COD_MOD, COD_SIT, SER, NUM_DOC e DT_DOC são obrigatórios
    if cod_sit == "08":
        # DT_E_S: opcional condicional, formato ddmmaaaa
        dt_e_s_valido, dt_e_s_obj = None, None
        if dt_e_s:
            dt_e_s_valido, dt_e_s_obj = _validar_data(dt_e_s)
            if not dt_e_s_valido:
                return None
        
        # Demais campos são facultativos, mas se preenchidos devem ser validados
        vl_doc_valido, vl_doc_float, _ = validar_valor_numerico(vl_doc, decimais=2, obrigatorio=False, positivo=False, nao_negativo=True)
        if not vl_doc_valido:
            return None
        
        vl_desc_valido, vl_desc_float, _ = validar_valor_numerico(vl_desc, decimais=2, obrigatorio=False, nao_negativo=True)
        if not vl_desc_valido:
            return None
        
        vl_serv_valido, vl_serv_float, _ = validar_valor_numerico(vl_serv, decimais=2, obrigatorio=False, positivo=False, nao_negativo=True)
        if not vl_serv_valido:
            return None
        
        vl_serv_nt_valido, vl_serv_nt_float, _ = validar_valor_numerico(vl_serv_nt, decimais=2, obrigatorio=False, nao_negativo=True)
        if not vl_serv_nt_valido:
            return None
        
        vl_terc_valido, vl_terc_float, _ = validar_valor_numerico(vl_terc, decimais=2, obrigatorio=False, nao_negativo=True)
        if not vl_terc_valido:
            return None
        
        vl_da_valido, vl_da_float, _ = validar_valor_numerico(vl_da, decimais=2, obrigatorio=False, nao_negativo=True)
        if not vl_da_valido:
            return None
        
        vl_bc_icms_valido, vl_bc_icms_float, _ = validar_valor_numerico(vl_bc_icms, decimais=2, obrigatorio=False, nao_negativo=True)
        if not vl_bc_icms_valido:
            return None
        
        vl_icms_valido, vl_icms_float, _ = validar_valor_numerico(vl_icms, decimais=2, obrigatorio=False, nao_negativo=True)
        if not vl_icms_valido:
            return None
        
        vl_pis_valido, vl_pis_float, _ = validar_valor_numerico(vl_pis, decimais=2, obrigatorio=False, nao_negativo=True)
        if not vl_pis_valido:
            return None
        
        vl_cofins_valido, vl_cofins_float, _ = validar_valor_numerico(vl_cofins, decimais=2, obrigatorio=False, nao_negativo=True)
        if not vl_cofins_valido:
            return None
        
        # COD_INF: opcional condicional, até 6 caracteres
        if cod_inf and len(cod_inf) > 6:
            return None
        
        # COD_MOD_DOC_REF: opcional condicional, valores válidos: ["21", "22", "62"]
        if cod_mod_doc_ref and cod_mod_doc_ref not in ["21", "22", "62"]:
            return None
        
        # CHV_DOCe_REF: opcional condicional, 44 dígitos, com validação de DV quando COD_MOD_DOC_REF=62
        if chv_doce_ref:
            if cod_mod_doc_ref == "62":
                if not _validar_chave_doc_eletronico(chv_doce_ref):
                    return None
            elif len(chv_doce_ref) != 44 or not chv_doce_ref.isdigit():
                return None
        
        # HASH_DOC_REF: opcional condicional, até 32 caracteres
        if hash_doc_ref and len(hash_doc_ref) > 32:
            return None
        
        # SER_DOC_REF: opcional condicional, até 4 caracteres
        if ser_doc_ref and len(ser_doc_ref) > 4:
            return None
        
        # NUM_DOC_REF: opcional condicional, numérico, até 9 dígitos, maior que zero
        if num_doc_ref and (not num_doc_ref.isdigit() or len(num_doc_ref) > 9 or int(num_doc_ref) <= 0):
            return None
        
        # MES_DOC_REF: opcional condicional, formato mmaaaa
        mes_doc_ref_valido, mes_doc_ref_dict = None, None
        if mes_doc_ref:
            mes_doc_ref_valido, mes_doc_ref_dict = _validar_periodo_fiscal(mes_doc_ref)
            if not mes_doc_ref_valido:
                return None
        
        # COD_MUN_DEST: opcional condicional (apenas saídas), 7 dígitos
        if cod_mun_dest and ind_oper == "1":
            if not _validar_codigo_municipio(cod_mun_dest):
                return None
        elif cod_mun_dest:
            return None
        
        # DED: opcional condicional, numérico com 2 decimais, não negativo
        ded_valido, ded_float, _ = validar_valor_numerico(ded, decimais=2, obrigatorio=False, nao_negativo=True)
        if not ded_valido:
            return None
        
        # Formatação
        def formatar_valor_monetario(valor_float):
            if valor_float is None:
                return ""
            return f"R$ {valor_float:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        
        def formatar_data(data_obj):
            if data_obj is None:
                return ""
            return data_obj.strftime("%d/%m/%Y")
        
        def formatar_periodo_fiscal(per_dict):
            if per_dict is None:
                return ""
            return f"{per_dict['mes']:02d}/{per_dict['ano']}"
        
        resultado = {
            "REG": {"titulo": "Registro", "valor": reg},
            "IND_OPER": {"titulo": "Indicador do tipo de prestação: 0: Entrada; 1: Saída", "valor": ind_oper, "descricao": {"0": "Entrada", "1": "Saída"}.get(ind_oper, "")},
            "IND_EMIT": {"titulo": "Indicador do emitente do documento fiscal: 0: Emissão própria; 1: Terceiros", "valor": ind_emit, "descricao": {"0": "Emissão própria", "1": "Terceiros"}.get(ind_emit, "")},
            "COD_PART": {"titulo": "Código do participante (Campo 02 do Registro 0150) do prestador, no caso de entradas", "valor": cod_part if cod_part else ""},
            "COD_MOD": {"titulo": "Código do modelo do documento fiscal, conforme a Tabela 4.1.1", "valor": cod_mod, "descricao": "NFCom"},
            "COD_SIT": {"titulo": "Código da situação do documento fiscal, conforme a Tabela 4.1.2", "valor": cod_sit},
            "SER": {"titulo": "Série do documento fiscal", "valor": ser},
            "NUM_DOC": {"titulo": "Número do documento fiscal", "valor": num_doc},
            "DT_DOC": {"titulo": "Data da emissão do documento fiscal", "valor": dt_doc, "valor_formatado": formatar_data(dt_doc_obj)},
            "DT_E_S": {"titulo": "Data da entrada ou da saída", "valor": dt_e_s if dt_e_s else "", "valor_formatado": formatar_data(dt_e_s_obj) if dt_e_s_obj else ""},
            "VL_DOC": {"titulo": "Valor do documento fiscal", "valor": vl_doc if vl_doc else "", "valor_formatado": formatar_valor_monetario(vl_doc_float) if vl_doc else ""},
            "VL_DESC": {"titulo": "Valor do desconto", "valor": vl_desc if vl_desc else "", "valor_formatado": formatar_valor_monetario(vl_desc_float) if vl_desc else ""},
            "VL_SERV": {"titulo": "Valor dos serviços tributados pelo ICMS", "valor": vl_serv if vl_serv else "", "valor_formatado": formatar_valor_monetario(vl_serv_float) if vl_serv else ""},
            "VL_SERV_NT": {"titulo": "Valores cobrados em nome do prestador sem destaque de ICMS", "valor": vl_serv_nt if vl_serv_nt else "", "valor_formatado": formatar_valor_monetario(vl_serv_nt_float) if vl_serv_nt else ""},
            "VL_TERC": {"titulo": "Valores cobrados em nome de terceiros", "valor": vl_terc if vl_terc else "", "valor_formatado": formatar_valor_monetario(vl_terc_float) if vl_terc else ""},
            "VL_DA": {"titulo": "Valor de despesas acessórias indicadas no documento fiscal", "valor": vl_da if vl_da else "", "valor_formatado": formatar_valor_monetario(vl_da_float) if vl_da else ""},
            "VL_BC_ICMS": {"titulo": "Valor da Base de Cálculo (BC) do ICMS", "valor": vl_bc_icms if vl_bc_icms else "", "valor_formatado": formatar_valor_monetario(vl_bc_icms_float) if vl_bc_icms else ""},
            "VL_ICMS": {"titulo": "Valor do ICMS", "valor": vl_icms if vl_icms else "", "valor_formatado": formatar_valor_monetario(vl_icms_float) if vl_icms else ""},
            "COD_INF": {"titulo": "Código da informação complementar do documento fiscal (campo 02 do Registro 0450)", "valor": cod_inf if cod_inf else ""},
            "VL_PIS": {"titulo": "Valor do PIS/Pasep", "valor": vl_pis if vl_pis else "", "valor_formatado": formatar_valor_monetario(vl_pis_float) if vl_pis else ""},
            "VL_COFINS": {"titulo": "Valor do Cofins", "valor": vl_cofins if vl_cofins else "", "valor_formatado": formatar_valor_monetario(vl_cofins_float) if vl_cofins else ""},
            "CHV_DOCe": {"titulo": "Chave da Nota Fiscal Fatura de Serviço de Comunicação Eletrônica", "valor": chv_doce},
            "FIN_DOCe": {"titulo": "Finalidade da emissão do documento eletrônico: 0 - NFCom Normal; 3 - NFCom de Substituição; 4 - NFCom de Ajuste", "valor": fin_doce, "descricao": {"0": "NFCom Normal", "3": "NFCom de Substituição", "4": "NFCom de Ajuste"}.get(fin_doce, "")},
            "TIP_FAT": {"titulo": "Tipo de faturamento do documento eletrônico: 0 - Faturamento Normal; 1 - Faturamento centralizado; 2 - Cofaturamento", "valor": tip_fat, "descricao": {"0": "Faturamento Normal", "1": "Faturamento centralizado", "2": "Cofaturamento"}.get(tip_fat, "")},
            "COD_MOD_DOC_REF": {"titulo": "Código do modelo do documento fiscal referenciado, conforme a Tabela 4.1.1", "valor": cod_mod_doc_ref if cod_mod_doc_ref else ""},
            "CHV_DOCe_REF": {"titulo": "Chave da nota referenciada", "valor": chv_doce_ref if chv_doce_ref else ""},
            "HASH_DOC_REF": {"titulo": "Código de autenticação digital do registro, campo 36 do registro do Arquivo tipo mestre de documento fiscal, conforme definido no Convênio 115/2003", "valor": hash_doc_ref if hash_doc_ref else ""},
            "SER_DOC_REF": {"titulo": "Série do documento fiscal referenciado", "valor": ser_doc_ref if ser_doc_ref else ""},
            "NUM_DOC_REF": {"titulo": "Número do documento fiscal referenciado", "valor": num_doc_ref if num_doc_ref else ""},
            "MES_DOC_REF": {"titulo": "Mês e ano da emissão do documento fiscal referenciado", "valor": mes_doc_ref if mes_doc_ref else "", "valor_formatado": formatar_periodo_fiscal(mes_doc_ref_dict) if mes_doc_ref_dict else ""},
            "COD_MUN_DEST": {"titulo": "Código do município do destinatário conforme a tabela do IBGE", "valor": cod_mun_dest if cod_mun_dest else ""},
            "DED": {"titulo": "Deduções", "valor": ded if ded else "", "valor_formatado": formatar_valor_monetario(ded_float) if ded else ""}
        }
        return resultado
    
    # Caso normal: COD_SIT = "00"
    # Todos os campos obrigatórios devem ser preenchidos
    
    # DT_E_S: opcional condicional, formato ddmmaaaa
    dt_e_s_valido, dt_e_s_obj = None, None
    if dt_e_s:
        dt_e_s_valido, dt_e_s_obj = _validar_data(dt_e_s)
        if not dt_e_s_valido:
            return None
    
    # VL_DOC: obrigatório, numérico com 2 decimais, maior que zero
    vl_doc_valido, vl_doc_float, _ = validar_valor_numerico(vl_doc, decimais=2, obrigatorio=True, positivo=True)
    if not vl_doc_valido:
        return None
    
    # VL_DESC: opcional condicional, numérico com 2 decimais, não negativo
    vl_desc_valido, vl_desc_float, _ = validar_valor_numerico(vl_desc, decimais=2, obrigatorio=False, nao_negativo=True)
    if not vl_desc_valido:
        return None
    
    # VL_SERV: obrigatório, numérico com 2 decimais, maior que zero
    vl_serv_valido, vl_serv_float, _ = validar_valor_numerico(vl_serv, decimais=2, obrigatorio=True, positivo=True)
    if not vl_serv_valido:
        return None
    
    # VL_SERV_NT: opcional condicional, numérico com 2 decimais, não negativo
    vl_serv_nt_valido, vl_serv_nt_float, _ = validar_valor_numerico(vl_serv_nt, decimais=2, obrigatorio=False, nao_negativo=True)
    if not vl_serv_nt_valido:
        return None
    
    # VL_TERC: opcional condicional, numérico com 2 decimais, não negativo
    vl_terc_valido, vl_terc_float, _ = validar_valor_numerico(vl_terc, decimais=2, obrigatorio=False, nao_negativo=True)
    if not vl_terc_valido:
        return None
    
    # VL_DA: opcional condicional, numérico com 2 decimais, não negativo
    vl_da_valido, vl_da_float, _ = validar_valor_numerico(vl_da, decimais=2, obrigatorio=False, nao_negativo=True)
    if not vl_da_valido:
        return None
    
    # VL_BC_ICMS: opcional condicional, numérico com 2 decimais, não negativo
    vl_bc_icms_valido, vl_bc_icms_float, _ = validar_valor_numerico(vl_bc_icms, decimais=2, obrigatorio=False, nao_negativo=True)
    if not vl_bc_icms_valido:
        return None
    
    # VL_ICMS: opcional condicional, numérico com 2 decimais, não negativo
    vl_icms_valido, vl_icms_float, _ = validar_valor_numerico(vl_icms, decimais=2, obrigatorio=False, nao_negativo=True)
    if not vl_icms_valido:
        return None
    
    # COD_INF: opcional condicional, até 6 caracteres
    if cod_inf and len(cod_inf) > 6:
        return None
    
    # VL_PIS: opcional condicional, numérico com 2 decimais, não negativo
    vl_pis_valido, vl_pis_float, _ = validar_valor_numerico(vl_pis, decimais=2, obrigatorio=False, nao_negativo=True)
    if not vl_pis_valido:
        return None
    
    # VL_COFINS: opcional condicional, numérico com 2 decimais, não negativo
    vl_cofins_valido, vl_cofins_float, _ = validar_valor_numerico(vl_cofins, decimais=2, obrigatorio=False, nao_negativo=True)
    if not vl_cofins_valido:
        return None
    
    # COD_MOD_DOC_REF: opcional condicional, valores válidos: ["21", "22", "62"]
    # Deve ser informado quando FIN_DOCe = "3" (Substituição)
    if fin_doce == "3":
        if not cod_mod_doc_ref or cod_mod_doc_ref not in ["21", "22", "62"]:
            return None
    elif cod_mod_doc_ref:
        # Não deve ser informado nas demais situações
        return None
    
    # CHV_DOCe_REF: opcional condicional
    # Obrigatório quando COD_MOD_DOC_REF = "62"
    if cod_mod_doc_ref == "62":
        if not chv_doce_ref or not _validar_chave_doc_eletronico(chv_doce_ref):
            return None
    elif chv_doce_ref:
        # Se COD_MOD_DOC_REF não for "62", CHV_DOCe_REF não deve ser informado
        return None
    
    # HASH_DOC_REF: opcional condicional
    # Não deve ser informado quando COD_MOD_DOC_REF for diferente de "21" e "22"
    # Quando COD_MOD_DOC_REF for "21" ou "22", é obrigatória a informação simultânea de SER_DOC_REF, NUM_DOC_REF e MES_DOC_REF, ou a informação de HASH_DOC_REF
    mes_doc_ref_dict = None
    if cod_mod_doc_ref in ["21", "22"]:
        # Se HASH_DOC_REF for informado, SER_DOC_REF, NUM_DOC_REF e MES_DOC_REF devem estar vazios
        if hash_doc_ref:
            if ser_doc_ref or num_doc_ref or mes_doc_ref:
                return None
            if len(hash_doc_ref) > 32:
                return None
        else:
            # Se HASH_DOC_REF não for informado, SER_DOC_REF, NUM_DOC_REF e MES_DOC_REF são obrigatórios
            if not ser_doc_ref or len(ser_doc_ref) > 4:
                return None
            if not num_doc_ref or not num_doc_ref.isdigit() or len(num_doc_ref) > 9 or int(num_doc_ref) <= 0:
                return None
            mes_doc_ref_valido, mes_doc_ref_dict = _validar_periodo_fiscal(mes_doc_ref)
            if not mes_doc_ref_valido:
                return None
    elif hash_doc_ref or ser_doc_ref or num_doc_ref or mes_doc_ref:
        # Se COD_MOD_DOC_REF não for "21" ou "22", esses campos não devem ser informados
        return None
    
    # COD_MUN_DEST: opcional condicional (apenas saídas), 7 dígitos
    if cod_mun_dest:
        if ind_oper != "1":
            return None
        if not _validar_codigo_municipio(cod_mun_dest):
            return None
    
    # DED: opcional condicional, numérico com 2 decimais, não negativo
    ded_valido, ded_float, _ = validar_valor_numerico(ded, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ded_valido:
        return None
    
    # Formatação
    def formatar_valor_monetario(valor_float):
        if valor_float is None:
            return ""
        return f"R$ {valor_float:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    def formatar_data(data_obj):
        if data_obj is None:
            return ""
        return data_obj.strftime("%d/%m/%Y")
    
    def formatar_periodo_fiscal(per_dict):
        if per_dict is None:
            return ""
        return f"{per_dict['mes']:02d}/{per_dict['ano']}"
    
    # Monta o resultado
    resultado = {
        "REG": {"titulo": "Registro", "valor": reg},
        "IND_OPER": {"titulo": "Indicador do tipo de prestação: 0: Entrada; 1: Saída", "valor": ind_oper, "descricao": {"0": "Entrada", "1": "Saída"}.get(ind_oper, "")},
        "IND_EMIT": {"titulo": "Indicador do emitente do documento fiscal: 0: Emissão própria; 1: Terceiros", "valor": ind_emit, "descricao": {"0": "Emissão própria", "1": "Terceiros"}.get(ind_emit, "")},
        "COD_PART": {"titulo": "Código do participante (Campo 02 do Registro 0150) do prestador, no caso de entradas", "valor": cod_part if cod_part else ""},
        "COD_MOD": {"titulo": "Código do modelo do documento fiscal, conforme a Tabela 4.1.1", "valor": cod_mod, "descricao": "NFCom"},
        "COD_SIT": {"titulo": "Código da situação do documento fiscal, conforme a Tabela 4.1.2", "valor": cod_sit},
        "SER": {"titulo": "Série do documento fiscal", "valor": ser},
        "NUM_DOC": {"titulo": "Número do documento fiscal", "valor": num_doc},
        "DT_DOC": {"titulo": "Data da emissão do documento fiscal", "valor": dt_doc, "valor_formatado": formatar_data(dt_doc_obj)},
        "DT_E_S": {"titulo": "Data da entrada ou da saída", "valor": dt_e_s if dt_e_s else "", "valor_formatado": formatar_data(dt_e_s_obj) if dt_e_s_obj else ""},
        "VL_DOC": {"titulo": "Valor do documento fiscal", "valor": vl_doc, "valor_formatado": formatar_valor_monetario(vl_doc_float)},
        "VL_DESC": {"titulo": "Valor do desconto", "valor": vl_desc if vl_desc else "", "valor_formatado": formatar_valor_monetario(vl_desc_float) if vl_desc else ""},
        "VL_SERV": {"titulo": "Valor dos serviços tributados pelo ICMS", "valor": vl_serv, "valor_formatado": formatar_valor_monetario(vl_serv_float)},
        "VL_SERV_NT": {"titulo": "Valores cobrados em nome do prestador sem destaque de ICMS", "valor": vl_serv_nt if vl_serv_nt else "", "valor_formatado": formatar_valor_monetario(vl_serv_nt_float) if vl_serv_nt else ""},
        "VL_TERC": {"titulo": "Valores cobrados em nome de terceiros", "valor": vl_terc if vl_terc else "", "valor_formatado": formatar_valor_monetario(vl_terc_float) if vl_terc else ""},
        "VL_DA": {"titulo": "Valor de despesas acessórias indicadas no documento fiscal", "valor": vl_da if vl_da else "", "valor_formatado": formatar_valor_monetario(vl_da_float) if vl_da else ""},
        "VL_BC_ICMS": {"titulo": "Valor da Base de Cálculo (BC) do ICMS", "valor": vl_bc_icms if vl_bc_icms else "", "valor_formatado": formatar_valor_monetario(vl_bc_icms_float) if vl_bc_icms else ""},
        "VL_ICMS": {"titulo": "Valor do ICMS", "valor": vl_icms if vl_icms else "", "valor_formatado": formatar_valor_monetario(vl_icms_float) if vl_icms else ""},
        "COD_INF": {"titulo": "Código da informação complementar do documento fiscal (campo 02 do Registro 0450)", "valor": cod_inf if cod_inf else ""},
        "VL_PIS": {"titulo": "Valor do PIS/Pasep", "valor": vl_pis if vl_pis else "", "valor_formatado": formatar_valor_monetario(vl_pis_float) if vl_pis else ""},
        "VL_COFINS": {"titulo": "Valor do Cofins", "valor": vl_cofins if vl_cofins else "", "valor_formatado": formatar_valor_monetario(vl_cofins_float) if vl_cofins else ""},
        "CHV_DOCe": {"titulo": "Chave da Nota Fiscal Fatura de Serviço de Comunicação Eletrônica", "valor": chv_doce},
        "FIN_DOCe": {"titulo": "Finalidade da emissão do documento eletrônico: 0 - NFCom Normal; 3 - NFCom de Substituição; 4 - NFCom de Ajuste", "valor": fin_doce, "descricao": {"0": "NFCom Normal", "3": "NFCom de Substituição", "4": "NFCom de Ajuste"}.get(fin_doce, "")},
        "TIP_FAT": {"titulo": "Tipo de faturamento do documento eletrônico: 0 - Faturamento Normal; 1 - Faturamento centralizado; 2 - Cofaturamento", "valor": tip_fat, "descricao": {"0": "Faturamento Normal", "1": "Faturamento centralizado", "2": "Cofaturamento"}.get(tip_fat, "")},
        "COD_MOD_DOC_REF": {"titulo": "Código do modelo do documento fiscal referenciado, conforme a Tabela 4.1.1", "valor": cod_mod_doc_ref if cod_mod_doc_ref else ""},
        "CHV_DOCe_REF": {"titulo": "Chave da nota referenciada", "valor": chv_doce_ref if chv_doce_ref else ""},
        "HASH_DOC_REF": {"titulo": "Código de autenticação digital do registro, campo 36 do registro do Arquivo tipo mestre de documento fiscal, conforme definido no Convênio 115/2003", "valor": hash_doc_ref if hash_doc_ref else ""},
        "SER_DOC_REF": {"titulo": "Série do documento fiscal referenciado", "valor": ser_doc_ref if ser_doc_ref else ""},
        "NUM_DOC_REF": {"titulo": "Número do documento fiscal referenciado", "valor": num_doc_ref if num_doc_ref else ""},
        "MES_DOC_REF": {"titulo": "Mês e ano da emissão do documento fiscal referenciado", "valor": mes_doc_ref if mes_doc_ref else "", "valor_formatado": formatar_periodo_fiscal(mes_doc_ref_dict) if mes_doc_ref_dict else ""},
        "COD_MUN_DEST": {"titulo": "Código do município do destinatário conforme a tabela do IBGE", "valor": cod_mun_dest if cod_mun_dest else ""},
        "DED": {"titulo": "Deduções", "valor": ded if ded else "", "valor_formatado": formatar_valor_monetario(ded_float) if ded else ""}
    }
    
    return resultado


def validar_d700_fiscal(linhas):
    """
    Valida uma ou mais linhas do registro D700 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |D700|IND_OPER|IND_EMIT|COD_PART|COD_MOD|COD_SIT|SER|NUM_DOC|DT_DOC|DT_E_S|VL_DOC|VL_DESC|VL_SERV|VL_SERV_NT|VL_TERC|VL_DA|VL_BC_ICMS|VL_ICMS|COD_INF|VL_PIS|VL_COFINS|CHV_DOCe|FIN_DOCe|TIP_FAT|COD_MOD_DOC_REF|CHV_DOCe_REF|HASH_DOC_REF|SER_DOC_REF|NUM_DOC_REF|MES_DOC_REF|COD_MUN_DEST|DED|
        
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
        resultado = _processar_linha_d700(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
