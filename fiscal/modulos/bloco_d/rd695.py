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


def _processar_linha_d695(linha):
    """
    Processa uma única linha do registro D695 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |D695|COD_MOD|SER|NRO_ORD_INI|NRO_ORD_FIN|DT_DOC_INI|DT_DOC_FIN|NOM_MEST|CHV_COD_DIG|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |D695|...|)
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
    if reg != "D695":
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
    
    # Extrai todos os campos (9 campos no total)
    cod_mod = obter_campo(1)
    ser = obter_campo(2)
    nro_ord_ini = obter_campo(3)
    nro_ord_fin = obter_campo(4)
    dt_doc_ini = obter_campo(5)
    dt_doc_fin = obter_campo(6)
    nom_mest = obter_campo(7)
    chv_cod_dig = obter_campo(8)
    
    # Validações dos campos obrigatórios
    
    # COD_MOD: obrigatório, valores válidos: ["21", "22"]
    if not cod_mod or cod_mod not in ["21", "22"]:
        return None
    
    # SER: obrigatório, até 4 caracteres
    if not ser or len(ser) > 4:
        return None
    
    # NRO_ORD_INI: obrigatório, numérico, até 9 dígitos, maior que zero
    if not nro_ord_ini or not nro_ord_ini.isdigit() or len(nro_ord_ini) > 9 or int(nro_ord_ini) <= 0:
        return None
    
    # NRO_ORD_FIN: obrigatório, numérico, até 9 dígitos, maior que zero, >= NRO_ORD_INI
    if not nro_ord_fin or not nro_ord_fin.isdigit() or len(nro_ord_fin) > 9 or int(nro_ord_fin) <= 0:
        return None
    if int(nro_ord_fin) < int(nro_ord_ini):
        return None
    
    # DT_DOC_INI: obrigatório, formato ddmmaaaa
    dt_doc_ini_valido, dt_doc_ini_obj = _validar_data(dt_doc_ini)
    if not dt_doc_ini_valido:
        return None
    
    # DT_DOC_FIN: obrigatório, formato ddmmaaaa, >= DT_DOC_INI
    dt_doc_fin_valido, dt_doc_fin_obj = _validar_data(dt_doc_fin)
    if not dt_doc_fin_valido:
        return None
    if dt_doc_fin_obj < dt_doc_ini_obj:
        return None
    
    # NOM_MEST: obrigatório, até 33 caracteres
    if not nom_mest or len(nom_mest) > 33:
        return None
    
    # CHV_COD_DIG: obrigatório, até 32 caracteres
    if not chv_cod_dig or len(chv_cod_dig) > 32:
        return None
    
    # Formatação de data
    def formatar_data(data_obj):
        if data_obj is None:
            return ""
        return data_obj.strftime("%d/%m/%Y")
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "COD_MOD": {
            "titulo": "Código do modelo do documento fiscal, conforme a Tabela 4.1.1",
            "valor": cod_mod,
            "descricao": {
                "21": "Nota Fiscal de Serviço de Comunicação",
                "22": "Nota Fiscal de Serviço de Telecomunicação"
            }.get(cod_mod, "")
        },
        "SER": {
            "titulo": "Série do documento fiscal",
            "valor": ser
        },
        "NRO_ORD_INI": {
            "titulo": "Número de ordem inicial",
            "valor": nro_ord_ini
        },
        "NRO_ORD_FIN": {
            "titulo": "Número de ordem final",
            "valor": nro_ord_fin
        },
        "DT_DOC_INI": {
            "titulo": "Data de emissão inicial dos documentos / Data inicial de vencimento da fatura",
            "valor": dt_doc_ini,
            "valor_formatado": formatar_data(dt_doc_ini_obj)
        },
        "DT_DOC_FIN": {
            "titulo": "Data de emissão final dos documentos / Data final do vencimento da fatura",
            "valor": dt_doc_fin,
            "valor_formatado": formatar_data(dt_doc_fin_obj)
        },
        "NOM_MEST": {
            "titulo": "Nome do arquivo Mestre de Documento Fiscal",
            "valor": nom_mest
        },
        "CHV_COD_DIG": {
            "titulo": "Chave de codificação digital do arquivo Mestre de Documento Fiscal",
            "valor": chv_cod_dig
        }
    }
    
    return resultado


def validar_d695_fiscal(linhas):
    """
    Valida uma ou mais linhas do registro D695 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |D695|COD_MOD|SER|NRO_ORD_INI|NRO_ORD_FIN|DT_DOC_INI|DT_DOC_FIN|NOM_MEST|CHV_COD_DIG|
        
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
        resultado = _processar_linha_d695(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
