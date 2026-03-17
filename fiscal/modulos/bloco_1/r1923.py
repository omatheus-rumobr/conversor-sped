import re
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


def _validar_chave_doc_eletronico(chave):
    """
    Valida a chave do documento eletrônico (44 dígitos) e o dígito verificador.
    Usado para NF-e (COD_MOD=55), CT-e (COD_MOD=57) e CT-e OS.
    
    Args:
        chave: String com a chave do documento eletrônico (44 dígitos)
        
    Returns:
        bool: True se válida, False caso contrário
    """
    if not chave or len(chave) != 44 or not chave.isdigit():
        return False
    
    # Extrai os 43 primeiros dígitos e o dígito verificador (último dígito)
    chave_43 = chave[:43]
    dv_informado = int(chave[43])
    
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
    if not valor_str:
        if obrigatorio:
            return False, None, f"Campo obrigatório não preenchido"
        return True, 0.0, None
    
    try:
        valor_float = float(valor_str)
        
        # Verifica precisão decimal
        partes_decimal = valor_str.split('.')
        if len(partes_decimal) == 2 and len(partes_decimal[1]) > decimais:
            return False, None, f"Valor com mais de {decimais} casas decimais"
        
        # Validações de sinal
        if positivo and valor_float <= 0:
            return False, None, "Valor deve ser maior que zero"
        if nao_negativo and valor_float < 0:
            return False, None, "Valor não pode ser negativo"
        
        return True, valor_float, None
    except ValueError:
        return False, None, "Valor não é numérico válido"


def _processar_linha_1923(linha):
    """
    Processa uma única linha do registro 1923 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |1923|COD_PART|COD_MOD|SER|SUB|NUM_DOC|DT_DOC|COD_ITEM|VL_AJ_ITEM|CHV_DOCe|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |1923|...|)
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
    if reg != "1923":
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
    
    # Extrai todos os campos (10 campos no total)
    cod_part = obter_campo(1)
    cod_mod = obter_campo(2)
    ser = obter_campo(3)
    sub = obter_campo(4)
    num_doc = obter_campo(5)
    dt_doc = obter_campo(6)
    cod_item = obter_campo(7)
    vl_aj_item = obter_campo(8)
    chv_doce = obter_campo(9)
    
    # Validações dos campos obrigatórios
    
    # COD_PART: obrigatório, até 60 caracteres
    # Quando se tratar de NFC-e (modelo 65), o campo não deve ser preenchido
    # Mas isso requer conhecimento do COD_MOD, então validamos apenas o formato
    if not cod_part:
        return None
    if len(cod_part) > 60:
        return None
    
    # COD_MOD: obrigatório, 2 caracteres
    if not cod_mod or len(cod_mod) != 2:
        return None
    
    # SER: obrigatório condicional, até 4 caracteres
    if ser and len(ser) > 4:
        return None
    
    # SUB: obrigatório condicional, numérico até 3 dígitos
    if sub:
        if not sub.isdigit() or len(sub) > 3:
            return None
    
    # NUM_DOC: obrigatório, numérico, maior que 0
    if not num_doc:
        return None
    try:
        num_doc_int = int(num_doc)
        if num_doc_int <= 0:
            return None
    except ValueError:
        return None
    
    # DT_DOC: obrigatório, formato DDMMAAAA
    if not dt_doc:
        return None
    dt_doc_valida, dt_doc_obj = _validar_data(dt_doc)
    if not dt_doc_valida:
        return None
    
    # COD_ITEM: obrigatório condicional, até 60 caracteres
    if cod_item and len(cod_item) > 60:
        return None
    
    # VL_AJ_ITEM: obrigatório, numérico com 2 decimais
    if not vl_aj_item:
        return None
    vl_aj_item_valido, vl_aj_item_float, vl_aj_item_erro = validar_valor_numerico(vl_aj_item, decimais=2, obrigatorio=True)
    if not vl_aj_item_valido:
        return None
    
    # CHV_DOCe: obrigatório condicional, 44 caracteres
    # Quando presente, deve ser válida se COD_MOD = "55" (NF-e) ou "57" (CT-e)
    if chv_doce:
        if len(chv_doce) != 44 or not chv_doce.isdigit():
            return None
        
        # Valida dígito verificador se for NF-e ou CT-e
        if cod_mod in ["55", "57"]:
            if not _validar_chave_doc_eletronico(chv_doce):
                return None
    
    # Formatação de valores monetários para exibição
    def formatar_valor(valor_str):
        if not valor_str:
            return ""
        try:
            valor_float = float(valor_str)
            return f"{valor_float:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        except ValueError:
            return valor_str
    
    # Formatação de data para exibição
    def formatar_data(data_str):
        if not data_str or len(data_str) != 8:
            return ""
        try:
            return f"{data_str[:2]}/{data_str[2:4]}/{data_str[4:8]}"
        except:
            return data_str
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "COD_PART": {
            "titulo": "Código do participante (campo 02 do Registro 0150): do emitente do documento ou do remetente das mercadorias, no caso de entradas; do adquirente, no caso de saídas",
            "valor": cod_part
        },
        "COD_MOD": {
            "titulo": "Código do modelo do documento fiscal, conforme a Tabela 4.1.1",
            "valor": cod_mod
        },
        "SER": {
            "titulo": "Série do documento fiscal",
            "valor": ser if ser else ""
        },
        "SUB": {
            "titulo": "Subsérie do documento fiscal",
            "valor": sub if sub else ""
        },
        "NUM_DOC": {
            "titulo": "Número do documento fiscal",
            "valor": num_doc
        },
        "DT_DOC": {
            "titulo": "Data da emissão do documento fiscal",
            "valor": dt_doc,
            "valor_formatado": formatar_data(dt_doc)
        },
        "COD_ITEM": {
            "titulo": "Código do item (campo 02 do Registro 0200)",
            "valor": cod_item if cod_item else ""
        },
        "VL_AJ_ITEM": {
            "titulo": "Valor do ajuste para a operação/item",
            "valor": vl_aj_item,
            "valor_formatado": formatar_valor(vl_aj_item)
        },
        "CHV_DOCe": {
            "titulo": "Chave do Documento Eletrônico",
            "valor": chv_doce if chv_doce else ""
        }
    }
    
    return resultado


def validar_1923(linhas):
    """
    Valida uma ou mais linhas do registro 1923 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |1923|COD_PART|COD_MOD|SER|SUB|NUM_DOC|DT_DOC|COD_ITEM|VL_AJ_ITEM|CHV_DOCe|
        
    Returns:
        String JSON com array de objetos contendo os campos validados.
        Cada objeto tem a estrutura {"CAMPO": {"titulo": "...", "valor": "...", "valor_formatado": "..."}}.
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
        resultado = _processar_linha_1923(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
