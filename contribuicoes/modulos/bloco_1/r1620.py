import json


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


def _processar_linha_1620(linha, per_apur_ant_1600=None):
    """
    Processa uma única linha do registro 1620 e retorna um dicionário.
    
    Formato:
      |1620|PER_APU_CRED|ORIG_CRED|COD_CRED|VL_CRED|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "1620"
    - PER_APU_CRED: obrigatório, formato mmaaaa, período válido
      - Deve ser anterior ou igual ao período de apuração (PER_APUR_ANT) do registro pai 1600
    - ORIG_CRED: obrigatório, valores válidos [01, 02]
    - COD_CRED: obrigatório, 3 dígitos (código conforme Tabela 4.3.6)
    - VL_CRED: obrigatório, numérico com 2 decimais, não negativo
    
    Nota: A chave deste registro é formada pelos campos: PER_APU_CRED + ORIG_CRED + COD_CRED.
    A validação de que COD_CRED deve existir na Tabela 4.3.6 deve ser feita em uma camada superior.
    A validação de que a soma dos valores do campo VL_CRED deve ser transportada para o campo
    VL_CRED_COFINS_DESC do registro pai 1600 deve ser feita em uma camada superior.
    
    Args:
        linha: String com uma linha do SPED
        per_apur_ant_1600: Período de apuração do registro pai 1600 (mmaaaa) - opcional, para validação
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |1620|...|)
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
    if reg != "1620":
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
    
    # Extrai todos os campos (5 campos no total)
    per_apu_cred = obter_campo(1)
    orig_cred = obter_campo(2)
    cod_cred = obter_campo(3)
    vl_cred = obter_campo(4)
    
    # Validações básicas dos campos obrigatórios
    
    # PER_APU_CRED: obrigatório, formato mmaaaa, período válido
    per_apu_cred_valido, per_apu_cred_tuplo = _validar_periodo_mmaaaa(per_apu_cred)
    if not per_apu_cred_valido:
        return None
    
    # PER_APU_CRED deve ser anterior ou igual ao período de apuração do registro pai 1600 (quando informado)
    if per_apur_ant_1600:
        ok_1600, per_1600_tuplo = _validar_periodo_mmaaaa(per_apur_ant_1600)
        if ok_1600 and per_apu_cred_tuplo:
            mes_cred, ano_cred = per_apu_cred_tuplo
            mes_1600, ano_1600 = per_1600_tuplo
            # Deve ser anterior ou igual (mesmo mês/ano ou anterior)
            if ano_cred > ano_1600 or (ano_cred == ano_1600 and mes_cred > mes_1600):
                return None
    
    # ORIG_CRED: obrigatório, valores válidos [01, 02]
    valores_validos_orig_cred = ["01", "02"]
    if not orig_cred or orig_cred not in valores_validos_orig_cred:
        return None
    
    # COD_CRED: obrigatório, 3 dígitos
    if not cod_cred or len(cod_cred) != 3 or not cod_cred.isdigit():
        return None
    
    # VL_CRED: obrigatório, numérico com 2 decimais, não negativo
    ok1, val1, _ = validar_valor_numerico(vl_cred, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok1:
        return None
    
    # Função auxiliar para formatar período
    def fmt_periodo(p):
        if p:
            mes, ano = p
            return f"{mes:02d}/{ano}"
        return ""
    
    # Função auxiliar para formatar valores monetários
    def fmt_valor(v):
        return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    # Monta o resultado
    descricoes_orig_cred = {
        "01": "Crédito decorrente de operações próprias",
        "02": "Crédito transferido por pessoa jurídica sucedida"
    }
    
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "PER_APU_CRED": {
            "titulo": "Período de Apuração do Crédito (MM/AAAA)",
            "valor": per_apu_cred,
            "valor_formatado": fmt_periodo(per_apu_cred_tuplo)
        },
        "ORIG_CRED": {
            "titulo": "Indicador da origem do crédito",
            "valor": orig_cred,
            "descricao": descricoes_orig_cred.get(orig_cred, "")
        },
        "COD_CRED": {
            "titulo": "Código do Tipo do Crédito, conforme Tabela 4.3.6",
            "valor": cod_cred
        },
        "VL_CRED": {
            "titulo": "Valor do Crédito a Descontar",
            "valor": vl_cred,
            "valor_formatado": fmt_valor(val1)
        }
    }
    
    return resultado


def validar_1620(linhas, per_apur_ant_1600=None):
    """
    Valida uma ou mais linhas do registro 1620 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |1620|PER_APU_CRED|ORIG_CRED|COD_CRED|VL_CRED|
        per_apur_ant_1600: Período de apuração do registro pai 1600 (mmaaaa) - opcional, para validação
        
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
        resultado = _processar_linha_1620(linha, per_apur_ant_1600=per_apur_ant_1600)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
