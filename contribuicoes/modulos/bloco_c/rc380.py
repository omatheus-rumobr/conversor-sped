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


def _processar_linha_c380(linha):
    """
    Processa uma única linha do registro C380 e retorna um dicionário.
    
    Formato:
      |C380|COD_MOD|DT_DOC_INI|DT_DOC_FIN|NUM_DOC_INI|NUM_DOC_FIN|VL_DOC|VL_DOC_CANC|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "C380"
    - COD_MOD: obrigatório, código do modelo do documento fiscal (2 caracteres)
      - Valor válido: [02]
      - 02: Nota Fiscal de Venda a Consumidor
    - DT_DOC_INI: obrigatório, data de emissão inicial dos documentos (ddmmaaaa)
    - DT_DOC_FIN: obrigatório, data de emissão final dos documentos (ddmmaaaa)
      - Deve ser >= DT_DOC_INI
    - NUM_DOC_INI: opcional, número do documento fiscal inicial (6 dígitos)
      - Se preenchido, deve ser maior que 0
      - Se NUM_DOC_INI e NUM_DOC_FIN estiverem preenchidos, NUM_DOC_INI <= NUM_DOC_FIN
    - NUM_DOC_FIN: opcional, número do documento fiscal final (6 dígitos)
      - Se preenchido, deve ser maior que 0
      - Se NUM_DOC_INI e NUM_DOC_FIN estiverem preenchidos, NUM_DOC_FIN >= NUM_DOC_INI
    - VL_DOC: obrigatório, valor total dos documentos emitidos (numérico, 2 decimais, não negativo)
    - VL_DOC_CANC: obrigatório, valor total dos documentos cancelados (numérico, 2 decimais, não negativo)
    
    Nota: No registro C380 e filhos deve a pessoa jurídica escriturar as notas fiscais de venda ao consumidor
    não emitidas por ECF (código 02), consolidando os valores dos documentos emitidos no período da escrituração.
    
    Nos registros filhos C381 (PIS/Pasep) e C385 (Cofins) devem ser detalhados os valores por CST, por item
    vendido e por alíquota, conforme o caso.
    
    Os valores de documentos fiscais cancelados não devem ser computados no valor total dos documentos
    (campo VL_DOC), nem nos registros filhos.
    
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
    # Remove primeiro e último se vazios (formato padrão SPED: |C380|...|)
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
    if reg != "C380":
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
    
    # Extrai todos os campos (8 campos no total)
    cod_mod = obter_campo(1)
    dt_doc_ini = obter_campo(2)
    dt_doc_fin = obter_campo(3)
    num_doc_ini = obter_campo(4)
    num_doc_fin = obter_campo(5)
    vl_doc = obter_campo(6)
    vl_doc_canc = obter_campo(7)
    
    # Validações básicas dos campos obrigatórios
    
    # COD_MOD: obrigatório, valor fixo "02"
    if not cod_mod or cod_mod != "02":
        return None
    
    # DT_DOC_INI: obrigatório, data de emissão inicial (ddmmaaaa)
    ok_dt_doc_ini, dt_doc_ini_obj = _validar_data(dt_doc_ini)
    if not ok_dt_doc_ini:
        return None
    
    # DT_DOC_FIN: obrigatório, data de emissão final (ddmmaaaa)
    ok_dt_doc_fin, dt_doc_fin_obj = _validar_data(dt_doc_fin)
    if not ok_dt_doc_fin:
        return None
    
    # Validação: DT_DOC_FIN deve ser >= DT_DOC_INI
    if dt_doc_fin_obj < dt_doc_ini_obj:
        return None
    
    # NUM_DOC_INI: opcional, número do documento inicial (6 dígitos)
    num_doc_ini_int = None
    if num_doc_ini:
        if not num_doc_ini.isdigit() or len(num_doc_ini) > 6:
            return None
        num_doc_ini_int = int(num_doc_ini)
        if num_doc_ini_int <= 0:
            return None
    
    # NUM_DOC_FIN: opcional, número do documento final (6 dígitos)
    num_doc_fin_int = None
    if num_doc_fin:
        if not num_doc_fin.isdigit() or len(num_doc_fin) > 6:
            return None
        num_doc_fin_int = int(num_doc_fin)
        if num_doc_fin_int <= 0:
            return None
    
    # Validação: se ambos NUM_DOC_INI e NUM_DOC_FIN estiverem preenchidos, NUM_DOC_FIN >= NUM_DOC_INI
    if num_doc_ini_int is not None and num_doc_fin_int is not None:
        if num_doc_fin_int < num_doc_ini_int:
            return None
    
    # VL_DOC: obrigatório, valor total dos documentos (numérico, 2 decimais, não negativo)
    ok_vl_doc, val_vl_doc, _ = validar_valor_numerico(vl_doc, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok_vl_doc:
        return None
    
    # VL_DOC_CANC: obrigatório, valor total dos documentos cancelados (numérico, 2 decimais, não negativo)
    ok_vl_doc_canc, val_vl_doc_canc, _ = validar_valor_numerico(vl_doc_canc, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok_vl_doc_canc:
        return None
    
    # Função auxiliar para formatar valores monetários
    def fmt_valor(v):
        if v is None:
            return ""
        return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    # Função auxiliar para formatar data
    def fmt_data(data_str):
        if not data_str or len(data_str) != 8:
            return ""
        return f"{data_str[:2]}/{data_str[2:4]}/{data_str[4:]}"
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "COD_MOD": {
            "titulo": "Código do modelo do documento fiscal, conforme a Tabela 4.1.1 (Código 02 – Nota Fiscal de Venda a Consumidor)",
            "valor": cod_mod,
            "descricao": "Nota Fiscal de Venda a Consumidor"
        },
        "DT_DOC_INI": {
            "titulo": "Data de Emissão Inicial dos Documentos",
            "valor": dt_doc_ini,
            "valor_formatado": fmt_data(dt_doc_ini)
        },
        "DT_DOC_FIN": {
            "titulo": "Data de Emissão Final dos Documentos",
            "valor": dt_doc_fin,
            "valor_formatado": fmt_data(dt_doc_fin)
        },
        "NUM_DOC_INI": {
            "titulo": "Número do documento fiscal inicial",
            "valor": num_doc_ini
        },
        "NUM_DOC_FIN": {
            "titulo": "Número do documento fiscal final",
            "valor": num_doc_fin
        },
        "VL_DOC": {
            "titulo": "Valor total dos documentos emitidos",
            "valor": vl_doc,
            "valor_formatado": fmt_valor(val_vl_doc)
        },
        "VL_DOC_CANC": {
            "titulo": "Valor total dos documentos cancelados",
            "valor": vl_doc_canc,
            "valor_formatado": fmt_valor(val_vl_doc_canc)
        }
    }
    
    return resultado


def validar_c380(linhas):
    """
    Valida uma ou mais linhas do registro C380 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |C380|COD_MOD|DT_DOC_INI|DT_DOC_FIN|NUM_DOC_INI|NUM_DOC_FIN|VL_DOC|VL_DOC_CANC|
        
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
        resultado = _processar_linha_c380(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
