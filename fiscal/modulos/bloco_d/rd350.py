import re
import json
from datetime import datetime


def _processar_linha_d350(linha):
    """
    Processa uma única linha do registro D350 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |D350|COD_MOD|ECF_MOD|ECF_FAB|ECF_CX|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |D350|...|)
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
    if reg != "D350":
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
    cod_mod = obter_campo(1)
    ecf_mod = obter_campo(2)
    ecf_fab = obter_campo(3)
    ecf_cx = obter_campo(4)
    
    # Validações dos campos obrigatórios
    
    # COD_MOD: obrigatório, valores válidos: ["2E", "13", "14", "15", "16"]
    if not cod_mod or cod_mod not in ["2E", "13", "14", "15", "16"]:
        return None
    
    # ECF_MOD: obrigatório, até 20 caracteres
    if not ecf_mod or len(ecf_mod) > 20:
        return None
    
    # ECF_FAB: obrigatório, até 21 caracteres
    if not ecf_fab or len(ecf_fab) > 21:
        return None
    
    # ECF_CX: obrigatório, numérico, até 3 dígitos, maior que zero
    if not ecf_cx:
        return None
    if not ecf_cx.isdigit() or len(ecf_cx) > 3 or int(ecf_cx) <= 0:
        return None
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "COD_MOD": {
            "titulo": "Código do modelo do documento fiscal, conforme a Tabela 4.1.1",
            "valor": cod_mod,
            "descricao": {
                "2E": "Cupom Fiscal Bilhete de Passagem",
                "13": "Bilhete de Passagem Rodoviário",
                "14": "Bilhete de Passagem Aquaviário",
                "15": "Bilhete de Passagem e Nota de Bagagem",
                "16": "Bilhete de Passagem Ferroviário"
            }.get(cod_mod, "")
        },
        "ECF_MOD": {
            "titulo": "Modelo do equipamento",
            "valor": ecf_mod
        },
        "ECF_FAB": {
            "titulo": "Número de série de fabricação do ECF",
            "valor": ecf_fab
        },
        "ECF_CX": {
            "titulo": "Número do caixa atribuído ao ECF",
            "valor": ecf_cx
        }
    }
    
    return resultado


def validar_d350_fiscal(linhas):
    """
    Valida uma ou mais linhas do registro D350 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |D350|COD_MOD|ECF_MOD|ECF_FAB|ECF_CX|
        
    Returns:
        String JSON com array de objetos contendo os campos validados.
        Cada objeto tem a estrutura {"CAMPO": {"titulo": "...", "valor": "...", "descricao": "..."}}.
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
        resultado = _processar_linha_d350(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
