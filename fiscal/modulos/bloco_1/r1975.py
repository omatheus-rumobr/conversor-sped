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


def _processar_linha_1975(linha):
    """
    Processa uma única linha do registro 1975 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |1975|ALIQ_IMP_BASE|G3_10|G3_11|G3_12|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |1975|...|)
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
    if reg != "1975":
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
    aliq_imp_base = obter_campo(1)
    g3_10 = obter_campo(2)
    g3_11 = obter_campo(3)
    g3_12 = obter_campo(4)
    
    # Validações dos campos obrigatórios
    
    # ALIQ_IMP_BASE: obrigatório, valores válidos: [3.50, 6.00, 8.00, 10.00]
    if not aliq_imp_base:
        return None
    aliq_imp_base_valido, aliq_imp_base_float, aliq_imp_base_erro = validar_valor_numerico(aliq_imp_base, decimais=2, obrigatorio=True)
    if not aliq_imp_base_valido:
        return None
    
    aliq_imp_base_validos = [3.50, 6.00, 8.00, 10.00]
    # Compara com tolerância para arredondamento
    aliq_valida = False
    for aliq_valida_item in aliq_imp_base_validos:
        if abs(aliq_imp_base_float - aliq_valida_item) < 0.001:
            aliq_valida = True
            break
    
    if not aliq_valida:
        return None
    
    # G3_10: obrigatório, numérico com 2 decimais, não negativo
    if not g3_10:
        return None
    g3_10_valido, g3_10_float, g3_10_erro = validar_valor_numerico(g3_10, decimais=2, obrigatorio=True, nao_negativo=True)
    if not g3_10_valido:
        return None
    
    # G3_11: obrigatório, numérico com 2 decimais, não negativo
    if not g3_11:
        return None
    g3_11_valido, g3_11_float, g3_11_erro = validar_valor_numerico(g3_11, decimais=2, obrigatorio=True, nao_negativo=True)
    if not g3_11_valido:
        return None
    
    # G3_12: obrigatório, numérico com 2 decimais, não negativo
    if not g3_12:
        return None
    g3_12_valido, g3_12_float, g3_12_erro = validar_valor_numerico(g3_12, decimais=2, obrigatorio=True, nao_negativo=True)
    if not g3_12_valido:
        return None
    
    # Validação de cálculo: G3_12 <= ALIQ_IMP_BASE * G3_11
    # Nota: ALIQ_IMP_BASE é um percentual, então precisa dividir por 100
    aliq_imp_base_percentual = aliq_imp_base_float / 100.0
    limite_g3_12 = aliq_imp_base_percentual * g3_11_float
    if g3_12_float > limite_g3_12 + 0.01:  # Tolerância para arredondamento
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
    
    # Formatação de alíquota para exibição
    def formatar_aliquota(valor_str):
        if not valor_str:
            return ""
        try:
            valor_float = float(valor_str)
            return f"{valor_float:,.2f}%".replace(',', 'X').replace('.', ',').replace('X', '.')
        except ValueError:
            return valor_str
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "ALIQ_IMP_BASE": {
            "titulo": "Alíquota incidente sobre as importações-base",
            "valor": aliq_imp_base,
            "valor_formatado": formatar_aliquota(aliq_imp_base)
        },
        "G3_10": {
            "titulo": "Saídas incentivadas de PI",
            "valor": g3_10,
            "valor_formatado": formatar_valor(g3_10)
        },
        "G3_11": {
            "titulo": "Importações-base para o crédito presumido",
            "valor": g3_11,
            "valor_formatado": formatar_valor(g3_11)
        },
        "G3_12": {
            "titulo": "Crédito presumido nas saídas internas",
            "valor": g3_12,
            "valor_formatado": formatar_valor(g3_12)
        }
    }
    
    return resultado


def validar_1975_fiscal(linhas):
    """
    Valida uma ou mais linhas do registro 1975 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |1975|ALIQ_IMP_BASE|G3_10|G3_11|G3_12|
        
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
        resultado = _processar_linha_1975(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
