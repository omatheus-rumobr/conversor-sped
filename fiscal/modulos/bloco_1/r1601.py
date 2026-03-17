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


def _processar_linha_1601(linha):
    """
    Processa uma única linha do registro 1601 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |1601|COD_PART_IP|COD_PART_IT|TOT_VS|TOT_ISS|TOT_OUTROS|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |1601|...|)
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
    if reg != "1601":
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
    
    # Extrai todos os campos (6 campos no total)
    cod_part_ip = obter_campo(1)
    cod_part_it = obter_campo(2)
    tot_vs = obter_campo(3)
    tot_iss = obter_campo(4)
    tot_outros = obter_campo(5)
    
    # Validações dos campos obrigatórios
    
    # COD_PART_IP: obrigatório, até 60 caracteres
    if not cod_part_ip or len(cod_part_ip) > 60:
        return None
    
    # COD_PART_IT: obrigatório condicional, até 60 caracteres
    if cod_part_it and len(cod_part_it) > 60:
        return None
    
    # TOT_VS: obrigatório, numérico com 2 decimais, não negativo
    if not tot_vs:
        return None
    tot_vs_valido, tot_vs_float, tot_vs_erro = validar_valor_numerico(tot_vs, decimais=2, obrigatorio=True, nao_negativo=True)
    if not tot_vs_valido:
        return None
    
    # TOT_ISS: obrigatório, numérico com 2 decimais, não negativo
    if not tot_iss:
        return None
    tot_iss_valido, tot_iss_float, tot_iss_erro = validar_valor_numerico(tot_iss, decimais=2, obrigatorio=True, nao_negativo=True)
    if not tot_iss_valido:
        return None
    
    # TOT_OUTROS: obrigatório, numérico com 2 decimais, não negativo
    if not tot_outros:
        return None
    tot_outros_valido, tot_outros_float, tot_outros_erro = validar_valor_numerico(tot_outros, decimais=2, obrigatorio=True, nao_negativo=True)
    if not tot_outros_valido:
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
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "COD_PART_IP": {
            "titulo": "Código do participante (campo 02 do Registro 0150): identificação da instituição que efetuou o pagamento",
            "valor": cod_part_ip
        },
        "COD_PART_IT": {
            "titulo": "Código do participante (campo 02 do Registro 0150): identificação do intermediador da transação",
            "valor": cod_part_it if cod_part_it else ""
        },
        "TOT_VS": {
            "titulo": "Valor total bruto das vendas e/ou prestações de serviços no campo de incidência do ICMS, incluindo operações com imunidade do imposto",
            "valor": tot_vs,
            "valor_formatado": formatar_valor(tot_vs)
        },
        "TOT_ISS": {
            "titulo": "Valor total bruto das prestações de serviços no campo de incidência do ISS",
            "valor": tot_iss,
            "valor_formatado": formatar_valor(tot_iss)
        },
        "TOT_OUTROS": {
            "titulo": "Valor total de operações deduzido dos valores dos campos TOT_VS e TOT_ISS",
            "valor": tot_outros,
            "valor_formatado": formatar_valor(tot_outros)
        }
    }
    
    return resultado


def validar_1601(linhas):
    """
    Valida uma ou mais linhas do registro 1601 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |1601|COD_PART_IP|COD_PART_IT|TOT_VS|TOT_ISS|TOT_OUTROS|
        
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
        resultado = _processar_linha_1601(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
