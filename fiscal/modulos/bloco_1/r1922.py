import re
import json
from datetime import datetime


def _processar_linha_1922(linha):
    """
    Processa uma única linha do registro 1922 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |1922|NUM_DA|NUM_PROC|IND_PROC|PROC|TXT_COMPL|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |1922|...|)
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
    if reg != "1922":
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
    
    # Extrai todos os campos (6 campos no total)
    num_da = obter_campo(1)
    num_proc = obter_campo(2)
    ind_proc = obter_campo(3)
    proc = obter_campo(4)
    txt_compl = obter_campo(5)
    
    # Validações dos campos obrigatórios condicionais
    
    # NUM_DA: obrigatório condicional (sem limite de tamanho especificado)
    # Não há validação específica além de verificar se está presente quando necessário
    
    # NUM_PROC: obrigatório condicional, até 60 caracteres
    if num_proc and len(num_proc) > 60:
        return None
    
    # IND_PROC: obrigatório condicional, valores válidos: ["0", "1", "2", "9"]
    if ind_proc:
        ind_proc_validos = ["0", "1", "2", "9"]
        if ind_proc not in ind_proc_validos:
            return None
    
    # PROC: obrigatório condicional (sem limite de tamanho especificado)
    # Não há validação específica além de verificar se está presente quando necessário
    
    # TXT_COMPL: obrigatório condicional (sem limite de tamanho especificado)
    # Não há validação específica além de verificar se está presente quando necessário
    
    # Mapeamento de códigos para descrições
    ind_proc_desc = {
        "0": "SEFAZ",
        "1": "Justiça Federal",
        "2": "Justiça Estadual",
        "9": "Outros"
    }
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "NUM_DA": {
            "titulo": "Número do documento de arrecadação estadual, se houver",
            "valor": num_da if num_da else ""
        },
        "NUM_PROC": {
            "titulo": "Número do processo ao qual o ajuste está vinculado, se houver",
            "valor": num_proc if num_proc else ""
        },
        "IND_PROC": {
            "titulo": "Indicador da origem do processo",
            "valor": ind_proc if ind_proc else "",
            "descricao": ind_proc_desc.get(ind_proc, "") if ind_proc else ""
        },
        "PROC": {
            "titulo": "Descrição resumida do processo que embasou o lançamento",
            "valor": proc if proc else ""
        },
        "TXT_COMPL": {
            "titulo": "Descrição complementar",
            "valor": txt_compl if txt_compl else ""
        }
    }
    
    return resultado


def validar_1922(linhas):
    """
    Valida uma ou mais linhas do registro 1922 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |1922|NUM_DA|NUM_PROC|IND_PROC|PROC|TXT_COMPL|
        
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
        resultado = _processar_linha_1922(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
