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


def _processar_linha_a120(linha):
    """
    Processa uma única linha do registro A120 e retorna um dicionário.
    
    Formato:
      |A120|VL_TOT_SERV|VL_BC_PIS|VL_PIS_IMP|DT_PAG_PIS|VL_BC_COFINS|VL_COFINS_IMP|DT_PAG_COFINS|LOC_EXE_SERV|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "A120"
    - VL_TOT_SERV: obrigatório, numérico com 2 decimais, não negativo
    - VL_BC_PIS: obrigatório, numérico com 2 decimais, não negativo
    - VL_PIS_IMP: opcional, numérico com 2 decimais, não negativo
    - DT_PAG_PIS: opcional, formato ddmmaaaa, data válida
    - VL_BC_COFINS: obrigatório, numérico com 2 decimais, não negativo
    - VL_COFINS_IMP: opcional, numérico com 2 decimais, não negativo
    - DT_PAG_COFINS: opcional, formato ddmmaaaa, data válida
    - LOC_EXE_SERV: obrigatório, valores válidos [0, 1]
    
    Nota: Este registro tem por objetivo informar detalhes das operações de importação de serviços
    com direito a crédito, referentes a documento fiscal escriturado em A100 e que no registro filho
    A170 conste CST_PIS ou CST_COFINS gerador de crédito (CST 50 a 56), bem como conste ser o registro
    A170 originário de operação de importação (campo IND_ORIG_CRED = 1). Esta validação deve ser feita
    em uma camada superior.
    
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
    # Remove primeiro e último se vazios (formato padrão SPED: |A120|...|)
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
    if reg != "A120":
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
    vl_tot_serv = obter_campo(1)
    vl_bc_pis = obter_campo(2)
    vl_pis_imp = obter_campo(3)
    dt_pag_pis = obter_campo(4)
    vl_bc_cofins = obter_campo(5)
    vl_cofins_imp = obter_campo(6)
    dt_pag_cofins = obter_campo(7)
    loc_exe_serv = obter_campo(8)
    
    # Validações básicas dos campos obrigatórios
    
    # VL_TOT_SERV: obrigatório, numérico com 2 decimais, não negativo
    ok1, val1, _ = validar_valor_numerico(vl_tot_serv, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok1:
        return None
    
    # VL_BC_PIS: obrigatório, numérico com 2 decimais, não negativo
    ok2, val2, _ = validar_valor_numerico(vl_bc_pis, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok2:
        return None
    
    # VL_PIS_IMP: opcional, numérico com 2 decimais, não negativo
    ok3, val3, _ = validar_valor_numerico(vl_pis_imp, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok3:
        return None
    
    # DT_PAG_PIS: opcional, formato ddmmaaaa, data válida
    dt_pag_pis_obj = None
    if dt_pag_pis:
        dt_pag_pis_valido, dt_pag_pis_obj = _validar_data(dt_pag_pis)
        if not dt_pag_pis_valido:
            return None
    
    # VL_BC_COFINS: obrigatório, numérico com 2 decimais, não negativo
    ok4, val4, _ = validar_valor_numerico(vl_bc_cofins, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok4:
        return None
    
    # VL_COFINS_IMP: opcional, numérico com 2 decimais, não negativo
    ok5, val5, _ = validar_valor_numerico(vl_cofins_imp, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok5:
        return None
    
    # DT_PAG_COFINS: opcional, formato ddmmaaaa, data válida
    dt_pag_cofins_obj = None
    if dt_pag_cofins:
        dt_pag_cofins_valido, dt_pag_cofins_obj = _validar_data(dt_pag_cofins)
        if not dt_pag_cofins_valido:
            return None
    
    # LOC_EXE_SERV: obrigatório, valores válidos [0, 1]
    if not loc_exe_serv or loc_exe_serv not in ["0", "1"]:
        return None
    
    # Função auxiliar para formatar valores monetários
    def fmt_valor(v):
        return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    # Função auxiliar para formatar data
    def fmt_data(dt):
        if dt:
            return dt.strftime("%d/%m/%Y")
        return ""
    
    # Monta o resultado
    descricoes_loc_exe_serv = {
        "0": "Executado no País",
        "1": "Executado no Exterior, cujo resultado se verifique no País"
    }
    
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "VL_TOT_SERV": {
            "titulo": "Valor total do serviço, prestado por pessoa física ou jurídica domiciliada no exterior",
            "valor": vl_tot_serv,
            "valor_formatado": fmt_valor(val1)
        },
        "VL_BC_PIS": {
            "titulo": "Valor da base de cálculo da Operação – PIS/PASEP – Importação",
            "valor": vl_bc_pis,
            "valor_formatado": fmt_valor(val2)
        },
        "VL_PIS_IMP": {
            "titulo": "Valor pago/recolhido de PIS/PASEP – Importação",
            "valor": vl_pis_imp,
            "valor_formatado": fmt_valor(val3) if vl_pis_imp else ""
        },
        "DT_PAG_PIS": {
            "titulo": "Data de pagamento do PIS/PASEP – Importação",
            "valor": dt_pag_pis,
            "valor_formatado": fmt_data(dt_pag_pis_obj) if dt_pag_pis_obj else ""
        },
        "VL_BC_COFINS": {
            "titulo": "Valor da base de cálculo da Operação – COFINS – Importação",
            "valor": vl_bc_cofins,
            "valor_formatado": fmt_valor(val4)
        },
        "VL_COFINS_IMP": {
            "titulo": "Valor pago/recolhido de COFINS – Importação",
            "valor": vl_cofins_imp,
            "valor_formatado": fmt_valor(val5) if vl_cofins_imp else ""
        },
        "DT_PAG_COFINS": {
            "titulo": "Data de pagamento do COFINS – Importação",
            "valor": dt_pag_cofins,
            "valor_formatado": fmt_data(dt_pag_cofins_obj) if dt_pag_cofins_obj else ""
        },
        "LOC_EXE_SERV": {
            "titulo": "Local da execução do serviço",
            "valor": loc_exe_serv,
            "descricao": descricoes_loc_exe_serv.get(loc_exe_serv, "")
        }
    }
    
    return resultado


def validar_a120(linhas):
    """
    Valida uma ou mais linhas do registro A120 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |A120|VL_TOT_SERV|VL_BC_PIS|VL_PIS_IMP|DT_PAG_PIS|VL_BC_COFINS|VL_COFINS_IMP|DT_PAG_COFINS|LOC_EXE_SERV|
        
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
        resultado = _processar_linha_a120(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
