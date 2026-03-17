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


def _float_igual(a, b, tolerancia=0.01):
    """Compara dois floats com tolerância."""
    if a is None or b is None:
        return False
    return abs(a - b) <= tolerancia


def _processar_linha_1300(linha, per_apu_escrit=None):
    """
    Processa uma única linha do registro 1300 e retorna um dicionário.
    
    Formato:
      |1300|IND_NAT_RET|PR_REC_RET|VL_RET_APU|VL_RET_DED|VL_RET_PER|VL_RET_DCOMP|SLD_RET|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "1300"
    - IND_NAT_RET: obrigatório, valores válidos:
      - Até 2013: [01, 02, 03, 04, 05, 99]
      - A partir de 2014: [01, 02, 03, 04, 05, 51, 52, 53, 54, 55, 99]
    - PR_REC_RET: obrigatório, formato mmaaaa, período válido
      - Deve ser anterior ou o mesmo da atual escrituração (quando informado)
    - VL_RET_APU: obrigatório, numérico com 2 decimais, não negativo
    - VL_RET_DED: obrigatório, numérico com 2 decimais, não negativo
    - VL_RET_PER: obrigatório, numérico com 2 decimais, não negativo
    - VL_RET_DCOMP: obrigatório, numérico com 2 decimais, não negativo
    - SLD_RET: obrigatório, numérico com 2 decimais, não negativo
      - Deve ser igual a VL_RET_APU - VL_RET_DED - VL_RET_PER - VL_RET_DCOMP
    
    Nota: A chave deste registro é formada pelos campos: IND_NAT_RET + PR_REC_RET.
    A validação de que os valores devem guardar correlação com os valores informados
    nos Campos VL_RET_NC e VL_RET_CUM dos Registros M200 deve ser feita em uma camada superior.
    
    Args:
        linha: String com uma linha do SPED
        per_apu_escrit: Período de apuração da escrituração atual (mmaaaa) - opcional, para validação
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |1300|...|)
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
    if reg != "1300":
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
    
    # Extrai todos os campos (8 campos no total)
    ind_nat_ret = obter_campo(1)
    pr_rec_ret = obter_campo(2)
    vl_ret_apu = obter_campo(3)
    vl_ret_ded = obter_campo(4)
    vl_ret_per = obter_campo(5)
    vl_ret_dcomp = obter_campo(6)
    sld_ret = obter_campo(7)
    
    # Validações básicas dos campos obrigatórios
    
    # IND_NAT_RET: obrigatório, valores válidos
    # Valores válidos até 2013: [01, 02, 03, 04, 05, 99]
    # Valores válidos a partir de 2014: [01, 02, 03, 04, 05, 51, 52, 53, 54, 55, 99]
    valores_validos_ind_nat_ret = ["01", "02", "03", "04", "05", "51", "52", "53", "54", "55", "99"]
    if not ind_nat_ret or ind_nat_ret not in valores_validos_ind_nat_ret:
        return None
    
    # PR_REC_RET: obrigatório, formato mmaaaa, período válido
    pr_rec_ret_valido, pr_rec_ret_tuplo = _validar_periodo_mmaaaa(pr_rec_ret)
    if not pr_rec_ret_valido:
        return None
    
    # PR_REC_RET deve ser anterior ou o mesmo da atual escrituração (quando informado)
    if per_apu_escrit:
        ok_escrit, per_escrit_tuplo = _validar_periodo_mmaaaa(per_apu_escrit)
        if ok_escrit and pr_rec_ret_tuplo:
            mes_rec, ano_rec = pr_rec_ret_tuplo
            mes_escrit, ano_escrit = per_escrit_tuplo
            if ano_rec > ano_escrit or (ano_rec == ano_escrit and mes_rec > mes_escrit):
                return None
    
    # VL_RET_APU: obrigatório, numérico com 2 decimais, não negativo
    ok1, val1, _ = validar_valor_numerico(vl_ret_apu, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok1:
        return None
    
    # VL_RET_DED: obrigatório, numérico com 2 decimais, não negativo
    ok2, val2, _ = validar_valor_numerico(vl_ret_ded, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok2:
        return None
    
    # VL_RET_PER: obrigatório, numérico com 2 decimais, não negativo
    ok3, val3, _ = validar_valor_numerico(vl_ret_per, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok3:
        return None
    
    # VL_RET_DCOMP: obrigatório, numérico com 2 decimais, não negativo
    ok4, val4, _ = validar_valor_numerico(vl_ret_dcomp, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok4:
        return None
    
    # SLD_RET: obrigatório, numérico com 2 decimais, não negativo
    ok5, val5, _ = validar_valor_numerico(sld_ret, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok5:
        return None
    
    # Validação: SLD_RET deve ser igual a VL_RET_APU - VL_RET_DED - VL_RET_PER - VL_RET_DCOMP
    sld_ret_calculado = val1 - val2 - val3 - val4
    if not _float_igual(val5, sld_ret_calculado):
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
    descricoes_ind_nat_ret = {
        "01": "Retenção por Órgãos, Autarquias e Fundações Federais",
        "02": "Retenção por outras Entidades da Administração Pública Federal",
        "03": "Retenção por Pessoas Jurídicas de Direito Privado",
        "04": "Recolhimento por Sociedade Cooperativa",
        "05": "Retenção por Fabricante de Máquinas e Veículos",
        "51": "Retenção por Órgãos, Autarquias e Fundações Federais (Regime Cumulativo - Lucro Real)",
        "52": "Retenção por outras Entidades da Administração Pública Federal (Regime Cumulativo - Lucro Real)",
        "53": "Retenção por Pessoas Jurídicas de Direito Privado (Regime Cumulativo - Lucro Real)",
        "54": "Recolhimento por Sociedade Cooperativa (Regime Cumulativo - Lucro Real)",
        "55": "Retenção por Fabricante de Máquinas e Veículos (Regime Cumulativo - Lucro Real)",
        "99": "Outras Retenções"
    }
    
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "IND_NAT_RET": {
            "titulo": "Indicador de Natureza da Retenção na Fonte",
            "valor": ind_nat_ret,
            "descricao": descricoes_ind_nat_ret.get(ind_nat_ret, "")
        },
        "PR_REC_RET": {
            "titulo": "Período do Recebimento e da Retenção (MM/AAAA)",
            "valor": pr_rec_ret,
            "valor_formatado": fmt_periodo(pr_rec_ret_tuplo)
        },
        "VL_RET_APU": {
            "titulo": "Valor Total da Retenção",
            "valor": vl_ret_apu,
            "valor_formatado": fmt_valor(val1)
        },
        "VL_RET_DED": {
            "titulo": "Valor da Retenção deduzida da Contribuição devida no período da escrituração e em períodos anteriores",
            "valor": vl_ret_ded,
            "valor_formatado": fmt_valor(val2)
        },
        "VL_RET_PER": {
            "titulo": "Valor da Retenção utilizada mediante Pedido de Restituição",
            "valor": vl_ret_per,
            "valor_formatado": fmt_valor(val3)
        },
        "VL_RET_DCOMP": {
            "titulo": "Valor da Retenção utilizada mediante Declaração de Compensação",
            "valor": vl_ret_dcomp,
            "valor_formatado": fmt_valor(val4)
        },
        "SLD_RET": {
            "titulo": "Saldo de Retenção a utilizar em períodos de apuração futuros (04 – 05 - 06 - 07)",
            "valor": sld_ret,
            "valor_formatado": fmt_valor(val5)
        }
    }
    
    return resultado


def validar_1300(linhas, per_apu_escrit=None):
    """
    Valida uma ou mais linhas do registro 1300 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |1300|IND_NAT_RET|PR_REC_RET|VL_RET_APU|VL_RET_DED|VL_RET_PER|VL_RET_DCOMP|SLD_RET|
        per_apu_escrit: Período de apuração da escrituração atual (mmaaaa) - opcional, para validação
        
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
        resultado = _processar_linha_1300(linha, per_apu_escrit=per_apu_escrit)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
