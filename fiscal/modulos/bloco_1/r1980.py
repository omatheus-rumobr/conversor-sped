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


def _processar_linha_1980(linha):
    """
    Processa uma única linha do registro 1980 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |1980|IND_AP|G4_01|G4_02|G4_03|G4_04|G4_05|G4_06|G4_07|G4_08|G4_09|G4_10|G4_11|G4_12|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |1980|...|)
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
    if reg != "1980":
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
    
    # Extrai todos os campos (14 campos no total)
    ind_ap = obter_campo(1)
    g4_01 = obter_campo(2)
    g4_02 = obter_campo(3)
    g4_03 = obter_campo(4)
    g4_04 = obter_campo(5)
    g4_05 = obter_campo(6)
    g4_06 = obter_campo(7)
    g4_07 = obter_campo(8)
    g4_08 = obter_campo(9)
    g4_09 = obter_campo(10)
    g4_10 = obter_campo(11)
    g4_11 = obter_campo(12)
    g4_12 = obter_campo(13)
    
    # Validações dos campos obrigatórios
    
    # IND_AP: obrigatório, valor válido: ["02"]
    if ind_ap != "02":
        return None
    
    # G4_01: obrigatório, numérico com 2 decimais, não negativo, deve ser >= 3 e <= 4
    if not g4_01:
        return None
    g4_01_valido, g4_01_float, g4_01_erro = validar_valor_numerico(g4_01, decimais=2, obrigatorio=True, nao_negativo=True)
    if not g4_01_valido:
        return None
    if g4_01_float < 3.0 or g4_01_float > 4.0:
        return None
    
    # G4_02: obrigatório, numérico com 2 decimais, não negativo
    if not g4_02:
        return None
    g4_02_valido, g4_02_float, g4_02_erro = validar_valor_numerico(g4_02, decimais=2, obrigatorio=True, nao_negativo=True)
    if not g4_02_valido:
        return None
    
    # G4_03: obrigatório, numérico com 2 decimais, não negativo
    if not g4_03:
        return None
    g4_03_valido, g4_03_float, g4_03_erro = validar_valor_numerico(g4_03, decimais=2, obrigatorio=True, nao_negativo=True)
    if not g4_03_valido:
        return None
    
    # G4_04: obrigatório, numérico com 2 decimais, não negativo, deve ser >= 2 e <= 4
    if not g4_04:
        return None
    g4_04_valido, g4_04_float, g4_04_erro = validar_valor_numerico(g4_04, decimais=2, obrigatorio=True, nao_negativo=True)
    if not g4_04_valido:
        return None
    if g4_04_float < 2.0 or g4_04_float > 4.0:
        return None
    
    # G4_05: obrigatório, numérico com 2 decimais, não negativo
    if not g4_05:
        return None
    g4_05_valido, g4_05_float, g4_05_erro = validar_valor_numerico(g4_05, decimais=2, obrigatorio=True, nao_negativo=True)
    if not g4_05_valido:
        return None
    
    # G4_06: obrigatório, numérico com 2 decimais, não negativo
    if not g4_06:
        return None
    g4_06_valido, g4_06_float, g4_06_erro = validar_valor_numerico(g4_06, decimais=2, obrigatorio=True, nao_negativo=True)
    if not g4_06_valido:
        return None
    
    # G4_07: obrigatório, numérico com 2 decimais
    if not g4_07:
        return None
    g4_07_valido, g4_07_float, g4_07_erro = validar_valor_numerico(g4_07, decimais=2, obrigatorio=True)
    if not g4_07_valido:
        return None
    
    # G4_08: obrigatório, numérico com 2 decimais, não negativo
    if not g4_08:
        return None
    g4_08_valido, g4_08_float, g4_08_erro = validar_valor_numerico(g4_08, decimais=2, obrigatorio=True, nao_negativo=True)
    if not g4_08_valido:
        return None
    
    # G4_09: obrigatório, numérico com 2 decimais, não negativo
    if not g4_09:
        return None
    g4_09_valido, g4_09_float, g4_09_erro = validar_valor_numerico(g4_09, decimais=2, obrigatorio=True, nao_negativo=True)
    if not g4_09_valido:
        return None
    
    # G4_10: obrigatório, numérico com 2 decimais, não negativo
    if not g4_10:
        return None
    g4_10_valido, g4_10_float, g4_10_erro = validar_valor_numerico(g4_10, decimais=2, obrigatorio=True, nao_negativo=True)
    if not g4_10_valido:
        return None
    
    # G4_11: obrigatório, numérico com 2 decimais
    if not g4_11:
        return None
    g4_11_valido, g4_11_float, g4_11_erro = validar_valor_numerico(g4_11, decimais=2, obrigatorio=True)
    if not g4_11_valido:
        return None
    
    # G4_12: obrigatório, numérico com 2 decimais, não negativo
    if not g4_12:
        return None
    g4_12_valido, g4_12_float, g4_12_erro = validar_valor_numerico(g4_12, decimais=2, obrigatorio=True, nao_negativo=True)
    if not g4_12_valido:
        return None
    
    # Validações de cálculos e relações entre campos
    
    # G4_08 <= G4_01 * G4_03 (Crédito presumido nas entradas <= Percentual de incentivo nas entradas * Entradas incentivadas)
    # Nota: G4_01 é um percentual, então precisa dividir por 100
    g4_01_percentual = g4_01_float / 100.0
    limite_g4_08 = g4_01_percentual * g4_03_float
    if g4_08_float > limite_g4_08 + 0.01:  # Tolerância para arredondamento
        return None
    
    # G4_09 <= G4_04 * G4_06 (Crédito presumido nas saídas <= Percentual de incentivo nas saídas * Saídas incentivadas)
    # Nota: G4_04 é um percentual, então precisa dividir por 100
    g4_04_percentual = g4_04_float / 100.0
    limite_g4_09 = g4_04_percentual * g4_06_float
    if g4_09_float > limite_g4_09 + 0.01:  # Tolerância para arredondamento
        return None
    
    # G4_10 = G4_08 + G4_09 (Dedução de incentivo = Crédito presumido nas entradas + Crédito presumido nas saídas)
    g4_10_calculado = g4_08_float + g4_09_float
    if abs(g4_10_float - g4_10_calculado) > 0.01:  # Tolerância para arredondamento
        return None
    
    # G4_11 = G4_07 - G4_10 (Saldo devedor após deduções = Saldo devedor antes - Dedução de incentivo)
    g4_11_calculado = g4_07_float - g4_10_float
    if abs(g4_11_float - g4_11_calculado) > 0.01:  # Tolerância para arredondamento
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
    
    # Formatação de percentual para exibição
    def formatar_percentual(valor_str):
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
        "IND_AP": {
            "titulo": "Indicador da sub-apuração por tipo de benefício (conforme Tabela 4.7.1)",
            "valor": ind_ap
        },
        "G4_01": {
            "titulo": "Entradas (percentual de incentivo)",
            "valor": g4_01,
            "valor_formatado": formatar_percentual(g4_01)
        },
        "G4_02": {
            "titulo": "Entradas não incentivadas de PI",
            "valor": g4_02,
            "valor_formatado": formatar_valor(g4_02)
        },
        "G4_03": {
            "titulo": "Entradas incentivadas de PI",
            "valor": g4_03,
            "valor_formatado": formatar_valor(g4_03)
        },
        "G4_04": {
            "titulo": "Saídas (percentual de incentivo)",
            "valor": g4_04,
            "valor_formatado": formatar_percentual(g4_04)
        },
        "G4_05": {
            "titulo": "Saídas não incentivadas de PI",
            "valor": g4_05,
            "valor_formatado": formatar_valor(g4_05)
        },
        "G4_06": {
            "titulo": "Saídas incentivadas de PI",
            "valor": g4_06,
            "valor_formatado": formatar_valor(g4_06)
        },
        "G4_07": {
            "titulo": "Saldo devedor do ICMS antes das deduções do incentivo (PI e itens não incentivados)",
            "valor": g4_07,
            "valor_formatado": formatar_valor(g4_07)
        },
        "G4_08": {
            "titulo": "Crédito presumido nas entradas incentivadas de PI",
            "valor": g4_08,
            "valor_formatado": formatar_valor(g4_08)
        },
        "G4_09": {
            "titulo": "Crédito presumido nas saídas incentivadas de PI",
            "valor": g4_09,
            "valor_formatado": formatar_valor(g4_09)
        },
        "G4_10": {
            "titulo": "Dedução de incentivo da Central de Distribuição (entradas/saídas)",
            "valor": g4_10,
            "valor_formatado": formatar_valor(g4_10)
        },
        "G4_11": {
            "titulo": "Saldo devedor do ICMS após deduções do incentivo",
            "valor": g4_11,
            "valor_formatado": formatar_valor(g4_11)
        },
        "G4_12": {
            "titulo": "Índice de recolhimento da central de distribuição",
            "valor": g4_12,
            "valor_formatado": formatar_valor(g4_12)
        }
    }
    
    return resultado


def validar_1980_fiscal(linhas):
    """
    Valida uma ou mais linhas do registro 1980 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |1980|IND_AP|G4_01|G4_02|G4_03|G4_04|G4_05|G4_06|G4_07|G4_08|G4_09|G4_10|G4_11|G4_12|
        
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
        resultado = _processar_linha_1980(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
