import re
import json
from datetime import datetime


def _processar_linha_0221(linha):
    """
    Processa uma única linha do registro 0221 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |0221|COD_ITEM_ATOMICO|QTD_CONTIDA|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |0221|...|)
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
    if reg != "0221":
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
    
    # Extrai todos os campos (3 campos no total)
    cod_item_atomico = obter_campo(1)
    qtd_contida = obter_campo(2)
    
    # Validações básicas dos campos obrigatórios
    # COD_ITEM_ATOMICO: obrigatório, até 60 caracteres
    # Validação: o valor informado no campo deve existir no campo COD_ITEM de um registro 0200
    # com TIPO_ITEM = "00" (validação básica de formato implementada; validação completa requer acesso ao registro 0200)
    if not cod_item_atomico or len(cod_item_atomico) > 60:
        return None
    
    # QTD_CONTIDA: obrigatório, numérico, deve ser maior ou igual a 1
    if not qtd_contida:
        return None
    
    # Converte QTD_CONTIDA para float para validar se é numérico e maior ou igual a 1
    try:
        # Remove vírgula e substitui por ponto para conversão
        qtd_contida_limpa = qtd_contida.replace(",", ".").replace(" ", "")
        qtd_contida_float = float(qtd_contida_limpa)
        if qtd_contida_float < 1:
            return None
    except ValueError:
        return None
    
    # Nota: A validação de que quando COD_ITEM_ATOMICO for igual ao COD_ITEM do Registro 0200 Pai,
    # QTD_CONTIDA deve ser igual a "1" não pode ser feita aqui sem acesso ao registro 0200 pai
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "COD_ITEM_ATOMICO": {
            "titulo": "Código do Item Atômico",
            "valor": cod_item_atomico
        },
        "QTD_CONTIDA": {
            "titulo": "Quantidade de Itens Atômicos Contidos no Item Informado no 0200 Pai",
            "valor": qtd_contida
        }
    }
    
    return resultado


def validar_0221(linhas):
    """
    Valida uma ou mais linhas do registro 0221 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |0221|COD_ITEM_ATOMICO|QTD_CONTIDA|
        
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
        resultado = _processar_linha_0221(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
