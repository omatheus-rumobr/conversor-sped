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
    Usado para NF-e (COD_MOD=55), NFC-e (COD_MOD=65) e NF3-e (COD_MOD=66).
    
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


def _processar_linha_b020(linha):
    """
    Processa uma única linha do registro B020 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |B020|IND_OPER|IND_EMIT|COD_PART|COD_MOD|COD_SIT|SER|NUM_DOC|CHV_NFE|DT_DOC|COD_MUN_SERV|VL_CONT|VL_MAT_TERC|VL_SUB|VL_ISNT_ISS|VL_DED_BC|VL_BC_ISS|VL_BC_ISS_RT|VL_ISS_RT|VL_ISS|COD_INF_OBS|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |B020|...|)
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
    if reg != "B020":
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
    
    # Extrai todos os campos (21 campos no total)
    ind_oper = obter_campo(1)
    ind_emit = obter_campo(2)
    cod_part = obter_campo(3)
    cod_mod = obter_campo(4)
    cod_sit = obter_campo(5)
    ser = obter_campo(6)
    num_doc = obter_campo(7)
    chv_nfe = obter_campo(8)
    dt_doc = obter_campo(9)
    cod_mun_serv = obter_campo(10)
    vl_cont = obter_campo(11)
    vl_mat_terc = obter_campo(12)
    vl_sub = obter_campo(13)
    vl_isnt_iss = obter_campo(14)
    vl_ded_bc = obter_campo(15)
    vl_bc_iss = obter_campo(16)
    vl_bc_iss_rt = obter_campo(17)
    vl_iss_rt = obter_campo(18)
    vl_iss = obter_campo(19)
    cod_inf_obs = obter_campo(20)
    
    # Validações dos campos obrigatórios
    
    # IND_OPER: obrigatório, valores válidos: ["0", "1"]
    if ind_oper not in ["0", "1"]:
        return None
    
    # IND_EMIT: obrigatório, valores válidos: ["0", "1"]
    if ind_emit not in ["0", "1"]:
        return None
    
    # Validação: se IND_EMIT = "1", então IND_OPER deve ser "0"
    if ind_emit == "1" and ind_oper != "0":
        return None
    
    # COD_MOD: obrigatório, valores válidos: ["01", "03", "3B", "04", "08", "55", "65", "66"]
    cod_mod_validos = ["01", "03", "3B", "04", "08", "55", "65", "66"]
    if cod_mod not in cod_mod_validos:
        return None
    
    # Validação: modelo "65" só pode ser informado se IND_OPER = "1"
    if cod_mod == "65" and ind_oper != "1":
        return None
    
    # COD_SIT: obrigatório, valores válidos: ["00", "02", "06", "08"]
    cod_sit_validos = ["00", "02", "06", "08"]
    if cod_sit not in cod_sit_validos:
        return None
    
    # Validação: para NF3-e (modelo 66) não pode ser informado COD_SIT = "06"
    if cod_mod == "66" and cod_sit == "06":
        return None
    
    # COD_PART: obrigatório condicional
    # Quando NFC-e (modelo 65), não deve ser preenchido
    if cod_mod == "65":
        if cod_part:  # Se estiver preenchido, é inválido
            return None
    # Quando NF3-e (modelo 66), obrigatório se IND_OPER = "0" ou VL_ISS_RT > 0
    elif cod_mod == "66":
        vl_iss_rt_valido_temp, vl_iss_rt_float_temp, _ = validar_valor_numerico(vl_iss_rt, decimais=2, obrigatorio=False, nao_negativo=True)
        if vl_iss_rt_valido_temp:
            if ind_oper == "0" or vl_iss_rt_float_temp > 0:
                if not cod_part:
                    return None
    # Para outros modelos, é obrigatório
    elif not cod_part:
        return None
    
    if cod_part and len(cod_part) > 60:
        return None
    
    # SER: obrigatório condicional
    # Obrigatório com 3 posições para NF-e (55), NF3-e (66) e NFC-e (65) de emissão própria
    # Para NF-e (55) e NF3-e (66) de terceiros também é obrigatório
    if cod_mod in ["55", "65", "66"]:
        if ind_emit == "0":  # Emissão própria
            if not ser:
                ser = "000"  # Se não existir série, informar 000
            elif len(ser) != 3:
                return None
        elif cod_mod in ["55", "66"]:  # NF-e e NF3-e de terceiros também precisam de série
            if not ser:
                ser = "000"
            elif len(ser) != 3:
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
    
    # CHV_NFE: obrigatório condicional
    # Obrigatório para COD_MOD = "55", "65", "66"
    if cod_mod in ["55", "65", "66"]:
        if not chv_nfe:
            return None
        if len(chv_nfe) != 44 or not chv_nfe.isdigit():
            return None
        # Valida dígito verificador apenas para emissão própria
        if ind_emit == "0":
            if not _validar_chave_doc_eletronico(chv_nfe):
                return None
        # Nota: Validações de CNPJ base, número do documento, série e UF não podem ser feitas
        # sem acesso ao registro 0000 e aos dados da chave
    
    # DT_DOC: obrigatório, formato DDMMAAAA
    if not dt_doc:
        return None
    dt_doc_valida, dt_doc_obj = _validar_data(dt_doc)
    if not dt_doc_valida:
        return None
    # Nota: Validações de DT_DOC contra DT_INI e DT_FIN do registro 0000 não podem ser feitas
    # sem acesso ao registro 0000
    
    # COD_MUN_SERV: obrigatório, 7 dígitos
    if not cod_mun_serv:
        return None
    if len(cod_mun_serv) != 7 or not cod_mun_serv.isdigit():
        return None
    # Nota: Validação contra tabela IBGE não pode ser feita diretamente
    
    # Todos os campos de valor são obrigatórios e numéricos com 2 decimais, não negativos
    campos_valor = {
        "VL_CONT": vl_cont,
        "VL_MAT_TERC": vl_mat_terc,
        "VL_SUB": vl_sub,
        "VL_ISNT_ISS": vl_isnt_iss,
        "VL_DED_BC": vl_ded_bc,
        "VL_BC_ISS": vl_bc_iss,
        "VL_BC_ISS_RT": vl_bc_iss_rt,
        "VL_ISS_RT": vl_iss_rt,
        "VL_ISS": vl_iss
    }
    
    valores = {}
    for campo_nome, campo_valor in campos_valor.items():
        if not campo_valor:
            return None
        campo_valido, campo_float, campo_erro = validar_valor_numerico(campo_valor, decimais=2, obrigatorio=True, nao_negativo=True)
        if not campo_valido:
            return None
        valores[campo_nome] = campo_float
    
    # Validação: Se COD_MOD = "65", VL_ISS_RT deve ser igual a zero
    if cod_mod == "65" and valores["VL_ISS_RT"] != 0.0:
        return None
    
    # COD_INF_OBS: opcional condicional, até 60 caracteres
    # Nota: Validação contra registro 0460 não pode ser feita diretamente
    if cod_inf_obs and len(cod_inf_obs) > 60:
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
        "02": "Documento cancelado",
        "06": "Documento inutilizado",
        "08": "Documento denegado"
    }
    
    # Formatação de valores monetários para exibição
    def formatar_valor(valor_str):
        if not valor_str:
            return ""
        try:
            valor_float = float(valor_str)
            return f"{valor_float:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        except ValueError:
            return valor_str
    
    # Formatação de data para exibição
    def formatar_data(data_str):
        if not data_str or len(data_str) != 8:
            return ""
        try:
            return f"{data_str[:2]}/{data_str[2:4]}/{data_str[4:8]}"
        except:
            return data_str
    
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
            "titulo": "Código do participante (campo 02 do Registro 0150)",
            "valor": cod_part if cod_part else ""
        },
        "COD_MOD": {
            "titulo": "Código do modelo do documento fiscal, conforme a Tabela 4.1.3",
            "valor": cod_mod
        },
        "COD_SIT": {
            "titulo": "Código da situação do documento conforme tabela 4.1.2",
            "valor": cod_sit,
            "descricao": cod_sit_desc.get(cod_sit, "")
        },
        "SER": {
            "titulo": "Série do documento fiscal",
            "valor": ser if ser else ""
        },
        "NUM_DOC": {
            "titulo": "Número do documento fiscal",
            "valor": num_doc
        },
        "CHV_NFE": {
            "titulo": "Chave da Nota Fiscal Eletrônica",
            "valor": chv_nfe if chv_nfe else ""
        },
        "DT_DOC": {
            "titulo": "Data da emissão do documento fiscal",
            "valor": dt_doc,
            "valor_formatado": formatar_data(dt_doc)
        },
        "COD_MUN_SERV": {
            "titulo": "Código do município onde o serviço foi prestado, conforme a tabela IBGE",
            "valor": cod_mun_serv
        },
        "VL_CONT": {
            "titulo": "Valor contábil (valor total do documento)",
            "valor": vl_cont,
            "valor_formatado": formatar_valor(vl_cont)
        },
        "VL_MAT_TERC": {
            "titulo": "Valor do material fornecido por terceiros na prestação do serviço",
            "valor": vl_mat_terc,
            "valor_formatado": formatar_valor(vl_mat_terc)
        },
        "VL_SUB": {
            "titulo": "Valor da subempreitada",
            "valor": vl_sub,
            "valor_formatado": formatar_valor(vl_sub)
        },
        "VL_ISNT_ISS": {
            "titulo": "Valor das operações isentas ou não-tributadas pelo ISS",
            "valor": vl_isnt_iss,
            "valor_formatado": formatar_valor(vl_isnt_iss)
        },
        "VL_DED_BC": {
            "titulo": "Valor da dedução da base de cálculo",
            "valor": vl_ded_bc,
            "valor_formatado": formatar_valor(vl_ded_bc)
        },
        "VL_BC_ISS": {
            "titulo": "Valor da base de cálculo do ISS",
            "valor": vl_bc_iss,
            "valor_formatado": formatar_valor(vl_bc_iss)
        },
        "VL_BC_ISS_RT": {
            "titulo": "Valor da base de cálculo de retenção do ISS",
            "valor": vl_bc_iss_rt,
            "valor_formatado": formatar_valor(vl_bc_iss_rt)
        },
        "VL_ISS_RT": {
            "titulo": "Valor do ISS retido pelo tomador",
            "valor": vl_iss_rt,
            "valor_formatado": formatar_valor(vl_iss_rt)
        },
        "VL_ISS": {
            "titulo": "Valor do ISS destacado",
            "valor": vl_iss,
            "valor_formatado": formatar_valor(vl_iss)
        },
        "COD_INF_OBS": {
            "titulo": "Código da observação do lançamento fiscal (campo 02 do Registro 0460)",
            "valor": cod_inf_obs if cod_inf_obs else ""
        }
    }
    
    return resultado


def validar_b020(linhas):
    """
    Valida uma ou mais linhas do registro B020 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |B020|IND_OPER|IND_EMIT|COD_PART|COD_MOD|COD_SIT|SER|NUM_DOC|CHV_NFE|DT_DOC|COD_MUN_SERV|VL_CONT|VL_MAT_TERC|VL_SUB|VL_ISNT_ISS|VL_DED_BC|VL_BC_ISS|VL_BC_ISS_RT|VL_ISS_RT|VL_ISS|COD_INF_OBS|
        
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
        resultado = _processar_linha_b020(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
