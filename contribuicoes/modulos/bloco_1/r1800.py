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


def _processar_linha_1800(linha):
    """
    Processa uma única linha do registro 1800 e retorna um dicionário.
    
    Formato:
      |1800|INC_IMOB|REC_RECEB_RET|REC_FIN_RET|BC_RET|ALIQ_RET|VL_REC_UNI|DT_REC_UNI|COD_REC|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "1800"
    - INC_IMOB: obrigatório, CNPJ do empreendimento (14 dígitos, formato "XXXXXXXXYYYYZZ")
    - REC_RECEB_RET: obrigatório, numérico com 2 decimais, não negativo
    - REC_FIN_RET: opcional, numérico com 2 decimais, não negativo
    - BC_RET: obrigatório, numérico com 2 decimais, não negativo
      - Deve ser igual a REC_RECEB_RET + REC_FIN_RET (com tolerância)
    - ALIQ_RET: obrigatório, numérico com 6 caracteres, 2 decimais
      - Valores válidos: 1% (0.01), 4% (0.04), 6% (0.06)
    - VL_REC_UNI: obrigatório, numérico com 2 decimais, não negativo
      - Deve ser igual a BC_RET * ALIQ_RET (com tolerância)
    - DT_REC_UNI: opcional, formato ddmmaaaa, data válida
    - COD_REC: opcional, 4 caracteres
    
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
    # Remove primeiro e último se vazios (formato padrão SPED: |1800|...|)
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
    if reg != "1800":
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
    inc_imob = obter_campo(1)
    rec_receb_ret = obter_campo(2)
    rec_fin_ret = obter_campo(3)
    bc_ret = obter_campo(4)
    aliq_ret = obter_campo(5)
    vl_rec_uni = obter_campo(6)
    dt_rec_uni = obter_campo(7)
    cod_rec = obter_campo(8)
    
    # Validações básicas dos campos obrigatórios
    
    # INC_IMOB: obrigatório, CNPJ válido (14 dígitos)
    if not inc_imob or not _validar_cnpj(inc_imob):
        return None
    
    # REC_RECEB_RET: obrigatório, numérico com 2 decimais, não negativo
    ok1, val1, _ = validar_valor_numerico(rec_receb_ret, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok1:
        return None
    
    # REC_FIN_RET: opcional, numérico com 2 decimais, não negativo
    ok2, val2, _ = validar_valor_numerico(rec_fin_ret, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok2:
        return None
    
    # BC_RET: obrigatório, numérico com 2 decimais, não negativo
    ok3, val3, _ = validar_valor_numerico(bc_ret, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok3:
        return None
    
    # Validação: BC_RET deve ser igual a REC_RECEB_RET + REC_FIN_RET (com tolerância)
    bc_ret_calculado = val1 + val2
    if not _float_igual(val3, bc_ret_calculado):
        return None
    
    # ALIQ_RET: obrigatório, numérico com 6 caracteres, 2 decimais
    # Valores válidos: 1% (0.01), 4% (0.04), 6% (0.06)
    if not aliq_ret:
        return None
    
    # Verifica formato: máximo 6 caracteres (incluindo ponto decimal)
    if len(aliq_ret) > 6:
        return None
    
    ok4, val4, _ = validar_valor_numerico(aliq_ret, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok4:
        return None
    
    # Valores válidos: 0.01 (1%), 0.04 (4%), 0.06 (6%)
    valores_validos_aliq = [0.01, 0.04, 0.06]
    if not any(_float_igual(val4, v) for v in valores_validos_aliq):
        return None
    
    # VL_REC_UNI: obrigatório, numérico com 2 decimais, não negativo
    ok5, val5, _ = validar_valor_numerico(vl_rec_uni, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok5:
        return None
    
    # Validação: VL_REC_UNI deve ser igual a BC_RET * ALIQ_RET (com tolerância)
    vl_rec_uni_calculado = val3 * val4
    if not _float_igual(val5, vl_rec_uni_calculado):
        return None
    
    # DT_REC_UNI: opcional, formato ddmmaaaa, data válida
    dt_rec_uni_obj = None
    if dt_rec_uni:
        dt_rec_uni_valido, dt_rec_uni_obj = _validar_data(dt_rec_uni)
        if not dt_rec_uni_valido:
            return None
    
    # COD_REC: opcional, 4 caracteres
    if cod_rec and len(cod_rec) > 4:
        return None
    
    # Função auxiliar para formatar CNPJ
    def fmt_cnpj(cnpj_str):
        if cnpj_str and len(cnpj_str) == 14:
            return f"{cnpj_str[:2]}.{cnpj_str[2:5]}.{cnpj_str[5:8]}/{cnpj_str[8:12]}-{cnpj_str[12:14]}"
        return cnpj_str
    
    # Função auxiliar para formatar valores monetários
    def fmt_valor(v):
        return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    # Função auxiliar para formatar porcentagem
    def fmt_percentual(v):
        return f"{v * 100:.2f}%"
    
    # Função auxiliar para formatar data
    def fmt_data(dt):
        if dt:
            return dt.strftime("%d/%m/%Y")
        return ""
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "INC_IMOB": {
            "titulo": "Empreendimento objeto de Incorporação Imobiliária, optante pelo RET",
            "valor": inc_imob,
            "valor_formatado": fmt_cnpj(inc_imob)
        },
        "REC_RECEB_RET": {
            "titulo": "Receitas recebidas pela incorporadora na venda das unidades imobiliárias que compõem a incorporação",
            "valor": rec_receb_ret,
            "valor_formatado": fmt_valor(val1)
        },
        "REC_FIN_RET": {
            "titulo": "Receitas Financeiras e Variações Monetárias decorrentes das vendas submetidas ao RET",
            "valor": rec_fin_ret,
            "valor_formatado": fmt_valor(val2) if rec_fin_ret else ""
        },
        "BC_RET": {
            "titulo": "Base de Cálculo do Recolhimento Unificado",
            "valor": bc_ret,
            "valor_formatado": fmt_valor(val3)
        },
        "ALIQ_RET": {
            "titulo": "Alíquota do Recolhimento Unificado",
            "valor": aliq_ret,
            "valor_formatado": fmt_percentual(val4)
        },
        "VL_REC_UNI": {
            "titulo": "Valor do Recolhimento Unificado",
            "valor": vl_rec_uni,
            "valor_formatado": fmt_valor(val5)
        },
        "DT_REC_UNI": {
            "titulo": "Data do recolhimento unificado",
            "valor": dt_rec_uni,
            "valor_formatado": fmt_data(dt_rec_uni_obj) if dt_rec_uni_obj else ""
        },
        "COD_REC": {
            "titulo": "Código da Receita",
            "valor": cod_rec
        }
    }
    
    return resultado


def validar_1800(linhas):
    """
    Valida uma ou mais linhas do registro 1800 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |1800|INC_IMOB|REC_RECEB_RET|REC_FIN_RET|BC_RET|ALIQ_RET|VL_REC_UNI|DT_REC_UNI|COD_REC|
        
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
        resultado = _processar_linha_1800(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
