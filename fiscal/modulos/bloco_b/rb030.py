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


def _processar_linha_b030(linha):
    """
    Processa uma única linha do registro B030 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |B030|COD_MOD|SER|NUM_DOC_INI|NUM_DOC_FIN|DT_DOC|QTD_CANC|VL_CONT|VL_ISNT_ISS|VL_BC_ISS|VL_ISS|COD_INF_OBS|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |B030|...|)
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
    if reg != "B030":
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
    
    # Extrai todos os campos (12 campos no total)
    cod_mod = obter_campo(1)
    ser = obter_campo(2)
    num_doc_ini = obter_campo(3)
    num_doc_fin = obter_campo(4)
    dt_doc = obter_campo(5)
    qtd_canc = obter_campo(6)
    vl_cont = obter_campo(7)
    vl_isnt_iss = obter_campo(8)
    vl_bc_iss = obter_campo(9)
    vl_iss = obter_campo(10)
    cod_inf_obs = obter_campo(11)
    
    # Validações dos campos obrigatórios
    
    # COD_MOD: obrigatório, valor válido: ["3A"]
    if cod_mod != "3A":
        return None
    
    # SER: obrigatório condicional (sem limite de tamanho especificado)
    # Não há validação específica além de verificar se está presente quando necessário
    
    # NUM_DOC_INI: obrigatório, numérico, maior que zero
    if not num_doc_ini:
        return None
    try:
        num_doc_ini_int = int(num_doc_ini)
        if num_doc_ini_int <= 0:
            return None
    except ValueError:
        return None
    
    # NUM_DOC_FIN: obrigatório, numérico, maior ou igual a NUM_DOC_INI
    if not num_doc_fin:
        return None
    try:
        num_doc_fin_int = int(num_doc_fin)
        if num_doc_fin_int < num_doc_ini_int:
            return None
    except ValueError:
        return None
    
    # DT_DOC: obrigatório, formato DDMMAAAA
    if not dt_doc:
        return None
    dt_doc_valida, dt_doc_obj = _validar_data(dt_doc)
    if not dt_doc_valida:
        return None
    # Nota: Validação de DT_DOC contra DT_INI e DT_FIN do registro 0000 não pode ser feita
    # sem acesso ao registro 0000
    
    # QTD_CANC: obrigatório, numérico, não negativo
    if not qtd_canc:
        return None
    qtd_canc_valido, qtd_canc_int, qtd_canc_erro = validar_valor_numerico(qtd_canc, decimais=0, obrigatorio=True, nao_negativo=True)
    if not qtd_canc_valido:
        return None
    
    # Todos os campos de valor são obrigatórios e numéricos com 2 decimais, não negativos
    campos_valor = {
        "VL_CONT": vl_cont,
        "VL_ISNT_ISS": vl_isnt_iss,
        "VL_BC_ISS": vl_bc_iss,
        "VL_ISS": vl_iss
    }
    
    valores = {}
    for campo_nome, campo_valor in campos_valor.items():
        if not campo_valor:
            return None
        campo_valido, campo_float, campo_erro = validar_valor_numerico(campo_valor, decimais=2, obrigatorio=True, nao_negativo=True)
        if not campo_valido:
            return None
        valores[campo_nome] = campo_float
    
    # COD_INF_OBS: opcional condicional, até 60 caracteres
    # Nota: Validação contra registro 0460 não pode ser feita diretamente
    if cod_inf_obs and len(cod_inf_obs) > 60:
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
        "COD_MOD": {
            "titulo": "Código do modelo do documento fiscal, conforme a Tabela 4.1.3",
            "valor": cod_mod
        },
        "SER": {
            "titulo": "Série do documento fiscal",
            "valor": ser if ser else ""
        },
        "NUM_DOC_INI": {
            "titulo": "Número do primeiro documento fiscal emitido no dia",
            "valor": num_doc_ini
        },
        "NUM_DOC_FIN": {
            "titulo": "Número do último documento fiscal emitido no dia",
            "valor": num_doc_fin
        },
        "DT_DOC": {
            "titulo": "Data da emissão dos documentos fiscais",
            "valor": dt_doc,
            "valor_formatado": formatar_data(dt_doc)
        },
        "QTD_CANC": {
            "titulo": "Quantidade de documentos cancelados",
            "valor": qtd_canc
        },
        "VL_CONT": {
            "titulo": "Valor contábil (valor total acumulado dos documentos)",
            "valor": vl_cont,
            "valor_formatado": formatar_valor(vl_cont)
        },
        "VL_ISNT_ISS": {
            "titulo": "Valor acumulado das operações isentas ou não-tributadas pelo ISS",
            "valor": vl_isnt_iss,
            "valor_formatado": formatar_valor(vl_isnt_iss)
        },
        "VL_BC_ISS": {
            "titulo": "Valor acumulado da base de cálculo do ISS",
            "valor": vl_bc_iss,
            "valor_formatado": formatar_valor(vl_bc_iss)
        },
        "VL_ISS": {
            "titulo": "Valor acumulado do ISS destacado",
            "valor": vl_iss,
            "valor_formatado": formatar_valor(vl_iss)
        },
        "COD_INF_OBS": {
            "titulo": "Código da observação do lançamento fiscal (campo 02 do Registro 0460)",
            "valor": cod_inf_obs if cod_inf_obs else ""
        }
    }
    
    return resultado


def validar_b030(linhas):
    """
    Valida uma ou mais linhas do registro B030 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |B030|COD_MOD|SER|NUM_DOC_INI|NUM_DOC_FIN|DT_DOC|QTD_CANC|VL_CONT|VL_ISNT_ISS|VL_BC_ISS|VL_ISS|COD_INF_OBS|
        
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
        resultado = _processar_linha_b030(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
