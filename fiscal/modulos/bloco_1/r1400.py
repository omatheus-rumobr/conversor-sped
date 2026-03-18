import re
import json
from datetime import datetime


def _processar_linha_1400(linha):
    """
    Processa uma única linha do registro 1400 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |1400|COD_ITEM_IPM|MUN|VALOR|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |1400|...|)
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
    if reg != "1400":
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
    
    # Extrai todos os campos (4 campos no total)
    cod_item_ipm = obter_campo(1)
    mun = obter_campo(2)
    valor = obter_campo(3)
    
    # Validações básicas dos campos obrigatórios
    # COD_ITEM_IPM: obrigatório, até 60 caracteres
    if not cod_item_ipm or len(cod_item_ipm) > 60:
        return None
    
    # MUN: obrigatório, 7 dígitos numéricos (código IBGE)
    if not mun or len(mun) != 7 or not mun.isdigit():
        return None
    
    # VALOR: obrigatório, numérico com 2 decimais, deve ser maior que 0
    if not valor:
        return None
    try:
        valor_float = float(valor)
        if valor_float <= 0:
            return None
        # Verifica se tem mais de 2 casas decimais
        partes_decimal = valor.split('.')
        if len(partes_decimal) == 2 and len(partes_decimal[1]) > 2:
            return None
    except ValueError:
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
        "COD_ITEM_IPM": {
            "titulo": "Código do item (Tabela 5.9.1 de Itens UF Índice de Participação dos Municípios ou Tabela 5.9.2 de Itens UF_ST Índice de participação dos Municípios) ou campo 02 do Registro 0200",
            "valor": cod_item_ipm
        },
        "MUN": {
            "titulo": "Código do Município de origem/destino",
            "valor": mun
        },
        "VALOR": {
            "titulo": "Valor mensal correspondente ao município",
            "valor": valor,
            "valor_formatado": formatar_valor(valor)
        }
    }
    
    return resultado


def validar_1400_fiscal(linhas):
    """
    Valida uma ou mais linhas do registro 1400 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |1400|COD_ITEM_IPM|MUN|VALOR|
        
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
        resultado = _processar_linha_1400(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
