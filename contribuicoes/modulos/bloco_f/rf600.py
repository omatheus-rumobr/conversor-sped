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


def _processar_linha_f600(linha, dt_fin_0000=None):
    """
    Processa uma única linha do registro F600 e retorna um dicionário.
    
    Formato:
      |F600|IND_NAT_RET|DT_RET|VL_BC_RET|VL_RET|COD_REC|IND_NAT_REC|CNPJ|VL_RET_PIS|VL_RET_COFINS|IND_DEC|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "F600"
    - IND_NAT_RET: obrigatório, valores válidos [01, 02, 03, 04, 05, 99]
    - DT_RET: obrigatório, formato ddmmaaaa
      - Deve ser menor ou igual à DT_FIN do arquivo (validação opcional)
    - VL_BC_RET: obrigatório, numérico com 4 decimais
    - VL_RET: obrigatório, numérico com 2 decimais
      - Deve ser = VL_RET_PIS + VL_RET_COFINS (validação)
    - COD_REC: opcional, 4 caracteres
    - IND_NAT_REC: opcional, valores válidos [0, 1]
    - CNPJ: obrigatório, 14 dígitos com validação de DV
    - VL_RET_PIS: obrigatório, numérico com 2 decimais
    - VL_RET_COFINS: obrigatório, numérico com 2 decimais
    - IND_DEC: obrigatório, valores válidos [0, 1]
    
    Nota: Neste registro devem ser informados pela pessoa jurídica beneficiária da retenção/recolhimento
    os valores da contribuição para o PIS/pasep e da Cofins retidos na Fonte, decorrentes de diversas
    hipóteses de retenção previstas na legislação tributária.
    
    Args:
        linha: String com uma linha do SPED
        dt_fin_0000: Data final do período (opcional, para validação de DT_RET)
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |F600|...|)
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
    if reg != "F600":
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
    ind_nat_ret = obter_campo(1)
    dt_ret = obter_campo(2)
    vl_bc_ret = obter_campo(3)
    vl_ret = obter_campo(4)
    cod_rec = obter_campo(5)
    ind_nat_rec = obter_campo(6)
    cnpj = obter_campo(7)
    vl_ret_pis = obter_campo(8)
    vl_ret_cofins = obter_campo(9)
    ind_dec = obter_campo(10)
    
    # Validações básicas dos campos obrigatórios
    
    # IND_NAT_RET: obrigatório, valores válidos [01, 02, 03, 04, 05, 99]
    ind_nat_ret_validos = ["01", "02", "03", "04", "05", "99"]
    if not ind_nat_ret or ind_nat_ret not in ind_nat_ret_validos:
        return None
    
    # DT_RET: obrigatório, formato ddmmaaaa
    ok_dt, dt_obj = _validar_data(dt_ret)
    if not ok_dt:
        return None
    
    # Validação opcional: DT_RET deve ser menor ou igual à DT_FIN (se fornecido)
    if dt_fin_0000:
        if dt_obj > dt_fin_0000:
            return None
    
    # VL_BC_RET: obrigatório, numérico com 4 decimais
    ok1, val1, _ = validar_valor_numerico(vl_bc_ret, decimais=4, obrigatorio=True, positivo=True)
    if not ok1:
        return None
    
    # VL_RET: obrigatório, numérico com 2 decimais
    ok2, val2, _ = validar_valor_numerico(vl_ret, decimais=2, obrigatorio=True, positivo=True)
    if not ok2:
        return None
    
    # COD_REC: opcional, 4 caracteres
    if cod_rec and len(cod_rec) > 4:
        return None
    
    # IND_NAT_REC: opcional, valores válidos [0, 1]
    ind_nat_rec_validos = ["0", "1"]
    if ind_nat_rec and ind_nat_rec not in ind_nat_rec_validos:
        return None
    
    # CNPJ: obrigatório, 14 dígitos com validação de DV
    # Remove formatação para validar
    cnpj_limpo = cnpj.replace(".", "").replace("/", "").replace("-", "").replace(" ", "")
    if not cnpj or len(cnpj_limpo) != 14 or not _validar_cnpj(cnpj):
        return None
    
    # VL_RET_PIS: obrigatório, numérico com 2 decimais
    ok3, val3, _ = validar_valor_numerico(vl_ret_pis, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok3:
        return None
    
    # VL_RET_COFINS: obrigatório, numérico com 2 decimais
    ok4, val4, _ = validar_valor_numerico(vl_ret_cofins, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok4:
        return None
    
    # Validação: VL_RET deve ser = VL_RET_PIS + VL_RET_COFINS
    vl_ret_calculado = round(val3 + val4, 2)
    # Permite pequena diferença devido a arredondamentos (tolerância de 0.01)
    if abs(val2 - vl_ret_calculado) > 0.01:
        return None
    
    # IND_DEC: obrigatório, valores válidos [0, 1]
    ind_dec_validos = ["0", "1"]
    if not ind_dec or ind_dec not in ind_dec_validos:
        return None
    
    # Função auxiliar para formatar valores monetários
    def fmt_valor(v):
        if v is None:
            return ""
        return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    # Função auxiliar para formatar valores com 4 decimais
    def fmt_valor_4dec(v):
        if v is None:
            return ""
        return f"{v:,.4f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    # Função auxiliar para formatar CNPJ
    def fmt_cnpj(cnpj_str):
        if not cnpj_str:
            return ""
        cnpj_limpo = cnpj_str.replace(".", "").replace("/", "").replace("-", "").replace(" ", "")
        if len(cnpj_limpo) == 14:
            # Formata CNPJ: 00.000.000/0000-00
            return f"{cnpj_limpo[:2]}.{cnpj_limpo[2:5]}.{cnpj_limpo[5:8]}/{cnpj_limpo[8:12]}-{cnpj_limpo[12:]}"
        return cnpj_str
    
    # Função auxiliar para formatar data
    def fmt_data(data_str):
        if not data_str or len(data_str) != 8:
            return ""
        return f"{data_str[:2]}/{data_str[2:4]}/{data_str[4:]}"
    
    # Descrições dos campos
    descricoes_ind_nat_ret = {
        "01": "Retenção por Órgãos, Autarquias e Fundações Federais",
        "02": "Retenção por outras Entidades da Administração Pública Federal",
        "03": "Retenção por Pessoas Jurídicas de Direito Privado",
        "04": "Recolhimento por Sociedade Cooperativa",
        "05": "Retenção por Fabricante de Máquinas e Veículos",
        "99": "Outras Retenções"
    }
    
    descricoes_ind_nat_rec = {
        "0": "Receita de Natureza Não Cumulativa",
        "1": "Receita de Natureza Cumulativa"
    }
    
    descricoes_ind_dec = {
        "0": "Beneficiária da Retenção / Recolhimento",
        "1": "Responsável pelo Recolhimento"
    }
    
    # Monta o resultado
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
        "DT_RET": {
            "titulo": "Data da Retenção",
            "valor": dt_ret,
            "valor_formatado": fmt_data(dt_ret)
        },
        "VL_BC_RET": {
            "titulo": "Base de calculo da retenção ou do recolhimento (sociedade cooperativa)",
            "valor": vl_bc_ret,
            "valor_formatado": fmt_valor_4dec(val1)
        },
        "VL_RET": {
            "titulo": "Valor Total Retido na Fonte / Recolhido (sociedade cooperativa)",
            "valor": vl_ret,
            "valor_formatado": fmt_valor(val2)
        },
        "COD_REC": {
            "titulo": "Código da Receita",
            "valor": cod_rec
        },
        "IND_NAT_REC": {
            "titulo": "Indicador da Natureza da Receita",
            "valor": ind_nat_rec,
            "descricao": descricoes_ind_nat_rec.get(ind_nat_rec, "") if ind_nat_rec else ""
        },
        "CNPJ": {
            "titulo": "CNPJ referente a: - Fonte Pagadora Responsável pela Retenção / Recolhimento (no caso de o registro ser escriturado pela pessoa jurídica beneficiária da retenção); ou - Pessoa Jurídica Beneficiária da Retenção / Recolhimento (no caso de o registro ser escriturado pela pessoa jurídica responsável pela retenção)",
            "valor": cnpj,
            "valor_formatado": fmt_cnpj(cnpj)
        },
        "VL_RET_PIS": {
            "titulo": "Valor Retido na Fonte – Parcela Referente ao PIS/Pasep",
            "valor": vl_ret_pis,
            "valor_formatado": fmt_valor(val3)
        },
        "VL_RET_COFINS": {
            "titulo": "Valor Retido na Fonte – Parcela Referente a COFINS",
            "valor": vl_ret_cofins,
            "valor_formatado": fmt_valor(val4)
        },
        "IND_DEC": {
            "titulo": "Indicador da condição da pessoa jurídica declarante",
            "valor": ind_dec,
            "descricao": descricoes_ind_dec.get(ind_dec, "")
        }
    }
    
    return resultado


def validar_f600(linhas, dt_fin_0000=None):
    """
    Valida uma ou mais linhas do registro F600 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |F600|IND_NAT_RET|DT_RET|VL_BC_RET|VL_RET|COD_REC|IND_NAT_REC|CNPJ|VL_RET_PIS|VL_RET_COFINS|IND_DEC|
        dt_fin_0000: Data final do período (opcional, para validação de DT_RET)
        
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
        resultado = _processar_linha_f600(linha, dt_fin_0000)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
