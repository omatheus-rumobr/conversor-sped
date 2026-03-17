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


def _processar_linha_d200(linha):
    """
    Processa uma única linha do registro D200 e retorna um dicionário.
    
    Formato:
      |D200|COD_MOD|COD_SIT|SER|SUB|NUM_DOC_INI|NUM_DOC_FIN|CFOP|DT_REF|VL_DOC|VL_DESC|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "D200"
    - COD_MOD: obrigatório, valores válidos [07, 08, 8B, 09, 10, 11, 26, 27, 57, 63, 67]
    - COD_SIT: obrigatório, valores válidos [00, 01, 06, 07, 08]
      - Não deve considerar documentos cancelados, denegados ou de numeração inutilizada
    - SER: opcional, máximo 4 caracteres
    - SUB: opcional, máximo 3 caracteres
    - NUM_DOC_INI: obrigatório, máximo 9 dígitos, deve ser > 0, e deve ser <= NUM_DOC_FIN
    - NUM_DOC_FIN: obrigatório, máximo 9 dígitos, deve ser > 0, e deve ser >= NUM_DOC_INI
    - CFOP: obrigatório, 4 dígitos
    - DT_REF: obrigatório, formato ddmmaaaa, data válida
    - VL_DOC: obrigatório, numérico com 2 decimais
    - VL_DESC: opcional, numérico com 2 decimais
    
    Nota: Escriturar neste registro a consolidação diária dos documentos fiscais válidos, referentes
    à prestação de serviços de transportes no período da escrituração. Devem ser informados apenas
    os documentos fiscais válidos.
    
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
    # Remove primeiro e último se vazios (formato padrão SPED: |D200|...|)
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
    if reg != "D200":
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
    
    # Extrai todos os campos (11 campos no total)
    cod_mod = obter_campo(1)
    cod_sit = obter_campo(2)
    ser = obter_campo(3)
    sub = obter_campo(4)
    num_doc_ini = obter_campo(5)
    num_doc_fin = obter_campo(6)
    cfop = obter_campo(7)
    dt_ref = obter_campo(8)
    vl_doc = obter_campo(9)
    vl_desc = obter_campo(10)
    
    # Validações básicas dos campos obrigatórios
    
    # COD_MOD: obrigatório, valores válidos [07, 08, 8B, 09, 10, 11, 26, 27, 57, 63, 67]
    cod_mod_validos = ["07", "08", "8B", "09", "10", "11", "26", "27", "57", "63", "67"]
    if not cod_mod or cod_mod not in cod_mod_validos:
        return None
    
    # COD_SIT: obrigatório, valores válidos [00, 01, 06, 07, 08]
    cod_sit_validos = ["00", "01", "06", "07", "08"]
    if not cod_sit or cod_sit not in cod_sit_validos:
        return None
    
    # SER: opcional, máximo 4 caracteres
    if ser and len(ser) > 4:
        return None
    
    # SUB: opcional, máximo 3 caracteres
    if sub and len(sub) > 3:
        return None
    
    # NUM_DOC_INI: obrigatório, máximo 9 dígitos, deve ser > 0
    if not num_doc_ini:
        return None
    if not num_doc_ini.isdigit() or len(num_doc_ini) > 9:
        return None
    num_doc_ini_int = int(num_doc_ini)
    if num_doc_ini_int <= 0:
        return None
    
    # NUM_DOC_FIN: obrigatório, máximo 9 dígitos, deve ser > 0
    if not num_doc_fin:
        return None
    if not num_doc_fin.isdigit() or len(num_doc_fin) > 9:
        return None
    num_doc_fin_int = int(num_doc_fin)
    if num_doc_fin_int <= 0:
        return None
    
    # Validação: NUM_DOC_INI deve ser <= NUM_DOC_FIN
    if num_doc_ini_int > num_doc_fin_int:
        return None
    
    # CFOP: obrigatório, 4 dígitos
    if not cfop or not cfop.isdigit() or len(cfop) != 4:
        return None
    
    # DT_REF: obrigatório, formato ddmmaaaa, data válida
    dt_ref_valido, dt_ref_obj = _validar_data(dt_ref)
    if not dt_ref_valido:
        return None
    
    # VL_DOC: obrigatório, numérico com 2 decimais
    ok1, val1, _ = validar_valor_numerico(vl_doc, decimais=2, obrigatorio=True)
    if not ok1:
        return None
    
    # VL_DESC: opcional, numérico com 2 decimais
    ok2, val2, _ = validar_valor_numerico(vl_desc, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok2:
        return None
    
    # Função auxiliar para formatar valores monetários
    def fmt_valor(v):
        if v is None:
            return ""
        return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    # Função auxiliar para formatar data
    def fmt_data(dt):
        if dt:
            return dt.strftime("%d/%m/%Y")
        return ""
    
    # Descrições dos campos
    descricoes_cod_mod = {
        "07": "Nota Fiscal de Serviço de Transporte",
        "08": "Conhecimento de Transporte Rodoviário de Cargas",
        "8B": "Conhecimento de Transporte de Cargas Avulso",
        "09": "Conhecimento de Transporte Aquaviário de Cargas",
        "10": "Conhecimento de Transporte Aéreo",
        "11": "Conhecimento de Transporte Ferroviário de Cargas",
        "26": "Conhecimento de Transporte Multimodal de Cargas",
        "27": "Nota Fiscal de Transporte Ferroviário de Carga",
        "57": "Conhecimento de Transporte Eletrônico – CT-E",
        "63": "Bilhete de Passagem Eletrônico - BP-e",
        "67": "Conhecimento de Transporte Eletrônico para Outros Serviços – CT-e OS"
    }
    
    descricoes_cod_sit = {
        "00": "Documento regular",
        "01": "Documento regular extemporâneo",
        "06": "Documento regular extemporâneo",
        "07": "Documento regular com pendência de entrega",
        "08": "Documento regular com pendência de entrega"
    }
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "COD_MOD": {
            "titulo": "Código do modelo do documento fiscal, conforme a Tabela 4.1.1",
            "valor": cod_mod,
            "descricao": descricoes_cod_mod.get(cod_mod, "")
        },
        "COD_SIT": {
            "titulo": "Código da situação do documento fiscal, conforme a Tabela 4.1.2",
            "valor": cod_sit,
            "descricao": descricoes_cod_sit.get(cod_sit, "")
        },
        "SER": {
            "titulo": "Série do documento fiscal",
            "valor": ser
        },
        "SUB": {
            "titulo": "Subsérie do documento fiscal",
            "valor": sub
        },
        "NUM_DOC_INI": {
            "titulo": "Número do documento fiscal inicial emitido no período (mesmo modelo, série e subsérie)",
            "valor": num_doc_ini
        },
        "NUM_DOC_FIN": {
            "titulo": "Número do documento fiscal final emitido no período (mesmo modelo, série e subsérie)",
            "valor": num_doc_fin
        },
        "CFOP": {
            "titulo": "Código Fiscal de Operação e Prestação conforme tabela indicada no item 4.2.2",
            "valor": cfop
        },
        "DT_REF": {
            "titulo": "Data do dia de referência do resumo diário",
            "valor": dt_ref,
            "valor_formatado": fmt_data(dt_ref_obj)
        },
        "VL_DOC": {
            "titulo": "Valor total dos documentos fiscais",
            "valor": vl_doc,
            "valor_formatado": fmt_valor(val1)
        },
        "VL_DESC": {
            "titulo": "Valor total dos descontos",
            "valor": vl_desc,
            "valor_formatado": fmt_valor(val2) if vl_desc else ""
        }
    }
    
    return resultado


def validar_d200(linhas):
    """
    Valida uma ou mais linhas do registro D200 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |D200|COD_MOD|COD_SIT|SER|SUB|NUM_DOC_INI|NUM_DOC_FIN|CFOP|DT_REF|VL_DOC|VL_DESC|
        
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
        resultado = _processar_linha_d200(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
