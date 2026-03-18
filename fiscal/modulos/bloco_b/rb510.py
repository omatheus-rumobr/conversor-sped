import re
import json
from datetime import datetime


def _validar_cpf(cpf_str):
    """
    Valida o CPF incluindo o dígito verificador.
    
    Args:
        cpf_str: String com o CPF (11 dígitos)
        
    Returns:
        bool: True se válido, False caso contrário
    """
    if not cpf_str or len(cpf_str) != 11 or not cpf_str.isdigit():
        return False
    
    # Verifica se todos os dígitos são iguais (CPFs inválidos conhecidos)
    if len(set(cpf_str)) == 1:
        return False
    
    # Extrai os 9 primeiros dígitos e os 2 dígitos verificadores
    cpf_9 = cpf_str[:9]
    dv1_informado = int(cpf_str[9])
    dv2_informado = int(cpf_str[10])
    
    # Calcula o primeiro dígito verificador
    soma = 0
    multiplicador = 10
    for digito in cpf_9:
        soma += int(digito) * multiplicador
        multiplicador -= 1
    
    resto = soma % 11
    if resto < 2:
        dv1_calculado = 0
    else:
        dv1_calculado = 11 - resto
    
    if dv1_calculado != dv1_informado:
        return False
    
    # Calcula o segundo dígito verificador
    cpf_10 = cpf_9 + str(dv1_calculado)
    soma = 0
    multiplicador = 11
    for digito in cpf_10:
        soma += int(digito) * multiplicador
        multiplicador -= 1
    
    resto = soma % 11
    if resto < 2:
        dv2_calculado = 0
    else:
        dv2_calculado = 11 - resto
    
    return dv2_calculado == dv2_informado


def _processar_linha_b510(linha):
    """
    Processa uma única linha do registro B510 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |B510|IND_PROF|IND_ESC|IND_SOC|CPF|NOME|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |B510|...|)
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
    if reg != "B510":
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
    ind_prof = obter_campo(1)
    ind_esc = obter_campo(2)
    ind_soc = obter_campo(3)
    cpf = obter_campo(4)
    nome = obter_campo(5)
    
    # Validações dos campos obrigatórios
    
    # IND_PROF: obrigatório, valores válidos: ["0", "1"]
    if ind_prof not in ["0", "1"]:
        return None
    
    # IND_ESC: obrigatório, valores válidos: ["0", "1"]
    if ind_esc not in ["0", "1"]:
        return None
    
    # IND_SOC: obrigatório, valores válidos: ["0", "1"]
    if ind_soc not in ["0", "1"]:
        return None
    
    # Validação: O profissional sócio necessariamente tem de ser habilitado (IND_SOC="0" implica IND_PROF="0")
    if ind_soc == "0" and ind_prof != "0":
        return None
    
    # CPF: obrigatório, 11 dígitos, com validação de dígito verificador
    if not cpf:
        return None
    if len(cpf) != 11 or not cpf.isdigit():
        return None
    if not _validar_cpf(cpf):
        return None
    
    # NOME: obrigatório, até 100 caracteres
    if not nome:
        return None
    if len(nome) > 100:
        return None
    
    # Mapeamento de códigos para descrições
    ind_prof_desc = {
        "0": "Profissional habilitado",
        "1": "Profissional não habilitado"
    }
    
    ind_esc_desc = {
        "0": "Nível superior",
        "1": "Nível médio"
    }
    
    ind_soc_desc = {
        "0": "Sócio",
        "1": "Não sócio"
    }
    
    # Formatação de CPF para exibição
    def formatar_cpf(cpf_str):
        if not cpf_str or len(cpf_str) != 11:
            return cpf_str
        return f"{cpf_str[:3]}.{cpf_str[3:6]}.{cpf_str[6:9]}-{cpf_str[9:11]}"
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "IND_PROF": {
            "titulo": "Indicador de habilitação",
            "valor": ind_prof,
            "descricao": ind_prof_desc.get(ind_prof, "")
        },
        "IND_ESC": {
            "titulo": "Indicador de escolaridade",
            "valor": ind_esc,
            "descricao": ind_esc_desc.get(ind_esc, "")
        },
        "IND_SOC": {
            "titulo": "Indicador de participação societária",
            "valor": ind_soc,
            "descricao": ind_soc_desc.get(ind_soc, "")
        },
        "CPF": {
            "titulo": "Número de inscrição do profissional no CPF",
            "valor": cpf,
            "valor_formatado": formatar_cpf(cpf)
        },
        "NOME": {
            "titulo": "Nome do profissional",
            "valor": nome
        }
    }
    
    return resultado


def validar_b510_fiscal(linhas):
    """
    Valida uma ou mais linhas do registro B510 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |B510|IND_PROF|IND_ESC|IND_SOC|CPF|NOME|
        
    Returns:
        String JSON com array de objetos contendo os campos validados.
        Cada objeto tem a estrutura {"CAMPO": {"titulo": "...", "valor": "...", "valor_formatado": "...", "descricao": "..."}}.
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
        resultado = _processar_linha_b510(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
