import re
import json
from datetime import datetime


def _validar_codigo_municipio(cod_mun_str):
    """
    Valida o código do município IBGE (7 dígitos).
    Aceita também códigos especiais: 9999999 (Exterior) e 9999998 (CT-e simplificado).
    
    Args:
        cod_mun_str: String com o código do município
        
    Returns:
        bool: True se válido, False caso contrário
    """
    if not cod_mun_str:
        return False
    
    # Códigos especiais permitidos
    if cod_mun_str in ["9999999", "9999998"]:
        return True
    
    # Deve ter 7 dígitos numéricos
    if len(cod_mun_str) != 7 or not cod_mun_str.isdigit():
        return False
    
    return True


def _processar_linha_d120(linha):
    """
    Processa uma única linha do registro D120 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |D120|COD_MUN_ORIG|COD_MUN_DEST|VEIC_ID|UF_ID|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |D120|...|)
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
    if reg != "D120":
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
    cod_mun_orig = obter_campo(1)
    cod_mun_dest = obter_campo(2)
    veic_id = obter_campo(3)
    uf_id = obter_campo(4)
    
    # Validações dos campos obrigatórios
    
    # COD_MUN_ORIG: obrigatório, 7 dígitos, deve existir na Tabela de Municípios do IBGE (ou 9999999 para Exterior)
    if not cod_mun_orig:
        return None
    if not _validar_codigo_municipio(cod_mun_orig):
        return None
    
    # COD_MUN_DEST: obrigatório, 7 dígitos, deve existir na Tabela de Municípios do IBGE (ou 9999999 para Exterior)
    if not cod_mun_dest:
        return None
    if not _validar_codigo_municipio(cod_mun_dest):
        return None
    
    # VEIC_ID: opcional condicional, 7 caracteres
    if veic_id and len(veic_id) > 7:
        return None
    
    # UF_ID: opcional condicional, 2 caracteres
    if uf_id and len(uf_id) > 2:
        return None
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "COD_MUN_ORIG": {
            "titulo": "Código do município de origem do serviço",
            "valor": cod_mun_orig
        },
        "COD_MUN_DEST": {
            "titulo": "Código do município de destino",
            "valor": cod_mun_dest
        },
        "VEIC_ID": {
            "titulo": "Placa de identificação do veículo",
            "valor": veic_id if veic_id else ""
        },
        "UF_ID": {
            "titulo": "Sigla da UF da placa do veículo",
            "valor": uf_id if uf_id else ""
        }
    }
    
    return resultado


def validar_d120_fiscal(linhas):
    """
    Valida uma ou mais linhas do registro D120 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |D120|COD_MUN_ORIG|COD_MUN_DEST|VEIC_ID|UF_ID|
        
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
        resultado = _processar_linha_d120(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
