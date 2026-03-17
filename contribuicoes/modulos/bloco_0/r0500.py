import json
from datetime import datetime


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


def _processar_linha_0500(linha, dt_fin_0000=None):
    """
    Processa uma única linha do registro 0500 e retorna um dicionário.
    
    Formato:
      |0500|DT_ALT|COD_NAT_CC|IND_CTA|NÍVEL|COD_CTA|NOME_CTA|COD_CTA_REF|CNPJ_EST|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "0500"
    - DT_ALT: obrigatório, formato ddmmaaaa, data válida
      - Não pode ser maior que DT_FIN do registro 0000 (quando informado)
    - COD_NAT_CC: obrigatório, valores válidos [01, 02, 03, 04, 05, 09]
    - IND_CTA: obrigatório, valores válidos [S, A]
    - NÍVEL: obrigatório, numérico
    - COD_CTA: obrigatório, até 255 caracteres
    - NOME_CTA: obrigatório, até 60 caracteres
    - COD_CTA_REF: opcional, até 60 caracteres
    - CNPJ_EST: opcional, 14 dígitos, validar DV se informado
    
    Nota: Não podem ser informados dois ou mais registros com a mesma combinação
    de conteúdo nos campos DT_ALT, COD_CTA e COD_CTA_REF.
    Esta validação deve ser feita em uma camada superior.
    
    Args:
        linha: String com uma linha do SPED
        dt_fin_0000: Data final (ddmmaaaa) do registro 0000 (opcional, para validação)
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |0500|...|)
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
    if reg != "0500":
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
    
    # Extrai todos os campos (9 campos no total)
    dt_alt = obter_campo(1)
    cod_nat_cc = obter_campo(2)
    ind_cta = obter_campo(3)
    nivel = obter_campo(4)
    cod_cta = obter_campo(5)
    nome_cta = obter_campo(6)
    cod_cta_ref = obter_campo(7)
    cnpj_est = obter_campo(8)
    
    # Validações básicas dos campos obrigatórios
    
    # DT_ALT: obrigatório, formato ddmmaaaa, data válida
    dt_alt_valida, dt_alt_obj = _validar_data(dt_alt)
    if not dt_alt_valida:
        return None
    
    # DT_ALT não pode ser maior que DT_FIN do registro 0000 (quando informado)
    if dt_fin_0000:
        ok_0000_fin, dt_fin_0000_obj = _validar_data(dt_fin_0000)
        if ok_0000_fin and dt_alt_obj:
            if dt_alt_obj > dt_fin_0000_obj:
                return None
    
    # COD_NAT_CC: obrigatório, valores válidos [01, 02, 03, 04, 05, 09]
    valores_validos_cod_nat_cc = ["01", "02", "03", "04", "05", "09"]
    if not cod_nat_cc or cod_nat_cc not in valores_validos_cod_nat_cc:
        return None
    
    # IND_CTA: obrigatório, valores válidos [S, A]
    if not ind_cta or ind_cta not in ["S", "A"]:
        return None
    
    # NÍVEL: obrigatório, numérico
    if not nivel:
        return None
    try:
        nivel_int = int(nivel)
        if nivel_int < 0:
            return None
    except ValueError:
        return None
    
    # COD_CTA: obrigatório, até 255 caracteres
    if not cod_cta or len(cod_cta) > 255:
        return None
    
    # NOME_CTA: obrigatório, até 60 caracteres
    if not nome_cta or len(nome_cta) > 60:
        return None
    
    # COD_CTA_REF: opcional, até 60 caracteres
    if cod_cta_ref and len(cod_cta_ref) > 60:
        return None
    
    # CNPJ_EST: opcional, se informado deve ser válido (14 dígitos, validar DV)
    if cnpj_est:
        if not _validar_cnpj(cnpj_est):
            return None
    
    # Função auxiliar para formatar data
    def fmt_data(d):
        return d.strftime("%d/%m/%Y") if d else ""
    
    # Monta o resultado
    descricoes_cod_nat_cc = {
        "01": "Contas de ativo",
        "02": "Contas de passivo",
        "03": "Patrimônio líquido",
        "04": "Contas de resultado",
        "05": "Contas de compensação",
        "09": "Outras"
    }
    
    descricoes_ind_cta = {
        "S": "Sintética (grupo de contas)",
        "A": "Analítica (conta)"
    }
    
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "DT_ALT": {
            "titulo": "Data da inclusão/alteração",
            "valor": dt_alt,
            "valor_formatado": fmt_data(dt_alt_obj)
        },
        "COD_NAT_CC": {
            "titulo": "Código da natureza da conta/grupo de contas",
            "valor": cod_nat_cc,
            "descricao": descricoes_cod_nat_cc.get(cod_nat_cc, "")
        },
        "IND_CTA": {
            "titulo": "Indicador do tipo de conta",
            "valor": ind_cta,
            "descricao": descricoes_ind_cta.get(ind_cta, "")
        },
        "NÍVEL": {
            "titulo": "Nível da conta analítica/grupo de contas",
            "valor": nivel
        },
        "COD_CTA": {
            "titulo": "Código da conta analítica/grupo de contas",
            "valor": cod_cta
        },
        "NOME_CTA": {
            "titulo": "Nome da conta analítica/grupo de contas",
            "valor": nome_cta
        }
    }
    
    # COD_CTA_REF: opcional
    if cod_cta_ref:
        resultado["COD_CTA_REF"] = {
            "titulo": "Código da conta correlacionada no Plano de Contas Referenciado, publicado pela RFB",
            "valor": cod_cta_ref
        }
    else:
        resultado["COD_CTA_REF"] = {
            "titulo": "Código da conta correlacionada no Plano de Contas Referenciado, publicado pela RFB",
            "valor": ""
        }
    
    # CNPJ_EST: opcional
    if cnpj_est:
        resultado["CNPJ_EST"] = {
            "titulo": "CNPJ do estabelecimento, no caso da conta informada no campo COD_CTA ser específica de um estabelecimento",
            "valor": cnpj_est
        }
    else:
        resultado["CNPJ_EST"] = {
            "titulo": "CNPJ do estabelecimento, no caso da conta informada no campo COD_CTA ser específica de um estabelecimento",
            "valor": ""
        }
    
    return resultado


def validar_0500(linhas, dt_fin_0000=None):
    """
    Valida uma ou mais linhas do registro 0500 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |0500|DT_ALT|COD_NAT_CC|IND_CTA|NÍVEL|COD_CTA|NOME_CTA|COD_CTA_REF|CNPJ_EST|
        dt_fin_0000: Data final (ddmmaaaa) do registro 0000 (opcional, para validação)
        
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
        resultado = _processar_linha_0500(linha, dt_fin_0000=dt_fin_0000)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
