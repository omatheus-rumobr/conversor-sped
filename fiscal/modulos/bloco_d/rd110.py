import re
import json
from datetime import datetime


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


def _processar_linha_d110(linha):
    """
    Processa uma única linha do registro D110 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |D110|NUM_ITEM|COD_ITEM|VL_SERV|VL_OUT|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |D110|...|)
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
    if reg != "D110":
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
    
    # Extrai todos os campos (5 campos no total)
    num_item = obter_campo(1)
    cod_item = obter_campo(2)
    vl_serv = obter_campo(3)
    vl_out = obter_campo(4)
    
    # Validações dos campos obrigatórios
    
    # NUM_ITEM: obrigatório, numérico, até 3 dígitos, maior que zero
    if not num_item:
        return None
    if not num_item.isdigit():
        return None
    num_item_int = int(num_item)
    if num_item_int <= 0:
        return None
    if len(num_item) > 3:
        return None
    
    # COD_ITEM: obrigatório, até 60 caracteres
    if not cod_item:
        return None
    if len(cod_item) > 60:
        return None
    
    # VL_SERV: obrigatório, numérico com 2 decimais, não negativo
    vl_serv_valido, vl_serv_float, _ = validar_valor_numerico(vl_serv, decimais=2, obrigatorio=True, nao_negativo=True)
    if not vl_serv_valido:
        return None
    
    # VL_OUT: opcional, numérico com 2 decimais, não negativo
    vl_out_valido, vl_out_float, _ = validar_valor_numerico(vl_out, decimais=2, obrigatorio=False, nao_negativo=True)
    if not vl_out_valido:
        return None
    
    # Formatação de valores monetários
    def formatar_valor_monetario(valor_float):
        if valor_float is None:
            return ""
        return f"R$ {valor_float:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "NUM_ITEM": {
            "titulo": "Número sequencial do item no documento fiscal",
            "valor": num_item
        },
        "COD_ITEM": {
            "titulo": "Código do item (campo 02 do Registro 0200)",
            "valor": cod_item
        },
        "VL_SERV": {
            "titulo": "Valor do serviço",
            "valor": vl_serv,
            "valor_formatado": formatar_valor_monetario(vl_serv_float)
        },
        "VL_OUT": {
            "titulo": "Outros valores",
            "valor": vl_out if vl_out else "",
            "valor_formatado": formatar_valor_monetario(vl_out_float) if vl_out else ""
        }
    }
    
    return resultado


def validar_d110(linhas):
    """
    Valida uma ou mais linhas do registro D110 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |D110|NUM_ITEM|COD_ITEM|VL_SERV|VL_OUT|
        
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
        resultado = _processar_linha_d110(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
