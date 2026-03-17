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


def _processar_linha_1210(linha):
    """
    Processa uma única linha do registro 1210 e retorna um dicionário.
    
    Formato:
      |1210|CNPJ|CST_PIS|COD_PART|DT_OPER|VL_OPER|VL_BC_PIS|ALIQ_PIS|VL_PIS|COD_CTA|DESC_COMPL|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "1210"
    - CNPJ: obrigatório, 14 dígitos, validar DV (deve existir no registro 0140)
    - CST_PIS: obrigatório, 2 dígitos (código conforme Tabela 4.3.3)
    - COD_PART: opcional, até 60 caracteres (deve existir no registro 0150)
    - DT_OPER: obrigatório, formato ddmmaaaa, data válida
    - VL_OPER: obrigatório, numérico com 2 decimais, > 0
    - VL_BC_PIS: obrigatório, numérico com 3 decimais, não negativo
    - ALIQ_PIS: obrigatório, numérico com 4 decimais, não negativo
    - VL_PIS: obrigatório, numérico com 2 decimais, não negativo
    - COD_CTA: opcional, até 255 caracteres
    - DESC_COMPL: opcional
    
    Nota: A chave deste registro é formada pelos campos: CNPJ + CST_PIS + COD_PART + DT_OPER + ALIQ_PIS + COD_CTA.
    A validação de que CNPJ deve existir no registro 0140, COD_PART deve existir no registro 0150,
    e CST_PIS deve existir na Tabela 4.3.3 deve ser feita em uma camada superior.
    A validação de que a soma dos valores do campo VL_PIS deve ser transportada para o campo VL_CONT_APUR
    do registro pai 1200 deve ser feita em uma camada superior.
    
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
    # Remove primeiro e último se vazios (formato padrão SPED: |1210|...|)
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
    if reg != "1210":
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
    cnpj = obter_campo(1)
    cst_pis = obter_campo(2)
    cod_part = obter_campo(3)
    dt_oper = obter_campo(4)
    vl_oper = obter_campo(5)
    vl_bc_pis = obter_campo(6)
    aliq_pis = obter_campo(7)
    vl_pis = obter_campo(8)
    cod_cta = obter_campo(9)
    desc_compl = obter_campo(10)
    
    # Validações básicas dos campos obrigatórios
    
    # CNPJ: obrigatório, 14 dígitos, validar DV
    if not cnpj or not _validar_cnpj(cnpj):
        return None
    
    # CST_PIS: obrigatório, 2 dígitos
    if not cst_pis or len(cst_pis) != 2 or not cst_pis.isdigit():
        return None
    
    # COD_PART: opcional, até 60 caracteres
    if cod_part and len(cod_part) > 60:
        return None
    
    # DT_OPER: obrigatório, formato ddmmaaaa, data válida
    dt_oper_valida, dt_oper_obj = _validar_data(dt_oper)
    if not dt_oper_valida:
        return None
    
    # VL_OPER: obrigatório, numérico com 2 decimais, > 0
    ok1, val1, _ = validar_valor_numerico(vl_oper, decimais=2, obrigatorio=True, positivo=True)
    if not ok1:
        return None
    
    # VL_BC_PIS: obrigatório, numérico com 3 decimais, não negativo
    ok2, val2, _ = validar_valor_numerico(vl_bc_pis, decimais=3, obrigatorio=True, nao_negativo=True)
    if not ok2:
        return None
    
    # ALIQ_PIS: obrigatório, numérico com 4 decimais, não negativo
    ok3, val3, _ = validar_valor_numerico(aliq_pis, decimais=4, obrigatorio=True, nao_negativo=True)
    if not ok3:
        return None
    
    # VL_PIS: obrigatório, numérico com 2 decimais, não negativo
    ok4, val4, _ = validar_valor_numerico(vl_pis, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok4:
        return None
    
    # COD_CTA: opcional, até 255 caracteres
    if cod_cta and len(cod_cta) > 255:
        return None
    
    # Função auxiliar para formatar data
    def fmt_data(d):
        return d.strftime("%d/%m/%Y") if d else ""
    
    # Função auxiliar para formatar valores monetários
    def fmt_valor(v):
        return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    # Função auxiliar para formatar valores com 3 decimais
    def fmt_valor_3dec(v):
        return f"{v:,.3f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    # Função auxiliar para formatar valores com 4 decimais
    def fmt_valor_4dec(v):
        return f"{v:,.4f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "CNPJ": {
            "titulo": "Número de inscrição do estabelecimento no CNPJ (Campo 04 do Registro 0140)",
            "valor": cnpj
        },
        "CST_PIS": {
            "titulo": "Código da Situação Tributária referente ao PIS/PASEP, conforme a Tabela indicada no item 4.3.3",
            "valor": cst_pis
        },
        "DT_OPER": {
            "titulo": "Data da Operação",
            "valor": dt_oper,
            "valor_formatado": fmt_data(dt_oper_obj)
        },
        "VL_OPER": {
            "titulo": "Valor da Operação",
            "valor": vl_oper,
            "valor_formatado": fmt_valor(val1)
        },
        "VL_BC_PIS": {
            "titulo": "Base de cálculo do PIS/PASEP (em valor ou em quantidade)",
            "valor": vl_bc_pis,
            "valor_formatado": fmt_valor_3dec(val2)
        },
        "ALIQ_PIS": {
            "titulo": "Alíquota da PIS (em percentual ou em reais)",
            "valor": aliq_pis,
            "valor_formatado": fmt_valor_4dec(val3)
        },
        "VL_PIS": {
            "titulo": "Valor do PIS/PASEP",
            "valor": vl_pis,
            "valor_formatado": fmt_valor(val4)
        }
    }
    
    # COD_PART: opcional
    if cod_part:
        resultado["COD_PART"] = {
            "titulo": "Código do participante (Campo 02 do Registro 0150)",
            "valor": cod_part
        }
    else:
        resultado["COD_PART"] = {
            "titulo": "Código do participante (Campo 02 do Registro 0150)",
            "valor": ""
        }
    
    # COD_CTA: opcional
    if cod_cta:
        resultado["COD_CTA"] = {
            "titulo": "Código da conta analítica contábil debitada/creditada",
            "valor": cod_cta
        }
    else:
        resultado["COD_CTA"] = {
            "titulo": "Código da conta analítica contábil debitada/creditada",
            "valor": ""
        }
    
    # DESC_COMPL: opcional
    if desc_compl:
        resultado["DESC_COMPL"] = {
            "titulo": "Descrição complementar do Documento/Operação",
            "valor": desc_compl
        }
    else:
        resultado["DESC_COMPL"] = {
            "titulo": "Descrição complementar do Documento/Operação",
            "valor": ""
        }
    
    return resultado


def validar_1210(linhas):
    """
    Valida uma ou mais linhas do registro 1210 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |1210|CNPJ|CST_PIS|COD_PART|DT_OPER|VL_OPER|VL_BC_PIS|ALIQ_PIS|VL_PIS|COD_CTA|DESC_COMPL|
        
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
        resultado = _processar_linha_1210(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
