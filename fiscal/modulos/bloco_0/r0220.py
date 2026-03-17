import re
import json
from datetime import datetime


def _validar_codigo_barras(cod_barra):
    """
    Valida formato básico de código de barras GTIN (GTIN-8, GTIN-12, GTIN-13 ou GTIN-14).
    
    Args:
        cod_barra: String com código de barras
        
    Returns:
        bool: True se formato válido, False caso contrário
    """
    if not cod_barra:
        return False
    
    # Remove espaços
    cod_limpo = cod_barra.replace(" ", "")
    
    # GTIN-8: 8 dígitos
    # GTIN-12: 12 dígitos (UPC-A)
    # GTIN-13: 13 dígitos (EAN-13)
    # GTIN-14: 14 dígitos
    if cod_limpo.isdigit() and len(cod_limpo) in [8, 12, 13, 14]:
        return True
    
    return False


def _processar_linha_0220(linha):
    """
    Processa uma única linha do registro 0220 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |0220|UNID_CONV|FAT_CONV|COD_BARRA|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |0220|...|)
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
    if reg != "0220":
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
    unid_conv = obter_campo(1)
    fat_conv = obter_campo(2)
    cod_barra = obter_campo(3)
    
    # Validações básicas dos campos obrigatórios
    # UNID_CONV: obrigatório, até 6 caracteres
    # Validação: o valor informado no campo deve existir no campo UNID do registro 0190
    # (validação básica de formato implementada; validação completa requer acesso ao registro 0190)
    if not unid_conv or len(unid_conv) > 6:
        return None
    
    # FAT_CONV: obrigatório, numérico, deve ser maior que zero
    if not fat_conv:
        return None
    
    # Converte FAT_CONV para float para validar se é numérico e maior que zero
    try:
        # Remove vírgula e substitui por ponto para conversão
        fat_conv_limpa = fat_conv.replace(",", ".").replace(" ", "")
        fat_conv_float = float(fat_conv_limpa)
        if fat_conv_float <= 0:
            return None
    except ValueError:
        return None
    
    # COD_BARRA: opcional condicional, se informado deve ser código GTIN válido
    if cod_barra and not _validar_codigo_barras(cod_barra):
        return None
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "UNID_CONV": {
            "titulo": "Unidade Comercial a ser Convertida na Unidade de Estoque",
            "valor": unid_conv
        },
        "FAT_CONV": {
            "titulo": "Fator de Conversão",
            "valor": fat_conv
        }
    }
    
    # COD_BARRA é opcional
    if cod_barra:
        resultado["COD_BARRA"] = {
            "titulo": "Representação Alfanumérica do Código de Barra da Unidade Comercial do Produto",
            "valor": cod_barra
        }
    else:
        resultado["COD_BARRA"] = {
            "titulo": "Representação Alfanumérica do Código de Barra da Unidade Comercial do Produto",
            "valor": ""
        }
    
    return resultado


def validar_0220(linhas):
    """
    Valida uma ou mais linhas do registro 0220 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |0220|UNID_CONV|FAT_CONV|COD_BARRA|
        
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
        resultado = _processar_linha_0220(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
