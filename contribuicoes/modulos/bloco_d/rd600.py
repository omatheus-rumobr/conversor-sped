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


def _processar_linha_d600(linha, dt_ini_0000=None, dt_fin_0000=None):
    """
    Processa uma única linha do registro D600 e retorna um dicionário.
    
    Formato:
      |D600|COD_MOD|COD_MUN|SER|SUB|IND_REC|QTD_CONS|DT_DOC_INI|DT_DOC_FIN|VL_DOC|VL_DESC|VL_SERV|VL_SERV_NT|VL_TERC|VL_DA|VL_BC_ICMS|VL_ICMS|VL_PIS|VL_COFINS|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "D600"
    - COD_MOD: obrigatório, valores válidos [21, 22]
    - COD_MUN: opcional, 7 dígitos (código IBGE)
    - SER: opcional, máximo 4 caracteres
    - SUB: opcional, máximo 3 caracteres (numérico)
    - IND_REC: obrigatório, valores válidos [0-9]
    - QTD_CONS: obrigatório, numérico inteiro, deve ser > 0
    - DT_DOC_INI: obrigatório, formato ddmmaaaa, data válida
    - DT_DOC_FIN: obrigatório, formato ddmmaaaa, data válida
    - VL_DOC: obrigatório, numérico com 2 decimais, deve ser > 0
    - VL_DESC: opcional, numérico com 2 decimais
    - VL_SERV: obrigatório, numérico com 2 decimais
    - VL_SERV_NT: opcional, numérico com 2 decimais
    - VL_TERC: opcional, numérico com 2 decimais
    - VL_DA: opcional, numérico com 2 decimais
    - VL_BC_ICMS: opcional, numérico com 2 decimais
    - VL_ICMS: opcional, numérico com 2 decimais
    - VL_PIS: opcional, numérico com 2 decimais
    - VL_COFINS: opcional, numérico com 2 decimais
    
    Nota: Neste registro será informada a consolidação das receitas auferidas pelas empresas de comunicação
    e de telecomunicação, de acordo com a natureza dos serviços prestados. Devem ser objeto de escrituração
    as receitas efetivamente realizadas, mesmo que ainda a faturar, desde que os serviços já tenham sido
    prestados ao consumidor dos mesmos.
    
    Args:
        linha: String com uma linha do SPED
        dt_ini_0000: Data inicial da escrituração (ddmmaaaa) - opcional, para validação
        dt_fin_0000: Data final da escrituração (ddmmaaaa) - opcional, para validação
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |D600|...|)
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
    if reg != "D600":
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
    
    # Extrai todos os campos (19 campos no total)
    cod_mod = obter_campo(1)
    cod_mun = obter_campo(2)
    ser = obter_campo(3)
    sub = obter_campo(4)
    ind_rec = obter_campo(5)
    qtd_cons = obter_campo(6)
    dt_doc_ini = obter_campo(7)
    dt_doc_fin = obter_campo(8)
    vl_doc = obter_campo(9)
    vl_desc = obter_campo(10)
    vl_serv = obter_campo(11)
    vl_serv_nt = obter_campo(12)
    vl_terc = obter_campo(13)
    vl_da = obter_campo(14)
    vl_bc_icms = obter_campo(15)
    vl_icms = obter_campo(16)
    vl_pis = obter_campo(17)
    vl_cofins = obter_campo(18)
    
    # Validações básicas dos campos obrigatórios
    
    # COD_MOD: obrigatório, valores válidos [21, 22]
    cod_mod_validos = ["21", "22"]
    if not cod_mod or cod_mod not in cod_mod_validos:
        return None
    
    # COD_MUN: opcional, 7 dígitos (código IBGE)
    if cod_mun:
        if not cod_mun.isdigit() or len(cod_mun) != 7:
            return None
    
    # SER: opcional, máximo 4 caracteres
    if ser and len(ser) > 4:
        return None
    
    # SUB: opcional, máximo 3 caracteres (numérico)
    if sub:
        if len(sub) > 3 or not sub.isdigit():
            return None
    
    # IND_REC: obrigatório, valores válidos [0-9]
    ind_rec_validos = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    if not ind_rec or ind_rec not in ind_rec_validos:
        return None
    
    # QTD_CONS: obrigatório, numérico inteiro, deve ser > 0
    if not qtd_cons:
        return None
    try:
        qtd_cons_int = int(qtd_cons)
        if qtd_cons_int <= 0:
            return None
    except ValueError:
        return None
    
    # DT_DOC_INI: obrigatório, formato ddmmaaaa, data válida
    dt_doc_ini_valido, dt_doc_ini_obj = _validar_data(dt_doc_ini)
    if not dt_doc_ini_valido:
        return None
    
    # DT_DOC_FIN: obrigatório, formato ddmmaaaa, data válida
    dt_doc_fin_valido, dt_doc_fin_obj = _validar_data(dt_doc_fin)
    if not dt_doc_fin_valido:
        return None
    
    # Validação: DT_DOC_INI deve ser <= DT_DOC_FIN
    if dt_doc_ini_obj and dt_doc_fin_obj and dt_doc_ini_obj > dt_doc_fin_obj:
        return None
    
    # VL_DOC: obrigatório, numérico com 2 decimais, deve ser > 0
    ok1, val1, _ = validar_valor_numerico(vl_doc, decimais=2, obrigatorio=True, positivo=True)
    if not ok1:
        return None
    
    # VL_DESC: opcional, numérico com 2 decimais
    ok2, val2, _ = validar_valor_numerico(vl_desc, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok2:
        return None
    
    # VL_SERV: obrigatório, numérico com 2 decimais
    ok3, val3, _ = validar_valor_numerico(vl_serv, decimais=2, obrigatorio=True)
    if not ok3:
        return None
    
    # VL_SERV_NT: opcional, numérico com 2 decimais
    ok4, val4, _ = validar_valor_numerico(vl_serv_nt, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok4:
        return None
    
    # VL_TERC: opcional, numérico com 2 decimais
    ok5, val5, _ = validar_valor_numerico(vl_terc, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok5:
        return None
    
    # VL_DA: opcional, numérico com 2 decimais
    ok6, val6, _ = validar_valor_numerico(vl_da, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok6:
        return None
    
    # VL_BC_ICMS: opcional, numérico com 2 decimais
    ok7, val7, _ = validar_valor_numerico(vl_bc_icms, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok7:
        return None
    
    # VL_ICMS: opcional, numérico com 2 decimais
    ok8, val8, _ = validar_valor_numerico(vl_icms, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok8:
        return None
    
    # VL_PIS: opcional, numérico com 2 decimais
    ok9, val9, _ = validar_valor_numerico(vl_pis, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok9:
        return None
    
    # VL_COFINS: opcional, numérico com 2 decimais
    ok10, val10, _ = validar_valor_numerico(vl_cofins, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok10:
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
        "21": "Nota Fiscal de Serviço de Comunicação",
        "22": "Nota Fiscal de Serviço de Telecomunicação"
    }
    
    descricoes_ind_rec = {
        "0": "Receita própria - serviços prestados",
        "1": "Receita própria - cobrança de débitos",
        "2": "Receita própria - venda de serviço pré-pago – faturamento de períodos anteriores",
        "3": "Receita própria - venda de serviço pré-pago – faturamento no período",
        "4": "Outras receitas próprias de serviços de comunicação e telecomunicação",
        "5": "Receita própria - co-faturamento",
        "6": "Receita própria – serviços a faturar em período futuro",
        "7": "Outras receitas próprias de natureza não-cumulativa",
        "8": "Outras receitas de terceiros",
        "9": "Outras receitas"
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
        "COD_MUN": {
            "titulo": "Código do município dos terminais faturados, conforme a tabela IBGE",
            "valor": cod_mun
        },
        "SER": {
            "titulo": "Série do documento fiscal",
            "valor": ser
        },
        "SUB": {
            "titulo": "Subsérie do documento fiscal",
            "valor": sub
        },
        "IND_REC": {
            "titulo": "Indicador do tipo de receita",
            "valor": ind_rec,
            "descricao": descricoes_ind_rec.get(ind_rec, "")
        },
        "QTD_CONS": {
            "titulo": "Quantidade de documentos consolidados neste registro",
            "valor": qtd_cons
        },
        "DT_DOC_INI": {
            "titulo": "Data Inicial dos documentos consolidados no período",
            "valor": dt_doc_ini,
            "valor_formatado": fmt_data(dt_doc_ini_obj)
        },
        "DT_DOC_FIN": {
            "titulo": "Data Final dos documentos consolidados no período",
            "valor": dt_doc_fin,
            "valor_formatado": fmt_data(dt_doc_fin_obj)
        },
        "VL_DOC": {
            "titulo": "Valor total acumulado dos documentos fiscais",
            "valor": vl_doc,
            "valor_formatado": fmt_valor(val1)
        },
        "VL_DESC": {
            "titulo": "Valor acumulado dos descontos",
            "valor": vl_desc,
            "valor_formatado": fmt_valor(val2) if vl_desc else ""
        },
        "VL_SERV": {
            "titulo": "Valor acumulado das prestações de serviços tributados pelo ICMS",
            "valor": vl_serv,
            "valor_formatado": fmt_valor(val3)
        },
        "VL_SERV_NT": {
            "titulo": "Valor acumulado dos serviços não-tributados pelo ICMS",
            "valor": vl_serv_nt,
            "valor_formatado": fmt_valor(val4) if vl_serv_nt else ""
        },
        "VL_TERC": {
            "titulo": "Valores cobrados em nome de terceiros",
            "valor": vl_terc,
            "valor_formatado": fmt_valor(val5) if vl_terc else ""
        },
        "VL_DA": {
            "titulo": "Valor acumulado das despesas acessórias",
            "valor": vl_da,
            "valor_formatado": fmt_valor(val6) if vl_da else ""
        },
        "VL_BC_ICMS": {
            "titulo": "Valor acumulado da base de cálculo do ICMS",
            "valor": vl_bc_icms,
            "valor_formatado": fmt_valor(val7) if vl_bc_icms else ""
        },
        "VL_ICMS": {
            "titulo": "Valor acumulado do ICMS",
            "valor": vl_icms,
            "valor_formatado": fmt_valor(val8) if vl_icms else ""
        },
        "VL_PIS": {
            "titulo": "Valor do PIS/PASEP",
            "valor": vl_pis,
            "valor_formatado": fmt_valor(val9) if vl_pis else ""
        },
        "VL_COFINS": {
            "titulo": "Valor da COFINS",
            "valor": vl_cofins,
            "valor_formatado": fmt_valor(val10) if vl_cofins else ""
        }
    }
    
    return resultado


def validar_d600(linhas, dt_ini_0000=None, dt_fin_0000=None):
    """
    Valida uma ou mais linhas do registro D600 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |D600|COD_MOD|COD_MUN|SER|SUB|IND_REC|QTD_CONS|DT_DOC_INI|DT_DOC_FIN|VL_DOC|VL_DESC|VL_SERV|VL_SERV_NT|VL_TERC|VL_DA|VL_BC_ICMS|VL_ICMS|VL_PIS|VL_COFINS|
        dt_ini_0000: Data inicial da escrituração (ddmmaaaa) - opcional, para validação
        dt_fin_0000: Data final da escrituração (ddmmaaaa) - opcional, para validação
        
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
        resultado = _processar_linha_d600(linha, dt_ini_0000, dt_fin_0000)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
