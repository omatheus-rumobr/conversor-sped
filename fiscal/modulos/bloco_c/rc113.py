import re
import json
from datetime import datetime


def _processar_linha_c113(linha):
    """
    Processa uma única linha do registro C113 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |C113|IND_OPER|IND_EMIT|COD_PART|COD_MOD|SER|SUB|NUM_DOC|DT_DOC|CHV_DOCe|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |C113|...|)
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
    if reg != "C113":
        return None
    
    # Função auxiliar para obter campo ou string vazia
    def obter_campo(indice):
        if indice < len(partes):
            valor = partes[indice].strip()
            return valor if valor else ""
        return ""
    
    # Extrai todos os campos (10 campos no total)
    ind_oper = obter_campo(1)
    ind_emit = obter_campo(2)
    cod_part = obter_campo(3)
    cod_mod = obter_campo(4)
    ser = obter_campo(5)
    sub = obter_campo(6)
    num_doc = obter_campo(7)
    dt_doc = obter_campo(8)
    chv_doce = obter_campo(9)
    
    # Validação do campo IND_OPER: valores válidos [0, 1]
    if not ind_oper or ind_oper not in ["0", "1"]:
        return None
    
    # Validação do campo IND_EMIT: valores válidos [0, 1]
    if not ind_emit or ind_emit not in ["0", "1"]:
        return None
    
    # Validação: se IND_EMIT = 1, então IND_OPER deve ser 0
    if ind_emit == "1" and ind_oper != "0":
        return None
    
    # Validação do campo COD_PART: obrigatório
    if not cod_part:
        return None
    
    # Validação do campo COD_MOD: obrigatório, não pode ser "2D", "02" ou "2E"
    if not cod_mod:
        return None
    
    if cod_mod in ["2D", "02", "2E"]:
        return None
    
    # Validação do campo SUB: se preenchido, deve ser numérico
    if sub:
        try:
            int(sub)
        except ValueError:
            return None
    
    # Validação do campo NUM_DOC: obrigatório, numérico, maior que 0
    if not num_doc:
        return None
    
    try:
        num_doc_int = int(num_doc)
        if num_doc_int <= 0:
            return None
    except ValueError:
        return None
    
    # Validação de formato de data (ddmmaaaa)
    def validar_data(data_str):
        if not data_str:
            return False  # DT_DOC é obrigatório
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
    
    # Valida formato da data (obrigatória)
    if not validar_data(dt_doc):
        return None
    
    # Validação do campo CHV_DOCe: se preenchido, deve ter 44 caracteres
    if chv_doce and len(chv_doce) != 44:
        return None
    
    # Monta o dicionário com título e valor
    descricoes_ind_oper = {
        "0": "Entrada/aquisição",
        "1": "Saída/prestação"
    }
    
    descricoes_ind_emit = {
        "0": "Emissão própria",
        "1": "Terceiros"
    }
    
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "IND_OPER": {
            "titulo": "Indicador do Tipo de Operação",
            "valor": ind_oper,
            "descricao": descricoes_ind_oper.get(ind_oper, "")
        },
        "IND_EMIT": {
            "titulo": "Indicador do Emitente do Título",
            "valor": ind_emit,
            "descricao": descricoes_ind_emit.get(ind_emit, "")
        },
        "COD_PART": {
            "titulo": "Código do Participante Emitente do Documento Referenciado",
            "valor": cod_part
        },
        "COD_MOD": {
            "titulo": "Código do Documento Fiscal",
            "valor": cod_mod
        },
        "SER": {
            "titulo": "Série do Documento Fiscal",
            "valor": ser
        },
        "SUB": {
            "titulo": "Subsérie do Documento Fiscal",
            "valor": sub
        },
        "NUM_DOC": {
            "titulo": "Número do Documento Fiscal",
            "valor": num_doc
        },
        "DT_DOC": {
            "titulo": "Data da Emissão do Documento Fiscal",
            "valor": dt_doc
        },
        "CHV_DOCe": {
            "titulo": "Chave do Documento Eletrônico",
            "valor": chv_doce
        }
    }
    
    return resultado


def validar_c113(linhas):
    """
    Valida e processa uma ou múltiplas linhas do registro C113 (Documento Fiscal Referenciado) do SPED.
    
    Este registro tem por objetivo informar, detalhadamente, outros documentos fiscais que tenham sido mencionados nas
    informações complementares do documento que está sendo escriturado no registro C100.
    
    Args:
        linhas: Pode ser:
                - Uma string com uma linha do SPED
                - Uma lista de strings (cada string é uma linha)
                - Uma string com múltiplas linhas separadas por \\n
                Formato: |C113|IND_OPER|IND_EMIT|COD_PART|COD_MOD|SER|SUB|NUM_DOC|DT_DOC|CHV_DOCe|
        
    Returns:
        str: JSON com um array contendo os campos validados de cada linha processada.
             Retorna um array vazio [] se nenhuma linha válida for encontrada.
             Retorna None se o input for inválido.
        
    Validações principais:
        - Campo REG deve ser exatamente "C113"
        - IND_OPER: obrigatório, valores válidos [0, 1]
          - 0: Entrada/aquisição
          - 1: Saída/prestação
        - IND_EMIT: obrigatório, valores válidos [0, 1]
          - 0: Emissão própria
          - 1: Terceiros
          - Se IND_EMIT = 1, então IND_OPER deve ser 0
        - COD_PART: obrigatório
        - COD_MOD: obrigatório, não pode ser "2D", "02" ou "2E"
        - SER: opcional, série do documento fiscal
        - SUB: opcional, subsérie do documento fiscal (numérico)
        - NUM_DOC: obrigatório, número do documento fiscal (numérico, maior que 0)
        - DT_DOC: obrigatório, data no formato ddmmaaaa
        - CHV_DOCe: opcional, chave do documento eletrônico (44 caracteres)
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
        resultado = _processar_linha_c113(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    # Retorna JSON com array de resultados
    return json.dumps(resultados, ensure_ascii=False, indent=2)