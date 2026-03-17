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


def _processar_linha_p210(linha):
    """
    Processa uma única linha do registro P210 e retorna um dicionário.
    
    Formato:
      |P210|IND_AJ|VL_AJ|COD_AJ|NUM_DOC|DESCR_AJ|DT_REF|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "P210"
    - IND_AJ: obrigatório, indicador do tipo de ajuste (1 dígito)
      - Valores válidos: [0, 1]
      - 0: Ajuste de redução
      - 1: Ajuste de acréscimo
    - VL_AJ: obrigatório, valor do ajuste (numérico, 2 decimais)
    - COD_AJ: obrigatório, código do ajuste conforme Tabela 4.3.8 (2 caracteres)
    - NUM_DOC: opcional, número do processo, documento ou ato concessório
    - DESCR_AJ: opcional, descrição resumida do ajuste (texto livre)
    - DT_REF: opcional, data de referência do ajuste (formato ddmmaaaa)
    
    Nota: Registro a ser preenchido caso a pessoa jurídica tenha de proceder a ajustes da contribuição
    apurada no período, decorrentes de ação judicial, de processo de consulta, da legislação tributária
    da contribuição, de estorno ou de outras situações.
    
    Este registro será utilizado pela pessoa jurídica para detalhar as informações prestadas nos campos
    04 e 05 do registro pai P200.
    
    A soma de todos os valores do campo VL_AJ deve ser transportada para o campo 04 (VL_TOT_AJ_REDUC)
    ou campo 05 (VL_TOT_AJ_ACRES) do registro P200, de acordo com o indicador de ajuste (campo IND_AJ).
    
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
    # Remove primeiro e último se vazios (formato padrão SPED: |P210|...|)
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
    if reg != "P210":
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
    
    # Extrai todos os campos (7 campos no total)
    ind_aj = obter_campo(1)
    vl_aj = obter_campo(2)
    cod_aj = obter_campo(3)
    num_doc = obter_campo(4)
    descr_aj = obter_campo(5)
    dt_ref = obter_campo(6)
    
    # Validações básicas dos campos obrigatórios
    
    # IND_AJ: obrigatório, valores válidos [0, 1]
    ind_aj_validos = ["0", "1"]
    if not ind_aj or ind_aj not in ind_aj_validos:
        return None
    
    # VL_AJ: obrigatório, valor do ajuste (numérico, 2 decimais)
    ok1, val1, _ = validar_valor_numerico(vl_aj, decimais=2, obrigatorio=True, positivo=True)
    if not ok1:
        return None
    
    # COD_AJ: obrigatório, código do ajuste conforme Tabela 4.3.8 (2 caracteres)
    if not cod_aj or len(cod_aj) != 2:
        return None
    
    # NUM_DOC: opcional, número do processo, documento ou ato concessório
    # Não há validação específica além de ser texto livre
    
    # DESCR_AJ: opcional, descrição resumida do ajuste (texto livre)
    # Não há validação específica além de ser texto livre
    
    # DT_REF: opcional, data de referência do ajuste (formato ddmmaaaa)
    if dt_ref:
        ok_dt, dt_obj = _validar_data(dt_ref)
        if not ok_dt:
            return None
    else:
        dt_obj = None
    
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
    
    # Descrições dos campos
    descricoes_ind_aj = {
        "0": "Ajuste de redução",
        "1": "Ajuste de acréscimo"
    }
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "IND_AJ": {
            "titulo": "Indicador do tipo de ajuste",
            "valor": ind_aj,
            "descricao": descricoes_ind_aj.get(ind_aj, "")
        },
        "VL_AJ": {
            "titulo": "Valor do ajuste",
            "valor": vl_aj,
            "valor_formatado": fmt_valor(val1)
        },
        "COD_AJ": {
            "titulo": "Código do ajuste, conforme a Tabela indicada no item 4.3.8., versão 1.01",
            "valor": cod_aj
        },
        "NUM_DOC": {
            "titulo": "Número do processo, documento ou ato concessório ao qual o ajuste está vinculado, se houver",
            "valor": num_doc
        },
        "DESCR_AJ": {
            "titulo": "Descrição resumida do ajuste",
            "valor": descr_aj
        },
        "DT_REF": {
            "titulo": "Data de referência do ajuste (ddmmaaaa)",
            "valor": dt_ref,
            "valor_formatado": fmt_data(dt_ref) if dt_ref else ""
        }
    }
    
    return resultado


def validar_p210(linhas):
    """
    Valida uma ou mais linhas do registro P210 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |P210|IND_AJ|VL_AJ|COD_AJ|NUM_DOC|DESCR_AJ|DT_REF|
        
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
        resultado = _processar_linha_p210(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
