import re
import json
from datetime import datetime


def _processar_linha_0305(linha):
    """
    Processa uma única linha do registro 0305 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |0305|COD_CCUS|FUNC|VIDA_UTIL|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |0305|...|)
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
    if reg != "0305":
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
    cod_ccus = obter_campo(1)
    func = obter_campo(2)
    vida_util = obter_campo(3)
    
    # Validações básicas dos campos obrigatórios
    # COD_CCUS: obrigatório, até 60 caracteres
    # Validação: o conteúdo informado deve existir no campo COD_CCUS do registro 0600
    # (validação básica de formato implementada; validação completa requer acesso ao registro 0600)
    if not cod_ccus or len(cod_ccus) > 60:
        return None
    
    # FUNC: obrigatório
    if not func:
        return None
    
    # VIDA_UTIL: opcional condicional, se informado deve ter 3 dígitos numéricos
    if vida_util:
        if not vida_util.isdigit() or len(vida_util) != 3:
            return None
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "COD_CCUS": {
            "titulo": "Código do Centro de Custo onde o Bem está sendo ou será Utilizado",
            "valor": cod_ccus
        },
        "FUNC": {
            "titulo": "Descrição Sucinta da Função do Bem na Atividade do Estabelecimento",
            "valor": func
        }
    }
    
    # VIDA_UTIL é opcional
    if vida_util:
        resultado["VIDA_UTIL"] = {
            "titulo": "Vida Útil Estimada do Bem, em Número de Meses",
            "valor": vida_util
        }
    else:
        resultado["VIDA_UTIL"] = {
            "titulo": "Vida Útil Estimada do Bem, em Número de Meses",
            "valor": ""
        }
    
    return resultado


def validar_0305(linhas):
    """
    Valida uma ou mais linhas do registro 0305 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |0305|COD_CCUS|FUNC|VIDA_UTIL|
        
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
        resultado = _processar_linha_0305(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
