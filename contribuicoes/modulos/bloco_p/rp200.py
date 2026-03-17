import json


def _validar_periodo_referencia(periodo_str):
    """
    Valida se o período de referência está no formato MMAAAA (6 dígitos).
    
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


def _processar_linha_p200(linha):
    """
    Processa uma única linha do registro P200 e retorna um dicionário.
    
    Formato:
      |P200|PER_REF|VL_TOT_CONT_APU|VL_TOT_AJ_REDUC|VL_TOT_AJ_ACRES|VL_TOT_CONT_DEV|COD_REC|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "P200"
    - PER_REF: obrigatório, período de referência da escrituração (MMAAAA) - 6 dígitos
    - VL_TOT_CONT_APU: obrigatório, valor total apurado da Contribuição Previdenciária sobre a Receita Bruta (numérico, 2 decimais)
    - VL_TOT_AJ_REDUC: opcional, valor total de "Ajustes de redução" (numérico, 2 decimais)
    - VL_TOT_AJ_ACRES: opcional, valor total de "Ajustes de acréscimo" (numérico, 2 decimais)
    - VL_TOT_CONT_DEV: obrigatório, valor total da Contribuição Previdenciária sobre a Receita Bruta a recolher (numérico, 2 decimais)
      - Validação: VL_TOT_CONT_DEV = VL_TOT_CONT_APU - VL_TOT_AJ_REDUC + VL_TOT_AJ_ACRES
    - COD_REC: obrigatório, código de receita (6 caracteres)
      - Valores válidos: ["298501", "298504", "298506", "299101"]
    
    Nota: Registro de consolidação da contribuição previdenciária incidente sobre o valor da receita bruta,
    devida pela empresa no período, correspondente ao somatório da contribuição sobre a receita bruta mensal
    de cada estabelecimento, apurada no Registro "P100".
    
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
    # Remove primeiro e último se vazios (formato padrão SPED: |P200|...|)
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
    if reg != "P200":
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
    
    # Extrai todos os campos (7 campos no total)
    per_ref = obter_campo(1)
    vl_tot_cont_apu = obter_campo(2)
    vl_tot_aj_reduc = obter_campo(3)
    vl_tot_aj_acres = obter_campo(4)
    vl_tot_cont_dev = obter_campo(5)
    cod_rec = obter_campo(6)
    
    # Validações básicas dos campos obrigatórios
    
    # PER_REF: obrigatório, período de referência (MMAAAA) - 6 dígitos
    ok_periodo, periodo_tuple = _validar_periodo_referencia(per_ref)
    if not ok_periodo:
        return None
    
    # VL_TOT_CONT_APU: obrigatório, numérico com 2 decimais
    ok1, val1, _ = validar_valor_numerico(vl_tot_cont_apu, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok1:
        return None
    
    # VL_TOT_AJ_REDUC: opcional, numérico com 2 decimais
    ok2, val2, _ = validar_valor_numerico(vl_tot_aj_reduc, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok2:
        return None
    
    # VL_TOT_AJ_ACRES: opcional, numérico com 2 decimais
    ok3, val3, _ = validar_valor_numerico(vl_tot_aj_acres, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok3:
        return None
    
    # VL_TOT_CONT_DEV: obrigatório, numérico com 2 decimais
    ok4, val4, _ = validar_valor_numerico(vl_tot_cont_dev, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok4:
        return None
    
    # Validação: VL_TOT_CONT_DEV = VL_TOT_CONT_APU - VL_TOT_AJ_REDUC + VL_TOT_AJ_ACRES
    vl_tot_cont_dev_calculado = round(val1 - val2 + val3, 2)
    # Permite pequena diferença devido a arredondamentos (tolerância de 0.01)
    if abs(val4 - vl_tot_cont_dev_calculado) > 0.01:
        return None
    
    # COD_REC: obrigatório, código de receita (6 caracteres)
    cod_rec_validos = ["298501", "298504", "298506", "299101"]
    if not cod_rec or len(cod_rec) != 6 or cod_rec not in cod_rec_validos:
        return None
    
    # Função auxiliar para formatar valores monetários
    def fmt_valor(v):
        if v is None:
            return ""
        return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    # Função auxiliar para formatar período de referência
    def fmt_periodo(periodo_str):
        if not periodo_str or len(periodo_str) != 6:
            return ""
        return f"{periodo_str[:2]}/{periodo_str[2:]}"
    
    # Descrições dos campos
    descricoes_cod_rec = {
        "298501": "Art. 7º da Lei 12.546/2011",
        "298504": "Art. 7º da Lei 12.546/2011: Empresa do setor de construção – Inscrição no CEI até 30/11/2015",
        "298506": "Art. 7º da Lei 12.546/2011: Empresa do setor de construção – Inscrição no CEI a partir de 01/12/2015",
        "299101": "Art. 8º da Lei 12.546/2011"
    }
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "PER_REF": {
            "titulo": "Período de referencia da escrituração (MMAAAA)",
            "valor": per_ref,
            "valor_formatado": fmt_periodo(per_ref)
        },
        "VL_TOT_CONT_APU": {
            "titulo": "Valor total apurado da Contribuição Previdenciária sobre a Receita Bruta (Somatório do Campo 10 \"VL_CONT_APU\", do(s) Registro(s) P100)",
            "valor": vl_tot_cont_apu,
            "valor_formatado": fmt_valor(val1)
        },
        "VL_TOT_AJ_REDUC": {
            "titulo": "Valor total de \"Ajustes de redução\" (Registro P210, Campo 03, quando Campo 02 = \"0\")",
            "valor": vl_tot_aj_reduc,
            "valor_formatado": fmt_valor(val2) if vl_tot_aj_reduc else ""
        },
        "VL_TOT_AJ_ACRES": {
            "titulo": "Valor total de \"Ajustes de acréscimo\" (Registro P210, Campo 03, quando Campo 02 = \"1\")",
            "valor": vl_tot_aj_acres,
            "valor_formatado": fmt_valor(val3) if vl_tot_aj_acres else ""
        },
        "VL_TOT_CONT_DEV": {
            "titulo": "Valor total da Contribuição Previdenciária sobre a Receita Bruta a recolher (Campo 03 – Campo 04 + Campo 05)",
            "valor": vl_tot_cont_dev,
            "valor_formatado": fmt_valor(val4)
        },
        "COD_REC": {
            "titulo": "Código de Receita referente à Contribuição Previdenciária, conforme informado em DCTF",
            "valor": cod_rec,
            "descricao": descricoes_cod_rec.get(cod_rec, "")
        }
    }
    
    return resultado


def validar_p200(linhas):
    """
    Valida uma ou mais linhas do registro P200 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |P200|PER_REF|VL_TOT_CONT_APU|VL_TOT_AJ_REDUC|VL_TOT_AJ_ACRES|VL_TOT_CONT_DEV|COD_REC|
        
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
        resultado = _processar_linha_p200(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
