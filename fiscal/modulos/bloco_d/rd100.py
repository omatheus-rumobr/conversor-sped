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


def _validar_chave_doc_eletronico(chave):
    """
    Valida a chave do documento eletrônico (44 dígitos) e o dígito verificador.
    Usado para CT-e (COD_MOD=57), CT-e OS (COD_MOD=67) e BP-e (COD_MOD=63).
    
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


def _processar_linha_d100(linha):
    """
    Processa uma única linha do registro D100 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |D100|IND_OPER|IND_EMIT|COD_PART|COD_MOD|COD_SIT|SER|SUB|NUM_DOC|CHV_CTE|DT_DOC|DT_A_P|TP_CT-e|CHV_CTE_REF|VL_DOC|VL_DESC|IND_FRT|VL_SERV|VL_BC_ICMS|VL_ICMS|VL_NT|COD_INF|COD_CTA|COD_MUN_ORIG|COD_MUN_DEST|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |D100|...|)
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
    if reg != "D100":
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
    
    # Extrai todos os campos (25 campos no total)
    ind_oper = obter_campo(1)
    ind_emit = obter_campo(2)
    cod_part = obter_campo(3)
    cod_mod = obter_campo(4)
    cod_sit = obter_campo(5)
    ser = obter_campo(6)
    sub = obter_campo(7)
    num_doc = obter_campo(8)
    chv_cte = obter_campo(9)
    dt_doc = obter_campo(10)
    dt_a_p = obter_campo(11)
    tp_cte = obter_campo(12)
    chv_cte_ref = obter_campo(13)
    vl_doc = obter_campo(14)
    vl_desc = obter_campo(15)
    ind_frt = obter_campo(16)
    vl_serv = obter_campo(17)
    vl_bc_icms = obter_campo(18)
    vl_icms = obter_campo(19)
    vl_nt = obter_campo(20)
    cod_inf = obter_campo(21)
    cod_cta = obter_campo(22)
    cod_mun_orig = obter_campo(23)
    cod_mun_dest = obter_campo(24)
    
    # Validações dos campos obrigatórios
    
    # IND_OPER: obrigatório, valores válidos: ["0", "1"]
    if ind_oper not in ["0", "1"]:
        return None
    
    # IND_EMIT: obrigatório, valores válidos: ["0", "1"]
    if ind_emit not in ["0", "1"]:
        return None
    
    # Validação: se IND_EMIT = 1 (terceiros), então IND_OPER deve ser 0 (entradas)
    if ind_emit == "1" and ind_oper != "0":
        return None
    
    # COD_MOD: obrigatório, valores válidos: ["07", "08", "8B", "09", "10", "11", "26", "27", "57", "63", "67"]
    cod_mod_validos = ["07", "08", "8B", "09", "10", "11", "26", "27", "57", "63", "67"]
    if cod_mod not in cod_mod_validos:
        return None
    
    # COD_SIT: obrigatório, valores válidos: ["00", "01", "02", "03", "04", "05", "06", "07", "08"]
    cod_sit_validos = ["00", "01", "02", "03", "04", "05", "06", "07", "08"]
    if cod_sit not in cod_sit_validos:
        return None
    
    # COD_PART: obrigatório, exceto para BP-e (modelo 63)
    if cod_mod != "63":
        if not cod_part:
            return None
        if len(cod_part) > 60:
            return None
    else:
        # Para BP-e, COD_PART não deve ser preenchido
        if cod_part:
            return None
    
    # SER: obrigatório condicional
    # Para CT-e e CT-e OS (COD_MOD 57 e 67), deve ter 3 posições. Se não existir série, informar 000.
    if cod_mod in ["57", "67"]:
        if not ser:
            ser = "000"
        elif len(ser) != 3:
            return None
    
    # SUB: obrigatório condicional (mesmas regras de SER)
    # Não há validação específica de tamanho para SUB no manual, mas geralmente é 3 caracteres
    
    # NUM_DOC: obrigatório, maior que zero
    if not num_doc or not num_doc.isdigit() or int(num_doc) <= 0:
        return None
    
    # CHV_CTE: obrigatório condicional
    # Obrigatório para COD_MOD 57, 63 e 67, exceto para COD_SIT = 05 (numeração inutilizada)
    if cod_mod in ["57", "63", "67"]:
        if cod_sit == "05":
            # Para numeração inutilizada, CHV_CTE não deve ser preenchido
            if chv_cte:
                return None
        else:
            # Para outros casos, CHV_CTE é obrigatório
            if not chv_cte:
                return None
            if len(chv_cte) != 44 or not chv_cte.isdigit():
                return None
            if not _validar_chave_doc_eletronico(chv_cte):
                return None
    else:
        # Para outros modelos, CHV_CTE não deve ser preenchido
        if chv_cte:
            return None
    
    # DT_DOC: obrigatório, formato ddmmaaaa
    if not dt_doc:
        return None
    dt_doc_valida, dt_doc_obj = _validar_data(dt_doc)
    if not dt_doc_valida:
        return None
    
    # Validação: Se COD_MOD for 07, 09, 10, 11, 26 ou 27, a data deve ser menor que 01/01/2019
    if cod_mod in ["07", "09", "10", "11", "26", "27"]:
        data_limite = datetime(2019, 1, 1)
        if dt_doc_obj >= data_limite:
            return None
    
    # DT_A_P: obrigatório condicional
    # Obrigatório para saídas (IND_OPER = 1), opcional para entradas
    if ind_oper == "1":
        if not dt_a_p:
            return None
        dt_a_p_valida, dt_a_p_obj = _validar_data(dt_a_p)
        if not dt_a_p_valida:
            return None
        # Para operações de prestação, DT_A_P deve ser maior ou igual a DT_DOC
        if dt_a_p_obj < dt_doc_obj:
            return None
    
    # TP_CT-e: obrigatório condicional (quando COD_MOD for 57, 63 ou 67)
    if cod_mod in ["57", "63", "67"]:
        if not tp_cte:
            return None
        if not tp_cte.isdigit() or len(tp_cte) != 1:
            return None
    
    # CHV_CTE_REF: obrigatório condicional
    # Quando TP_CT-e for igual a "3" ou "6", informar a chave do documento substituído
    if tp_cte in ["3", "6"]:
        if not chv_cte_ref:
            return None
        if len(chv_cte_ref) != 44 or not chv_cte_ref.isdigit():
            return None
        if not _validar_chave_doc_eletronico(chv_cte_ref):
            return None
    else:
        # Nas demais situações, não deve ser preenchido
        if chv_cte_ref:
            return None
    
    # VL_DOC: obrigatório, numérico com 2 decimais, não negativo
    vl_doc_valido, vl_doc_float, _ = validar_valor_numerico(vl_doc, decimais=2, obrigatorio=True, nao_negativo=True)
    if not vl_doc_valido:
        return None
    
    # VL_DESC: opcional, numérico com 2 decimais, não negativo
    vl_desc_valido, vl_desc_float, _ = validar_valor_numerico(vl_desc, decimais=2, obrigatorio=False, nao_negativo=True)
    if not vl_desc_valido:
        return None
    
    # IND_FRT: obrigatório, exceto para BP-e (modelo 63)
    # Valores válidos: ["0", "1", "2", "9"]
    if cod_mod != "63":
        if ind_frt not in ["0", "1", "2", "9"]:
            return None
    else:
        # Para BP-e, IND_FRT não deve ser preenchido
        if ind_frt:
            return None
    
    # VL_SERV: obrigatório, numérico com 2 decimais, não negativo
    vl_serv_valido, vl_serv_float, _ = validar_valor_numerico(vl_serv, decimais=2, obrigatorio=True, nao_negativo=True)
    if not vl_serv_valido:
        return None
    
    # VL_BC_ICMS: opcional, numérico com 2 decimais, não negativo
    vl_bc_icms_valido, vl_bc_icms_float, _ = validar_valor_numerico(vl_bc_icms, decimais=2, obrigatorio=False, nao_negativo=True)
    if not vl_bc_icms_valido:
        return None
    
    # VL_ICMS: opcional, numérico com 2 decimais, não negativo
    vl_icms_valido, vl_icms_float, _ = validar_valor_numerico(vl_icms, decimais=2, obrigatorio=False, nao_negativo=True)
    if not vl_icms_valido:
        return None
    
    # VL_NT: opcional, numérico com 2 decimais, não negativo
    vl_nt_valido, vl_nt_float, _ = validar_valor_numerico(vl_nt, decimais=2, obrigatorio=False, nao_negativo=True)
    if not vl_nt_valido:
        return None
    
    # COD_INF: opcional, até 6 caracteres
    if cod_inf and len(cod_inf) > 6:
        return None
    
    # COD_CTA: opcional (sem validação específica de formato)
    
    # COD_MUN_ORIG: obrigatório condicional
    # Campo obrigatório nas saídas para todos os modelos (a partir de 2022)
    # Campo obrigatório nas entradas, se COD_MOD for "57", "63" ou "67"
    if ind_oper == "1" or (ind_oper == "0" and cod_mod in ["57", "63", "67"]):
        if not cod_mun_orig:
            return None
        if not _validar_codigo_municipio(cod_mun_orig):
            return None
    
    # COD_MUN_DEST: obrigatório condicional
    # Campo obrigatório nas entradas, se COD_MOD for "57", "63" ou "67"
    if ind_oper == "0" and cod_mod in ["57", "63", "67"]:
        if not cod_mun_dest:
            return None
        if not _validar_codigo_municipio(cod_mun_dest):
            return None
    
    # Mapeamento de códigos para descrições
    ind_oper_desc = {
        "0": "Aquisição",
        "1": "Prestação"
    }
    
    ind_emit_desc = {
        "0": "Emissão própria",
        "1": "Terceiros"
    }
    
    cod_sit_desc = {
        "00": "Documento regular",
        "01": "Documento regular extemporâneo",
        "02": "Documento cancelado",
        "03": "Documento cancelado extemporâneo",
        "04": "NF-e ou CT-e denegado",
        "05": "NF-e ou CT-e Numeração inutilizada",
        "06": "Documento de transporte complementar",
        "07": "Documento de transporte escriturado extemporaneamente",
        "08": "Documento Fiscal emitido com base em Regime Especial ou Norma Específica"
    }
    
    ind_frt_desc = {
        "0": "Por conta do emitente",
        "1": "Por conta do destinatário/remetente",
        "2": "Por conta de terceiros",
        "9": "Sem cobrança de frete"
    }
    
    # Formatação de valores monetários
    def formatar_valor_monetario(valor_float):
        if valor_float is None:
            return ""
        return f"R$ {valor_float:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    # Formatação de data
    def formatar_data(data_str):
        if not data_str or len(data_str) != 8:
            return data_str
        return f"{data_str[:2]}/{data_str[2:4]}/{data_str[4:8]}"
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "IND_OPER": {
            "titulo": "Indicador do tipo de operação",
            "valor": ind_oper,
            "descricao": ind_oper_desc.get(ind_oper, "")
        },
        "IND_EMIT": {
            "titulo": "Indicador do emitente do documento fiscal",
            "valor": ind_emit,
            "descricao": ind_emit_desc.get(ind_emit, "")
        },
        "COD_PART": {
            "titulo": "Código do participante",
            "valor": cod_part if cod_part else ""
        },
        "COD_MOD": {
            "titulo": "Código do modelo do documento fiscal",
            "valor": cod_mod
        },
        "COD_SIT": {
            "titulo": "Código da situação do documento fiscal",
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
        "NUM_DOC": {
            "titulo": "Número do documento fiscal",
            "valor": num_doc
        },
        "CHV_CTE": {
            "titulo": "Chave do Conhecimento de Transporte Eletrônico ou do Bilhete de Passagem Eletrônico",
            "valor": chv_cte if chv_cte else ""
        },
        "DT_DOC": {
            "titulo": "Data da emissão do documento fiscal",
            "valor": dt_doc,
            "valor_formatado": formatar_data(dt_doc)
        },
        "DT_A_P": {
            "titulo": "Data da aquisição ou da prestação do serviço",
            "valor": dt_a_p if dt_a_p else "",
            "valor_formatado": formatar_data(dt_a_p) if dt_a_p else ""
        },
        "TP_CT-e": {
            "titulo": "Tipo de Conhecimento de Transporte Eletrônico",
            "valor": tp_cte if tp_cte else ""
        },
        "CHV_CTE_REF": {
            "titulo": "Chave do Documento Eletrônico Substituído",
            "valor": chv_cte_ref if chv_cte_ref else ""
        },
        "VL_DOC": {
            "titulo": "Valor total do documento fiscal",
            "valor": vl_doc,
            "valor_formatado": formatar_valor_monetario(vl_doc_float)
        },
        "VL_DESC": {
            "titulo": "Valor total do desconto",
            "valor": vl_desc if vl_desc else "",
            "valor_formatado": formatar_valor_monetario(vl_desc_float) if vl_desc else ""
        },
        "IND_FRT": {
            "titulo": "Indicador do tipo do frete",
            "valor": ind_frt if ind_frt else "",
            "descricao": ind_frt_desc.get(ind_frt, "") if ind_frt else ""
        },
        "VL_SERV": {
            "titulo": "Valor total da prestação de serviço",
            "valor": vl_serv,
            "valor_formatado": formatar_valor_monetario(vl_serv_float)
        },
        "VL_BC_ICMS": {
            "titulo": "Valor da base de cálculo do ICMS",
            "valor": vl_bc_icms if vl_bc_icms else "",
            "valor_formatado": formatar_valor_monetario(vl_bc_icms_float) if vl_bc_icms else ""
        },
        "VL_ICMS": {
            "titulo": "Valor do ICMS",
            "valor": vl_icms if vl_icms else "",
            "valor_formatado": formatar_valor_monetario(vl_icms_float) if vl_icms else ""
        },
        "VL_NT": {
            "titulo": "Valor não-tributado",
            "valor": vl_nt if vl_nt else "",
            "valor_formatado": formatar_valor_monetario(vl_nt_float) if vl_nt else ""
        },
        "COD_INF": {
            "titulo": "Código da informação complementar do documento fiscal",
            "valor": cod_inf if cod_inf else ""
        },
        "COD_CTA": {
            "titulo": "Código da conta analítica contábil debitada/creditada",
            "valor": cod_cta if cod_cta else ""
        },
        "COD_MUN_ORIG": {
            "titulo": "Código do município de origem do serviço",
            "valor": cod_mun_orig if cod_mun_orig else ""
        },
        "COD_MUN_DEST": {
            "titulo": "Código do município de destino",
            "valor": cod_mun_dest if cod_mun_dest else ""
        }
    }
    
    return resultado


def validar_d100_fiscal(linhas):
    """
    Valida uma ou mais linhas do registro D100 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |D100|IND_OPER|IND_EMIT|COD_PART|COD_MOD|COD_SIT|SER|SUB|NUM_DOC|CHV_CTE|DT_DOC|DT_A_P|TP_CT-e|CHV_CTE_REF|VL_DOC|VL_DESC|IND_FRT|VL_SERV|VL_BC_ICMS|VL_ICMS|VL_NT|COD_INF|COD_CTA|COD_MUN_ORIG|COD_MUN_DEST|
        
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
        resultado = _processar_linha_d100(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
