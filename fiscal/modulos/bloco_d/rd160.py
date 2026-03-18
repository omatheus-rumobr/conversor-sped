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


def _validar_cnpj(cnpj_str):
    """
    Valida o CNPJ incluindo o dígito verificador.
    
    Args:
        cnpj_str: String com o CNPJ (14 dígitos)
        
    Returns:
        bool: True se válido, False caso contrário
    """
    if not cnpj_str or len(cnpj_str) != 14 or not cnpj_str.isdigit():
        return False
    
    # Verifica se todos os dígitos são iguais (CNPJs inválidos conhecidos)
    if len(set(cnpj_str)) == 1:
        return False
    
    # Extrai os 12 primeiros dígitos e os 2 dígitos verificadores
    cnpj_12 = cnpj_str[:12]
    dv1_informado = int(cnpj_str[12])
    dv2_informado = int(cnpj_str[13])
    
    # Calcula o primeiro dígito verificador
    multiplicadores1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma = sum(int(cnpj_12[i]) * multiplicadores1[i] for i in range(12))
    resto = soma % 11
    if resto < 2:
        dv1_calculado = 0
    else:
        dv1_calculado = 11 - resto
    
    if dv1_calculado != dv1_informado:
        return False
    
    # Calcula o segundo dígito verificador
    cnpj_13 = cnpj_12 + str(dv1_calculado)
    multiplicadores2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma = sum(int(cnpj_13[i]) * multiplicadores2[i] for i in range(13))
    resto = soma % 11
    if resto < 2:
        dv2_calculado = 0
    else:
        dv2_calculado = 11 - resto
    
    return dv2_calculado == dv2_informado


def _validar_cnpj_cpf(cnpj_cpf_str):
    """
    Valida CNPJ ou CPF baseado no tamanho.
    Se tiver 14 caracteres, valida como CNPJ.
    Se tiver 11 caracteres, valida como CPF.
    
    Args:
        cnpj_cpf_str: String com CNPJ ou CPF
        
    Returns:
        bool: True se válido, False caso contrário
    """
    if not cnpj_cpf_str:
        return False
    
    # Remove espaços e caracteres não numéricos para validação
    cnpj_cpf_limpo = ''.join(filter(str.isdigit, cnpj_cpf_str))
    
    if len(cnpj_cpf_limpo) == 14:
        return _validar_cnpj(cnpj_cpf_limpo)
    elif len(cnpj_cpf_limpo) == 11:
        return _validar_cpf(cnpj_cpf_limpo)
    else:
        return False


def _processar_linha_d160(linha):
    """
    Processa uma única linha do registro D160 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |D160|DESPACHO|CNPJ_CPF_REM|IE_REM|COD_MUN_ORI|CNPJ_CPF_DEST|IE_DEST|COD_MUN_DEST|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |D160|...|)
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
    if reg != "D160":
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
    despacho = obter_campo(1)
    cnpj_cpf_rem = obter_campo(2)
    ie_rem = obter_campo(3)
    cod_mun_ori = obter_campo(4)
    cnpj_cpf_dest = obter_campo(5)
    ie_dest = obter_campo(6)
    cod_mun_dest = obter_campo(7)
    
    # Validações dos campos obrigatórios
    
    # DESPACHO: opcional condicional (sem validação específica de formato no manual)
    
    # CNPJ_CPF_REM: opcional condicional
    # Validação: se 14 caracteres = CNPJ, se 11 = CPF
    if cnpj_cpf_rem:
        # Remove espaços e caracteres não numéricos para validação
        cnpj_cpf_rem_limpo = ''.join(filter(str.isdigit, cnpj_cpf_rem))
        if len(cnpj_cpf_rem_limpo) not in [11, 14]:
            return None
        if not _validar_cnpj_cpf(cnpj_cpf_rem_limpo):
            return None
    
    # IE_REM: opcional condicional, até 14 caracteres
    if ie_rem and len(ie_rem) > 14:
        return None
    
    # COD_MUN_ORI: obrigatório, 7 dígitos, deve existir na Tabela de Municípios do IBGE (ou 9999999 para Exterior)
    if not cod_mun_ori:
        return None
    if not _validar_codigo_municipio(cod_mun_ori):
        return None
    
    # CNPJ_CPF_DEST: opcional condicional
    # Validação: se 14 caracteres = CNPJ, se 11 = CPF
    if cnpj_cpf_dest:
        # Remove espaços e caracteres não numéricos para validação
        cnpj_cpf_dest_limpo = ''.join(filter(str.isdigit, cnpj_cpf_dest))
        if len(cnpj_cpf_dest_limpo) not in [11, 14]:
            return None
        if not _validar_cnpj_cpf(cnpj_cpf_dest_limpo):
            return None
    
    # IE_DEST: opcional condicional, até 14 caracteres
    if ie_dest and len(ie_dest) > 14:
        return None
    
    # COD_MUN_DEST: obrigatório, 7 dígitos, deve existir na Tabela de Municípios do IBGE (ou 9999999 para Exterior)
    if not cod_mun_dest:
        return None
    if not _validar_codigo_municipio(cod_mun_dest):
        return None
    
    # Formatação de CNPJ/CPF para exibição
    def formatar_cnpj_cpf(cnpj_cpf_str):
        if not cnpj_cpf_str:
            return ""
        # Remove espaços e caracteres não numéricos
        cnpj_cpf_limpo = ''.join(filter(str.isdigit, cnpj_cpf_str))
        if len(cnpj_cpf_limpo) == 14:
            # Formata CNPJ: XX.XXX.XXX/XXXX-XX
            return f"{cnpj_cpf_limpo[:2]}.{cnpj_cpf_limpo[2:5]}.{cnpj_cpf_limpo[5:8]}/{cnpj_cpf_limpo[8:12]}-{cnpj_cpf_limpo[12:14]}"
        elif len(cnpj_cpf_limpo) == 11:
            # Formata CPF: XXX.XXX.XXX-XX
            return f"{cnpj_cpf_limpo[:3]}.{cnpj_cpf_limpo[3:6]}.{cnpj_cpf_limpo[6:9]}-{cnpj_cpf_limpo[9:11]}"
        return cnpj_cpf_str
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "DESPACHO": {
            "titulo": "Identificação do número do despacho",
            "valor": despacho if despacho else ""
        },
        "CNPJ_CPF_REM": {
            "titulo": "CNPJ ou CPF do remetente das mercadorias",
            "valor": cnpj_cpf_rem if cnpj_cpf_rem else "",
            "valor_formatado": formatar_cnpj_cpf(cnpj_cpf_rem) if cnpj_cpf_rem else ""
        },
        "IE_REM": {
            "titulo": "Inscrição Estadual do remetente",
            "valor": ie_rem if ie_rem else ""
        },
        "COD_MUN_ORI": {
            "titulo": "Código do Município de origem",
            "valor": cod_mun_ori
        },
        "CNPJ_CPF_DEST": {
            "titulo": "CNPJ ou CPF do destinatário das mercadorias",
            "valor": cnpj_cpf_dest if cnpj_cpf_dest else "",
            "valor_formatado": formatar_cnpj_cpf(cnpj_cpf_dest) if cnpj_cpf_dest else ""
        },
        "IE_DEST": {
            "titulo": "Inscrição Estadual do destinatário",
            "valor": ie_dest if ie_dest else ""
        },
        "COD_MUN_DEST": {
            "titulo": "Código do Município de destino",
            "valor": cod_mun_dest
        }
    }
    
    return resultado


def validar_d160_fiscal(linhas):
    """
    Valida uma ou mais linhas do registro D160 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |D160|DESPACHO|CNPJ_CPF_REM|IE_REM|COD_MUN_ORI|CNPJ_CPF_DEST|IE_DEST|COD_MUN_DEST|
        
    Returns:
        String JSON com array de objetos contendo os campos validados.
        Cada objeto tem a estrutura {"CAMPO": {"titulo": "...", "valor": "...", "valor_formatado": "..."}}.
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
        resultado = _processar_linha_d160(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
