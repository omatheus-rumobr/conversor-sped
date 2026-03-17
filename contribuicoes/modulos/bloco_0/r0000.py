import re
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


def _validar_suframa(suframa):
    """
    Valida o formato básico da inscrição SUFRAMA (9 caracteres).
    Valida também o dígito verificador (DV) usando módulo 11.
    """
    if not suframa:
        return False
    
    # Remove formatação
    suframa_limpo = suframa.replace(".", "").replace("-", "").replace(" ", "")
    
    if not suframa_limpo.isdigit() or len(suframa_limpo) != 9:
        return False
    
    # Validação do dígito verificador (módulo 11)
    # Os 8 primeiros dígitos são o número base
    # O 9º dígito é o DV
    numero_base = suframa_limpo[:8]
    dv_informado = int(suframa_limpo[8])
    
    multiplicadores = [2, 3, 4, 5, 6, 7, 8, 9]
    soma = sum(int(numero_base[i]) * multiplicadores[i] for i in range(8))
    resto = soma % 11
    
    # Se resto for 0 ou 1, DV é 0; caso contrário, DV é 11 - resto
    dv_calculado = 0 if resto < 2 else 11 - resto
    
    return dv_informado == dv_calculado


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


def _validar_nome(nome):
    """
    Valida se o nome contém apenas caracteres permitidos.
    Caracteres permitidos: abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ /,.-@:&*+_<>()!?'$%1234567890
    
    Args:
        nome: String com o nome
        
    Returns:
        bool: True se válido, False caso contrário
    """
    if not nome:
        return False
    
    # Caracteres permitidos conforme manual
    caracteres_permitidos = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ /,.-@:&*+_<>()!?'$%1234567890")
    
    return all(c in caracteres_permitidos for c in nome)


def _processar_linha_0000(linha):
    """
    Processa uma única linha do registro 0000 e retorna um dicionário.
    
    Formato:
      |0000|COD_VER|TIPO_ESCRIT|IND_SIT_ESP|NUM_REC_ANTERIOR|DT_INI|DT_FIN|NOME|CNPJ|UF|COD_MUN|SUFRAMA|IND_NAT_PJ|IND_ATIV|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "0000"
    - COD_VER: obrigatório, 3 dígitos, validar conforme tabela e data DT_FIN (validação externa)
    - TIPO_ESCRIT: obrigatório, valores [0, 1]
    - IND_SIT_ESP: opcional, valores [0, 1, 2, 3, 4]
    - NUM_REC_ANTERIOR: opcional, obrigatório se TIPO_ESCRIT = 1, até 41 caracteres, maiúsculas
    - DT_INI: obrigatório, ddmmaaaa, mesmo mês/ano de DT_FIN, primeiro dia do mês (exceto abertura)
    - DT_FIN: obrigatório, ddmmaaaa, mesmo mês/ano de DT_INI, último dia do mês (exceto casos especiais)
    - NOME: obrigatório, até 100 caracteres, sem acentos, caracteres permitidos específicos
    - CNPJ: obrigatório, 14 dígitos, validar DV
    - UF: obrigatório, sigla válida
    - COD_MUN: obrigatório, 7 dígitos, deve existir na tabela IBGE (validação externa)
    - SUFRAMA: opcional, 9 caracteres, validar DV se informado
    - IND_NAT_PJ: opcional, valores [00, 01, 02, 03, 04, 05]
    - IND_ATIV: obrigatório, valores [0, 1, 2, 3, 4, 9]
    
    Args:
        linha: String com uma linha do SPED
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |0000|...|)
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
    if reg != "0000":
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
    
    # Extrai todos os campos (14 campos no total)
    cod_ver = obter_campo(1)
    tipo_escrit = obter_campo(2)
    ind_sit_esp = obter_campo(3)
    num_rec_anterior = obter_campo(4)
    dt_ini = obter_campo(5)
    dt_fin = obter_campo(6)
    nome = obter_campo(7)
    cnpj = obter_campo(8)
    uf = obter_campo(9)
    cod_mun = obter_campo(10)
    suframa = obter_campo(11)
    ind_nat_pj = obter_campo(12)
    ind_ativ = obter_campo(13)
    
    # Validações básicas dos campos obrigatórios
    
    # COD_VER: obrigatório, deve ter 3 dígitos
    if not cod_ver or not cod_ver.isdigit() or len(cod_ver) != 3:
        return None
    
    # TIPO_ESCRIT: obrigatório, valores válidos [0, 1]
    if tipo_escrit not in ["0", "1"]:
        return None
    
    # IND_SIT_ESP: opcional, valores válidos [0, 1, 2, 3, 4]
    if ind_sit_esp and ind_sit_esp not in ["0", "1", "2", "3", "4"]:
        return None
    
    # NUM_REC_ANTERIOR: obrigatório se TIPO_ESCRIT = 1, opcional caso contrário, até 41 caracteres
    if tipo_escrit == "1":
        if not num_rec_anterior or len(num_rec_anterior) > 41:
            return None
        # Deve estar em maiúsculas
        if num_rec_anterior != num_rec_anterior.upper():
            return None
    elif num_rec_anterior and len(num_rec_anterior) > 41:
        return None
    
    # DT_INI: obrigatório, formato ddmmaaaa
    dt_ini_valida, dt_ini_obj = _validar_data(dt_ini)
    if not dt_ini_valida:
        return None
    
    # DT_FIN: obrigatório, formato ddmmaaaa, deve estar no mesmo mês/ano de DT_INI
    dt_fin_valida, dt_fin_obj = _validar_data(dt_fin)
    if not dt_fin_valida:
        return None
    
    # Valida se DT_FIN está no mesmo mês/ano de DT_INI
    if dt_ini_obj and dt_fin_obj:
        if dt_ini_obj.year != dt_fin_obj.year or dt_ini_obj.month != dt_fin_obj.month:
            return None
        # DT_INI deve ser <= DT_FIN
        if dt_ini_obj > dt_fin_obj:
            return None
    
    # NOME: obrigatório, até 100 caracteres, caracteres permitidos específicos
    if not nome or len(nome) > 100:
        return None
    if not _validar_nome(nome):
        return None
    
    # CNPJ: obrigatório, validar formato e DV
    if not cnpj or not _validar_cnpj(cnpj):
        return None
    
    # UF: obrigatório, deve ser sigla válida
    if not uf or not _validar_uf(uf):
        return None
    
    # COD_MUN: obrigatório, 7 dígitos
    if not cod_mun or not cod_mun.isdigit() or len(cod_mun) != 7:
        return None
    
    # SUFRAMA: opcional, se informado deve ter 9 caracteres e DV válido
    if suframa:
        if not _validar_suframa(suframa):
            return None
    
    # IND_NAT_PJ: opcional, valores válidos [00, 01, 02, 03, 04, 05]
    if ind_nat_pj and ind_nat_pj not in ["00", "01", "02", "03", "04", "05"]:
        return None
    
    # IND_ATIV: obrigatório, valores válidos [0, 1, 2, 3, 4, 9]
    if ind_ativ not in ["0", "1", "2", "3", "4", "9"]:
        return None
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "COD_VER": {
            "titulo": "Código da versão do leiaute conforme a tabela 3.1.1",
            "valor": cod_ver
        },
        "TIPO_ESCRIT": {
            "titulo": "Tipo de escrituração",
            "valor": tipo_escrit,
            "descricao": "0 - Original" if tipo_escrit == "0" else "1 - Retificadora"
        }
    }
    
    # IND_SIT_ESP: opcional
    if ind_sit_esp:
        descricoes_sit_esp = {
            "0": "Abertura",
            "1": "Cisão",
            "2": "Fusão",
            "3": "Incorporação",
            "4": "Encerramento"
        }
        resultado["IND_SIT_ESP"] = {
            "titulo": "Indicador de situação especial",
            "valor": ind_sit_esp,
            "descricao": descricoes_sit_esp.get(ind_sit_esp, "")
        }
    else:
        resultado["IND_SIT_ESP"] = {
            "titulo": "Indicador de situação especial",
            "valor": ""
        }
    
    # NUM_REC_ANTERIOR: opcional
    if num_rec_anterior:
        resultado["NUM_REC_ANTERIOR"] = {
            "titulo": "Número do Recibo da Escrituração anterior a ser retificada",
            "valor": num_rec_anterior
        }
    else:
        resultado["NUM_REC_ANTERIOR"] = {
            "titulo": "Número do Recibo da Escrituração anterior a ser retificada",
            "valor": ""
        }
    
    def fmt_data(d):
        return d.strftime("%d/%m/%Y") if d else ""
    
    resultado["DT_INI"] = {
        "titulo": "Data inicial das informações contidas no arquivo",
        "valor": dt_ini,
        "valor_formatado": fmt_data(dt_ini_obj)
    }
    
    resultado["DT_FIN"] = {
        "titulo": "Data final das informações contidas no arquivo",
        "valor": dt_fin,
        "valor_formatado": fmt_data(dt_fin_obj)
    }
    
    resultado["NOME"] = {
        "titulo": "Nome empresarial da pessoa jurídica",
        "valor": nome
    }
    
    resultado["CNPJ"] = {
        "titulo": "Número de inscrição do estabelecimento matriz da pessoa jurídica no CNPJ",
        "valor": cnpj
    }
    
    resultado["UF"] = {
        "titulo": "Sigla da Unidade da Federação da pessoa jurídica",
        "valor": uf
    }
    
    resultado["COD_MUN"] = {
        "titulo": "Código do município do domicílio fiscal da pessoa jurídica, conforme a tabela IBGE",
        "valor": cod_mun
    }
    
    # SUFRAMA: opcional
    if suframa:
        resultado["SUFRAMA"] = {
            "titulo": "Inscrição da pessoa jurídica na Suframa",
            "valor": suframa
        }
    else:
        resultado["SUFRAMA"] = {
            "titulo": "Inscrição da pessoa jurídica na Suframa",
            "valor": ""
        }
    
    # IND_NAT_PJ: opcional
    if ind_nat_pj:
        descricoes_nat_pj = {
            "00": "Pessoa jurídica em geral (não participante de SCP como sócia ostensiva)",
            "01": "Sociedade cooperativa (não participante de SCP como sócia ostensiva)",
            "02": "Entidade sujeita ao PIS/Pasep exclusivamente com base na Folha de Salários",
            "03": "Pessoa jurídica em geral participante de SCP como sócia ostensiva",
            "04": "Sociedade cooperativa participante de SCP como sócia ostensiva",
            "05": "Sociedade em Conta de Participação - SCP"
        }
        resultado["IND_NAT_PJ"] = {
            "titulo": "Indicador da natureza da pessoa jurídica",
            "valor": ind_nat_pj,
            "descricao": descricoes_nat_pj.get(ind_nat_pj, "")
        }
    else:
        resultado["IND_NAT_PJ"] = {
            "titulo": "Indicador da natureza da pessoa jurídica",
            "valor": ""
        }
    
    descricoes_ativ = {
        "0": "Industrial ou equiparado a industrial",
        "1": "Prestador de serviços",
        "2": "Atividade de comércio",
        "3": "Pessoas jurídicas referidas nos §§ 6º, 8º e 9º do art. 3º da Lei nº 9.718, de 1998",
        "4": "Atividade imobiliária",
        "9": "Outros"
    }
    
    resultado["IND_ATIV"] = {
        "titulo": "Indicador de tipo de atividade preponderante",
        "valor": ind_ativ,
        "descricao": descricoes_ativ.get(ind_ativ, "")
    }
    
    return resultado


def validar_0000(linhas):
    """
    Valida uma ou mais linhas do registro 0000 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |0000|COD_VER|TIPO_ESCRIT|IND_SIT_ESP|NUM_REC_ANTERIOR|DT_INI|DT_FIN|NOME|CNPJ|UF|COD_MUN|SUFRAMA|IND_NAT_PJ|IND_ATIV|
        
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
        resultado = _processar_linha_0000(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
