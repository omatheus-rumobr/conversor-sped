import json
from datetime import datetime


def _validar_cnpj(cnpj):
    """
    Valida o formato básico do CNPJ (14 dígitos).
    Não valida o dígito verificador completo, apenas o formato.
    """
    if not cnpj:
        return False

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


def _validar_uf(uf):
    """
    Valida se a UF é uma sigla válida do Brasil.
    
    Args:
        uf: String com sigla da UF
        
    Returns:
        bool: True se válida, False caso contrário
    """
    ufs_validas = [
        'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA',
        'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN',
        'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
    ]
    return uf.upper() in ufs_validas


def _processar_linha_0000(linha):
    """
    Processa uma única linha do registro 0000 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |0000|COD_VER|COD_FIN|DT_INI|DT_FIN|NOME|CNPJ|CPF|UF|IE|COD_MUN|IM|SUFRAMA|IND_PERFIL|IND_ATIV|
        
    Returns:
        dict: Dicionário com os campos validados contendo título e valor, ou None se inválido
    """
    if not linha or not isinstance(linha, str):
        return None
    
    linha = linha.strip()
    

    if not linha:
        return None
    

    partes = linha.split('|')

    if partes and not partes[0]:
        partes = partes[1:]
    if partes and not partes[-1]:
        partes = partes[:-1]
    

    if len(partes) < 1:
        return None
    

    reg = partes[0].strip() if partes else ""
    

    if reg != "0000":
        return None
    

    def obter_campo(indice):
        if indice < len(partes):
            valor = partes[indice].strip()

            if valor == "-":
                return ""
            return valor if valor else ""
        return ""
    

    cod_ver = obter_campo(1)
    cod_fin = obter_campo(2)
    dt_ini = obter_campo(3)
    dt_fin = obter_campo(4)
    nome = obter_campo(5)
    cnpj = obter_campo(6)
    cpf = obter_campo(7)
    uf = obter_campo(8)
    ie = obter_campo(9)
    cod_mun = obter_campo(10)
    im = obter_campo(11)
    suframa = obter_campo(12)
    ind_perfil = obter_campo(13)
    ind_ativ = obter_campo(14)
    

    if not cod_ver or not cod_ver.isdigit() or len(cod_ver) != 3:
        return None
    

    if cod_fin not in ["0", "1"]:
        return None
    

    dt_ini_valida, dt_ini_obj = _validar_data(dt_ini)
    if not dt_ini_valida:
        return None
    

    dt_fin_valida, dt_fin_obj = _validar_data(dt_fin)
    if not dt_fin_valida:
        return None
    

    if dt_ini_obj and dt_fin_obj:
        if dt_ini_obj.year != dt_fin_obj.year or dt_ini_obj.month != dt_fin_obj.month:
            return None
    

    if not nome or len(nome) > 100:
        return None
    

    cnpj_valido = _validar_cnpj(cnpj) if cnpj else False
    cpf_valido = _validar_cpf(cpf) if cpf else False
    
    if not cnpj_valido and not cpf_valido:
        return None
    

    if cnpj_valido and cpf_valido:
        return None
    

    if not uf or not _validar_uf(uf):
        return None
    

    if not ie or len(ie) > 14:
        return None
    

    if not cod_mun or not cod_mun.isdigit() or len(cod_mun) != 7:
        return None
    

    if ind_perfil not in ["A", "B", "C"]:
        return None
    
 
    if ind_ativ not in ["0", "1"]:
        return None
    

    if cpf_valido and ind_ativ != "1":
        return None
    

    if suframa and len(suframa) != 9:
        return None
    

    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "COD_VER": {
            "titulo": "Código da Versão do Leiaute",
            "valor": cod_ver
        },
        "COD_FIN": {
            "titulo": "Código da Finalidade do Arquivo",
            "valor": cod_fin,
            "descricao": "0 - Remessa do arquivo original" if cod_fin == "0" else "1 - Remessa do arquivo substituto"
        },
        "DT_INI": {
            "titulo": "Data Inicial",
            "valor": dt_ini
        },
        "DT_FIN": {
            "titulo": "Data Final",
            "valor": dt_fin
        },
        "NOME": {
            "titulo": "Nome Empresarial da Entidade",
            "valor": nome
        }
    }
    

    if cnpj_valido:
        resultado["CNPJ"] = {
            "titulo": "Número de Inscrição no CNPJ",
            "valor": cnpj
        }
    else:
        resultado["CNPJ"] = {
            "titulo": "Número de Inscrição no CNPJ",
            "valor": ""
        }
    
    if cpf_valido:
        resultado["CPF"] = {
            "titulo": "Número de Inscrição no CPF",
            "valor": cpf
        }
    else:
        resultado["CPF"] = {
            "titulo": "Número de Inscrição no CPF",
            "valor": ""
        }
    
    resultado["UF"] = {
        "titulo": "Sigla da Unidade da Federação",
        "valor": uf
    }
    
    resultado["IE"] = {
        "titulo": "Inscrição Estadual",
        "valor": ie
    }
    
    resultado["COD_MUN"] = {
        "titulo": "Código do Município",
        "valor": cod_mun
    }
    

    if im:
        resultado["IM"] = {
            "titulo": "Inscrição Municipal",
            "valor": im
        }
    else:
        resultado["IM"] = {
            "titulo": "Inscrição Municipal",
            "valor": ""
        }
    

    if suframa:
        resultado["SUFRAMA"] = {
            "titulo": "Inscrição na SUFRAMA",
            "valor": suframa
        }
    else:
        resultado["SUFRAMA"] = {
            "titulo": "Inscrição na SUFRAMA",
            "valor": ""
        }
    
    resultado["IND_PERFIL"] = {
        "titulo": "Perfil de Apresentação do Arquivo Fiscal",
        "valor": ind_perfil,
        "descricao": f"{ind_perfil} - Perfil {ind_perfil}"
    }
    
    resultado["IND_ATIV"] = {
        "titulo": "Indicador de Tipo de Atividade",
        "valor": ind_ativ,
        "descricao": "0 - Industrial ou equiparado a industrial" if ind_ativ == "0" else "1 - Outros"
    }
    
    return resultado


def validar_0000_fiscal(linhas):
    """
    Valida uma ou mais linhas do registro 0000 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |0000|COD_VER|...|
        
    Returns:
        String JSON com array de objetos contendo os campos validados.
        Cada objeto tem a estrutura {"CAMPO": {"titulo": "...", "valor": "..."}}.
        Retorna "[]" se nenhuma linha for válida.
    """
    if not linhas:
        return json.dumps([], ensure_ascii=False, indent=2)
    

    if isinstance(linhas, str):
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
        resultado = _processar_linha_0000(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
