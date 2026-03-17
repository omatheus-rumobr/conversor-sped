import re
import json
from datetime import datetime


def _validar_cnpj(cnpj):
    """
    Valida o formato básico do CNPJ (14 dígitos).
    Não valida o dígito verificador completo, apenas o formato.
    """
    if not cnpj:
        return False
    # Remove formatação
    cnpj_limpo = cnpj.replace(".", "").replace("/", "").replace("-", "").replace(" ", "")
    if not cnpj_limpo.isdigit() or len(cnpj_limpo) != 14:
        return False
    return True


def _validar_cpf(cpf):
    """
    Valida o formato básico do CPF (11 dígitos).
    Não valida o dígito verificador completo, apenas o formato.
    """
    if not cpf:
        return False
    # Remove formatação
    cpf_limpo = cpf.replace(".", "").replace("-", "").replace(" ", "")
    if not cpf_limpo.isdigit() or len(cpf_limpo) != 11:
        return False
    return True


def _validar_data(data_str):
    """
    Valida se a data está no formato ddmmaaaa e se é uma data válida.
    
    Args:
        data_str: String com data no formato ddmmaaaa
        
    Returns:
        tuple: (True/False, datetime object ou None)
    """
    if not data_str or len(data_str) != 8 or not data_str.isdigit():
        return False, None
    
    try:
        dia = int(data_str[:2])
        mes = int(data_str[2:4])
        ano = int(data_str[4:8])
        data_obj = datetime(ano, mes, dia)
        return True, data_obj
    except ValueError:
        return False, None


def _processar_linha_0175(linha):
    """
    Processa uma única linha do registro 0175 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |0175|DT_ALT|NR_CAMPO|CONT_ANT|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |0175|...|)
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
    if reg != "0175":
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
    dt_alt = obter_campo(1)
    nr_campo = obter_campo(2)
    cont_ant = obter_campo(3)
    
    # Validações básicas dos campos obrigatórios
    # DT_ALT: obrigatório, formato ddmmaaaa, data válida
    dt_alt_valida, dt_alt_obj = _validar_data(dt_alt)
    if not dt_alt_valida:
        return None
    
    # NR_CAMPO: obrigatório, valores válidos [03, 04, 05, 06, 08, 09, 10, 11, 12, 13]
    valores_validos_nr_campo = ["03", "04", "05", "06", "08", "09", "10", "11", "12", "13"]
    if not nr_campo or nr_campo not in valores_validos_nr_campo:
        return None
    
    # CONT_ANT: obrigatório, até 100 caracteres
    if not cont_ant or len(cont_ant) > 100:
        return None
    
    # Validações específicas conforme NR_CAMPO
    # Se NR_CAMPO = 05 (CNPJ), validar formato
    if nr_campo == "05" and not _validar_cnpj(cont_ant):
        return None
    
    # Se NR_CAMPO = 06 (CPF), validar formato
    if nr_campo == "06" and not _validar_cpf(cont_ant):
        return None
    
    # Se NR_CAMPO = 08 (COD_MUN), validar formato (7 dígitos)
    if nr_campo == "08":
        if not cont_ant.isdigit() or len(cont_ant) != 7:
            return None
    
    # Mapeamento de descrições dos campos do registro 0150
    descricoes_campos = {
        "03": "NOME",
        "04": "COD_PAIS",
        "05": "CNPJ",
        "06": "CPF",
        "08": "COD_MUN",
        "09": "SUFRAMA",
        "10": "END",
        "11": "NUM",
        "12": "COMPL",
        "13": "BAIRRO"
    }
    
    nome_campo = descricoes_campos.get(nr_campo, f"Campo {nr_campo}")
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "DT_ALT": {
            "titulo": "Data de Alteração do Cadastro",
            "valor": dt_alt
        },
        "NR_CAMPO": {
            "titulo": "Número do Campo Alterado",
            "valor": nr_campo,
            "descricao": f"{nr_campo} - {nome_campo}"
        },
        "CONT_ANT": {
            "titulo": "Conteúdo Anterior do Campo",
            "valor": cont_ant
        }
    }
    
    return resultado


def validar_0175(linhas):
    """
    Valida uma ou mais linhas do registro 0175 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |0175|DT_ALT|NR_CAMPO|CONT_ANT|
        
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
        resultado = _processar_linha_0175(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
