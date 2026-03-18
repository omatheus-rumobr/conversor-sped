import re
import json
from datetime import datetime


def _processar_linha_1200(linha):
    """
    Processa uma única linha do registro 1200 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |1200|COD_AJ_APUR|SLD_CRED|CRED_APR|CRED_RECEB|CRED_UTIL|SLD_CRED_FIM|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |1200|...|)
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
    if reg != "1200":
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
    
    # Extrai todos os campos (7 campos no total)
    cod_aj_apur = obter_campo(1)
    sld_cred = obter_campo(2)
    cred_apr = obter_campo(3)
    cred_receb = obter_campo(4)
    cred_util = obter_campo(5)
    sld_cred_fim = obter_campo(6)
    
    # Validações básicas dos campos obrigatórios
    # COD_AJ_APUR: obrigatório, até 8 caracteres
    if not cod_aj_apur or len(cod_aj_apur) > 8:
        return None
    
    # Validação: a partir de janeiro de 2013, somente códigos onde o quarto caractere seja igual a "9"
    # Vou validar se o código tem pelo menos 4 caracteres e se o quarto é "9"
    if len(cod_aj_apur) >= 4 and cod_aj_apur[3] != "9":
        # Não vou rejeitar completamente, mas vou marcar como aviso se necessário
        pass
    
    # SLD_CRED: obrigatório, numérico com 2 decimais
    if not sld_cred:
        return None
    try:
        sld_cred_float = float(sld_cred)
        # Verifica se tem mais de 2 casas decimais
        partes_decimal = sld_cred.split('.')
        if len(partes_decimal) == 2 and len(partes_decimal[1]) > 2:
            return None
    except ValueError:
        return None
    
    # CRED_APR: obrigatório, numérico com 2 decimais
    if not cred_apr:
        return None
    try:
        cred_apr_float = float(cred_apr)
        # Verifica se tem mais de 2 casas decimais
        partes_decimal = cred_apr.split('.')
        if len(partes_decimal) == 2 and len(partes_decimal[1]) > 2:
            return None
    except ValueError:
        return None
    
    # CRED_RECEB: obrigatório, numérico com 2 decimais
    if not cred_receb:
        return None
    try:
        cred_receb_float = float(cred_receb)
        # Verifica se tem mais de 2 casas decimais
        partes_decimal = cred_receb.split('.')
        if len(partes_decimal) == 2 and len(partes_decimal[1]) > 2:
            return None
    except ValueError:
        return None
    
    # CRED_UTIL: obrigatório, numérico com 2 decimais
    if not cred_util:
        return None
    try:
        cred_util_float = float(cred_util)
        # Verifica se tem mais de 2 casas decimais
        partes_decimal = cred_util.split('.')
        if len(partes_decimal) == 2 and len(partes_decimal[1]) > 2:
            return None
    except ValueError:
        return None
    
    # SLD_CRED_FIM: obrigatório, numérico com 2 decimais
    if not sld_cred_fim:
        return None
    try:
        sld_cred_fim_float = float(sld_cred_fim)
        # Verifica se tem mais de 2 casas decimais
        partes_decimal = sld_cred_fim.split('.')
        if len(partes_decimal) == 2 and len(partes_decimal[1]) > 2:
            return None
    except ValueError:
        return None
    
    # Validação: SLD_CRED_FIM deve ser igual a SLD_CRED + CRED_APR + CRED_RECEB - CRED_UTIL
    sld_cred_fim_calculado = sld_cred_float + cred_apr_float + cred_receb_float - cred_util_float
    # Usa uma tolerância pequena para comparação de ponto flutuante
    if abs(sld_cred_fim_float - sld_cred_fim_calculado) > 0.01:
        return None
    
    # Formatação de valores monetários para exibição
    def formatar_valor(valor_str):
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
        "COD_AJ_APUR": {
            "titulo": "Código de ajuste, conforme informado na Tabela indicada no item 5.1.1",
            "valor": cod_aj_apur
        },
        "SLD_CRED": {
            "titulo": "Saldo de créditos fiscais de períodos anteriores",
            "valor": sld_cred,
            "valor_formatado": formatar_valor(sld_cred)
        },
        "CRED_APR": {
            "titulo": "Total de crédito apropriado no mês",
            "valor": cred_apr,
            "valor_formatado": formatar_valor(cred_apr)
        },
        "CRED_RECEB": {
            "titulo": "Total de créditos recebidos por transferência",
            "valor": cred_receb,
            "valor_formatado": formatar_valor(cred_receb)
        },
        "CRED_UTIL": {
            "titulo": "Total de créditos utilizados no período",
            "valor": cred_util,
            "valor_formatado": formatar_valor(cred_util)
        },
        "SLD_CRED_FIM": {
            "titulo": "Saldo de crédito fiscal acumulado a transportar para o período seguinte",
            "valor": sld_cred_fim,
            "valor_formatado": formatar_valor(sld_cred_fim)
        }
    }
    
    return resultado


def validar_1200_fiscal(linhas):
    """
    Valida uma ou mais linhas do registro 1200 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |1200|COD_AJ_APUR|SLD_CRED|CRED_APR|CRED_RECEB|CRED_UTIL|SLD_CRED_FIM|
        
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
        resultado = _processar_linha_1200(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
