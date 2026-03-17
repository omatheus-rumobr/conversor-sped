import json
from datetime import datetime


def _validar_cnpj(cnpj):
    """
    Valida o formato básico do CNPJ (14 dígitos).
    Valida também o dígito verificador (DV).
    """
    if not cnpj:
        return False
    
    # Remove formatação
    cnpj_limpo = cnpj.replace(".", "").replace("/", "").replace("-", "").replace(" ", "")
    
    if not cnpj_limpo.isdigit() or len(cnpj_limpo) != 14:
        return False
    
    # Validação do dígito verificador
    # Verifica se todos os dígitos são iguais (CNPJ inválido)
    if len(set(cnpj_limpo)) == 1:
        return False
    
    # Calcula primeiro dígito verificador
    multiplicadores1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma = sum(int(cnpj_limpo[i]) * multiplicadores1[i] for i in range(12))
    resto = soma % 11
    dv1 = 0 if resto < 2 else 11 - resto
    
    if int(cnpj_limpo[12]) != dv1:
        return False
    
    # Calcula segundo dígito verificador
    multiplicadores2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma = sum(int(cnpj_limpo[i]) * multiplicadores2[i] for i in range(13))
    resto = soma % 11
    dv2 = 0 if resto < 2 else 11 - resto
    
    if int(cnpj_limpo[13]) != dv2:
        return False
    
    return True


def _obter_base_cnpj(cnpj):
    """
    Retorna os 8 primeiros dígitos do CNPJ (base).
    """
    if not cnpj:
        return None
    
    cnpj_limpo = cnpj.replace(".", "").replace("/", "").replace("-", "").replace(" ", "")
    
    if len(cnpj_limpo) != 14:
        return None
    
    return cnpj_limpo[:8]


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


def _processar_linha_0035(linha, dt_fin_0000=None, cnpj_0000=None):
    """
    Processa uma única linha do registro 0035 e retorna um dicionário.
    
    Formato:
      |0035|COD_SCP|DESC_SCP|INF_COMP|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "0035"
    - COD_SCP: obrigatório, 14 dígitos numéricos, sem formatação
      - Para fatos geradores a partir de abril/2021 (DT_FIN >= 01/04/2021):
        * Deve ser CNPJ válido (com DV)
        * Não pode ser mesmo CNPJ base do registro 0000
    - DESC_SCP: obrigatório, descrição da SCP
    - INF_COMP: opcional, informações complementares
    
    Nota: Este registro é obrigatório quando IND_NAT_PJ do 0000 for "03", "04" ou "05".
    Esta validação deve ser feita em uma camada superior.
    
    Args:
        linha: String com uma linha do SPED
        dt_fin_0000: Data final do período (ddmmaaaa) do registro 0000 (opcional, para validação de CNPJ)
        cnpj_0000: CNPJ do registro 0000 (opcional, para validação de que não é mesmo CNPJ base)
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |0035|...|)
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
    if reg != "0035":
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
    
    # Extrai todos os campos
    cod_scp = obter_campo(1)
    desc_scp = obter_campo(2)
    inf_comp = obter_campo(3)
    
    # COD_SCP: obrigatório, 14 dígitos numéricos, sem formatação
    if not cod_scp:
        return None
    
    # Remove formatação para validação
    cod_scp_limpo = cod_scp.replace(".", "").replace("/", "").replace("-", "").replace(" ", "")
    
    # Deve ter exatamente 14 dígitos numéricos
    if not cod_scp_limpo.isdigit() or len(cod_scp_limpo) != 14:
        return None
    
    # Verifica se o valor original tinha formatação (não permitido)
    if cod_scp != cod_scp_limpo:
        return None
    
    # Para fatos geradores a partir de abril/2021, validar como CNPJ
    validar_como_cnpj = False
    if dt_fin_0000:
        ok_data, dt_fin_obj = _validar_data(dt_fin_0000)
        if ok_data and dt_fin_obj:
            # Data limite: 01/04/2021
            data_limite = datetime(2021, 4, 1)
            if dt_fin_obj >= data_limite:
                validar_como_cnpj = True
    
    if validar_como_cnpj:
        # Deve ser CNPJ válido (com DV)
        if not _validar_cnpj(cod_scp_limpo):
            return None
        
        # Não pode ser mesmo CNPJ base do registro 0000
        if cnpj_0000:
            cnpj_0000_limpo = cnpj_0000.replace(".", "").replace("/", "").replace("-", "").replace(" ", "")
            base_cnpj_0000 = _obter_base_cnpj(cnpj_0000_limpo)
            base_cod_scp = _obter_base_cnpj(cod_scp_limpo)
            
            if base_cnpj_0000 and base_cod_scp and base_cnpj_0000 == base_cod_scp:
                return None
    
    # DESC_SCP: obrigatório
    if not desc_scp:
        return None
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "COD_SCP": {
            "titulo": "Identificação da SCP",
            "valor": cod_scp
        },
        "DESC_SCP": {
            "titulo": "Descrição da SCP",
            "valor": desc_scp
        }
    }
    
    # INF_COMP: opcional
    if inf_comp:
        resultado["INF_COMP"] = {
            "titulo": "Informação Complementar",
            "valor": inf_comp
        }
    else:
        resultado["INF_COMP"] = {
            "titulo": "Informação Complementar",
            "valor": ""
        }
    
    return resultado


def validar_0035(linhas, dt_fin_0000=None, cnpj_0000=None):
    """
    Valida uma ou mais linhas do registro 0035 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |0035|COD_SCP|DESC_SCP|INF_COMP|
        dt_fin_0000: Data final do período (ddmmaaaa) do registro 0000 (opcional, para validação de CNPJ)
        cnpj_0000: CNPJ do registro 0000 (opcional, para validação de que não é mesmo CNPJ base)
        
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
        resultado = _processar_linha_0035(linha, dt_fin_0000=dt_fin_0000, cnpj_0000=cnpj_0000)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
