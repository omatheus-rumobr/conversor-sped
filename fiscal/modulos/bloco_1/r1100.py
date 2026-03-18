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


def _processar_linha_1100(linha):
    """
    Processa uma única linha do registro 1100 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |1100|IND_DOC|NRO_DE|DT_DE|NAT_EXP|NRO_RE|DT_RE|CHC_EMB|DT_CHC|DT_AVB|TP_CHC|PAIS|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |1100|...|)
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
    if reg != "1100":
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
    
    # Extrai todos os campos (12 campos no total)
    ind_doc = obter_campo(1)
    nro_de = obter_campo(2)
    dt_de = obter_campo(3)
    nat_exp = obter_campo(4)
    nro_re = obter_campo(5)
    dt_re = obter_campo(6)
    chc_emb = obter_campo(7)
    dt_chc = obter_campo(8)
    dt_avb = obter_campo(9)
    tp_chc = obter_campo(10)
    pais = obter_campo(11)
    
    # Validações básicas dos campos obrigatórios
    # IND_DOC: obrigatório, valores válidos [0, 1, 2]
    if not ind_doc or ind_doc not in ["0", "1", "2"]:
        return None
    
    # NRO_DE: obrigatório, até 14 caracteres
    if not nro_de or len(nro_de) > 14:
        return None
    
    # DT_DE: obrigatório, formato DDMMAAAA
    if not dt_de:
        return None
    dt_de_valida, dt_de_obj = _validar_data(dt_de)
    if not dt_de_valida:
        return None
    
    # NAT_EXP: obrigatório, valores válidos [0, 1]
    if not nat_exp or nat_exp not in ["0", "1"]:
        return None
    
    # NRO_RE e DT_RE: obrigatórios condicionais (se IND_DOC = 0)
    if ind_doc == "0":
        if not nro_re or len(nro_re) > 12:
            return None
        if not dt_re:
            return None
        dt_re_valida, dt_re_obj = _validar_data(dt_re)
        if not dt_re_valida:
            return None
    
    # CHC_EMB e DT_CHC: obrigatórios condicionais (se informados, devem ser válidos)
    if chc_emb:
        if len(chc_emb) > 18:
            return None
        if dt_chc:
            dt_chc_valida, dt_chc_obj = _validar_data(dt_chc)
            if not dt_chc_valida:
                return None
    
    # DT_AVB: obrigatório, formato DDMMAAAA
    if not dt_avb:
        return None
    dt_avb_valida, dt_avb_obj = _validar_data(dt_avb)
    if not dt_avb_valida:
        return None
    
    # TP_CHC: obrigatório, valores válidos conforme manual
    tp_chc_validos = ["01", "02", "03", "04", "06", "07", "08", "09", "10", "11", "12", "13", "14", 
                      "16", "17", "18", "19", "20", "91", "92", "93", "99"]
    if not tp_chc or tp_chc not in tp_chc_validos:
        return None
    
    # PAIS: obrigatório, 3 dígitos
    if not pais or len(pais) != 3 or not pais.isdigit():
        return None
    
    # Mapeamento de descrições
    ind_doc_desc = {
        "0": "Declaração de Exportação",
        "1": "Declaração Simplificada de Exportação",
        "2": "Declaração Única de Exportação"
    }
    
    nat_exp_desc = {
        "0": "Exportação Direta",
        "1": "Exportação Indireta"
    }
    
    tp_chc_desc = {
        "01": "AWB",
        "02": "MAWB",
        "03": "HAWB",
        "04": "COMAT",
        "06": "R. EXPRESSAS",
        "07": "ETIQ. REXPRESSAS",
        "08": "HR. EXPRESSAS",
        "09": "AV7",
        "10": "BL",
        "11": "MBL",
        "12": "HBL",
        "13": "CRT",
        "14": "DSIC",
        "16": "COMAT BL",
        "17": "RWB",
        "18": "HRWB",
        "19": "TIF/DTA",
        "20": "CP2",
        "91": "NÃO IATA",
        "92": "MNAO IATA",
        "93": "HNAO IATA",
        "99": "OUTROS"
    }
    
    # Formatação de datas para exibição
    def formatar_data(data_str):
        if len(data_str) == 8 and data_str.isdigit():
            return f"{data_str[:2]}/{data_str[2:4]}/{data_str[4:8]}"
        return data_str
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "IND_DOC": {
            "titulo": "Tipo de documento",
            "valor": ind_doc,
            "descricao": ind_doc_desc.get(ind_doc, "")
        },
        "NRO_DE": {
            "titulo": "Número da declaração",
            "valor": nro_de
        },
        "DT_DE": {
            "titulo": "Data da declaração",
            "valor": dt_de,
            "valor_formatado": formatar_data(dt_de)
        },
        "NAT_EXP": {
            "titulo": "Natureza da exportação",
            "valor": nat_exp,
            "descricao": nat_exp_desc.get(nat_exp, "")
        }
    }
    
    # Adiciona campos condicionais se IND_DOC = 0
    if ind_doc == "0":
        resultado["NRO_RE"] = {
            "titulo": "Nº do registro de Exportação",
            "valor": nro_re
        }
        resultado["DT_RE"] = {
            "titulo": "Data do Registro de Exportação",
            "valor": dt_re,
            "valor_formatado": formatar_data(dt_re)
        }
    
    # Adiciona campos condicionais se informados
    if chc_emb:
        resultado["CHC_EMB"] = {
            "titulo": "Nº do conhecimento de embarque",
            "valor": chc_emb
        }
        if dt_chc:
            resultado["DT_CHC"] = {
                "titulo": "Data do conhecimento de embarque",
                "valor": dt_chc,
                "valor_formatado": formatar_data(dt_chc)
            }
    
    resultado["DT_AVB"] = {
        "titulo": "Data da averbação da Declaração de exportação",
        "valor": dt_avb,
        "valor_formatado": formatar_data(dt_avb)
    }
    
    resultado["TP_CHC"] = {
        "titulo": "Tipo de conhecimento de embarque",
        "valor": tp_chc,
        "descricao": tp_chc_desc.get(tp_chc, "")
    }
    
    resultado["PAIS"] = {
        "titulo": "Código do país de destino da mercadoria",
        "valor": pais
    }
    
    return resultado


def validar_1100_fiscal(linhas):
    """
    Valida uma ou mais linhas do registro 1100 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |1100|IND_DOC|NRO_DE|DT_DE|NAT_EXP|NRO_RE|DT_RE|CHC_EMB|DT_CHC|DT_AVB|TP_CHC|PAIS|
        
    Returns:
        String JSON com array de objetos contendo os campos validados.
        Cada objeto tem a estrutura {"CAMPO": {"titulo": "...", "valor": "...", "descricao": "..."}}.
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
        resultado = _processar_linha_1100(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
