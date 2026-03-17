import json


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


def _processar_linha_f560(linha):
    """
    Processa uma única linha do registro F560 e retorna um dicionário.
    
    Formato:
      |F560|VL_REC_COMP|CST_PIS|VL_DESC_PIS|QUANT_BC_PIS|ALIQ_PIS_QUANT|VL_PIS|CST_COFINS|VL_DESC_COFINS|QUANT_BC_COFINS|ALIQ_COFINS_QUANT|VL_COFINS|COD_MOD|CFOP|COD_CTA|INFO_COMPL|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "F560"
    - VL_REC_COMP: obrigatório, numérico com 2 decimais
    - CST_PIS: obrigatório, valores válidos [03, 05, 06, 07, 08, 09, 49, 99]
    - VL_DESC_PIS: opcional, numérico com 2 decimais
    - QUANT_BC_PIS: opcional, numérico com 3 decimais (base de cálculo em quantidade)
    - ALIQ_PIS_QUANT: opcional, numérico com 8 dígitos e 4 decimais (alíquota em reais)
    - VL_PIS: opcional, numérico com 2 decimais
      - Deve corresponder a QUANT_BC_PIS * ALIQ_PIS_QUANT (validação, se ambos preenchidos)
    - CST_COFINS: obrigatório, valores válidos [03, 05, 06, 07, 08, 09, 49, 99]
    - VL_DESC_COFINS: opcional, numérico com 2 decimais
    - QUANT_BC_COFINS: opcional, numérico com 3 decimais (base de cálculo em quantidade)
    - ALIQ_COFINS_QUANT: opcional, numérico com 8 dígitos e 4 decimais (alíquota em reais)
    - VL_COFINS: opcional, numérico com 2 decimais
      - Deve corresponder a QUANT_BC_COFINS * ALIQ_COFINS_QUANT (validação, se ambos preenchidos)
    - COD_MOD: opcional, 2 caracteres
    - CFOP: opcional, 4 dígitos
    - COD_CTA: opcional, máximo 255 caracteres
    - INFO_COMPL: opcional, sem limite de tamanho
    
    Nota: Registro específico para a pessoa jurídica submetida ao regime de apuração com base no lucro
    presumido, optante pela apuração da contribuição para o PIS/Pasep e da Cofins pelo regime de competência,
    que apure as contribuições por unidade de medida de produto (alíquota em reais).
    
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
    # Remove primeiro e último se vazios (formato padrão SPED: |F560|...|)
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
    if reg != "F560":
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
    
    # Extrai todos os campos (16 campos no total)
    vl_rec_comp = obter_campo(1)
    cst_pis = obter_campo(2)
    vl_desc_pis = obter_campo(3)
    quant_bc_pis = obter_campo(4)
    aliq_pis_quant = obter_campo(5)
    vl_pis = obter_campo(6)
    cst_cofins = obter_campo(7)
    vl_desc_cofins = obter_campo(8)
    quant_bc_cofins = obter_campo(9)
    aliq_cofins_quant = obter_campo(10)
    vl_cofins = obter_campo(11)
    cod_mod = obter_campo(12)
    cfop = obter_campo(13)
    cod_cta = obter_campo(14)
    info_compl = obter_campo(15)
    
    # Validações básicas dos campos obrigatórios
    
    # VL_REC_COMP: obrigatório, numérico com 2 decimais
    ok1, val1, _ = validar_valor_numerico(vl_rec_comp, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok1:
        return None
    
    # CST_PIS: obrigatório, valores válidos [03, 05, 06, 07, 08, 09, 49, 99]
    cst_pis_validos = ["03", "05", "06", "07", "08", "09", "49", "99"]
    if not cst_pis or len(cst_pis) != 2 or cst_pis not in cst_pis_validos:
        return None
    
    # VL_DESC_PIS: opcional, numérico com 2 decimais
    ok2, val2, _ = validar_valor_numerico(vl_desc_pis, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok2:
        return None
    
    # QUANT_BC_PIS: opcional, numérico com 3 decimais (base de cálculo em quantidade)
    ok3, val3, _ = validar_valor_numerico(quant_bc_pis, decimais=3, obrigatorio=False, nao_negativo=True)
    if not ok3:
        return None
    
    # ALIQ_PIS_QUANT: opcional, numérico com 8 dígitos e 4 decimais (alíquota em reais)
    # Normaliza vírgula para ponto
    aliq_pis_quant_normalizada = aliq_pis_quant.replace(",", ".") if aliq_pis_quant else ""
    ok4, val4, _ = validar_valor_numerico(aliq_pis_quant_normalizada, decimais=4, obrigatorio=False, nao_negativo=True)
    if not ok4:
        return None
    # Valida se tem no máximo 8 dígitos na parte inteira
    if aliq_pis_quant_normalizada:
        partes_aliq = aliq_pis_quant_normalizada.split(".")
        if len(partes_aliq[0]) > 8:
            return None
    
    # VL_PIS: opcional, numérico com 2 decimais
    ok5, val5, _ = validar_valor_numerico(vl_pis, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok5:
        return None
    
    # Validação: VL_PIS deve corresponder a QUANT_BC_PIS * ALIQ_PIS_QUANT (se ambos preenchidos)
    # Nota: não divide por 100 porque a alíquota já está em reais, não em percentual
    if quant_bc_pis and aliq_pis_quant_normalizada and vl_pis:
        vl_pis_calculado = round(val3 * val4, 2)
        # Permite pequena diferença devido a arredondamentos (tolerância de 0.01)
        if abs(val5 - vl_pis_calculado) > 0.01:
            return None
    
    # CST_COFINS: obrigatório, valores válidos [03, 05, 06, 07, 08, 09, 49, 99]
    cst_cofins_validos = ["03", "05", "06", "07", "08", "09", "49", "99"]
    if not cst_cofins or len(cst_cofins) != 2 or cst_cofins not in cst_cofins_validos:
        return None
    
    # VL_DESC_COFINS: opcional, numérico com 2 decimais
    ok6, val6, _ = validar_valor_numerico(vl_desc_cofins, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok6:
        return None
    
    # QUANT_BC_COFINS: opcional, numérico com 3 decimais (base de cálculo em quantidade)
    ok7, val7, _ = validar_valor_numerico(quant_bc_cofins, decimais=3, obrigatorio=False, nao_negativo=True)
    if not ok7:
        return None
    
    # ALIQ_COFINS_QUANT: opcional, numérico com 8 dígitos e 4 decimais (alíquota em reais)
    # Normaliza vírgula para ponto
    aliq_cofins_quant_normalizada = aliq_cofins_quant.replace(",", ".") if aliq_cofins_quant else ""
    ok8, val8, _ = validar_valor_numerico(aliq_cofins_quant_normalizada, decimais=4, obrigatorio=False, nao_negativo=True)
    if not ok8:
        return None
    # Valida se tem no máximo 8 dígitos na parte inteira
    if aliq_cofins_quant_normalizada:
        partes_aliq = aliq_cofins_quant_normalizada.split(".")
        if len(partes_aliq[0]) > 8:
            return None
    
    # VL_COFINS: opcional, numérico com 2 decimais
    ok9, val9, _ = validar_valor_numerico(vl_cofins, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok9:
        return None
    
    # Validação: VL_COFINS deve corresponder a QUANT_BC_COFINS * ALIQ_COFINS_QUANT (se ambos preenchidos)
    # Nota: não divide por 100 porque a alíquota já está em reais, não em percentual
    if quant_bc_cofins and aliq_cofins_quant_normalizada and vl_cofins:
        vl_cofins_calculado = round(val7 * val8, 2)
        # Permite pequena diferença devido a arredondamentos (tolerância de 0.01)
        if abs(val9 - vl_cofins_calculado) > 0.01:
            return None
    
    # COD_MOD: opcional, 2 caracteres
    if cod_mod and len(cod_mod) > 2:
        return None
    
    # CFOP: opcional, 4 dígitos
    if cfop:
        if not cfop.isdigit() or len(cfop) != 4:
            return None
    
    # COD_CTA: opcional, máximo 255 caracteres
    if cod_cta and len(cod_cta) > 255:
        return None
    
    # INFO_COMPL: opcional, sem limite de tamanho (não precisa validar)
    
    # Função auxiliar para formatar valores monetários
    def fmt_valor(v):
        if v is None:
            return ""
        return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    # Função auxiliar para formatar quantidade (3 decimais)
    def fmt_quantidade(v):
        if v is None:
            return ""
        return f"{v:,.3f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    # Função auxiliar para formatar alíquota em reais (4 decimais)
    def fmt_aliq_reais(v):
        if v is None:
            return ""
        return f"{v:,.4f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    # Descrições dos campos
    descricoes_cst_pis = {
        "03": "Operação Tributável com Alíquota por Unidade de Medida de Produto",
        "05": "Operação Tributável por Substituição Tributária",
        "06": "Operação Tributável a Alíquota Zero",
        "07": "Operação Isenta da Contribuição",
        "08": "Operação sem Incidência da Contribuição",
        "09": "Operação com Suspensão da Contribuição",
        "49": "Outras Operações de Saída",
        "99": "Outras Operações"
    }
    
    descricoes_cst_cofins = {
        "03": "Operação Tributável com Alíquota por Unidade de Medida de Produto",
        "05": "Operação Tributável por Substituição Tributária",
        "06": "Operação Tributável a Alíquota Zero",
        "07": "Operação Isenta da Contribuição",
        "08": "Operação sem Incidência da Contribuição",
        "09": "Operação com Suspensão da Contribuição",
        "49": "Outras Operações de Saída",
        "99": "Outras Operações"
    }
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "VL_REC_COMP": {
            "titulo": "Valor total da receita auferida, referente à combinação de CST e Alíquota",
            "valor": vl_rec_comp,
            "valor_formatado": fmt_valor(val1)
        },
        "CST_PIS": {
            "titulo": "Código da Situação Tributária referente ao PIS/PASEP",
            "valor": cst_pis,
            "descricao": descricoes_cst_pis.get(cst_pis, "")
        },
        "VL_DESC_PIS": {
            "titulo": "Valor do desconto / exclusão",
            "valor": vl_desc_pis,
            "valor_formatado": fmt_valor(val2) if vl_desc_pis else ""
        },
        "QUANT_BC_PIS": {
            "titulo": "Base de cálculo em quantidade - PIS/PASEP",
            "valor": quant_bc_pis,
            "valor_formatado": fmt_quantidade(val3) if quant_bc_pis else ""
        },
        "ALIQ_PIS_QUANT": {
            "titulo": "Alíquota do PIS/PASEP (em reais)",
            "valor": aliq_pis_quant,
            "valor_formatado": fmt_aliq_reais(val4) if aliq_pis_quant else ""
        },
        "VL_PIS": {
            "titulo": "Valor do PIS/PASEP",
            "valor": vl_pis,
            "valor_formatado": fmt_valor(val5) if vl_pis else ""
        },
        "CST_COFINS": {
            "titulo": "Código da Situação Tributária referente a COFINS",
            "valor": cst_cofins,
            "descricao": descricoes_cst_cofins.get(cst_cofins, "")
        },
        "VL_DESC_COFINS": {
            "titulo": "Valor do desconto / exclusão",
            "valor": vl_desc_cofins,
            "valor_formatado": fmt_valor(val6) if vl_desc_cofins else ""
        },
        "QUANT_BC_COFINS": {
            "titulo": "Base de cálculo em quantidade – COFINS",
            "valor": quant_bc_cofins,
            "valor_formatado": fmt_quantidade(val7) if quant_bc_cofins else ""
        },
        "ALIQ_COFINS_QUANT": {
            "titulo": "Alíquota da COFINS (em reais)",
            "valor": aliq_cofins_quant,
            "valor_formatado": fmt_aliq_reais(val8) if aliq_cofins_quant else ""
        },
        "VL_COFINS": {
            "titulo": "Valor da COFINS",
            "valor": vl_cofins,
            "valor_formatado": fmt_valor(val9) if vl_cofins else ""
        },
        "COD_MOD": {
            "titulo": "Código do modelo do documento fiscal conforme a Tabela 4.1.1",
            "valor": cod_mod
        },
        "CFOP": {
            "titulo": "Código fiscal de operação e prestação",
            "valor": cfop
        },
        "COD_CTA": {
            "titulo": "Código da conta analítica contábil debitada / creditada",
            "valor": cod_cta
        },
        "INFO_COMPL": {
            "titulo": "Informação complementar",
            "valor": info_compl
        }
    }
    
    return resultado


def validar_f560(linhas):
    """
    Valida uma ou mais linhas do registro F560 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |F560|VL_REC_COMP|CST_PIS|VL_DESC_PIS|QUANT_BC_PIS|ALIQ_PIS_QUANT|VL_PIS|CST_COFINS|VL_DESC_COFINS|QUANT_BC_COFINS|ALIQ_COFINS_QUANT|VL_COFINS|COD_MOD|CFOP|COD_CTA|INFO_COMPL|
        
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
        resultado = _processar_linha_f560(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
