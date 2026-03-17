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


def _processar_linha_c405(linha):
    """
    Processa uma única linha do registro C405 e retorna um dicionário.
    
    Formato:
      |C405|DT_DOC|CRO|CRZ|NUM_COO_FIN|GT_FIN|VL_BRT|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "C405"
    - DT_DOC: obrigatório, data do movimento a que se refere a Redução Z (ddmmaaaa)
      - Validação: o valor informado deve ser menor ou igual à DT_FIN deste arquivo (validação em camada superior)
    - CRO: obrigatório, posição do Contador de Reinício de Operação (3 dígitos)
      - Deve ser maior que 0
    - CRZ: obrigatório, posição do Contador de Redução Z (6 dígitos)
      - Deve ser maior que 0
    - NUM_COO_FIN: obrigatório, número do Contador de Ordem de Operação do último documento emitido no dia (6 dígitos)
      - Deve ser maior que 0
    - GT_FIN: obrigatório, valor do Grande Total final (numérico, 2 decimais)
      - Valor acumulado no totalizador geral final
      - Validação: deve ser maior ou igual ao campo VL_BRT, exceto se houver reinício de operação
    - VL_BRT: obrigatório, valor da venda bruta (numérico, 2 decimais)
      - Valor acumulado no totalizador de venda bruta
    
    Nota: Este registro deve ser apresentado com as informações da Redução Z de cada equipamento em funcionamento
    na data das operações de venda à qual se refere a redução. Inclui todos os documentos fiscais totalizados na
    Redução Z, inclusive as operações de venda realizadas durante o período de tolerância do Equipamento ECF.
    
    Registro obrigatório, se existir C400.
    
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
    # Remove primeiro e último se vazios (formato padrão SPED: |C405|...|)
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
    if reg != "C405":
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
    dt_doc = obter_campo(1)
    cro = obter_campo(2)
    crz = obter_campo(3)
    num_coo_fin = obter_campo(4)
    gt_fin = obter_campo(5)
    vl_brt = obter_campo(6)
    
    # Validações básicas dos campos obrigatórios
    
    # DT_DOC: obrigatório, data do movimento (ddmmaaaa)
    ok_dt_doc, dt_doc_obj = _validar_data(dt_doc)
    if not ok_dt_doc:
        return None
    
    # CRO: obrigatório, posição do Contador de Reinício de Operação (3 dígitos, maior que 0)
    if not cro or not cro.isdigit() or len(cro) > 3 or int(cro) <= 0:
        return None
    
    # CRZ: obrigatório, posição do Contador de Redução Z (6 dígitos, maior que 0)
    if not crz or not crz.isdigit() or len(crz) > 6 or int(crz) <= 0:
        return None
    
    # NUM_COO_FIN: obrigatório, número do COO na Redução Z (6 dígitos, maior que 0)
    if not num_coo_fin or not num_coo_fin.isdigit() or len(num_coo_fin) > 6 or int(num_coo_fin) <= 0:
        return None
    
    # GT_FIN: obrigatório, valor do Grande Total final (numérico, 2 decimais)
    ok_gt_fin, val_gt_fin, _ = validar_valor_numerico(gt_fin, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok_gt_fin:
        return None
    
    # VL_BRT: obrigatório, valor da venda bruta (numérico, 2 decimais)
    ok_vl_brt, val_vl_brt, _ = validar_valor_numerico(vl_brt, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok_vl_brt:
        return None
    
    # Validação: GT_FIN deve ser maior ou igual a VL_BRT, exceto se houver reinício de operação
    # Como não temos como saber se houve reinício de operação apenas com este registro, vamos validar
    # apenas se GT_FIN < VL_BRT quando CRO = 1 (sem reinício), mas como não temos certeza, vamos apenas
    # registrar a validação básica. A validação completa deve ser feita em camada superior.
    # Por enquanto, vamos apenas garantir que os valores sejam válidos
    
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
        "DT_DOC": {
            "titulo": "Data do movimento a que se refere a Redução Z",
            "valor": dt_doc,
            "valor_formatado": fmt_data(dt_doc)
        },
        "CRO": {
            "titulo": "Posição do Contador de Reinício de Operação",
            "valor": cro
        },
        "CRZ": {
            "titulo": "Posição do Contador de Redução Z",
            "valor": crz
        },
        "NUM_COO_FIN": {
            "titulo": "Número do Contador de Ordem de Operação do último documento emitido no dia (Número do COO na Redução Z)",
            "valor": num_coo_fin
        },
        "GT_FIN": {
            "titulo": "Valor do Grande Total final",
            "valor": gt_fin,
            "valor_formatado": fmt_valor(val_gt_fin)
        },
        "VL_BRT": {
            "titulo": "Valor da venda bruta",
            "valor": vl_brt,
            "valor_formatado": fmt_valor(val_vl_brt)
        }
    }
    
    return resultado


def validar_c405(linhas):
    """
    Valida uma ou mais linhas do registro C405 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |C405|DT_DOC|CRO|CRZ|NUM_COO_FIN|GT_FIN|VL_BRT|
        
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
        resultado = _processar_linha_c405(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
