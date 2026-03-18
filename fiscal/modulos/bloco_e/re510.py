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


def _processar_linha_e510(linha):
    """
    Processa uma única linha do registro E510 e retorna um dicionário.

    Formato:
      |E510|CFOP|CST_IPI|VL_CONT_IPI|VL_BC_IPI|VL_IPI|

    Regras (manual 3.1.8):
    - REG deve ser "E510"
    - CFOP: obrigatório, 4 dígitos numéricos
    - CST_IPI: obrigatório, 2 caracteres, valores válidos conforme tabela
    - VL_CONT_IPI, VL_BC_IPI, VL_IPI: obrigatórios, numéricos com 2 decimais, não negativos

    Args:
        linha: String com uma linha do SPED

    Returns:
        dict: Dicionário com os campos validados contendo título e valor, ou None se inválido
    """
    if not linha or not isinstance(linha, str):
        return None

    linha = linha.strip()
    if not linha:
        return None

    partes = linha.split("|")
    if partes and not partes[0]:
        partes = partes[1:]
    if partes and not partes[-1]:
        partes = partes[:-1]

    if len(partes) < 1:
        return None

    reg = partes[0].strip() if partes else ""
    if reg != "E510":
        return None

    def obter_campo(indice):
        if indice < len(partes):
            valor = partes[indice].strip()
            if valor == "-":
                return ""
            return valor if valor else ""
        return ""

    cfop = obter_campo(1)
    cst_ipi = obter_campo(2)
    vl_cont_ipi = obter_campo(3)
    vl_bc_ipi = obter_campo(4)
    vl_ipi = obter_campo(5)

    # CFOP: obrigatório, 4 dígitos numéricos
    if not cfop or not cfop.isdigit() or len(cfop) != 4:
        return None

    # CST_IPI: obrigatório, 2 caracteres, valores válidos conforme tabela
    cst_ipi_validos = ["00", "01", "02", "03", "04", "05", "49", "50", "51", "52", "53", "54", "55", "99"]
    if not cst_ipi or len(cst_ipi) != 2 or cst_ipi not in cst_ipi_validos:
        return None

    # VL_CONT_IPI: obrigatório, numérico com 2 decimais, não negativo
    vl_cont_ipi_ok, vl_cont_ipi_float, _ = validar_valor_numerico(vl_cont_ipi, decimais=2, obrigatorio=True, nao_negativo=True)
    if not vl_cont_ipi_ok:
        return None

    # VL_BC_IPI: obrigatório, numérico com 2 decimais, não negativo
    vl_bc_ipi_ok, vl_bc_ipi_float, _ = validar_valor_numerico(vl_bc_ipi, decimais=2, obrigatorio=True, nao_negativo=True)
    if not vl_bc_ipi_ok:
        return None

    # VL_IPI: obrigatório, numérico com 2 decimais, não negativo
    vl_ipi_ok, vl_ipi_float, _ = validar_valor_numerico(vl_ipi, decimais=2, obrigatorio=True, nao_negativo=True)
    if not vl_ipi_ok:
        return None

    def fmt_moeda(v):
        return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    descricao_cst_ipi = {
        "00": "Entrada com recuperação de crédito",
        "01": "Entrada tributada com alíquota zero",
        "02": "Entrada isenta",
        "03": "Entrada não-tributada",
        "04": "Entrada imune",
        "05": "Entrada com suspensão",
        "49": "Outras entradas",
        "50": "Saída tributada",
        "51": "Saída tributada com alíquota zero",
        "52": "Saída isenta",
        "53": "Saída não-tributada",
        "54": "Saída imune",
        "55": "Saída com suspensão",
        "99": "Outras saídas",
    }.get(cst_ipi, "")

    return {
        "REG": {"titulo": "Registro", "valor": reg},
        "CFOP": {
            "titulo": "Código Fiscal de Operação e Prestação do agrupamento de itens",
            "valor": cfop,
        },
        "CST_IPI": {
            "titulo": "Código da Situação Tributária referente ao IPI, conforme a Tabela indicada no item 4.3.2",
            "valor": cst_ipi,
            "descricao": descricao_cst_ipi,
        },
        "VL_CONT_IPI": {
            "titulo": 'Parcela correspondente ao "Valor Contábil" referente ao CFOP e ao Código de Tributação do IPI',
            "valor": vl_cont_ipi,
            "valor_formatado": fmt_moeda(vl_cont_ipi_float),
        },
        "VL_BC_IPI": {
            "titulo": 'Parcela correspondente ao "Valor da base de cálculo do IPI" referente ao CFOP e ao Código de Tributação do IPI, para operações tributadas',
            "valor": vl_bc_ipi,
            "valor_formatado": fmt_moeda(vl_bc_ipi_float),
        },
        "VL_IPI": {
            "titulo": 'Parcela correspondente ao "Valor do IPI" referente ao CFOP e ao Código de Tributação do IPI, para operações tributadas',
            "valor": vl_ipi,
            "valor_formatado": fmt_moeda(vl_ipi_float),
        },
    }


def validar_e510_fiscal(linhas):
    """
    Valida uma ou mais linhas do registro E510 do SPED EFD Fiscal.

    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |E510|CFOP|CST_IPI|VL_CONT_IPI|VL_BC_IPI|VL_IPI|

    Returns:
        String JSON com array de objetos contendo os campos validados.
        Retorna "[]" se nenhuma linha for válida.
    """
    if not linhas:
        return json.dumps([], ensure_ascii=False, indent=2)

    if isinstance(linhas, str):
        if "\n" in linhas:
            linhas_para_processar = [l.strip() for l in linhas.split("\n") if l.strip()]
        else:
            linhas_para_processar = [linhas.strip()] if linhas.strip() else []
    elif isinstance(linhas, list):
        linhas_para_processar = [l.strip() if isinstance(l, str) else str(l).strip() for l in linhas if l]
    else:
        linhas_para_processar = [str(linhas).strip()] if str(linhas).strip() else []

    resultados = []
    for l in linhas_para_processar:
        r = _processar_linha_e510(l)
        if r is not None:
            resultados.append(r)

    return json.dumps(resultados, ensure_ascii=False, indent=2)
