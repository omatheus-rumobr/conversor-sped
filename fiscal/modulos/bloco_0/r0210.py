import re
import json
from datetime import datetime


def _processar_linha_0210(linha):
    """
    Processa uma única linha do registro 0210 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |0210|COD_ITEM_COMP|QTD_COMP|PERDA|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |0210|...|)
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
    if reg != "0210":
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
    cod_item_comp = obter_campo(1)
    qtd_comp = obter_campo(2)
    perda = obter_campo(3)
    
    # Validações básicas dos campos obrigatórios
    # COD_ITEM_COMP: obrigatório, até 60 caracteres
    # Validação: o código do componente/insumo deverá existir no campo COD_ITEM do Registro 0200
    # (validação básica de formato implementada; validação completa requer acesso ao registro 0200)
    if not cod_item_comp or len(cod_item_comp) > 60:
        return None
    
    # QTD_COMP: obrigatório, numérico, deve ser maior que zero
    if not qtd_comp:
        return None
    
    # Converte QTD_COMP para float para validar se é numérico e maior que zero
    try:
        # Remove vírgula e substitui por ponto para conversão
        qtd_comp_limpa = qtd_comp.replace(",", ".").replace(" ", "")
        qtd_comp_float = float(qtd_comp_limpa)
        if qtd_comp_float <= 0:
            return None
    except ValueError:
        return None
    
    # PERDA: obrigatório, numérico (percentual)
    # A documentação menciona 4 dígitos, mas isso pode incluir decimais
    # Vou validar apenas se é numérico e não negativo
    if not perda:
        return None
    
    # Converte PERDA para float para validar se é numérico
    try:
        # Remove vírgula e substitui por ponto para conversão
        perda_limpa = perda.replace(",", ".").replace(" ", "")
        perda_float = float(perda_limpa)
        # Valida se não é negativo
        if perda_float < 0:
            return None
    except ValueError:
        return None
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "COD_ITEM_COMP": {
            "titulo": "Código do Item Componente/Insumo",
            "valor": cod_item_comp
        },
        "QTD_COMP": {
            "titulo": "Quantidade do Item Componente/Insumo para se Produzir uma Unidade do Item Composto/Resultante",
            "valor": qtd_comp
        },
        "PERDA": {
            "titulo": "Perda/Quebra Normal Percentual do Insumo/Componente",
            "valor": perda
        }
    }
    
    return resultado


def validar_0210_fiscal(linhas):
    """
    Valida uma ou mais linhas do registro 0210 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |0210|COD_ITEM_COMP|QTD_COMP|PERDA|
        
    Returns:
        String JSON com array de objetos contendo os campos validados.
        Cada objeto tem a estrutura {"CAMPO": {"titulo": "...", "valor": "..."}}.
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
        resultado = _processar_linha_0210(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
