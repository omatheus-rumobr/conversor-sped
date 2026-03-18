import re
import json
from datetime import datetime


def _processar_linha_1350(linha):
    """
    Processa uma única linha do registro 1350 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |1350|SERIE|FABRICANTE|MODELO|TIPO_MEDICAO|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |1350|...|)
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
    if reg != "1350":
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
    serie = obter_campo(1)
    fabricante = obter_campo(2)
    modelo = obter_campo(3)
    tipo_medicao = obter_campo(4)
    
    # Validações básicas dos campos obrigatórios
    # SERIE: obrigatório
    if not serie:
        return None
    
    # FABRICANTE: obrigatório, até 60 caracteres
    if not fabricante or len(fabricante) > 60:
        return None
    
    # MODELO: obrigatório
    if not modelo:
        return None
    
    # TIPO_MEDICAO: obrigatório, valores válidos [0, 1]
    if not tipo_medicao or tipo_medicao not in ["0", "1"]:
        return None
    
    # Mapeamento de descrições
    tipo_medicao_desc = {
        "0": "Analógico",
        "1": "Digital"
    }
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "SERIE": {
            "titulo": "Número de Série da Bomba",
            "valor": serie
        },
        "FABRICANTE": {
            "titulo": "Nome do Fabricante da Bomba",
            "valor": fabricante
        },
        "MODELO": {
            "titulo": "Modelo da Bomba",
            "valor": modelo
        },
        "TIPO_MEDICAO": {
            "titulo": "Identificador de medição",
            "valor": tipo_medicao,
            "descricao": tipo_medicao_desc.get(tipo_medicao, "")
        }
    }
    
    return resultado


def validar_1350_fiscal(linhas):
    """
    Valida uma ou mais linhas do registro 1350 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |1350|SERIE|FABRICANTE|MODELO|TIPO_MEDICAO|
        
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
        resultado = _processar_linha_1350(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
