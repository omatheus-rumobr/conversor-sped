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


def _validar_periodo_apuracao(periodo_str):
    """
    Valida se o período de apuração está no formato MMAAAA (6 dígitos).
    
    Args:
        periodo_str: String com período no formato MMAAAA
        
    Returns:
        tuple: (True/False, (mes, ano) ou None)
    """
    if not periodo_str or len(periodo_str) != 6 or not periodo_str.isdigit():
        return False, None
    
    try:
        mes = int(periodo_str[:2])
        ano = int(periodo_str[2:6])
        
        # Valida mês (1-12)
        if mes < 1 or mes > 12:
            return False, None
        
        # Valida ano (deve ser razoável, por exemplo entre 1900 e 2100)
        if ano < 1900 or ano > 2100:
            return False, None
        
        return True, (mes, ano)
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


def validar_valor_numerico(valor_str, decimais=2, obrigatorio=False, positivo=False, nao_negativo=False):
    """
    Valida um valor numérico com precisão decimal específica.

    Args:
        valor_str: String com o valor numérico
        decimais: Número máximo de casas decimais permitidas
        obrigatorio: Se True, o campo não pode estar vazio
        positivo: Se True, o valor deve ser maior que 0
        nao_negativo: Se True, o valor deve ser maior ou igual a 0

    Returns:
        tuple: (True/False, valor float ou None, mensagem de erro ou None)
    """
    if valor_str is None:
        valor_str = ""

    if not valor_str:
        if obrigatorio:
            return False, None, "Campo obrigatório não preenchido"
        return True, 0.0, None

    try:
        valor_float = float(valor_str)

        # Verifica precisão decimal (quando houver ponto decimal)
        partes_decimal = valor_str.split(".")
        if len(partes_decimal) == 2 and len(partes_decimal[1]) > decimais:
            return False, None, f"Valor com mais de {decimais} casas decimais"

        if positivo and valor_float <= 0:
            return False, None, "Valor deve ser maior que zero"
        if nao_negativo and valor_float < 0:
            return False, None, "Valor não pode ser negativo"

        return True, valor_float, None
    except ValueError:
        return False, None, "Valor não é numérico válido"


def _processar_linha_f800(linha, dt_fin_0000=None):
    """
    Processa uma única linha do registro F800 e retorna um dicionário.
    
    Formato:
      |F800|IND_NAT_EVEN|DT_EVEN|CNPJ_SUCED|PA_CONT_CRED|COD_CRED|VL_CRED_PIS|VL_CRED_COFINS|PER_CRED_CIS|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "F800"
    - IND_NAT_EVEN: obrigatório, valores válidos [01, 02, 03, 04, 99]
    - DT_EVEN: obrigatório, formato ddmmaaaa
      - Deve ser menor ou igual à DT_FIN do arquivo (validação opcional)
    - CNPJ_SUCED: obrigatório, CNPJ da pessoa jurídica sucedida (14 dígitos)
    - PA_CONT_CRED: obrigatório, período de apuração no formato MMAAAA (6 dígitos)
    - COD_CRED: obrigatório, código do crédito conforme Tabela 4.3.6 (3 dígitos)
    - VL_CRED_PIS: obrigatório, valor numérico com 2 decimais
    - VL_CRED_COFINS: obrigatório, valor numérico com 2 decimais
    - PER_CRED_CIS: opcional, percentual com 6 dígitos totais e 2 decimais
    
    Nota: Devem ser escriturados neste registro os créditos oriundos da versão de bens e direitos
    referidos no art. 3º das Leis nº 10.637/2002 e nº 10.833/2003, bem como os créditos referentes
    à importação referidos na Lei nº 10.865/2004, transferidos em decorrência de eventos de fusão,
    incorporação e cisão de pessoa jurídica domiciliada no País.
    
    Args:
        linha: String com uma linha do SPED
        dt_fin_0000: Data final do período (opcional, para validação de DT_EVEN)
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |F800|...|)
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
    if reg != "F800":
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
    ind_nat_even = obter_campo(1)
    dt_even = obter_campo(2)
    cnpj_suced = obter_campo(3)
    pa_cont_cred = obter_campo(4)
    cod_cred = obter_campo(5)
    vl_cred_pis = obter_campo(6)
    vl_cred_cofins = obter_campo(7)
    per_cred_cis = obter_campo(8)
    
    # Validações básicas dos campos obrigatórios
    
    # IND_NAT_EVEN: obrigatório, valores válidos [01, 02, 03, 04, 99]
    ind_nat_even_validos = ["01", "02", "03", "04", "99"]
    if not ind_nat_even or ind_nat_even not in ind_nat_even_validos:
        return None
    
    # DT_EVEN: obrigatório, formato ddmmaaaa
    ok_dt, dt_obj = _validar_data(dt_even)
    if not ok_dt:
        return None
    
    # Validação opcional: DT_EVEN deve ser menor ou igual à DT_FIN (se fornecido)
    if dt_fin_0000:
        if dt_obj > dt_fin_0000:
            return None
    
    # CNPJ_SUCED: obrigatório, CNPJ da pessoa jurídica sucedida (14 dígitos)
    # Remove formatação para validar
    cnpj_suced_limpo = cnpj_suced.replace(".", "").replace("/", "").replace("-", "").replace(" ", "")
    if not cnpj_suced or len(cnpj_suced_limpo) != 14 or not _validar_cnpj(cnpj_suced):
        return None
    
    # PA_CONT_CRED: obrigatório, período de apuração no formato MMAAAA (6 dígitos)
    ok_periodo, periodo_tuple = _validar_periodo_apuracao(pa_cont_cred)
    if not ok_periodo:
        return None
    
    # COD_CRED: obrigatório, código do crédito conforme Tabela 4.3.6 (3 dígitos)
    if not cod_cred or len(cod_cred) != 3 or not cod_cred.isdigit():
        return None
    
    # VL_CRED_PIS: obrigatório, valor numérico com 2 decimais
    ok1, val1, _ = validar_valor_numerico(vl_cred_pis, decimais=2, obrigatorio=True, positivo=True)
    if not ok1:
        return None
    
    # VL_CRED_COFINS: obrigatório, valor numérico com 2 decimais
    ok2, val2, _ = validar_valor_numerico(vl_cred_cofins, decimais=2, obrigatorio=True, positivo=True)
    if not ok2:
        return None
    
    # PER_CRED_CIS: opcional, percentual com 6 dígitos totais e 2 decimais
    # Formato: 6 dígitos totais, sendo 4 inteiros e 2 decimais (ex: 1234.56)
    if per_cred_cis:
        ok3, val3, _ = validar_valor_numerico(per_cred_cis, decimais=2, obrigatorio=False, nao_negativo=True)
        if not ok3:
            return None
        # Valida se o valor está no intervalo válido para percentual (0 a 100)
        if val3 > 100:
            return None
    else:
        val3 = None
    
    # Função auxiliar para formatar valores monetários
    def fmt_valor(v):
        if v is None:
            return ""
        return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    # Função auxiliar para formatar percentual
    def fmt_percentual(v):
        if v is None:
            return ""
        return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") + "%"
    
    # Função auxiliar para formatar CNPJ
    def fmt_cnpj(cnpj_str):
        if not cnpj_str:
            return ""
        cnpj_limpo = cnpj_str.replace(".", "").replace("/", "").replace("-", "").replace(" ", "")
        if len(cnpj_limpo) == 14:
            # Formata CNPJ: 00.000.000/0000-00
            return f"{cnpj_limpo[:2]}.{cnpj_limpo[2:5]}.{cnpj_limpo[5:8]}/{cnpj_limpo[8:12]}-{cnpj_limpo[12:]}"
        return cnpj_str
    
    # Função auxiliar para formatar data
    def fmt_data(data_str):
        if not data_str or len(data_str) != 8:
            return ""
        return f"{data_str[:2]}/{data_str[2:4]}/{data_str[4:]}"
    
    # Função auxiliar para formatar período de apuração
    def fmt_periodo(periodo_str):
        if not periodo_str or len(periodo_str) != 6:
            return ""
        return f"{periodo_str[:2]}/{periodo_str[2:]}"
    
    # Descrições dos campos
    descricoes_ind_nat_even = {
        "01": "Incorporação",
        "02": "Fusão",
        "03": "Cisão Total",
        "04": "Cisão Parcial",
        "99": "Outros"
    }
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "IND_NAT_EVEN": {
            "titulo": "Indicador da Natureza do Evento de Sucessão",
            "valor": ind_nat_even,
            "descricao": descricoes_ind_nat_even.get(ind_nat_even, "")
        },
        "DT_EVEN": {
            "titulo": "Data do Evento",
            "valor": dt_even,
            "valor_formatado": fmt_data(dt_even)
        },
        "CNPJ_SUCED": {
            "titulo": "CNPJ da Pessoa Jurídica Sucedida",
            "valor": cnpj_suced,
            "valor_formatado": fmt_cnpj(cnpj_suced)
        },
        "PA_CONT_CRED": {
            "titulo": "Período de Apuração do Crédito – Mês/Ano (MM/AAAA)",
            "valor": pa_cont_cred,
            "valor_formatado": fmt_periodo(pa_cont_cred)
        },
        "COD_CRED": {
            "titulo": "Código do crédito transferido, conforme Tabela 4.3.6",
            "valor": cod_cred
        },
        "VL_CRED_PIS": {
            "titulo": "Valor do Crédito Transferido de PIS/Pasep",
            "valor": vl_cred_pis,
            "valor_formatado": fmt_valor(val1)
        },
        "VL_CRED_COFINS": {
            "titulo": "Valor do Crédito Transferido de Cofins",
            "valor": vl_cred_cofins,
            "valor_formatado": fmt_valor(val2)
        },
        "PER_CRED_CIS": {
            "titulo": "Percentual do crédito original transferido, no caso de evento de Cisão",
            "valor": per_cred_cis,
            "valor_formatado": fmt_percentual(val3) if per_cred_cis else ""
        }
    }
    
    return resultado


def validar_f800(linhas, dt_fin_0000=None):
    """
    Valida uma ou mais linhas do registro F800 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |F800|IND_NAT_EVEN|DT_EVEN|CNPJ_SUCED|PA_CONT_CRED|COD_CRED|VL_CRED_PIS|VL_CRED_COFINS|PER_CRED_CIS|
        dt_fin_0000: Data final do período (opcional, para validação de DT_EVEN)
        
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
        resultado = _processar_linha_f800(linha, dt_fin_0000)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
