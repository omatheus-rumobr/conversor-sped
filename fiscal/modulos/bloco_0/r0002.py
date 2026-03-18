import re
import json
from datetime import datetime


def _processar_linha_0002(linha):
    """
    Processa uma única linha do registro 0002 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |0002|CLAS_ESTAB_IND|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |0002|...|)
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
    if reg != "0002":
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
    
    # Extrai todos os campos (2 campos no total)
    clas_estab_ind = obter_campo(1)
    
    # Validações básicas dos campos obrigatórios
    # CLAS_ESTAB_IND: obrigatório, 2 dígitos numéricos
    # Deve constar na Tabela 4.5.5 – Classificação de Contribuintes do IPI
    if not clas_estab_ind:
        return None
    
    # Valida formato: deve ser numérico com 2 dígitos
    if not clas_estab_ind.isdigit() or len(clas_estab_ind) != 2:
        return None
    
    # Validação adicional: valores válidos da Tabela 4.5.5
    # Como não temos acesso à tabela completa, validamos apenas o formato
    # Os valores típicos são: 00, 01, 02, 03, 04, 05, 06, 07, 08, 09, 10, etc.
    # Aceita qualquer valor numérico de 2 dígitos (00 a 99)
    # Se necessário, pode-se restringir aos valores específicos da tabela
    
    # Mapeamento básico de descrições (valores comuns da Tabela 4.5.5)
    # Nota: Este mapeamento pode precisar ser ajustado conforme a tabela oficial
    descricoes_clas = {
        "00": "00 - Outros",
        "01": "01 - Indústria",
        "02": "02 - Equiparado a industrial",
        "03": "03 - Produtor rural",
        "04": "04 - Importador",
        "05": "05 - Comerciante",
        "06": "06 - Prestador de serviços",
        "07": "07 - Outros"
    }
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "CLAS_ESTAB_IND": {
            "titulo": "Classificação do Estabelecimento Industrial ou Equiparado a Industrial",
            "valor": clas_estab_ind,
            "descricao": descricoes_clas.get(clas_estab_ind, f"{clas_estab_ind} - Classificação conforme Tabela 4.5.5")
        }
    }
    
    return resultado


def validar_0002_fiscal(linhas):
    """
    Valida uma ou mais linhas do registro 0002 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |0002|CLAS_ESTAB_IND|
        
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
        resultado = _processar_linha_0002(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)