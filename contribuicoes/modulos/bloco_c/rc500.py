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


def _validar_chave_nfe(chave_nfe):
    """
    Valida a chave da NF-e (44 dígitos) e o dígito verificador.
    
    Args:
        chave_nfe: String com a chave da NF-e (44 dígitos)
        
    Returns:
        bool: True se válida, False caso contrário
    """
    if not chave_nfe or len(chave_nfe) != 44 or not chave_nfe.isdigit():
        return False
    
    # Extrai os 43 primeiros dígitos e o dígito verificador (último dígito)
    chave_43 = chave_nfe[:43]
    dv_informado = int(chave_nfe[43])
    
    # Calcula o dígito verificador usando módulo 11
    soma = 0
    multiplicador = 2
    
    # Percorre os 43 dígitos de trás para frente
    for i in range(42, -1, -1):
        soma += int(chave_43[i]) * multiplicador
        multiplicador += 1
        if multiplicador > 9:
            multiplicador = 2
    
    # Calcula o resto da divisão por 11
    resto = soma % 11
    
    # Se o resto for 0 ou 1, o dígito verificador é 0
    # Caso contrário, é 11 - resto
    if resto < 2:
        dv_calculado = 0
    else:
        dv_calculado = 11 - resto
    
    return dv_calculado == dv_informado


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


def _processar_linha_c500(linha):
    """
    Processa uma única linha do registro C500 e retorna um dicionário.
    
    Formato:
      |C500|COD_PART|COD_MOD|COD_SIT|SER|SUB|NUM_DOC|DT_DOC|DT_ENT|VL_DOC|VL_ICMS|COD_INF|VL_PIS|VL_COFINS|CHV_DOCe|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "C500"
    - COD_PART: obrigatório, código do participante do fornecedor (60 caracteres)
      - Validação: deve existir no campo COD_PART do registro 0150 (validação em camada superior)
    - COD_MOD: obrigatório, código do modelo do documento fiscal (2 caracteres)
      - Valores válidos: [06, 28, 29, 55, 66]
    - COD_SIT: obrigatório, código da situação do documento fiscal (2 dígitos)
      - Valores válidos: [00, 01, 02, 03, 06, 07, 08]
    - SER: opcional, série do documento fiscal (4 caracteres)
    - SUB: opcional, subsérie do documento fiscal (3 dígitos)
    - NUM_DOC: obrigatório, número do documento fiscal (9 dígitos)
      - Deve ser maior que 0
      - Na impossibilidade de informar o número específico, preencher com "000000000"
    - DT_DOC: obrigatório, data de emissão do documento fiscal (ddmmaaaa)
    - DT_ENT: opcional, data de entrada (ddmmaaaa)
      - Deve ser >= DT_DOC
    - VL_DOC: obrigatório, valor total do documento fiscal (numérico, 2 decimais, positivo)
    - VL_ICMS: opcional, valor acumulado do ICMS (numérico, 2 decimais)
    - COD_INF: opcional, código da informação complementar do documento fiscal (6 caracteres)
    - VL_PIS: opcional, valor do PIS/PASEP (numérico, 2 decimais)
    - VL_COFINS: opcional, valor da COFINS (numérico, 2 decimais)
    - CHV_DOCe: opcional, chave do documento fiscal eletrônico (44 dígitos)
      - Obrigatório para COD_MOD = 66 ou 55 a partir de 01/01/2020
      - Validação do dígito verificador quando preenchido
    
    Nota: Este registro informa as operações sujeitas à apuração de créditos de PIS/Pasep e de Cofins,
    referentes a energia elétrica, água canalizada ou gás, utilizados como insumo.
    
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
    # Remove primeiro e último se vazios (formato padrão SPED: |C500|...|)
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
    if reg != "C500":
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
    
    # Extrai todos os campos (15 campos no total)
    cod_part = obter_campo(1)
    cod_mod = obter_campo(2)
    cod_sit = obter_campo(3)
    ser = obter_campo(4)
    sub = obter_campo(5)
    num_doc = obter_campo(6)
    dt_doc = obter_campo(7)
    dt_ent = obter_campo(8)
    vl_doc = obter_campo(9)
    vl_icms = obter_campo(10)
    cod_inf = obter_campo(11)
    vl_pis = obter_campo(12)
    vl_cofins = obter_campo(13)
    chv_doce = obter_campo(14)
    
    # Validações básicas dos campos obrigatórios
    
    # COD_PART: obrigatório, código do participante (60 caracteres)
    if not cod_part or len(cod_part) > 60:
        return None
    
    # COD_MOD: obrigatório, valores válidos [06, 28, 29, 55, 66]
    cod_mod_validos = ["06", "28", "29", "55", "66"]
    if not cod_mod or cod_mod not in cod_mod_validos:
        return None
    
    # COD_SIT: obrigatório, valores válidos [00, 01, 02, 03, 06, 07, 08]
    cod_sit_validos = ["00", "01", "02", "03", "06", "07", "08"]
    if not cod_sit or cod_sit not in cod_sit_validos:
        return None
    
    # SER: opcional, série do documento fiscal (4 caracteres)
    if ser and len(ser) > 4:
        return None
    
    # SUB: opcional, subsérie do documento fiscal (3 dígitos)
    if sub and (not sub.isdigit() or len(sub) > 3):
        return None
    
    # NUM_DOC: obrigatório, número do documento fiscal (9 dígitos, maior que 0)
    if not num_doc or not num_doc.isdigit() or len(num_doc) > 9:
        return None
    # Permite "000000000" como valor especial conforme manual
    if num_doc != "000000000" and int(num_doc) <= 0:
        return None
    
    # DT_DOC: obrigatório, data de emissão do documento fiscal (ddmmaaaa)
    ok_dt_doc, data_dt_doc = _validar_data(dt_doc)
    if not ok_dt_doc:
        return None
    
    # DT_ENT: opcional, data de entrada (ddmmaaaa), deve ser >= DT_DOC
    data_dt_ent = None
    if dt_ent:
        ok_dt_ent, data_dt_ent = _validar_data(dt_ent)
        if not ok_dt_ent or (data_dt_ent and data_dt_ent < data_dt_doc):
            return None
    
    # VL_DOC: obrigatório, valor total do documento fiscal (numérico, 2 decimais, positivo)
    ok_vl_doc, val_vl_doc, _ = validar_valor_numerico(vl_doc, decimais=2, obrigatorio=True, positivo=True)
    if not ok_vl_doc:
        return None
    
    # VL_ICMS: opcional, valor acumulado do ICMS (numérico, 2 decimais)
    ok_vl_icms, val_vl_icms, _ = validar_valor_numerico(vl_icms, decimais=2, nao_negativo=True)
    if not ok_vl_icms:
        return None
    
    # COD_INF: opcional, código da informação complementar (6 caracteres)
    if cod_inf and len(cod_inf) > 6:
        return None
    
    # VL_PIS: opcional, valor do PIS/PASEP (numérico, 2 decimais)
    ok_vl_pis, val_vl_pis, _ = validar_valor_numerico(vl_pis, decimais=2, nao_negativo=True)
    if not ok_vl_pis:
        return None
    
    # VL_COFINS: opcional, valor da COFINS (numérico, 2 decimais)
    ok_vl_cofins, val_vl_cofins, _ = validar_valor_numerico(vl_cofins, decimais=2, nao_negativo=True)
    if not ok_vl_cofins:
        return None
    
    # CHV_DOCe: opcional, chave do documento fiscal eletrônico (44 dígitos)
    # Obrigatório para COD_MOD = 66 ou 55 a partir de 01/01/2020
    # Por enquanto, validamos apenas o formato quando preenchido
    # A validação de obrigatoriedade baseada em data deve ser feita em camada superior
    if chv_doce:
        if not _validar_chave_nfe(chv_doce):
            return None
    elif cod_mod in ["55", "66"]:
        # Se COD_MOD é 55 ou 66 e CHV_DOCe não está preenchido, pode ser inválido
        # Mas como não temos a data de apuração aqui, vamos apenas validar o formato quando preenchido
        pass
    
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
    descricoes_cod_mod = {
        "06": "Nota Fiscal/Conta de Energia Elétrica",
        "28": "Nota Fiscal/Consumo Fornecimento de Gás",
        "29": "Nota Fiscal/Conta de fornecimento D'água Canalizada",
        "55": "NF-e (Nota Fiscal Eletrônica)",
        "66": "Nota Fiscal de Energia Elétrica Eletrônica – NF3e"
    }
    
    descricoes_cod_sit = {
        "00": "Documento regular",
        "01": "Documento regular extemporâneo",
        "02": "Documento cancelado",
        "03": "Documento cancelado extemporâneo",
        "06": "Documento Complementar",
        "07": "Documento Complementar extemporâneo",
        "08": "Documento Fiscal emitido com base em Regime Especial ou Norma Específica"
    }
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg,
            "descricao": "Texto fixo contendo 'C500'"
        },
        "COD_PART": {
            "titulo": "Código do participante do fornecedor (campo 02 do Registro 0150)",
            "valor": cod_part
        },
        "COD_MOD": {
            "titulo": "Código do modelo do documento fiscal",
            "valor": cod_mod,
            "descricao": descricoes_cod_mod.get(cod_mod, "")
        },
        "COD_SIT": {
            "titulo": "Código da situação do documento fiscal",
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
        "NUM_DOC": {
            "titulo": "Número do documento fiscal",
            "valor": num_doc
        },
        "DT_DOC": {
            "titulo": "Data da emissão do documento fiscal",
            "valor": dt_doc,
            "valor_formatado": fmt_data(dt_doc)
        },
        "DT_ENT": {
            "titulo": "Data da entrada",
            "valor": dt_ent,
            "valor_formatado": fmt_data(dt_ent) if dt_ent else ""
        },
        "VL_DOC": {
            "titulo": "Valor total do documento fiscal",
            "valor": vl_doc,
            "valor_formatado": fmt_valor(val_vl_doc)
        },
        "VL_ICMS": {
            "titulo": "Valor acumulado do ICMS",
            "valor": vl_icms,
            "valor_formatado": fmt_valor(val_vl_icms)
        },
        "COD_INF": {
            "titulo": "Código da informação complementar do documento fiscal (campo 02 do Registro 0450)",
            "valor": cod_inf
        },
        "VL_PIS": {
            "titulo": "Valor do PIS/PASEP",
            "valor": vl_pis,
            "valor_formatado": fmt_valor(val_vl_pis)
        },
        "VL_COFINS": {
            "titulo": "Valor da COFINS",
            "valor": vl_cofins,
            "valor_formatado": fmt_valor(val_vl_cofins)
        },
        "CHV_DOCe": {
            "titulo": "Chave do Documento Fiscal Eletrônico",
            "valor": chv_doce
        }
    }
    
    return resultado


def validar_c500(linhas):
    """
    Valida uma ou mais linhas do registro C500 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |C500|COD_PART|COD_MOD|COD_SIT|SER|SUB|NUM_DOC|DT_DOC|DT_ENT|VL_DOC|VL_ICMS|COD_INF|VL_PIS|VL_COFINS|CHV_DOCe|
        
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
        resultado = _processar_linha_c500(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
