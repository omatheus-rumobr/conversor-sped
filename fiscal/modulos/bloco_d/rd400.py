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


def _processar_linha_d400(linha):
    """
    Processa uma única linha do registro D400 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |D400|COD_PART|COD_MOD|COD_SIT|SER|SUB|NUM_DOC|DT_DOC|VL_DOC|VL_DESC|VL_SERV|VL_BC_ICMS|VL_ICMS|VL_PIS|VL_COFINS|COD_CTA|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |D400|...|)
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
    if reg != "D400":
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
    
    # Extrai todos os campos (16 campos no total)
    cod_part = obter_campo(1)
    cod_mod = obter_campo(2)
    cod_sit = obter_campo(3)
    ser = obter_campo(4)
    sub = obter_campo(5)
    num_doc = obter_campo(6)
    dt_doc = obter_campo(7)
    vl_doc = obter_campo(8)
    vl_desc = obter_campo(9)
    vl_serv = obter_campo(10)
    vl_bc_icms = obter_campo(11)
    vl_icms = obter_campo(12)
    vl_pis = obter_campo(13)
    vl_cofins = obter_campo(14)
    cod_cta = obter_campo(15)
    
    # Validações dos campos obrigatórios sempre presentes
    
    # COD_MOD: obrigatório, valor válido: "18"
    if not cod_mod or cod_mod != "18":
        return None
    
    # COD_SIT: obrigatório, valores válidos: ["00", "01", "02", "03", "06", "07", "08"]
    if not cod_sit or cod_sit not in ["00", "01", "02", "03", "06", "07", "08"]:
        return None
    
    # NUM_DOC: obrigatório, numérico, maior que zero
    if not num_doc or not num_doc.isdigit() or int(num_doc) <= 0:
        return None
    
    # Validações condicionais baseadas no COD_SIT
    
    # Exceção 1: COD_SIT = "02" ou "03" (cancelado)
    # Apenas REG, COD_SIT, COD_MOD, SER, SUB e NUM_DOC são obrigatórios, demais campos devem estar vazios
    if cod_sit in ["02", "03"]:
        # SER e SUB são obrigatórios nesta exceção
        if not ser or len(ser) > 4:
            return None
        if not sub or not sub.isdigit() or len(sub) > 3:
            return None
        
        # Demais campos devem estar vazios
        if cod_part or dt_doc or vl_doc or vl_desc or vl_serv or vl_bc_icms or vl_icms or vl_pis or vl_cofins or cod_cta:
            return None
        
        # Monta resultado para exceção 1
        resultado = {
            "REG": {"titulo": "Registro", "valor": reg},
            "COD_PART": {"titulo": "Código do participante (campo 02 do Registro 0150): - agência, filial ou posto", "valor": ""},
            "COD_MOD": {"titulo": "Código do modelo do documento fiscal, conforme a Tabela 4.1.1", "valor": cod_mod},
            "COD_SIT": {"titulo": "Código da situação do documento fiscal, conforme a Tabela 4.1.2", "valor": cod_sit},
            "SER": {"titulo": "Série do documento fiscal", "valor": ser},
            "SUB": {"titulo": "Subsérie do documento fiscal", "valor": sub},
            "NUM_DOC": {"titulo": "Número do documento fiscal resumo", "valor": num_doc},
            "DT_DOC": {"titulo": "Data da emissão do documento fiscal", "valor": "", "valor_formatado": ""},
            "VL_DOC": {"titulo": "Valor total do documento fiscal", "valor": "", "valor_formatado": ""},
            "VL_DESC": {"titulo": "Valor acumulado dos descontos", "valor": "", "valor_formatado": ""},
            "VL_SERV": {"titulo": "Valor acumulado da prestação de serviço", "valor": "", "valor_formatado": ""},
            "VL_BC_ICMS": {"titulo": "Valor total da base de cálculo do ICMS", "valor": "", "valor_formatado": ""},
            "VL_ICMS": {"titulo": "Valor total do ICMS", "valor": "", "valor_formatado": ""},
            "VL_PIS": {"titulo": "Valor do PIS", "valor": "", "valor_formatado": ""},
            "VL_COFINS": {"titulo": "Valor da COFINS", "valor": "", "valor_formatado": ""},
            "COD_CTA": {"titulo": "Código da conta analítica contábil debitada/creditada", "valor": ""}
        }
        return resultado
    
    # Exceção 2 e 3: COD_SIT = "06", "07" ou "08"
    # REG, COD_PART, COD_MOD, COD_SIT, SER, SUB, NUM_DOC e DT_DOC são obrigatórios, demais campos são facultativos
    if cod_sit in ["06", "07", "08"]:
        # COD_PART: obrigatório
        if not cod_part or len(cod_part) > 60:
            return None
        
        # SER: obrigatório
        if not ser or len(ser) > 4:
            return None
        
        # SUB: obrigatório
        if not sub or not sub.isdigit() or len(sub) > 3:
            return None
        
        # DT_DOC: obrigatório, formato ddmmaaaa
        dt_doc_valido, dt_doc_obj = _validar_data(dt_doc)
        if not dt_doc_valido:
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
        
        # Formatação
        def formatar_valor_monetario(valor_float):
            if valor_float is None:
                return ""
            return f"R$ {valor_float:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        
        def formatar_data(data_obj):
            if data_obj is None:
                return ""
            return data_obj.strftime("%d/%m/%Y")
        
        resultado = {
            "REG": {"titulo": "Registro", "valor": reg},
            "COD_PART": {"titulo": "Código do participante (campo 02 do Registro 0150): - agência, filial ou posto", "valor": cod_part},
            "COD_MOD": {"titulo": "Código do modelo do documento fiscal, conforme a Tabela 4.1.1", "valor": cod_mod},
            "COD_SIT": {"titulo": "Código da situação do documento fiscal, conforme a Tabela 4.1.2", "valor": cod_sit},
            "SER": {"titulo": "Série do documento fiscal", "valor": ser},
            "SUB": {"titulo": "Subsérie do documento fiscal", "valor": sub},
            "NUM_DOC": {"titulo": "Número do documento fiscal resumo", "valor": num_doc},
            "DT_DOC": {"titulo": "Data da emissão do documento fiscal", "valor": dt_doc, "valor_formatado": formatar_data(dt_doc_obj)},
            "VL_DOC": {"titulo": "Valor total do documento fiscal", "valor": vl_doc if vl_doc else "", "valor_formatado": formatar_valor_monetario(vl_doc_float) if vl_doc else ""},
            "VL_DESC": {"titulo": "Valor acumulado dos descontos", "valor": vl_desc if vl_desc else "", "valor_formatado": formatar_valor_monetario(vl_desc_float) if vl_desc else ""},
            "VL_SERV": {"titulo": "Valor acumulado da prestação de serviço", "valor": vl_serv if vl_serv else "", "valor_formatado": formatar_valor_monetario(vl_serv_float) if vl_serv else ""},
            "VL_BC_ICMS": {"titulo": "Valor total da base de cálculo do ICMS", "valor": vl_bc_icms if vl_bc_icms else "", "valor_formatado": formatar_valor_monetario(vl_bc_icms_float) if vl_bc_icms else ""},
            "VL_ICMS": {"titulo": "Valor total do ICMS", "valor": vl_icms if vl_icms else "", "valor_formatado": formatar_valor_monetario(vl_icms_float) if vl_icms else ""},
            "VL_PIS": {"titulo": "Valor do PIS", "valor": vl_pis if vl_pis else "", "valor_formatado": formatar_valor_monetario(vl_pis_float) if vl_pis else ""},
            "VL_COFINS": {"titulo": "Valor da COFINS", "valor": vl_cofins if vl_cofins else "", "valor_formatado": formatar_valor_monetario(vl_cofins_float) if vl_cofins else ""},
            "COD_CTA": {"titulo": "Código da conta analítica contábil debitada/creditada", "valor": cod_cta if cod_cta else ""}
        }
        return resultado
    
    # Caso normal: COD_SIT = "00" ou "01"
    # Todos os campos obrigatórios devem ser preenchidos
    
    # COD_PART: obrigatório, até 60 caracteres
    if not cod_part or len(cod_part) > 60:
        return None
    
    # SER: opcional condicional, até 4 caracteres
    if ser and len(ser) > 4:
        return None
    
    # SUB: opcional condicional, numérico, até 3 dígitos
    if sub and (not sub.isdigit() or len(sub) > 3):
        return None
    
    # DT_DOC: obrigatório, formato ddmmaaaa
    dt_doc_valido, dt_doc_obj = _validar_data(dt_doc)
    if not dt_doc_valido:
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
    
    # VL_BC_ICMS: opcional condicional, numérico com 2 decimais, não negativo
    vl_bc_icms_valido, vl_bc_icms_float, _ = validar_valor_numerico(vl_bc_icms, decimais=2, obrigatorio=False, nao_negativo=True)
    if not vl_bc_icms_valido:
        return None
    
    # VL_ICMS: opcional condicional, numérico com 2 decimais, não negativo
    vl_icms_valido, vl_icms_float, _ = validar_valor_numerico(vl_icms, decimais=2, obrigatorio=False, nao_negativo=True)
    if not vl_icms_valido:
        return None
    
    # VL_PIS: opcional condicional, numérico com 2 decimais, não negativo
    vl_pis_valido, vl_pis_float, _ = validar_valor_numerico(vl_pis, decimais=2, obrigatorio=False, nao_negativo=True)
    if not vl_pis_valido:
        return None
    
    # VL_COFINS: opcional condicional, numérico com 2 decimais, não negativo
    vl_cofins_valido, vl_cofins_float, _ = validar_valor_numerico(vl_cofins, decimais=2, obrigatorio=False, nao_negativo=True)
    if not vl_cofins_valido:
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
    
    # Monta o resultado
    resultado = {
        "REG": {"titulo": "Registro", "valor": reg},
        "COD_PART": {"titulo": "Código do participante (campo 02 do Registro 0150): - agência, filial ou posto", "valor": cod_part},
        "COD_MOD": {"titulo": "Código do modelo do documento fiscal, conforme a Tabela 4.1.1", "valor": cod_mod},
        "COD_SIT": {"titulo": "Código da situação do documento fiscal, conforme a Tabela 4.1.2", "valor": cod_sit},
        "SER": {"titulo": "Série do documento fiscal", "valor": ser if ser else ""},
        "SUB": {"titulo": "Subsérie do documento fiscal", "valor": sub if sub else ""},
        "NUM_DOC": {"titulo": "Número do documento fiscal resumo", "valor": num_doc},
        "DT_DOC": {"titulo": "Data da emissão do documento fiscal", "valor": dt_doc, "valor_formatado": formatar_data(dt_doc_obj)},
        "VL_DOC": {"titulo": "Valor total do documento fiscal", "valor": vl_doc, "valor_formatado": formatar_valor_monetario(vl_doc_float)},
        "VL_DESC": {"titulo": "Valor acumulado dos descontos", "valor": vl_desc if vl_desc else "", "valor_formatado": formatar_valor_monetario(vl_desc_float) if vl_desc else ""},
        "VL_SERV": {"titulo": "Valor acumulado da prestação de serviço", "valor": vl_serv, "valor_formatado": formatar_valor_monetario(vl_serv_float)},
        "VL_BC_ICMS": {"titulo": "Valor total da base de cálculo do ICMS", "valor": vl_bc_icms if vl_bc_icms else "", "valor_formatado": formatar_valor_monetario(vl_bc_icms_float) if vl_bc_icms else ""},
        "VL_ICMS": {"titulo": "Valor total do ICMS", "valor": vl_icms if vl_icms else "", "valor_formatado": formatar_valor_monetario(vl_icms_float) if vl_icms else ""},
        "VL_PIS": {"titulo": "Valor do PIS", "valor": vl_pis if vl_pis else "", "valor_formatado": formatar_valor_monetario(vl_pis_float) if vl_pis else ""},
        "VL_COFINS": {"titulo": "Valor da COFINS", "valor": vl_cofins if vl_cofins else "", "valor_formatado": formatar_valor_monetario(vl_cofins_float) if vl_cofins else ""},
        "COD_CTA": {"titulo": "Código da conta analítica contábil debitada/creditada", "valor": cod_cta if cod_cta else ""}
    }
    
    return resultado


def validar_d400(linhas):
    """
    Valida uma ou mais linhas do registro D400 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |D400|COD_PART|COD_MOD|COD_SIT|SER|SUB|NUM_DOC|DT_DOC|VL_DOC|VL_DESC|VL_SERV|VL_BC_ICMS|VL_ICMS|VL_PIS|VL_COFINS|COD_CTA|
        
    Returns:
        String JSON com array de objetos contendo os campos validados.
        Cada objeto tem a estrutura {"CAMPO": {"titulo": "...", "valor": "...", "valor_formatado": "..."}}.
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
        resultado = _processar_linha_d400(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
