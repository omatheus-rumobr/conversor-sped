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


def _processar_linha_c180(linha):
    """
    Processa uma única linha do registro C180 e retorna um dicionário.
    
    Formato:
      |C180|COD_MOD|DT_DOC_INI|DT_DOC_FIN|COD_ITEM|COD_NCM|EX_IPI|VL_TOT_ITEM|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "C180"
    - COD_MOD: obrigatório, código da NF-e ou da NFC-e (2 caracteres)
      - Valores válidos: [55, 65]
      - 55: NF-e (Nota Fiscal Eletrônica)
      - 65: NFC-e (Nota Fiscal de Consumidor Eletrônica)
    - DT_DOC_INI: obrigatório, data de emissão inicial dos documentos (ddmmaaaa)
    - DT_DOC_FIN: obrigatório, data de emissão final dos documentos (ddmmaaaa)
      - Deve ser >= DT_DOC_INI
    - COD_ITEM: obrigatório, código do item (60 caracteres)
      - Validação: deve existir no registro 0200 (validação em camada superior)
    - COD_NCM: opcional, código da Nomenclatura Comum do Mercosul (8 caracteres)
      - Obrigatório em situações específicas (validação em camada superior)
      - Pode ser "00" para serviços
    - EX_IPI: opcional, código EX conforme a TIPI (3 caracteres)
    - VL_TOT_ITEM: obrigatório, valor total do item (numérico, 2 decimais, positivo)
    
    Nota: Este registro deve ser preenchido para consolidar as operações de vendas realizadas pela pessoa
    jurídica, por item vendido (Registro 0200), mediante emissão de NF-e (Modelo 55) e NFC-e (modelo 65).
    
    Os valores consolidados por item vendido (bens ou serviços, no caso de nota conjugada) serão segregados
    e totalizados, nos registros filhos (C181 e C185), por CST-PIS (Tabela 4.3.3), CST-Cofins (Tabela 4.3.4),
    CFOP e alíquotas.
    
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
    # Remove primeiro e último se vazios (formato padrão SPED: |C180|...|)
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
    if reg != "C180":
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
    cod_item = obter_campo(4)
    cod_ncm = obter_campo(5)
    ex_ipi = obter_campo(6)
    vl_tot_item = obter_campo(7)
    
    # Validações básicas dos campos obrigatórios
    
    # COD_MOD: obrigatório, valores válidos [55, 65]
    cod_mod_validos = ["55", "65"]
    if not cod_mod or cod_mod not in cod_mod_validos:
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
    
    # COD_ITEM: obrigatório, código do item (60 caracteres)
    if not cod_item or len(cod_item) > 60:
        return None
    
    # COD_NCM: opcional, código NCM (8 caracteres)
    if cod_ncm and len(cod_ncm) > 8:
        return None
    
    # EX_IPI: opcional, código EX conforme TIPI (3 caracteres)
    if ex_ipi and len(ex_ipi) > 3:
        return None
    
    # VL_TOT_ITEM: obrigatório, valor total do item (numérico, 2 decimais, positivo)
    ok_vl_tot_item, val_vl_tot_item, _ = validar_valor_numerico(vl_tot_item, decimais=2, obrigatorio=True, positivo=True)
    if not ok_vl_tot_item:
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
    
    # Descrições dos campos
    descricoes_cod_mod = {
        "55": "NF-e (Nota Fiscal Eletrônica)",
        "65": "NFC-e (Nota Fiscal de Consumidor Eletrônica)"
    }
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "COD_MOD": {
            "titulo": "Texto fixo contendo \"55\" ou \"65\" (Código da NF-e ou da NFC-e, conforme a Tabela 4.1.1)",
            "valor": cod_mod,
            "descricao": descricoes_cod_mod.get(cod_mod, "")
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
        "COD_ITEM": {
            "titulo": "Código do Item (campo 02 do Registro 0200)",
            "valor": cod_item
        },
        "COD_NCM": {
            "titulo": "Código da Nomenclatura Comum do Mercosul",
            "valor": cod_ncm
        },
        "EX_IPI": {
            "titulo": "Código EX, conforme a TIPI",
            "valor": ex_ipi
        },
        "VL_TOT_ITEM": {
            "titulo": "Valor Total do Item",
            "valor": vl_tot_item,
            "valor_formatado": fmt_valor(val_vl_tot_item)
        }
    }
    
    return resultado


def validar_c180(linhas):
    """
    Valida uma ou mais linhas do registro C180 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |C180|COD_MOD|DT_DOC_INI|DT_DOC_FIN|COD_ITEM|COD_NCM|EX_IPI|VL_TOT_ITEM|
        
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
        resultado = _processar_linha_c180(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
