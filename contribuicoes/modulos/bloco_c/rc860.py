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


def validar_valor_inteiro(valor_str, obrigatorio=False, positivo=False, nao_negativo=False):
    """
    Valida um valor inteiro.

    Args:
        valor_str: String com o valor inteiro
        obrigatorio: Se True, o campo não pode estar vazio
        positivo: Se True, o valor deve ser maior que 0
        nao_negativo: Se True, o valor deve ser maior ou igual a 0

    Returns:
        tuple: (True/False, valor int ou None, mensagem de erro ou None)
    """
    if valor_str is None:
        valor_str = ""

    if not valor_str:
        if obrigatorio:
            return False, None, "Campo obrigatório não preenchido"
        return True, 0, None

    try:
        valor_int = int(valor_str)

        if positivo and valor_int <= 0:
            return False, None, "Valor deve ser maior que zero"
        if nao_negativo and valor_int < 0:
            return False, None, "Valor não pode ser negativo"

        return True, valor_int, None
    except ValueError:
        return False, None, "Valor não é inteiro válido"


def _processar_linha_c860(linha):
    """
    Processa uma única linha do registro C860 e retorna um dicionário.
    
    Formato:
      |C860|COD_MOD|NR_SAT|DT_DOC|DOC_INI|DOC_FIM|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "C860"
    - COD_MOD: obrigatório, código do modelo do documento fiscal (2 caracteres)
      - Valores válidos: [59] (Cupom Fiscal Eletrônico)
    - NR_SAT: obrigatório, número de série do equipamento SAT (9 dígitos)
    - DT_DOC: opcional, data de emissão dos documentos fiscais (ddmmaaaa)
      - Validação: deve estar compreendida dentro das datas informadas no registro 0000 (validação em camada superior)
    - DOC_INI: opcional, número do documento inicial (9 dígitos)
      - Validação: deve ser menor ou igual ao DOC_FIM
    - DOC_FIM: opcional, número do documento final (9 dígitos)
      - Validação: deve ser maior ou igual ao DOC_INI
    
    Nota: Este registro tem por objetivo identificar os equipamentos SAT-CF-e.
    
    As operações de vendas com emissão de cupom fiscal eletrônico - CF-e-SAT devem ser escrituradas de forma
    consolidada por equipamento SAT-CF-e (no registro C860), com base nos totais de vendas diárias de cada
    equipamento, sendo as receitas demonstradas e segregadas no registro filho C870, para cada item vendido no dia.
    
    Não poderão ser informados dois ou mais registros com a mesma combinação COD_MOD, NR_SAT, DOC_INI e DOC_FIM
    (validação em camada superior).
    
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
    # Remove primeiro e último se vazios (formato padrão SPED: |C860|...|)
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
    if reg != "C860":
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
    
    # Extrai todos os campos (6 campos no total)
    cod_mod = obter_campo(1)
    nr_sat = obter_campo(2)
    dt_doc = obter_campo(3)
    doc_ini = obter_campo(4)
    doc_fim = obter_campo(5)
    
    # Validações básicas dos campos obrigatórios
    
    # COD_MOD: obrigatório, valores válidos [59]
    if not cod_mod or cod_mod != "59":
        return None
    
    # NR_SAT: obrigatório, número de série do equipamento SAT (9 dígitos)
    if not nr_sat or not nr_sat.isdigit() or len(nr_sat) > 9:
        return None
    
    # DT_DOC: opcional, data de emissão dos documentos fiscais (ddmmaaaa)
    data_dt_doc = None
    if dt_doc:
        ok_dt_doc, data_dt_doc = _validar_data(dt_doc)
        if not ok_dt_doc:
            return None
    
    # DOC_INI: opcional, número do documento inicial (9 dígitos)
    ok_doc_ini, val_doc_ini, _ = validar_valor_inteiro(doc_ini, obrigatorio=False, nao_negativo=True)
    if not ok_doc_ini:
        return None
    if doc_ini and len(doc_ini) > 9:
        return None
    
    # DOC_FIM: opcional, número do documento final (9 dígitos)
    ok_doc_fim, val_doc_fim, _ = validar_valor_inteiro(doc_fim, obrigatorio=False, nao_negativo=True)
    if not ok_doc_fim:
        return None
    if doc_fim and len(doc_fim) > 9:
        return None
    
    # Validação: DOC_FIM >= DOC_INI quando ambos estiverem preenchidos
    if doc_ini and doc_fim and val_doc_fim is not None and val_doc_ini is not None:
        if val_doc_fim < val_doc_ini:
            return None
    
    # Função auxiliar para formatar data
    def fmt_data(data_str):
        if not data_str or len(data_str) != 8:
            return ""
        return f"{data_str[:2]}/{data_str[2:4]}/{data_str[4:]}"
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg,
            "descricao": "Texto fixo contendo 'C860'"
        },
        "COD_MOD": {
            "titulo": "Código do modelo do documento fiscal",
            "valor": cod_mod,
            "descricao": "Cupom Fiscal Eletrônico"
        },
        "NR_SAT": {
            "titulo": "Número de Série do equipamento SAT",
            "valor": nr_sat
        },
        "DT_DOC": {
            "titulo": "Data de emissão dos documentos fiscais",
            "valor": dt_doc,
            "valor_formatado": fmt_data(dt_doc) if dt_doc else ""
        },
        "DOC_INI": {
            "titulo": "Número do documento inicial",
            "valor": doc_ini
        },
        "DOC_FIM": {
            "titulo": "Número do documento final",
            "valor": doc_fim
        }
    }
    
    return resultado


def validar_c860(linhas):
    """
    Valida uma ou mais linhas do registro C860 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |C860|COD_MOD|NR_SAT|DT_DOC|DOC_INI|DOC_FIM|
        
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
        resultado = _processar_linha_c860(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
