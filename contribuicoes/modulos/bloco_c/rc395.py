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


def _processar_linha_c395(linha):
    """
    Processa uma única linha do registro C395 e retorna um dicionário.
    
    Formato:
      |C395|COD_MOD|COD_PART|SER|SUB_SER|NUM_DOC|DT_DOC|VL_DOC|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "C395"
    - COD_MOD: obrigatório, código do modelo do documento fiscal (2 caracteres)
      - Valores válidos: [02, 2D, 2E, 59, 60, 65]
    - COD_PART: opcional, código do participante emitente do documento (60 caracteres)
      - Validação: deve existir no campo COD_PART do registro 0150 (validação em camada superior)
    - SER: obrigatório, série do documento fiscal (3 caracteres)
      - Se no documento fiscal escriturado não constar série, informar o campo com "000"
    - SUB_SER: opcional, subsérie do documento fiscal (3 caracteres)
    - NUM_DOC: obrigatório, número do documento fiscal (6 caracteres)
      - Informe apenas caracteres numéricos (0 a 9)
      - Deve ser maior que 0
    - DT_DOC: obrigatório, data da emissão do documento fiscal (ddmmaaaa)
    - VL_DOC: obrigatório, valor total do documento fiscal (numérico, 2 decimais, positivo)
    
    Nota: No Registro C395 a pessoa jurídica poderá escriturar eventuais aquisições com direito a crédito
    (aquisição de bens a serem utilizados como insumos, por exemplo) cuja operação esteja documentada por
    nota fiscal de venda a consumidor.
    
    No Registro filho C396 deve ser detalhado os dados fiscais necessários para a apuração dos créditos
    de PIS/Pasep e de Cofins.
    
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
    # Remove primeiro e último se vazios (formato padrão SPED: |C395|...|)
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
    if reg != "C395":
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
    cod_part = obter_campo(2)
    ser = obter_campo(3)
    sub_ser = obter_campo(4)
    num_doc = obter_campo(5)
    dt_doc = obter_campo(6)
    vl_doc = obter_campo(7)
    
    # Validações básicas dos campos obrigatórios
    
    # COD_MOD: obrigatório, valores válidos [02, 2D, 2E, 59, 60, 65]
    cod_mod_validos = ["02", "2D", "2E", "59", "60", "65"]
    if not cod_mod or cod_mod not in cod_mod_validos:
        return None
    
    # COD_PART: opcional, código do participante (60 caracteres)
    if cod_part and len(cod_part) > 60:
        return None
    
    # SER: obrigatório, série do documento fiscal (3 caracteres)
    if not ser or len(ser) != 3:
        return None
    
    # SUB_SER: opcional, subsérie do documento fiscal (3 caracteres)
    if sub_ser and len(sub_ser) > 3:
        return None
    
    # NUM_DOC: obrigatório, número do documento fiscal (6 caracteres, numérico, maior que 0)
    if not num_doc or not num_doc.isdigit() or len(num_doc) > 6 or int(num_doc) <= 0:
        return None
    
    # DT_DOC: obrigatório, data da emissão do documento fiscal (ddmmaaaa)
    ok_dt_doc, dt_doc_obj = _validar_data(dt_doc)
    if not ok_dt_doc:
        return None
    
    # VL_DOC: obrigatório, valor total do documento fiscal (numérico, 2 decimais, positivo)
    ok_vl_doc, val_vl_doc, _ = validar_valor_numerico(vl_doc, decimais=2, obrigatorio=True, positivo=True)
    if not ok_vl_doc:
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
    
    # Descrições dos campos COD_MOD
    descricoes_cod_mod = {
        "02": "Nota Fiscal de Venda a Consumidor",
        "2D": "Cupom Fiscal emitido por ECF",
        "2E": "Bilhete de Passagem emitido por ECF",
        "59": "Cupom Fiscal",
        "60": "Cupom Fiscal vinculado a nota fiscal",
        "65": "NFC-e (Nota Fiscal de Consumidor Eletrônica)"
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
        "COD_PART": {
            "titulo": "Código do participante emitente do documento (campo 02 do Registro 0150)",
            "valor": cod_part
        },
        "SER": {
            "titulo": "Série do documento fiscal",
            "valor": ser
        },
        "SUB_SER": {
            "titulo": "Subsérie do documento fiscal",
            "valor": sub_ser
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
        "VL_DOC": {
            "titulo": "Valor total do documento fiscal",
            "valor": vl_doc,
            "valor_formatado": fmt_valor(val_vl_doc)
        }
    }
    
    return resultado


def validar_c395(linhas):
    """
    Valida uma ou mais linhas do registro C395 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |C395|COD_MOD|COD_PART|SER|SUB_SER|NUM_DOC|DT_DOC|VL_DOC|
        
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
        resultado = _processar_linha_c395(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
