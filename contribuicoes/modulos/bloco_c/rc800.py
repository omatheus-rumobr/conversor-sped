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


def _validar_chave_cfe(chave_cfe):
    """
    Valida a chave do CF-e (44 dígitos) e o dígito verificador.
    
    Args:
        chave_cfe: String com a chave do CF-e (44 dígitos)
        
    Returns:
        bool: True se válida, False caso contrário
    """
    if not chave_cfe or len(chave_cfe) != 44 or not chave_cfe.isdigit():
        return False
    
    # Extrai os 43 primeiros dígitos e o dígito verificador (último dígito)
    chave_43 = chave_cfe[:43]
    dv_informado = int(chave_cfe[43])
    
    # Calcula o dígito verificador usando módulo 11
    soma = 0
    multiplicador = 2
    
    # Percorre os 43 dígitos de trás para frente
    for i in range(42, -1, -1):
        soma += int(chave_43[i]) * multiplicador
        multiplicador += 1
        if multiplicador > 9:
            multiplicador = 2
    
    # Calcula o resto da divisão por 11
    resto = soma % 11
    
    # Se o resto for 0 ou 1, o dígito verificador é 0
    # Caso contrário, é 11 - resto
    if resto < 2:
        dv_calculado = 0
    else:
        dv_calculado = 11 - resto
    
    return dv_calculado == dv_informado


def _validar_cpf(cpf):
    """
    Valida o formato básico do CPF (11 dígitos).
    Valida também o dígito verificador (DV).
    """
    if not cpf:
        return False
    
    # Remove formatação
    cpf_limpo = cpf.replace(".", "").replace("/", "").replace("-", "").replace(" ", "")
    
    if not cpf_limpo.isdigit() or len(cpf_limpo) != 11:
        return False
    
    # Validação do dígito verificador
    # Verifica se todos os dígitos são iguais (CPF inválido)
    if len(set(cpf_limpo)) == 1:
        return False
    
    # Calcula primeiro dígito verificador
    multiplicadores1 = [10, 9, 8, 7, 6, 5, 4, 3, 2]
    soma = sum(int(cpf_limpo[i]) * multiplicadores1[i] for i in range(9))
    resto = soma % 11
    dv1 = 0 if resto < 2 else 11 - resto
    
    if int(cpf_limpo[9]) != dv1:
        return False
    
    # Calcula segundo dígito verificador
    multiplicadores2 = [11, 10, 9, 8, 7, 6, 5, 4, 3, 2]
    soma = sum(int(cpf_limpo[i]) * multiplicadores2[i] for i in range(10))
    resto = soma % 11
    dv2 = 0 if resto < 2 else 11 - resto
    
    if int(cpf_limpo[10]) != dv2:
        return False
    
    return True


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


def _validar_cpf_cnpj(cpf_cnpj):
    """
    Valida CPF (11 dígitos) ou CNPJ (14 dígitos) conforme o tamanho.
    
    Args:
        cpf_cnpj: String com CPF ou CNPJ
        
    Returns:
        bool: True se válido, False caso contrário
    """
    if not cpf_cnpj:
        return False
    
    # Remove formatação
    cpf_cnpj_limpo = cpf_cnpj.replace(".", "").replace("/", "").replace("-", "").replace(" ", "")
    
    if not cpf_cnpj_limpo.isdigit():
        return False
    
    if len(cpf_cnpj_limpo) == 11:
        return _validar_cpf(cpf_cnpj_limpo)
    elif len(cpf_cnpj_limpo) == 14:
        return _validar_cnpj(cpf_cnpj_limpo)
    else:
        return False


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


def _processar_linha_c800(linha):
    """
    Processa uma única linha do registro C800 e retorna um dicionário.
    
    Formato:
      |C800|COD_MOD|COD_SIT|NUM_CFE|DT_DOC|VL_CFE|VL_PIS|VL_COFINS|CNPJ_CPF|NR_SAT|CHV_CFE|VL_DESC|VL_MERC|VL_OUT_DA|VL_ICMS|VL_PIS_ST|VL_COFINS_ST|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "C800"
    - COD_MOD: obrigatório, código do modelo do documento fiscal (2 caracteres)
      - Valores válidos: [59]
    - COD_SIT: obrigatório, código da situação do documento fiscal (2 dígitos)
      - Valores válidos: [00, 01, 02, 03]
    - NUM_CFE: obrigatório, número do Cupom Fiscal Eletrônico (9 dígitos)
    - DT_DOC: obrigatório, data da emissão do Cupom Fiscal Eletrônico (ddmmaaaa)
      - Validação: deve ser menor ou igual à DT_FIN do registro 0000 (validação em camada superior)
    - VL_CFE: obrigatório, valor total do Cupom Fiscal Eletrônico (numérico, 2 decimais)
      - Validação: deve ser igual à soma do campo VL_OPR dos registros C850 filhos (validação em camada superior)
    - VL_PIS: opcional, valor total do PIS (numérico, 2 decimais)
    - VL_COFINS: opcional, valor total da COFINS (numérico, 2 decimais)
    - CNPJ_CPF: opcional, CNPJ ou CPF do destinatário (14 dígitos para CNPJ, 11 dígitos para CPF)
      - Validação: se 14 caracteres, valida como CNPJ; se 11 caracteres, valida como CPF
    - NR_SAT: opcional, número de série do equipamento SAT (9 dígitos)
    - CHV_CFE: opcional, chave do Cupom Fiscal Eletrônico (44 dígitos)
      - Validação do dígito verificador quando preenchido
      - Validações de consistência com outros campos devem ser feitas em camada superior
    - VL_DESC: opcional, valor total do desconto/exclusão sobre item (numérico, 2 decimais)
    - VL_MERC: opcional, valor total das mercadorias e serviços (numérico, 2 decimais)
    - VL_OUT_DA: opcional, valor de outras despesas acessórias (numérico, 2 decimais)
    - VL_ICMS: opcional, valor do ICMS (numérico, 2 decimais)
    - VL_PIS_ST: opcional, valor total do PIS retido por substituição tributária (numérico, 2 decimais)
    - VL_COFINS_ST: opcional, valor total da COFINS retido por substituição tributária (numérico, 2 decimais)
    
    Nota: Registro para escrituração pela pessoa jurídica, da receita da venda de bens e serviços mediante
    a emissão de cupom fiscal eletrônico – CF-e (código 59).
    
    Para cupom fiscal eletrônico cancelado, informar somente os campos REG, COD_MOD, COD_SIT, NUM_CFE,
    NR_SAT e CHV_CFE.
    
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
    # Remove primeiro e último se vazios (formato padrão SPED: |C800|...|)
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
    if reg != "C800":
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
    
    # Extrai todos os campos (17 campos no total)
    cod_mod = obter_campo(1)
    cod_sit = obter_campo(2)
    num_cfe = obter_campo(3)
    dt_doc = obter_campo(4)
    vl_cfe = obter_campo(5)
    vl_pis = obter_campo(6)
    vl_cofins = obter_campo(7)
    cnpj_cpf = obter_campo(8)
    nr_sat = obter_campo(9)
    chv_cfe = obter_campo(10)
    vl_desc = obter_campo(11)
    vl_merc = obter_campo(12)
    vl_out_da = obter_campo(13)
    vl_icms = obter_campo(14)
    vl_pis_st = obter_campo(15)
    vl_cofins_st = obter_campo(16)
    
    # Validações básicas dos campos obrigatórios
    
    # COD_MOD: obrigatório, valores válidos [59]
    if not cod_mod or cod_mod != "59":
        return None
    
    # COD_SIT: obrigatório, valores válidos [00, 01, 02, 03]
    cod_sit_validos = ["00", "01", "02", "03"]
    if not cod_sit or cod_sit not in cod_sit_validos:
        return None
    
    # NUM_CFE: obrigatório, número do Cupom Fiscal Eletrônico (9 dígitos)
    if not num_cfe or not num_cfe.isdigit() or len(num_cfe) > 9:
        return None
    
    # DT_DOC: obrigatório, data da emissão do Cupom Fiscal Eletrônico (ddmmaaaa)
    ok_dt_doc, data_dt_doc = _validar_data(dt_doc)
    if not ok_dt_doc:
        return None
    
    # VL_CFE: obrigatório, valor total do Cupom Fiscal Eletrônico (numérico, 2 decimais)
    ok_vl_cfe, val_vl_cfe, _ = validar_valor_numerico(vl_cfe, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok_vl_cfe:
        return None
    
    # VL_PIS: opcional, valor total do PIS (numérico, 2 decimais)
    ok_vl_pis, val_vl_pis, _ = validar_valor_numerico(vl_pis, decimais=2, nao_negativo=True)
    if not ok_vl_pis:
        return None
    
    # VL_COFINS: opcional, valor total da COFINS (numérico, 2 decimais)
    ok_vl_cofins, val_vl_cofins, _ = validar_valor_numerico(vl_cofins, decimais=2, nao_negativo=True)
    if not ok_vl_cofins:
        return None
    
    # CNPJ_CPF: opcional, CNPJ ou CPF do destinatário (14 dígitos para CNPJ, 11 dígitos para CPF)
    if cnpj_cpf:
        if not _validar_cpf_cnpj(cnpj_cpf):
            return None
    
    # NR_SAT: opcional, número de série do equipamento SAT (9 dígitos)
    if nr_sat and (not nr_sat.isdigit() or len(nr_sat) > 9):
        return None
    
    # CHV_CFE: opcional, chave do Cupom Fiscal Eletrônico (44 dígitos)
    if chv_cfe:
        if not _validar_chave_cfe(chv_cfe):
            return None
    
    # VL_DESC: opcional, valor total do desconto/exclusão sobre item (numérico, 2 decimais)
    ok_vl_desc, val_vl_desc, _ = validar_valor_numerico(vl_desc, decimais=2, nao_negativo=True)
    if not ok_vl_desc:
        return None
    
    # VL_MERC: opcional, valor total das mercadorias e serviços (numérico, 2 decimais)
    ok_vl_merc, val_vl_merc, _ = validar_valor_numerico(vl_merc, decimais=2, nao_negativo=True)
    if not ok_vl_merc:
        return None
    
    # VL_OUT_DA: opcional, valor de outras despesas acessórias (numérico, 2 decimais)
    ok_vl_out_da, val_vl_out_da, _ = validar_valor_numerico(vl_out_da, decimais=2, nao_negativo=True)
    if not ok_vl_out_da:
        return None
    
    # VL_ICMS: opcional, valor do ICMS (numérico, 2 decimais)
    ok_vl_icms, val_vl_icms, _ = validar_valor_numerico(vl_icms, decimais=2)
    if not ok_vl_icms:
        return None
    
    # VL_PIS_ST: opcional, valor total do PIS retido por substituição tributária (numérico, 2 decimais)
    ok_vl_pis_st, val_vl_pis_st, _ = validar_valor_numerico(vl_pis_st, decimais=2, nao_negativo=True)
    if not ok_vl_pis_st:
        return None
    
    # VL_COFINS_ST: opcional, valor total da COFINS retido por substituição tributária (numérico, 2 decimais)
    ok_vl_cofins_st, val_vl_cofins_st, _ = validar_valor_numerico(vl_cofins_st, decimais=2, nao_negativo=True)
    if not ok_vl_cofins_st:
        return None
    
    # Função auxiliar para formatar valores monetários
    def fmt_valor(v):
        if v is None:
            return ""
        return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    # Função auxiliar para formatar data
    def fmt_data(data_str):
        if not data_str or len(data_str) != 8:
            return ""
        return f"{data_str[:2]}/{data_str[2:4]}/{data_str[4:]}"
    
    # Função auxiliar para formatar CPF/CNPJ
    def fmt_cpf_cnpj(cpf_cnpj_str):
        if not cpf_cnpj_str:
            return ""
        cpf_cnpj_limpo = cpf_cnpj_str.replace(".", "").replace("/", "").replace("-", "").replace(" ", "")
        if len(cpf_cnpj_limpo) == 11:
            return f"{cpf_cnpj_limpo[:3]}.{cpf_cnpj_limpo[3:6]}.{cpf_cnpj_limpo[6:9]}-{cpf_cnpj_limpo[9:11]}"
        elif len(cpf_cnpj_limpo) == 14:
            return f"{cpf_cnpj_limpo[:2]}.{cpf_cnpj_limpo[2:5]}.{cpf_cnpj_limpo[5:8]}/{cpf_cnpj_limpo[8:12]}-{cpf_cnpj_limpo[12:14]}"
        return cpf_cnpj_str
    
    # Descrições dos campos
    descricoes_cod_sit = {
        "00": "Documento regular",
        "01": "Documento regular extemporâneo",
        "02": "Documento cancelado",
        "03": "Documento cancelado extemporâneo"
    }
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg,
            "descricao": "Texto fixo contendo 'C800'"
        },
        "COD_MOD": {
            "titulo": "Código do modelo do documento fiscal",
            "valor": cod_mod,
            "descricao": "Cupom Fiscal Eletrônico"
        },
        "COD_SIT": {
            "titulo": "Código da situação do documento fiscal",
            "valor": cod_sit,
            "descricao": descricoes_cod_sit.get(cod_sit, "")
        },
        "NUM_CFE": {
            "titulo": "Número do Cupom Fiscal Eletrônico",
            "valor": num_cfe
        },
        "DT_DOC": {
            "titulo": "Data da emissão do Cupom Fiscal Eletrônico",
            "valor": dt_doc,
            "valor_formatado": fmt_data(dt_doc)
        },
        "VL_CFE": {
            "titulo": "Valor total do Cupom Fiscal Eletrônico",
            "valor": vl_cfe,
            "valor_formatado": fmt_valor(val_vl_cfe)
        },
        "VL_PIS": {
            "titulo": "Valor total do PIS",
            "valor": vl_pis,
            "valor_formatado": fmt_valor(val_vl_pis)
        },
        "VL_COFINS": {
            "titulo": "Valor total da COFINS",
            "valor": vl_cofins,
            "valor_formatado": fmt_valor(val_vl_cofins)
        },
        "CNPJ_CPF": {
            "titulo": "CNPJ ou CPF do destinatário",
            "valor": cnpj_cpf,
            "valor_formatado": fmt_cpf_cnpj(cnpj_cpf) if cnpj_cpf else ""
        },
        "NR_SAT": {
            "titulo": "Número de Série do equipamento SAT",
            "valor": nr_sat
        },
        "CHV_CFE": {
            "titulo": "Chave do Cupom Fiscal Eletrônico",
            "valor": chv_cfe
        },
        "VL_DESC": {
            "titulo": "Valor total do desconto/exclusão sobre item",
            "valor": vl_desc,
            "valor_formatado": fmt_valor(val_vl_desc)
        },
        "VL_MERC": {
            "titulo": "Valor total das mercadorias e serviços",
            "valor": vl_merc,
            "valor_formatado": fmt_valor(val_vl_merc)
        },
        "VL_OUT_DA": {
            "titulo": "Valor de outras desp. Acessórias (acréscimo)",
            "valor": vl_out_da,
            "valor_formatado": fmt_valor(val_vl_out_da)
        },
        "VL_ICMS": {
            "titulo": "Valor do ICMS",
            "valor": vl_icms,
            "valor_formatado": fmt_valor(val_vl_icms)
        },
        "VL_PIS_ST": {
            "titulo": "Valor total do PIS retido por subst. trib.",
            "valor": vl_pis_st,
            "valor_formatado": fmt_valor(val_vl_pis_st)
        },
        "VL_COFINS_ST": {
            "titulo": "Valor total da COFINS retido por subst. trib.",
            "valor": vl_cofins_st,
            "valor_formatado": fmt_valor(val_vl_cofins_st)
        }
    }
    
    return resultado


def validar_c800(linhas):
    """
    Valida uma ou mais linhas do registro C800 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |C800|COD_MOD|COD_SIT|NUM_CFE|DT_DOC|VL_CFE|VL_PIS|VL_COFINS|CNPJ_CPF|NR_SAT|CHV_CFE|VL_DESC|VL_MERC|VL_OUT_DA|VL_ICMS|VL_PIS_ST|VL_COFINS_ST|
        
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
        resultado = _processar_linha_c800(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
