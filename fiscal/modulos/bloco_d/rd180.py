import re
import json
from datetime import datetime


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


def _validar_cpf(cpf_str):
    """
    Valida o CPF incluindo o dígito verificador.
    
    Args:
        cpf_str: String com o CPF (11 dígitos)
        
    Returns:
        bool: True se válido, False caso contrário
    """
    if not cpf_str or len(cpf_str) != 11 or not cpf_str.isdigit():
        return False
    
    # Verifica se todos os dígitos são iguais (CPFs inválidos conhecidos)
    if len(set(cpf_str)) == 1:
        return False
    
    # Extrai os 9 primeiros dígitos e os 2 dígitos verificadores
    cpf_9 = cpf_str[:9]
    dv1_informado = int(cpf_str[9])
    dv2_informado = int(cpf_str[10])
    
    # Calcula o primeiro dígito verificador
    soma = 0
    multiplicador = 10
    for digito in cpf_9:
        soma += int(digito) * multiplicador
        multiplicador -= 1
    
    resto = soma % 11
    if resto < 2:
        dv1_calculado = 0
    else:
        dv1_calculado = 11 - resto
    
    if dv1_calculado != dv1_informado:
        return False
    
    # Calcula o segundo dígito verificador
    cpf_10 = cpf_9 + str(dv1_calculado)
    soma = 0
    multiplicador = 11
    for digito in cpf_10:
        soma += int(digito) * multiplicador
        multiplicador -= 1
    
    resto = soma % 11
    if resto < 2:
        dv2_calculado = 0
    else:
        dv2_calculado = 11 - resto
    
    return dv2_calculado == dv2_informado


def _validar_cnpj(cnpj_str):
    """
    Valida o CNPJ incluindo o dígito verificador.
    
    Args:
        cnpj_str: String com o CNPJ (14 dígitos)
        
    Returns:
        bool: True se válido, False caso contrário
    """
    if not cnpj_str or len(cnpj_str) != 14 or not cnpj_str.isdigit():
        return False
    
    # Verifica se todos os dígitos são iguais (CNPJs inválidos conhecidos)
    if len(set(cnpj_str)) == 1:
        return False
    
    # Extrai os 12 primeiros dígitos e os 2 dígitos verificadores
    cnpj_12 = cnpj_str[:12]
    dv1_informado = int(cnpj_str[12])
    dv2_informado = int(cnpj_str[13])
    
    # Calcula o primeiro dígito verificador
    multiplicadores1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma = sum(int(cnpj_12[i]) * multiplicadores1[i] for i in range(12))
    resto = soma % 11
    if resto < 2:
        dv1_calculado = 0
    else:
        dv1_calculado = 11 - resto
    
    if dv1_calculado != dv1_informado:
        return False
    
    # Calcula o segundo dígito verificador
    cnpj_13 = cnpj_12 + str(dv1_calculado)
    multiplicadores2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma = sum(int(cnpj_13[i]) * multiplicadores2[i] for i in range(13))
    resto = soma % 11
    if resto < 2:
        dv2_calculado = 0
    else:
        dv2_calculado = 11 - resto
    
    return dv2_calculado == dv2_informado


def _validar_cnpj_cpf(cnpj_cpf_str):
    """
    Valida CNPJ ou CPF baseado no tamanho.
    Se tiver 14 caracteres, valida como CNPJ.
    Se tiver 11 caracteres, valida como CPF.
    
    Args:
        cnpj_cpf_str: String com CNPJ ou CPF
        
    Returns:
        bool: True se válido, False caso contrário
    """
    if not cnpj_cpf_str:
        return False
    
    # Remove espaços e caracteres não numéricos para validação
    cnpj_cpf_limpo = ''.join(filter(str.isdigit, cnpj_cpf_str))
    
    if len(cnpj_cpf_limpo) == 14:
        return _validar_cnpj(cnpj_cpf_limpo)
    elif len(cnpj_cpf_limpo) == 11:
        return _validar_cpf(cnpj_cpf_limpo)
    else:
        return False


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


def _processar_linha_d180(linha):
    """
    Processa uma única linha do registro D180 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |D180|NUM_SEQ|IND_EMIT|CNPJ_CPF_EMIT|UF_EMIT|IE_EMIT|COD_MUN_ORIG|CNPJ_CPF_TOM|UF_TOM|IE_TOM|COD_MUN_DEST|COD_MOD|SER|SUB|NUM_DOC|DT_DOC|VL_DOC|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |D180|...|)
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
    if reg != "D180":
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
    
    # Extrai todos os campos (17 campos no total)
    num_seq = obter_campo(1)
    ind_emit = obter_campo(2)
    cnpj_cpf_emit = obter_campo(3)
    uf_emit = obter_campo(4)
    ie_emit = obter_campo(5)
    cod_mun_orig = obter_campo(6)
    cnpj_cpf_tom = obter_campo(7)
    uf_tom = obter_campo(8)
    ie_tom = obter_campo(9)
    cod_mun_dest = obter_campo(10)
    cod_mod = obter_campo(11)
    ser = obter_campo(12)
    sub = obter_campo(13)
    num_doc = obter_campo(14)
    dt_doc = obter_campo(15)
    vl_doc = obter_campo(16)
    
    # Validações dos campos obrigatórios
    
    # NUM_SEQ: obrigatório, numérico inteiro, não negativo
    if not num_seq:
        return None
    try:
        num_seq_int = int(float(num_seq))  # Permite conversão de float para int
        if num_seq_int < 0:
            return None
    except ValueError:
        return None
    
    # IND_EMIT: obrigatório, valores válidos: ["0", "1"]
    if ind_emit not in ["0", "1"]:
        return None
    
    # CNPJ_CPF_EMIT: obrigatório, 14 ou 11 dígitos, com validação de dígito verificador
    if not cnpj_cpf_emit:
        return None
    cnpj_cpf_emit_limpo = ''.join(filter(str.isdigit, cnpj_cpf_emit))
    if len(cnpj_cpf_emit_limpo) not in [11, 14]:
        return None
    if not _validar_cnpj_cpf(cnpj_cpf_emit_limpo):
        return None
    
    # UF_EMIT: obrigatório, 2 caracteres
    if not uf_emit or len(uf_emit) != 2:
        return None
    
    # IE_EMIT: opcional condicional, até 14 caracteres
    if ie_emit and len(ie_emit) > 14:
        return None
    
    # COD_MUN_ORIG: obrigatório, 7 dígitos, deve existir na Tabela de Municípios do IBGE (ou 9999999 para Exterior)
    if not cod_mun_orig:
        return None
    if not _validar_codigo_municipio(cod_mun_orig):
        return None
    
    # CNPJ_CPF_TOM: obrigatório, 14 ou 11 dígitos, com validação de dígito verificador
    if not cnpj_cpf_tom:
        return None
    cnpj_cpf_tom_limpo = ''.join(filter(str.isdigit, cnpj_cpf_tom))
    if len(cnpj_cpf_tom_limpo) not in [11, 14]:
        return None
    if not _validar_cnpj_cpf(cnpj_cpf_tom_limpo):
        return None
    
    # UF_TOM: obrigatório, 2 caracteres
    if not uf_tom or len(uf_tom) != 2:
        return None
    
    # IE_TOM: opcional condicional, até 14 caracteres
    if ie_tom and len(ie_tom) > 14:
        return None
    
    # COD_MUN_DEST: obrigatório, 7 dígitos, deve existir na Tabela de Municípios do IBGE (ou 9999999 para Exterior)
    if not cod_mun_dest:
        return None
    if not _validar_codigo_municipio(cod_mun_dest):
        return None
    
    # COD_MOD: obrigatório, 2 caracteres
    if not cod_mod or len(cod_mod) > 2:
        return None
    
    # SER: obrigatório, até 4 caracteres
    if not ser or len(ser) > 4:
        return None
    
    # SUB: opcional condicional, até 3 caracteres
    if sub and len(sub) > 3:
        return None
    
    # NUM_DOC: obrigatório, maior que zero
    if not num_doc:
        return None
    if not num_doc.isdigit() or int(num_doc) <= 0:
        return None
    
    # DT_DOC: obrigatório, formato ddmmaaaa
    if not dt_doc:
        return None
    dt_doc_valida, dt_doc_obj = _validar_data(dt_doc)
    if not dt_doc_valida:
        return None
    
    # VL_DOC: obrigatório, numérico com 2 decimais, não negativo
    vl_doc_valido, vl_doc_float, _ = validar_valor_numerico(vl_doc, decimais=2, obrigatorio=True, nao_negativo=True)
    if not vl_doc_valido:
        return None
    
    # Mapeamento de códigos para descrições
    ind_emit_desc = {
        "0": "Emissão própria",
        "1": "Terceiros"
    }
    
    # Formatação de CNPJ/CPF para exibição
    def formatar_cnpj_cpf(cnpj_cpf_str):
        if not cnpj_cpf_str:
            return ""
        # Remove espaços e caracteres não numéricos
        cnpj_cpf_limpo = ''.join(filter(str.isdigit, cnpj_cpf_str))
        if len(cnpj_cpf_limpo) == 14:
            # Formata CNPJ: XX.XXX.XXX/XXXX-XX
            return f"{cnpj_cpf_limpo[:2]}.{cnpj_cpf_limpo[2:5]}.{cnpj_cpf_limpo[5:8]}/{cnpj_cpf_limpo[8:12]}-{cnpj_cpf_limpo[12:14]}"
        elif len(cnpj_cpf_limpo) == 11:
            # Formata CPF: XXX.XXX.XXX-XX
            return f"{cnpj_cpf_limpo[:3]}.{cnpj_cpf_limpo[3:6]}.{cnpj_cpf_limpo[6:9]}-{cnpj_cpf_limpo[9:11]}"
        return cnpj_cpf_str
    
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
        "NUM_SEQ": {
            "titulo": "Número de ordem sequencial do modal",
            "valor": num_seq
        },
        "IND_EMIT": {
            "titulo": "Indicador do emitente do documento fiscal",
            "valor": ind_emit,
            "descricao": ind_emit_desc.get(ind_emit, "")
        },
        "CNPJ_CPF_EMIT": {
            "titulo": "CNPJ ou CPF do participante emitente do modal",
            "valor": cnpj_cpf_emit,
            "valor_formatado": formatar_cnpj_cpf(cnpj_cpf_emit)
        },
        "UF_EMIT": {
            "titulo": "Sigla da unidade da federação do participante emitente do modal",
            "valor": uf_emit
        },
        "IE_EMIT": {
            "titulo": "Inscrição Estadual do participante emitente do modal",
            "valor": ie_emit if ie_emit else ""
        },
        "COD_MUN_ORIG": {
            "titulo": "Código do município de origem do serviço",
            "valor": cod_mun_orig
        },
        "CNPJ_CPF_TOM": {
            "titulo": "CNPJ/CPF do participante tomador do serviço",
            "valor": cnpj_cpf_tom,
            "valor_formatado": formatar_cnpj_cpf(cnpj_cpf_tom)
        },
        "UF_TOM": {
            "titulo": "Sigla da unidade da federação do participante tomador do serviço",
            "valor": uf_tom
        },
        "IE_TOM": {
            "titulo": "Inscrição Estadual do participante tomador do serviço",
            "valor": ie_tom if ie_tom else ""
        },
        "COD_MUN_DEST": {
            "titulo": "Código do município de destino",
            "valor": cod_mun_dest
        },
        "COD_MOD": {
            "titulo": "Código do modelo do documento fiscal",
            "valor": cod_mod
        },
        "SER": {
            "titulo": "Série do documento fiscal",
            "valor": ser
        },
        "SUB": {
            "titulo": "Subsérie do documento fiscal",
            "valor": sub if sub else ""
        },
        "NUM_DOC": {
            "titulo": "Número do documento fiscal",
            "valor": num_doc
        },
        "DT_DOC": {
            "titulo": "Data da emissão do documento fiscal",
            "valor": dt_doc,
            "valor_formatado": formatar_data(dt_doc)
        },
        "VL_DOC": {
            "titulo": "Valor total do documento fiscal",
            "valor": vl_doc,
            "valor_formatado": formatar_valor_monetario(vl_doc_float)
        }
    }
    
    return resultado


def validar_d180(linhas):
    """
    Valida uma ou mais linhas do registro D180 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |D180|NUM_SEQ|IND_EMIT|CNPJ_CPF_EMIT|UF_EMIT|IE_EMIT|COD_MUN_ORIG|CNPJ_CPF_TOM|UF_TOM|IE_TOM|COD_MUN_DEST|COD_MOD|SER|SUB|NUM_DOC|DT_DOC|VL_DOC|
        
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
        resultado = _processar_linha_d180(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
