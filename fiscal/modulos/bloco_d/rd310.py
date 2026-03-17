import re
import json
from datetime import datetime


def _validar_codigo_municipio(cod_mun_str):
    """
    Valida o código do município IBGE (7 dígitos).
    Aceita também códigos especiais: 9999999 (Exterior) e 9999998 (CT-e simplificado).
    
    Args:
        cod_mun_str: String com o código do município
        
    Returns:
        bool: True se válido, False caso contrário
    """
    if not cod_mun_str:
        return False
    
    # Códigos especiais permitidos
    if cod_mun_str in ["9999999", "9999998"]:
        return True
    
    # Deve ter 7 dígitos numéricos
    if len(cod_mun_str) != 7 or not cod_mun_str.isdigit():
        return False
    
    return True


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


def _processar_linha_d310(linha):
    """
    Processa uma única linha do registro D310 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |D310|COD_MUN_ORIG|VL_SERV|VL_BC_ICMS|VL_ICMS|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |D310|...|)
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
    if reg != "D310":
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
    cod_mun_orig = obter_campo(1)
    vl_serv = obter_campo(2)
    vl_bc_icms = obter_campo(3)
    vl_icms = obter_campo(4)
    
    # Validações dos campos obrigatórios
    
    # COD_MUN_ORIG: obrigatório, 7 dígitos, deve existir na Tabela de Municípios do IBGE
    if not cod_mun_orig:
        return None
    if not _validar_codigo_municipio(cod_mun_orig):
        return None
    
    # VL_SERV: obrigatório, numérico com 2 decimais, maior que zero
    vl_serv_valido, vl_serv_float, _ = validar_valor_numerico(vl_serv, decimais=2, obrigatorio=True, positivo=True)
    if not vl_serv_valido:
        return None
    
    # VL_BC_ICMS: opcional condicional, numérico com 2 decimais, não negativo
    vl_bc_icms_valido, vl_bc_icms_float, _ = validar_valor_numerico(vl_bc_icms, decimais=2, obrigatorio=False, nao_negativo=True)
    if not vl_bc_icms_valido:
        return None
    
    # VL_ICMS: opcional condicional, numérico com 2 decimais, não negativo
    vl_icms_valido, vl_icms_float, _ = validar_valor_numerico(vl_icms, decimais=2, obrigatorio=False, nao_negativo=True)
    if not vl_icms_valido:
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
        "COD_MUN_ORIG": {
            "titulo": "Código do município de origem do serviço, conforme a tabela IBGE",
            "valor": cod_mun_orig
        },
        "VL_SERV": {
            "titulo": "Valor total da prestação de serviço",
            "valor": vl_serv,
            "valor_formatado": formatar_valor_monetario(vl_serv_float)
        },
        "VL_BC_ICMS": {
            "titulo": "Valor total da base de cálculo do ICMS",
            "valor": vl_bc_icms if vl_bc_icms else "",
            "valor_formatado": formatar_valor_monetario(vl_bc_icms_float) if vl_bc_icms else ""
        },
        "VL_ICMS": {
            "titulo": "Valor total do ICMS",
            "valor": vl_icms if vl_icms else "",
            "valor_formatado": formatar_valor_monetario(vl_icms_float) if vl_icms else ""
        }
    }
    
    return resultado


def validar_d310(linhas):
    """
    Valida uma ou mais linhas do registro D310 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |D310|COD_MUN_ORIG|VL_SERV|VL_BC_ICMS|VL_ICMS|
        
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
        resultado = _processar_linha_d310(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
