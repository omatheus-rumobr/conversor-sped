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


def _processar_linha_d162(linha):
    """
    Processa uma única linha do registro D162 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |D162|COD_MOD|SER|NUM_DOC|DT_DOC|VL_DOC|VL_MERC|QTD_VOL|PESO_BRT|PESO_LIQ|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |D162|...|)
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
    if reg != "D162":
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
    cod_mod = obter_campo(1)
    ser = obter_campo(2)
    num_doc = obter_campo(3)
    dt_doc = obter_campo(4)
    vl_doc = obter_campo(5)
    vl_merc = obter_campo(6)
    qtd_vol = obter_campo(7)
    peso_brt = obter_campo(8)
    peso_liq = obter_campo(9)
    
    # Validações dos campos obrigatórios
    
    # COD_MOD: opcional condicional, valores válidos: ["01", "1B", "04", "55"]
    if cod_mod:
        cod_mod_validos = ["01", "1B", "04", "55"]
        if cod_mod not in cod_mod_validos:
            return None
    
    # SER: opcional condicional, até 4 caracteres
    if ser and len(ser) > 4:
        return None
    
    # NUM_DOC: obrigatório, maior que zero
    if not num_doc:
        return None
    if not num_doc.isdigit() or int(num_doc) <= 0:
        return None
    
    # DT_DOC: opcional condicional, formato ddmmaaaa
    if dt_doc:
        dt_doc_valida, dt_doc_obj = _validar_data(dt_doc)
        if not dt_doc_valida:
            return None
    
    # VL_DOC: opcional condicional, numérico com 2 decimais, não negativo
    vl_doc_valido, vl_doc_float, _ = validar_valor_numerico(vl_doc, decimais=2, obrigatorio=False, nao_negativo=True)
    if not vl_doc_valido:
        return None
    
    # VL_MERC: opcional condicional, numérico com 2 decimais
    # Validação: se informado, deve ser maior que zero
    if vl_merc:
        vl_merc_valido, vl_merc_float, _ = validar_valor_numerico(vl_merc, decimais=2, obrigatorio=False, positivo=True)
        if not vl_merc_valido:
            return None
    else:
        vl_merc_float = None
    
    # QTD_VOL: obrigatório, numérico inteiro, não negativo
    if not qtd_vol:
        return None
    try:
        qtd_vol_int = int(float(qtd_vol))  # Permite conversão de float para int
        if qtd_vol_int < 0:
            return None
    except ValueError:
        return None
    
    # PESO_BRT: opcional condicional, numérico com 2 decimais, não negativo
    peso_brt_valido, peso_brt_float, _ = validar_valor_numerico(peso_brt, decimais=2, obrigatorio=False, nao_negativo=True)
    if not peso_brt_valido:
        return None
    
    # PESO_LIQ: opcional condicional, numérico com 2 decimais, não negativo
    peso_liq_valido, peso_liq_float, _ = validar_valor_numerico(peso_liq, decimais=2, obrigatorio=False, nao_negativo=True)
    if not peso_liq_valido:
        return None
    
    # Formatação de valores monetários
    def formatar_valor_monetario(valor_float):
        if valor_float is None:
            return ""
        return f"R$ {valor_float:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    # Formatação de data
    def formatar_data(data_str):
        if not data_str or len(data_str) != 8:
            return data_str
        return f"{data_str[:2]}/{data_str[2:4]}/{data_str[4:8]}"
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "COD_MOD": {
            "titulo": "Código do modelo do documento fiscal",
            "valor": cod_mod if cod_mod else ""
        },
        "SER": {
            "titulo": "Série do documento fiscal",
            "valor": ser if ser else ""
        },
        "NUM_DOC": {
            "titulo": "Número do documento fiscal",
            "valor": num_doc
        },
        "DT_DOC": {
            "titulo": "Data da emissão do documento fiscal",
            "valor": dt_doc if dt_doc else "",
            "valor_formatado": formatar_data(dt_doc) if dt_doc else ""
        },
        "VL_DOC": {
            "titulo": "Valor total do documento fiscal",
            "valor": vl_doc if vl_doc else "",
            "valor_formatado": formatar_valor_monetario(vl_doc_float) if vl_doc else ""
        },
        "VL_MERC": {
            "titulo": "Valor das mercadorias constantes no documento fiscal",
            "valor": vl_merc if vl_merc else "",
            "valor_formatado": formatar_valor_monetario(vl_merc_float) if vl_merc else ""
        },
        "QTD_VOL": {
            "titulo": "Quantidade de volumes transportados",
            "valor": qtd_vol
        },
        "PESO_BRT": {
            "titulo": "Peso bruto dos volumes transportados (em kg)",
            "valor": peso_brt if peso_brt else "",
            "valor_formatado": formatar_valor_monetario(peso_brt_float) if peso_brt else ""
        },
        "PESO_LIQ": {
            "titulo": "Peso líquido dos volumes transportados (em kg)",
            "valor": peso_liq if peso_liq else "",
            "valor_formatado": formatar_valor_monetario(peso_liq_float) if peso_liq else ""
        }
    }
    
    return resultado


def validar_d162(linhas):
    """
    Valida uma ou mais linhas do registro D162 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |D162|COD_MOD|SER|NUM_DOC|DT_DOC|VL_DOC|VL_MERC|QTD_VOL|PESO_BRT|PESO_LIQ|
        
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
        resultado = _processar_linha_d162(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
