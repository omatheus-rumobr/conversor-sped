import re
import json
from datetime import datetime


def _processar_linha_1700(linha):
    """
    Processa uma única linha do registro 1700 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |1700|COD_DISP|COD_MOD|SER|SUB|NUM_DOC_INI|NUM_DOC_FIN|NUM_AUT|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |1700|...|)
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
    if reg != "1700":
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
    
    # Extrai todos os campos (8 campos no total)
    cod_disp = obter_campo(1)
    cod_mod = obter_campo(2)
    ser = obter_campo(3)
    sub = obter_campo(4)
    num_doc_ini = obter_campo(5)
    num_doc_fin = obter_campo(6)
    num_aut = obter_campo(7)
    
    # Validações dos campos obrigatórios
    
    # COD_DISP: obrigatório, valores válidos: ["00","01","02","03","04","05"]
    cod_disp_validos = ["00", "01", "02", "03", "04", "05"]
    if cod_disp not in cod_disp_validos:
        return None
    
    # COD_MOD: obrigatório, 2 caracteres
    if not cod_mod or len(cod_mod) != 2:
        return None
    
    # SER: obrigatório condicional, até 4 caracteres
    if ser and len(ser) > 4:
        return None
    
    # SUB: obrigatório condicional, até 3 caracteres
    if sub and len(sub) > 3:
        return None
    
    # NUM_DOC_INI: obrigatório, numérico, até 12 dígitos
    if not num_doc_ini:
        return None
    if not num_doc_ini.isdigit() or len(num_doc_ini) > 12:
        return None
    
    # NUM_DOC_FIN: obrigatório, numérico, até 12 dígitos
    if not num_doc_fin:
        return None
    if not num_doc_fin.isdigit() or len(num_doc_fin) > 12:
        return None
    
    # Validação: NUM_DOC_FIN deve ser maior ou igual a NUM_DOC_INI
    try:
        num_doc_ini_int = int(num_doc_ini)
        num_doc_fin_int = int(num_doc_fin)
        if num_doc_fin_int < num_doc_ini_int:
            return None
    except ValueError:
        return None
    
    # NUM_AUT: obrigatório, até 60 caracteres
    if not num_aut or len(num_aut) > 60:
        return None
    
    # Mapeamento de códigos para descrições
    cod_disp_desc = {
        "00": "Formulário de Segurança – impressor autônomo",
        "01": "FS-DA – Formulário de Segurança para Impressão de DANFE",
        "02": "Formulário de segurança - NF-e",
        "03": "Formulário Contínuo",
        "04": "Blocos",
        "05": "Jogos Soltos"
    }
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "COD_DISP": {
            "titulo": "Código dispositivo autorizado",
            "valor": cod_disp,
            "descricao": cod_disp_desc.get(cod_disp, "")
        },
        "COD_MOD": {
            "titulo": "Código do modelo do dispositivo autorizado, conforme a Tabela 4.1.1",
            "valor": cod_mod
        },
        "SER": {
            "titulo": "Série do dispositivo autorizado",
            "valor": ser if ser else ""
        },
        "SUB": {
            "titulo": "Subsérie do dispositivo autorizado",
            "valor": sub if sub else ""
        },
        "NUM_DOC_INI": {
            "titulo": "Número do dispositivo autorizado (utilizado) inicial",
            "valor": num_doc_ini
        },
        "NUM_DOC_FIN": {
            "titulo": "Número do dispositivo autorizado (utilizado) final",
            "valor": num_doc_fin
        },
        "NUM_AUT": {
            "titulo": "Número da autorização, conforme dispositivo autorizado",
            "valor": num_aut
        }
    }
    
    return resultado


def validar_1700(linhas):
    """
    Valida uma ou mais linhas do registro 1700 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |1700|COD_DISP|COD_MOD|SER|SUB|NUM_DOC_INI|NUM_DOC_FIN|NUM_AUT|
        
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
        resultado = _processar_linha_1700(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
