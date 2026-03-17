import json
from datetime import datetime


def _validar_periodo_mmaaaa(periodo_str):
    """
    Valida se o período está no formato mmaaaa e se é um período válido.
    
    Args:
        periodo_str: String com período no formato mmaaaa
        
    Returns:
        tuple: (True/False, (mes, ano) ou None)
    """
    if not periodo_str or len(periodo_str) != 6 or not periodo_str.isdigit():
        return False, None
    
    try:
        mes = int(periodo_str[:2])
        ano = int(periodo_str[2:6])
        
        if mes < 1 or mes > 12:
            return False, None
        
        return True, (mes, ano)
    except ValueError:
        return False, None


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


def _float_igual(a, b, tolerancia=0.01):
    """Compara dois floats com tolerância."""
    if a is None or b is None:
        return False
    return abs(a - b) <= tolerancia


def _processar_linha_1600(linha, per_apu_escrit=None, dt_ini_escrit=None, dt_fin_escrit=None):
    """
    Processa uma única linha do registro 1600 e retorna um dicionário.
    
    Formato:
      |1600|PER_APUR_ANT|NAT_CONT_REC|VL_CONT_APUR|VL_CRED_COFINS_DESC|VL_CONT_DEV|VL_OUT_DED|VL_CONT_EXT|VL_MUL|VL_JUR|DT_RECOL|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "1600"
    - PER_APUR_ANT: obrigatório, formato mmaaaa, período válido, anterior ao período da escrituração atual
    - NAT_CONT_REC: obrigatório, 2 caracteres (código conforme Tabela 4.3.5)
    - VL_CONT_APUR: obrigatório, numérico com 2 decimais, não negativo
    - VL_CRED_COFINS_DESC: obrigatório, numérico com 2 decimais, não negativo
    - VL_CONT_DEV: obrigatório, numérico com 2 decimais, não negativo
      - Deve ser igual a VL_CONT_APUR - VL_CRED_COFINS_DESC
    - VL_OUT_DED: obrigatório, numérico com 2 decimais, não negativo
    - VL_CONT_EXT: obrigatório, numérico com 2 decimais, não negativo
      - Deve ser igual a VL_CONT_DEV - VL_OUT_DED
    - VL_MUL: opcional, numérico com 2 decimais, não negativo
    - VL_JUR: opcional, numérico com 2 decimais, não negativo
    - DT_RECOL: opcional, formato ddmmaaaa, data válida
      - Deve ser informado se VL_CONT_EXT > 0
      - Deve estar compreendida no período da atual escrituração (quando informado)
    
    Nota: A chave deste registro é formada pelos campos: PER_APUR_ANT + NAT_CONT_REC + DT_RECOL.
    A validação de que NAT_CONT_REC deve existir na Tabela 4.3.5 deve ser feita
    em uma camada superior que tenha acesso a essa tabela.
    As validações de correspondência com registros 1610 e 1620 devem ser feitas em uma camada superior.
    
    Args:
        linha: String com uma linha do SPED
        per_apu_escrit: Período de apuração da escrituração atual (mmaaaa) - opcional, para validação
        dt_ini_escrit: Data inicial do período da escrituração atual (ddmmaaaa) - opcional, para validação
        dt_fin_escrit: Data final do período da escrituração atual (ddmmaaaa) - opcional, para validação
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |1600|...|)
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
    if reg != "1600":
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
    
    # Extrai todos os campos (11 campos no total)
    per_apur_ant = obter_campo(1)
    nat_cont_rec = obter_campo(2)
    vl_cont_apur = obter_campo(3)
    vl_cred_cofins_desc = obter_campo(4)
    vl_cont_dev = obter_campo(5)
    vl_out_ded = obter_campo(6)
    vl_cont_ext = obter_campo(7)
    vl_mul = obter_campo(8)
    vl_jur = obter_campo(9)
    dt_recol = obter_campo(10)
    
    # Validações básicas dos campos obrigatórios
    
    # PER_APUR_ANT: obrigatório, formato mmaaaa, período válido
    per_apur_ant_valido, per_apur_ant_tuplo = _validar_periodo_mmaaaa(per_apur_ant)
    if not per_apur_ant_valido:
        return None
    
    # PER_APUR_ANT deve ser anterior ao período da escrituração atual (quando informado)
    if per_apu_escrit:
        ok_escrit, per_escrit_tuplo = _validar_periodo_mmaaaa(per_apu_escrit)
        if ok_escrit and per_apur_ant_tuplo:
            mes_ant, ano_ant = per_apur_ant_tuplo
            mes_escrit, ano_escrit = per_escrit_tuplo
            if ano_ant > ano_escrit or (ano_ant == ano_escrit and mes_ant >= mes_escrit):
                return None
    
    # NAT_CONT_REC: obrigatório, 2 caracteres
    if not nat_cont_rec or len(nat_cont_rec) != 2:
        return None
    
    # VL_CONT_APUR: obrigatório, numérico com 2 decimais, não negativo
    ok1, val1, _ = validar_valor_numerico(vl_cont_apur, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok1:
        return None
    
    # VL_CRED_COFINS_DESC: obrigatório, numérico com 2 decimais, não negativo
    ok2, val2, _ = validar_valor_numerico(vl_cred_cofins_desc, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok2:
        return None
    
    # VL_CONT_DEV: obrigatório, numérico com 2 decimais, não negativo
    ok3, val3, _ = validar_valor_numerico(vl_cont_dev, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok3:
        return None
    
    # Validação: VL_CONT_DEV deve ser igual a VL_CONT_APUR - VL_CRED_COFINS_DESC
    vl_cont_dev_calculado = val1 - val2
    if not _float_igual(val3, vl_cont_dev_calculado):
        return None
    
    # VL_OUT_DED: obrigatório, numérico com 2 decimais, não negativo
    ok4, val4, _ = validar_valor_numerico(vl_out_ded, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok4:
        return None
    
    # VL_CONT_EXT: obrigatório, numérico com 2 decimais, não negativo
    ok5, val5, _ = validar_valor_numerico(vl_cont_ext, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok5:
        return None
    
    # Validação: VL_CONT_EXT deve ser igual a VL_CONT_DEV - VL_OUT_DED
    vl_cont_ext_calculado = val3 - val4
    if not _float_igual(val5, vl_cont_ext_calculado):
        return None
    
    # VL_MUL: opcional, numérico com 2 decimais, não negativo
    ok6, val6, _ = validar_valor_numerico(vl_mul, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok6:
        return None
    if val6 is None:
        val6 = 0.0
    
    # VL_JUR: opcional, numérico com 2 decimais, não negativo
    ok7, val7, _ = validar_valor_numerico(vl_jur, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok7:
        return None
    if val7 is None:
        val7 = 0.0
    
    # DT_RECOL: opcional, formato ddmmaaaa, data válida
    dt_recol_valida = False
    dt_recol_obj = None
    if dt_recol:
        dt_recol_valida, dt_recol_obj = _validar_data(dt_recol)
        if not dt_recol_valida:
            return None
        
        # DT_RECOL deve estar compreendida no período da atual escrituração (quando informado)
        if dt_ini_escrit and dt_fin_escrit:
            ok_ini, dt_ini_obj = _validar_data(dt_ini_escrit)
            ok_fin, dt_fin_obj = _validar_data(dt_fin_escrit)
            if ok_ini and ok_fin and dt_recol_obj:
                if dt_recol_obj < dt_ini_obj or dt_recol_obj > dt_fin_obj:
                    return None
    
    # Validações condicionais: se VL_CONT_EXT > 0, então DT_RECOL deve ser informado
    if val5 > 0:
        if not dt_recol:
            return None
    
    # Função auxiliar para formatar período
    def fmt_periodo(p):
        if p:
            mes, ano = p
            return f"{mes:02d}/{ano}"
        return ""
    
    # Função auxiliar para formatar data
    def fmt_data(d):
        return d.strftime("%d/%m/%Y") if d else ""
    
    # Função auxiliar para formatar valores monetários
    def fmt_valor(v):
        return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "PER_APUR_ANT": {
            "titulo": "Período de Apuração da Contribuição Social Extemporânea (MMAAAA)",
            "valor": per_apur_ant,
            "valor_formatado": fmt_periodo(per_apur_ant_tuplo)
        },
        "NAT_CONT_REC": {
            "titulo": "Natureza da Contribuição a Recolher, conforme Tabela 4.3.5",
            "valor": nat_cont_rec
        },
        "VL_CONT_APUR": {
            "titulo": "Valor da Contribuição Apurada",
            "valor": vl_cont_apur,
            "valor_formatado": fmt_valor(val1)
        },
        "VL_CRED_COFINS_DESC": {
            "titulo": "Valor do Crédito de COFINS a Descontar, da Contribuição Social Extemporânea",
            "valor": vl_cred_cofins_desc,
            "valor_formatado": fmt_valor(val2)
        },
        "VL_CONT_DEV": {
            "titulo": "Valor da Contribuição Social Extemporânea Devida",
            "valor": vl_cont_dev,
            "valor_formatado": fmt_valor(val3)
        },
        "VL_OUT_DED": {
            "titulo": "Valor de Outras Deduções",
            "valor": vl_out_ded,
            "valor_formatado": fmt_valor(val4)
        },
        "VL_CONT_EXT": {
            "titulo": "Valor da Contribuição Social Extemporânea a pagar",
            "valor": vl_cont_ext,
            "valor_formatado": fmt_valor(val5)
        }
    }
    
    # VL_MUL: opcional
    if vl_mul:
        resultado["VL_MUL"] = {
            "titulo": "Valor da Multa",
            "valor": vl_mul,
            "valor_formatado": fmt_valor(val6)
        }
    else:
        resultado["VL_MUL"] = {
            "titulo": "Valor da Multa",
            "valor": "",
            "valor_formatado": ""
        }
    
    # VL_JUR: opcional
    if vl_jur:
        resultado["VL_JUR"] = {
            "titulo": "Valor dos Juros",
            "valor": vl_jur,
            "valor_formatado": fmt_valor(val7)
        }
    else:
        resultado["VL_JUR"] = {
            "titulo": "Valor dos Juros",
            "valor": "",
            "valor_formatado": ""
        }
    
    # DT_RECOL: opcional
    if dt_recol:
        resultado["DT_RECOL"] = {
            "titulo": "Data do Recolhimento",
            "valor": dt_recol,
            "valor_formatado": fmt_data(dt_recol_obj)
        }
    else:
        resultado["DT_RECOL"] = {
            "titulo": "Data do Recolhimento",
            "valor": "",
            "valor_formatado": ""
        }
    
    return resultado


def validar_1600(linhas, per_apu_escrit=None, dt_ini_escrit=None, dt_fin_escrit=None):
    """
    Valida uma ou mais linhas do registro 1600 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |1600|PER_APUR_ANT|NAT_CONT_REC|VL_CONT_APUR|VL_CRED_COFINS_DESC|VL_CONT_DEV|VL_OUT_DED|VL_CONT_EXT|VL_MUL|VL_JUR|DT_RECOL|
        per_apu_escrit: Período de apuração da escrituração atual (mmaaaa) - opcional, para validação
        dt_ini_escrit: Data inicial do período da escrituração atual (ddmmaaaa) - opcional, para validação
        dt_fin_escrit: Data final do período da escrituração atual (ddmmaaaa) - opcional, para validação
        
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
        resultado = _processar_linha_1600(linha, per_apu_escrit=per_apu_escrit, dt_ini_escrit=dt_ini_escrit, dt_fin_escrit=dt_fin_escrit)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
