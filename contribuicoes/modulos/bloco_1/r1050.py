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


def _float_igual(a, b, tolerancia=0.01):
    """Compara dois floats com tolerância."""
    if a is None or b is None:
        return False
    return abs(a - b) <= tolerancia


def _processar_linha_1050(linha):
    """
    Processa uma única linha do registro 1050 e retorna um dicionário.
    
    Formato:
      |1050|DT_REF|IND_AJ_BC|CNPJ|VL_AJ_TOT|VL_AJ_CST01|VL_AJ_CST02|VL_AJ_CST03|VL_AJ_CST04|VL_AJ_CST05|VL_AJ_CST06|VL_AJ_CST07|VL_AJ_CST08|VL_AJ_CST09|VL_AJ_CST49|VL_AJ_CST99|IND_APROP|NUM_REC|INFO_COMPL|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "1050"
    - DT_REF: obrigatório, formato ddmmaaaa, data válida
    - IND_AJ_BC: obrigatório, 2 caracteres (código conforme Tabela Externa 4.3.18)
    - CNPJ: obrigatório, 14 dígitos, validar DV
    - VL_AJ_TOT: obrigatório, numérico com 2 decimais
    - VL_AJ_CST01 a VL_AJ_CST09, VL_AJ_CST49, VL_AJ_CST99: obrigatórios, numéricos com 2 decimais
    - IND_APROP: obrigatório, valores válidos [01, 02, 03]
    - NUM_REC: opcional, até 80 caracteres
    - INFO_COMPL: opcional
    
    Validação: VL_AJ_TOT deve ser igual à soma dos valores VL_AJ_CST01 a VL_AJ_CST09, VL_AJ_CST49 e VL_AJ_CST99
    
    Nota: Este registro só é habilitado na versão 3.1.0 do leiaute do programa da EFD-Contribuições,
    a ser utilizado na escrituração dos fatos geradores ocorridos a partir de 01 de janeiro de 2019.
    A validação de que IND_AJ_BC deve existir na Tabela Externa 4.3.18 deve ser feita em uma camada superior.
    
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
    # Remove primeiro e último se vazios (formato padrão SPED: |1050|...|)
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
    if reg != "1050":
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
    
    # Extrai todos os campos (19 campos no total)
    dt_ref = obter_campo(1)
    ind_aj_bc = obter_campo(2)
    cnpj = obter_campo(3)
    vl_aj_tot = obter_campo(4)
    vl_aj_cst01 = obter_campo(5)
    vl_aj_cst02 = obter_campo(6)
    vl_aj_cst03 = obter_campo(7)
    vl_aj_cst04 = obter_campo(8)
    vl_aj_cst05 = obter_campo(9)
    vl_aj_cst06 = obter_campo(10)
    vl_aj_cst07 = obter_campo(11)
    vl_aj_cst08 = obter_campo(12)
    vl_aj_cst09 = obter_campo(13)
    vl_aj_cst49 = obter_campo(14)
    vl_aj_cst99 = obter_campo(15)
    ind_aprop = obter_campo(16)
    num_rec = obter_campo(17)
    info_compl = obter_campo(18)
    
    # Validações básicas dos campos obrigatórios
    
    # DT_REF: obrigatório, formato ddmmaaaa, data válida
    dt_ref_valida, dt_ref_obj = _validar_data(dt_ref)
    if not dt_ref_valida:
        return None
    
    # IND_AJ_BC: obrigatório, 2 caracteres
    if not ind_aj_bc or len(ind_aj_bc) != 2:
        return None
    
    # CNPJ: obrigatório, 14 dígitos, validar DV
    if not cnpj or not _validar_cnpj(cnpj):
        return None
    
    # VL_AJ_TOT: obrigatório, numérico com 2 decimais
    ok1, val1, _ = validar_valor_numerico(vl_aj_tot, decimais=2, obrigatorio=True)
    if not ok1:
        return None
    
    # VL_AJ_CST01 a VL_AJ_CST09, VL_AJ_CST49, VL_AJ_CST99: obrigatórios, numéricos com 2 decimais
    valores_cst = []
    campos_cst = [
        (vl_aj_cst01, "VL_AJ_CST01"),
        (vl_aj_cst02, "VL_AJ_CST02"),
        (vl_aj_cst03, "VL_AJ_CST03"),
        (vl_aj_cst04, "VL_AJ_CST04"),
        (vl_aj_cst05, "VL_AJ_CST05"),
        (vl_aj_cst06, "VL_AJ_CST06"),
        (vl_aj_cst07, "VL_AJ_CST07"),
        (vl_aj_cst08, "VL_AJ_CST08"),
        (vl_aj_cst09, "VL_AJ_CST09"),
        (vl_aj_cst49, "VL_AJ_CST49"),
        (vl_aj_cst99, "VL_AJ_CST99")
    ]
    
    for valor_str, nome_campo in campos_cst:
        ok, val, _ = validar_valor_numerico(valor_str, decimais=2, obrigatorio=True)
        if not ok:
            return None
        valores_cst.append(val)
    
    # Validação: VL_AJ_TOT deve ser igual à soma dos valores dos CSTs
    soma_csts = sum(valores_cst)
    if not _float_igual(val1, soma_csts):
        return None
    
    # IND_APROP: obrigatório, valores válidos [01, 02, 03]
    valores_validos_ind_aprop = ["01", "02", "03"]
    if not ind_aprop or ind_aprop not in valores_validos_ind_aprop:
        return None
    
    # NUM_REC: opcional, até 80 caracteres
    if num_rec and len(num_rec) > 80:
        return None
    
    # Função auxiliar para formatar data
    def fmt_data(d):
        return d.strftime("%d/%m/%Y") if d else ""
    
    # Função auxiliar para formatar valores monetários
    def fmt_valor(v):
        return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    # Monta o resultado
    descricoes_ind_aprop = {
        "01": "Referente ao PIS/Pasep e a Cofins",
        "02": "Referente unicamente ao PIS/Pasep",
        "03": "Referente unicamente à Cofins"
    }
    
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "DT_REF": {
            "titulo": "Data de referência do ajuste",
            "valor": dt_ref,
            "valor_formatado": fmt_data(dt_ref_obj)
        },
        "IND_AJ_BC": {
            "titulo": "Indicador da natureza do ajuste da base de cálculo, conforme Tabela Externa 4.3.18",
            "valor": ind_aj_bc
        },
        "CNPJ": {
            "titulo": "CNPJ do estabelecimento a que se refere o ajuste",
            "valor": cnpj
        },
        "VL_AJ_TOT": {
            "titulo": "Valor total do ajuste",
            "valor": vl_aj_tot,
            "valor_formatado": fmt_valor(val1)
        },
        "VL_AJ_CST01": {
            "titulo": "Parcela do ajuste a apropriar na base de cálculo referente ao CST 01",
            "valor": vl_aj_cst01,
            "valor_formatado": fmt_valor(valores_cst[0])
        },
        "VL_AJ_CST02": {
            "titulo": "Parcela do ajuste a apropriar na base de cálculo referente ao CST 02",
            "valor": vl_aj_cst02,
            "valor_formatado": fmt_valor(valores_cst[1])
        },
        "VL_AJ_CST03": {
            "titulo": "Parcela do ajuste a apropriar na base de cálculo referente ao CST 03",
            "valor": vl_aj_cst03,
            "valor_formatado": fmt_valor(valores_cst[2])
        },
        "VL_AJ_CST04": {
            "titulo": "Parcela do ajuste a apropriar na base de cálculo referente ao CST 04",
            "valor": vl_aj_cst04,
            "valor_formatado": fmt_valor(valores_cst[3])
        },
        "VL_AJ_CST05": {
            "titulo": "Parcela do ajuste a apropriar na base de cálculo referente ao CST 05",
            "valor": vl_aj_cst05,
            "valor_formatado": fmt_valor(valores_cst[4])
        },
        "VL_AJ_CST06": {
            "titulo": "Parcela do ajuste a apropriar na base de cálculo referente ao CST 06",
            "valor": vl_aj_cst06,
            "valor_formatado": fmt_valor(valores_cst[5])
        },
        "VL_AJ_CST07": {
            "titulo": "Parcela do ajuste a apropriar na base de cálculo referente ao CST 07",
            "valor": vl_aj_cst07,
            "valor_formatado": fmt_valor(valores_cst[6])
        },
        "VL_AJ_CST08": {
            "titulo": "Parcela do ajuste a apropriar na base de cálculo referente ao CST 08",
            "valor": vl_aj_cst08,
            "valor_formatado": fmt_valor(valores_cst[7])
        },
        "VL_AJ_CST09": {
            "titulo": "Parcela do ajuste a apropriar na base de cálculo referente ao CST 09",
            "valor": vl_aj_cst09,
            "valor_formatado": fmt_valor(valores_cst[8])
        },
        "VL_AJ_CST49": {
            "titulo": "Parcela do ajuste a apropriar na base de cálculo referente ao CST 49",
            "valor": vl_aj_cst49,
            "valor_formatado": fmt_valor(valores_cst[9])
        },
        "VL_AJ_CST99": {
            "titulo": "Parcela do ajuste a apropriar na base de cálculo referente ao CST 99",
            "valor": vl_aj_cst99,
            "valor_formatado": fmt_valor(valores_cst[10])
        },
        "IND_APROP": {
            "titulo": "Indicador de apropriação do ajuste",
            "valor": ind_aprop,
            "descricao": descricoes_ind_aprop.get(ind_aprop, "")
        }
    }
    
    # NUM_REC: opcional
    if num_rec:
        resultado["NUM_REC"] = {
            "titulo": "Número do recibo da escrituração a que se refere o ajuste",
            "valor": num_rec
        }
    else:
        resultado["NUM_REC"] = {
            "titulo": "Número do recibo da escrituração a que se refere o ajuste",
            "valor": ""
        }
    
    # INFO_COMPL: opcional
    if info_compl:
        resultado["INFO_COMPL"] = {
            "titulo": "Informação complementar do registro",
            "valor": info_compl
        }
    else:
        resultado["INFO_COMPL"] = {
            "titulo": "Informação complementar do registro",
            "valor": ""
        }
    
    return resultado


def validar_1050(linhas):
    """
    Valida uma ou mais linhas do registro 1050 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |1050|DT_REF|IND_AJ_BC|CNPJ|VL_AJ_TOT|VL_AJ_CST01|VL_AJ_CST02|VL_AJ_CST03|VL_AJ_CST04|VL_AJ_CST05|VL_AJ_CST06|VL_AJ_CST07|VL_AJ_CST08|VL_AJ_CST09|VL_AJ_CST49|VL_AJ_CST99|IND_APROP|NUM_REC|INFO_COMPL|
        
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
        resultado = _processar_linha_1050(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
