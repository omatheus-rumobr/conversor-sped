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


def _processar_linha_1970(linha):
    """
    Processa uma única linha do registro 1970 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |1970|IND_AP|G3_01|G3_02|G3_03|G3_04|G3_05|G3_06|G3_07|G3_T|G3_08|G3_09|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |1970|...|)
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
    if reg != "1970":
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
    ind_ap = obter_campo(1)
    g3_01 = obter_campo(2)
    g3_02 = obter_campo(3)
    g3_03 = obter_campo(4)
    g3_04 = obter_campo(5)
    g3_05 = obter_campo(6)
    g3_06 = obter_campo(7)
    g3_07 = obter_campo(8)
    g3_t = obter_campo(9)
    g3_08 = obter_campo(10)
    g3_09 = obter_campo(11)
    
    # Validações dos campos obrigatórios
    
    # IND_AP: obrigatório, numérico, 2 dígitos (conforme tabela 4.7.1)
    # Nota: A validação contra a tabela 4.7.1 não pode ser feita diretamente sem acesso à tabela
    if not ind_ap or not ind_ap.isdigit() or len(ind_ap) != 2:
        return None
    
    # Todos os campos G3_XX são obrigatórios e numéricos com 2 decimais, não negativos
    campos_g3 = {
        "G3_01": g3_01,
        "G3_02": g3_02,
        "G3_03": g3_03,
        "G3_04": g3_04,
        "G3_05": g3_05,
        "G3_06": g3_06,
        "G3_07": g3_07,
        "G3_T": g3_t,
        "G3_08": g3_08,
        "G3_09": g3_09
    }
    
    valores_g3 = {}
    for campo_nome, campo_valor in campos_g3.items():
        if not campo_valor:
            return None
        campo_valido, campo_float, campo_erro = validar_valor_numerico(campo_valor, decimais=2, obrigatorio=True, nao_negativo=True)
        if not campo_valido:
            return None
        valores_g3[campo_nome] = campo_float
    
    # Validações de cálculos e relações entre campos
    
    # G3_02 <= G3_01 (ICMS diferido nas importações <= Importações com ICMS diferido)
    if valores_g3["G3_02"] > valores_g3["G3_01"] + 0.01:  # Tolerância para arredondamento
        return None
    
    # G3_06 <= G3_05 (ICMS das saídas incentivadas <= Saídas incentivadas de PI para fora do Estado)
    if valores_g3["G3_06"] > valores_g3["G3_05"] + 0.01:  # Tolerância para arredondamento
        return None
    
    # G3_07 <= (G3_04 * G3_06) (Crédito presumido <= Percentual de incentivo * ICMS das saídas incentivadas)
    # Nota: G3_04 é um percentual, então precisa ser dividido por 100
    g3_04_percentual = valores_g3["G3_04"] / 100.0
    limite_g3_07 = g3_04_percentual * valores_g3["G3_06"]
    if valores_g3["G3_07"] > limite_g3_07 + 0.01:  # Tolerância para arredondamento
        return None
    
    # G3_09 = G3_08 - G3_T (Saldo devedor após deduções = Saldo devedor antes - Dedução de incentivo)
    g3_09_calculado = valores_g3["G3_08"] - valores_g3["G3_T"]
    if abs(valores_g3["G3_09"] - g3_09_calculado) > 0.01:  # Tolerância para arredondamento
        return None
    
    # Nota: A validação G3_T = G3_07 + soma de todos os G3_12 não pode ser feita diretamente
    # pois G3_12 está em outro registro (provavelmente 1971 ou similar)
    # Também não podemos validar contra o registro E111 sem acesso a ele
    
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
            "titulo": "Indicador da sub-apuração por tipo de benefício (conforme tabela 4.7.1)",
            "valor": ind_ap
        },
        "G3_01": {
            "titulo": "Importações com ICMS diferido",
            "valor": g3_01,
            "valor_formatado": formatar_valor(g3_01)
        },
        "G3_02": {
            "titulo": "ICMS diferido nas importações",
            "valor": g3_02,
            "valor_formatado": formatar_valor(g3_02)
        },
        "G3_03": {
            "titulo": "Saídas não incentivadas de PI",
            "valor": g3_03,
            "valor_formatado": formatar_valor(g3_03)
        },
        "G3_04": {
            "titulo": "Percentual de incentivo nas saídas para fora do Estado",
            "valor": g3_04,
            "valor_formatado": formatar_percentual(g3_04)
        },
        "G3_05": {
            "titulo": "Saídas incentivadas de PI para fora do Estado",
            "valor": g3_05,
            "valor_formatado": formatar_valor(g3_05)
        },
        "G3_06": {
            "titulo": "ICMS das saídas incentivadas de PI para fora do Estado",
            "valor": g3_06,
            "valor_formatado": formatar_valor(g3_06)
        },
        "G3_07": {
            "titulo": "Crédito presumido nas saídas para fora do Estado",
            "valor": g3_07,
            "valor_formatado": formatar_valor(g3_07)
        },
        "G3_T": {
            "titulo": "Dedução de incentivo da Importação (crédito presumido)",
            "valor": g3_t,
            "valor_formatado": formatar_valor(g3_t)
        },
        "G3_08": {
            "titulo": "Saldo devedor do ICMS antes das deduções do incentivo",
            "valor": g3_08,
            "valor_formatado": formatar_valor(g3_08)
        },
        "G3_09": {
            "titulo": "Saldo devedor do ICMS após deduções do incentivo",
            "valor": g3_09,
            "valor_formatado": formatar_valor(g3_09)
        }
    }
    
    return resultado


def validar_1970(linhas):
    """
    Valida uma ou mais linhas do registro 1970 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |1970|IND_AP|G3_01|G3_02|G3_03|G3_04|G3_05|G3_06|G3_07|G3_T|G3_08|G3_09|
        
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
        resultado = _processar_linha_1970(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
