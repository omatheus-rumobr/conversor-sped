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


def _validar_cpf(cpf):
    """
    Valida o formato básico do CPF (11 dígitos).
    Valida também o dígito verificador (DV).
    """
    if not cpf:
        return False
    
    # Remove formatação
    cpf_limpo = cpf.replace(".", "").replace("-", "").replace(" ", "")
    
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
    Valida se é um CPF (11 dígitos) ou CNPJ (14 dígitos) válido.
    """
    if not cpf_cnpj:
        return False
    
    # Remove formatação
    cpf_cnpj_limpo = cpf_cnpj.replace(".", "").replace("/", "").replace("-", "").replace(" ", "")
    
    if len(cpf_cnpj_limpo) == 11:
        return _validar_cpf(cpf_cnpj)
    elif len(cpf_cnpj_limpo) == 14:
        return _validar_cnpj(cpf_cnpj)
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


def _processar_linha_f200(linha, dt_ini_0000=None, dt_fin_0000=None):
    """
    Processa uma única linha do registro F200 e retorna um dicionário.
    
    Formato:
      |F200|IND_OPER|UNID_IMOB|IDENT_EMP|DESC_UNID_IMOB|NUM_CONT|CPF_CNPJ_ADQU|DT_OPER|VL_TOT_VEND|VL_REC_ACUM|VL_TOT_REC|CST_PIS|VL_BC_PIS|ALIQ_PIS|VL_PIS|CST_COFINS|VL_BC_COFINS|ALIQ_COFINS|VL_COFINS|PERC_REC_RECEB|IND_NAT_EMP|INF_COMP|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "F200"
    - IND_OPER: obrigatório, valores válidos [01, 02, 03, 04, 05]
    - UNID_IMOB: obrigatório, valores válidos [01, 02, 03, 04, 05, 06]
    - IDENT_EMP: obrigatório, sem limite de tamanho
    - DESC_UNID_IMOB: opcional, máximo 90 caracteres
    - NUM_CONT: opcional, máximo 90 caracteres
    - CPF_CNPJ_ADQU: obrigatório, 14 caracteres (CPF ou CNPJ)
    - DT_OPER: obrigatório, formato ddmmaaaa
    - VL_TOT_VEND: obrigatório, numérico com 2 decimais
    - VL_REC_ACUM: opcional, numérico com 2 decimais
    - VL_TOT_REC: obrigatório, numérico com 2 decimais
    - CST_PIS: obrigatório, 2 dígitos
    - VL_BC_PIS: opcional, numérico com 2 decimais
    - ALIQ_PIS: opcional, numérico com 8 dígitos e 4 decimais (percentual)
    - VL_PIS: opcional, numérico com 2 decimais
      - Deve corresponder a VL_BC_PIS * ALIQ_PIS / 100 (validação)
    - CST_COFINS: obrigatório, 2 dígitos
    - VL_BC_COFINS: opcional, numérico com 2 decimais
    - ALIQ_COFINS: opcional, numérico com 8 dígitos e 4 decimais (percentual)
    - VL_COFINS: opcional, numérico com 2 decimais
      - Deve corresponder a VL_BC_COFINS * ALIQ_COFINS / 100 (validação)
    - PERC_REC_RECEB: opcional, numérico com 6 dígitos e 2 decimais (percentual)
      - Deve ser = (VL_REC_ACUM + VL_TOT_REC) / VL_TOT_VEND (validação)
    - IND_NAT_EMP: opcional, valores válidos [1, 2, 3, 4]
    - INF_COMP: opcional, máximo 90 caracteres
    
    Nota: Este registro deve ser preenchido apenas pela pessoa jurídica que auferiu receita da atividade
    imobiliária, decorrente da aquisição de imóvel para venda, promoção de empreendimento de desmembramento
    ou loteamento de terrenos, incorporação imobiliária ou construção de prédio destinado à venda.
    
    Args:
        linha: String com uma linha do SPED
        dt_ini_0000: Data inicial do período (opcional, para validação de DT_OPER)
        dt_fin_0000: Data final do período (opcional, para validação de DT_OPER)
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |F200|...|)
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
    if reg != "F200":
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
    
    # Extrai todos os campos (22 campos no total)
    ind_oper = obter_campo(1)
    unid_imob = obter_campo(2)
    ident_emp = obter_campo(3)
    desc_unid_imob = obter_campo(4)
    num_cont = obter_campo(5)
    cpf_cnpj_adqu = obter_campo(6)
    dt_oper = obter_campo(7)
    vl_tot_vend = obter_campo(8)
    vl_rec_acum = obter_campo(9)
    vl_tot_rec = obter_campo(10)
    cst_pis = obter_campo(11)
    vl_bc_pis = obter_campo(12)
    aliq_pis = obter_campo(13)
    vl_pis = obter_campo(14)
    cst_cofins = obter_campo(15)
    vl_bc_cofins = obter_campo(16)
    aliq_cofins = obter_campo(17)
    vl_cofins = obter_campo(18)
    perc_rec_receb = obter_campo(19)
    ind_nat_emp = obter_campo(20)
    inf_comp = obter_campo(21)
    
    # Validações básicas dos campos obrigatórios
    
    # IND_OPER: obrigatório, valores válidos [01, 02, 03, 04, 05]
    ind_oper_validos = ["01", "02", "03", "04", "05"]
    if not ind_oper or ind_oper not in ind_oper_validos:
        return None
    
    # UNID_IMOB: obrigatório, valores válidos [01, 02, 03, 04, 05, 06]
    unid_imob_validos = ["01", "02", "03", "04", "05", "06"]
    if not unid_imob or unid_imob not in unid_imob_validos:
        return None
    
    # IDENT_EMP: obrigatório, sem limite de tamanho
    if not ident_emp:
        return None
    
    # DESC_UNID_IMOB: opcional, máximo 90 caracteres
    if desc_unid_imob and len(desc_unid_imob) > 90:
        return None
    
    # NUM_CONT: opcional, máximo 90 caracteres
    if num_cont and len(num_cont) > 90:
        return None
    
    # CPF_CNPJ_ADQU: obrigatório, 14 caracteres (CPF ou CNPJ)
    # Remove formatação para validar
    cpf_cnpj_limpo = cpf_cnpj_adqu.replace(".", "").replace("/", "").replace("-", "").replace(" ", "")
    if not cpf_cnpj_adqu or len(cpf_cnpj_limpo) not in [11, 14] or not _validar_cpf_cnpj(cpf_cnpj_adqu):
        return None
    
    # DT_OPER: obrigatório, formato ddmmaaaa
    ok_dt, dt_obj = _validar_data(dt_oper)
    if not ok_dt:
        return None
    
    # Validação opcional: DT_OPER deve estar dentro do período (se fornecido)
    if dt_ini_0000 and dt_fin_0000:
        if dt_obj < dt_ini_0000 or dt_obj > dt_fin_0000:
            return None
    
    # VL_TOT_VEND: obrigatório, numérico com 2 decimais
    ok1, val1, _ = validar_valor_numerico(vl_tot_vend, decimais=2, obrigatorio=True, positivo=True)
    if not ok1:
        return None
    
    # VL_REC_ACUM: opcional, numérico com 2 decimais
    ok2, val2, _ = validar_valor_numerico(vl_rec_acum, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok2:
        return None
    
    # VL_TOT_REC: obrigatório, numérico com 2 decimais
    ok3, val3, _ = validar_valor_numerico(vl_tot_rec, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok3:
        return None
    
    # CST_PIS: obrigatório, 2 dígitos
    if not cst_pis or len(cst_pis) != 2 or not cst_pis.isdigit():
        return None
    
    # VL_BC_PIS: opcional, numérico com 2 decimais
    ok4, val4, _ = validar_valor_numerico(vl_bc_pis, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok4:
        return None
    
    # ALIQ_PIS: opcional, numérico com 8 dígitos e 4 decimais (percentual)
    # Normaliza vírgula para ponto
    aliq_pis_normalizada = aliq_pis.replace(",", ".") if aliq_pis else ""
    ok5, val5, _ = validar_valor_numerico(aliq_pis_normalizada, decimais=4, obrigatorio=False, nao_negativo=True)
    if not ok5:
        return None
    # Valida se tem no máximo 8 dígitos na parte inteira
    if aliq_pis_normalizada:
        partes_aliq = aliq_pis_normalizada.split(".")
        if len(partes_aliq[0]) > 8:
            return None
    
    # VL_PIS: opcional, numérico com 2 decimais
    ok6, val6, _ = validar_valor_numerico(vl_pis, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok6:
        return None
    
    # Validação: VL_PIS deve corresponder a VL_BC_PIS * ALIQ_PIS / 100
    if vl_bc_pis and aliq_pis_normalizada and vl_pis:
        vl_pis_calculado = round((val4 * val5) / 100, 2)
        # Permite pequena diferença devido a arredondamentos (tolerância de 0.01)
        if abs(val6 - vl_pis_calculado) > 0.01:
            return None
    
    # CST_COFINS: obrigatório, 2 dígitos
    if not cst_cofins or len(cst_cofins) != 2 or not cst_cofins.isdigit():
        return None
    
    # VL_BC_COFINS: opcional, numérico com 2 decimais
    ok7, val7, _ = validar_valor_numerico(vl_bc_cofins, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok7:
        return None
    
    # ALIQ_COFINS: opcional, numérico com 8 dígitos e 4 decimais (percentual)
    # Normaliza vírgula para ponto
    aliq_cofins_normalizada = aliq_cofins.replace(",", ".") if aliq_cofins else ""
    ok8, val8, _ = validar_valor_numerico(aliq_cofins_normalizada, decimais=4, obrigatorio=False, nao_negativo=True)
    if not ok8:
        return None
    # Valida se tem no máximo 8 dígitos na parte inteira
    if aliq_cofins_normalizada:
        partes_aliq = aliq_cofins_normalizada.split(".")
        if len(partes_aliq[0]) > 8:
            return None
    
    # VL_COFINS: opcional, numérico com 2 decimais
    ok9, val9, _ = validar_valor_numerico(vl_cofins, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok9:
        return None
    
    # Validação: VL_COFINS deve corresponder a VL_BC_COFINS * ALIQ_COFINS / 100
    if vl_bc_cofins and aliq_cofins_normalizada and vl_cofins:
        vl_cofins_calculado = round((val7 * val8) / 100, 2)
        # Permite pequena diferença devido a arredondamentos (tolerância de 0.01)
        if abs(val9 - vl_cofins_calculado) > 0.01:
            return None
    
    # PERC_REC_RECEB: opcional, numérico com 6 dígitos e 2 decimais (percentual)
    # Normaliza vírgula para ponto
    perc_rec_receb_normalizada = perc_rec_receb.replace(",", ".") if perc_rec_receb else ""
    ok10, val10, _ = validar_valor_numerico(perc_rec_receb_normalizada, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok10:
        return None
    # Valida se tem no máximo 6 dígitos na parte inteira
    if perc_rec_receb_normalizada:
        partes_perc = perc_rec_receb_normalizada.split(".")
        if len(partes_perc[0]) > 6:
            return None
    
    # Validação: PERC_REC_RECEB deve ser = (VL_REC_ACUM + VL_TOT_REC) / VL_TOT_VEND
    if vl_rec_acum and vl_tot_rec and vl_tot_vend and perc_rec_receb_normalizada:
        perc_rec_receb_calculado = round(((val2 + val3) / val1) * 100, 2)
        # Permite pequena diferença devido a arredondamentos (tolerância de 0.01)
        if abs(val10 - perc_rec_receb_calculado) > 0.01:
            return None
    
    # IND_NAT_EMP: opcional, valores válidos [1, 2, 3, 4]
    ind_nat_emp_validos = ["1", "2", "3", "4"]
    if ind_nat_emp and ind_nat_emp not in ind_nat_emp_validos:
        return None
    
    # INF_COMP: opcional, máximo 90 caracteres
    if inf_comp and len(inf_comp) > 90:
        return None
    
    # Função auxiliar para formatar valores monetários
    def fmt_valor(v):
        if v is None:
            return ""
        return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    # Função auxiliar para formatar percentual
    def fmt_percentual(v):
        if v is None:
            return ""
        return f"{v:,.4f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    # Função auxiliar para formatar percentual com 2 decimais
    def fmt_percentual_2dec(v):
        if v is None:
            return ""
        return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    # Função auxiliar para formatar CPF/CNPJ
    def fmt_cpf_cnpj(cpf_cnpj_str):
        if not cpf_cnpj_str:
            return ""
        cpf_cnpj_limpo = cpf_cnpj_str.replace(".", "").replace("/", "").replace("-", "").replace(" ", "")
        if len(cpf_cnpj_limpo) == 11:
            # Formata CPF: 000.000.000-00
            return f"{cpf_cnpj_limpo[:3]}.{cpf_cnpj_limpo[3:6]}.{cpf_cnpj_limpo[6:9]}-{cpf_cnpj_limpo[9:]}"
        elif len(cpf_cnpj_limpo) == 14:
            # Formata CNPJ: 00.000.000/0000-00
            return f"{cpf_cnpj_limpo[:2]}.{cpf_cnpj_limpo[2:5]}.{cpf_cnpj_limpo[5:8]}/{cpf_cnpj_limpo[8:12]}-{cpf_cnpj_limpo[12:]}"
        return cpf_cnpj_str
    
    # Função auxiliar para formatar data
    def fmt_data(data_str):
        if not data_str or len(data_str) != 8:
            return ""
        return f"{data_str[:2]}/{data_str[2:4]}/{data_str[4:]}"
    
    # Descrições dos campos
    descricoes_ind_oper = {
        "01": "Venda a Vista de Unidade Concluída",
        "02": "Venda a Prazo de Unidade Concluída",
        "03": "Venda a Vista de Unidade em Construção",
        "04": "Venda a Prazo de Unidade em Construção",
        "05": "Outras"
    }
    
    descricoes_unid_imob = {
        "01": "Terreno adquirido para venda",
        "02": "Terreno decorrente de loteamento",
        "03": "Lote oriundo de desmembramento de terreno",
        "04": "Unidade resultante de incorporação imobiliária",
        "05": "Prédio construído/em construção para venda",
        "06": "Outras"
    }
    
    descricoes_ind_nat_emp = {
        "1": "Consórcio",
        "2": "SCP",
        "3": "Incorporação em Condomínio",
        "4": "Outras"
    }
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "IND_OPER": {
            "titulo": "Indicador do Tipo da Operação",
            "valor": ind_oper,
            "descricao": descricoes_ind_oper.get(ind_oper, "")
        },
        "UNID_IMOB": {
            "titulo": "Indicador do tipo de unidade imobiliária Vendida",
            "valor": unid_imob,
            "descricao": descricoes_unid_imob.get(unid_imob, "")
        },
        "IDENT_EMP": {
            "titulo": "Identificação/Nome do Empreendimento",
            "valor": ident_emp
        },
        "DESC_UNID_IMOB": {
            "titulo": "Descrição resumida da unidade imobiliária vendida",
            "valor": desc_unid_imob
        },
        "NUM_CONT": {
            "titulo": "Número do Contrato/Documento que formaliza a Venda da Unidade Imobiliária",
            "valor": num_cont
        },
        "CPF_CNPJ_ADQU": {
            "titulo": "Identificação da pessoa física (CPF) ou da pessoa jurídica (CNPJ) adquirente da unidade imobiliária",
            "valor": cpf_cnpj_adqu,
            "valor_formatado": fmt_cpf_cnpj(cpf_cnpj_adqu)
        },
        "DT_OPER": {
            "titulo": "Data da operação de venda da unidade imobiliária",
            "valor": dt_oper,
            "valor_formatado": fmt_data(dt_oper)
        },
        "VL_TOT_VEND": {
            "titulo": "Valor total da unidade imobiliária vendida atualizado até o período da escrituração",
            "valor": vl_tot_vend,
            "valor_formatado": fmt_valor(val1)
        },
        "VL_REC_ACUM": {
            "titulo": "Valor recebido acumulado até o mês anterior ao da escrituração",
            "valor": vl_rec_acum,
            "valor_formatado": fmt_valor(val2) if vl_rec_acum else ""
        },
        "VL_TOT_REC": {
            "titulo": "Valor total recebido no mês da escrituração",
            "valor": vl_tot_rec,
            "valor_formatado": fmt_valor(val3)
        },
        "CST_PIS": {
            "titulo": "Código da Situação Tributária referente ao PIS/PASEP, conforme a Tabela indicada no item 4.3.3",
            "valor": cst_pis
        },
        "VL_BC_PIS": {
            "titulo": "Base de Cálculo do PIS/PASEP",
            "valor": vl_bc_pis,
            "valor_formatado": fmt_valor(val4) if vl_bc_pis else ""
        },
        "ALIQ_PIS": {
            "titulo": "Alíquota do PIS/PASEP (em percentual)",
            "valor": aliq_pis,
            "valor_formatado": fmt_percentual(val5) if aliq_pis else ""
        },
        "VL_PIS": {
            "titulo": "Valor do PIS/PASEP",
            "valor": vl_pis,
            "valor_formatado": fmt_valor(val6) if vl_pis else ""
        },
        "CST_COFINS": {
            "titulo": "Código da Situação Tributária referente a COFINS, conforme a Tabela indicada no item 4.3.4",
            "valor": cst_cofins
        },
        "VL_BC_COFINS": {
            "titulo": "Base de Cálculo da COFINS",
            "valor": vl_bc_cofins,
            "valor_formatado": fmt_valor(val7) if vl_bc_cofins else ""
        },
        "ALIQ_COFINS": {
            "titulo": "Alíquota da COFINS (em percentual)",
            "valor": aliq_cofins,
            "valor_formatado": fmt_percentual(val8) if aliq_cofins else ""
        },
        "VL_COFINS": {
            "titulo": "Valor da COFINS",
            "valor": vl_cofins,
            "valor_formatado": fmt_valor(val9) if vl_cofins else ""
        },
        "PERC_REC_RECEB": {
            "titulo": "Percentual da receita total recebida até o mês, da unidade imobiliária vendida ((Campo 10 + Campo 11) / Campo 09)",
            "valor": perc_rec_receb,
            "valor_formatado": fmt_percentual_2dec(val10) if perc_rec_receb else ""
        },
        "IND_NAT_EMP": {
            "titulo": "Indicador da Natureza Específica do Empreendimento",
            "valor": ind_nat_emp,
            "descricao": descricoes_ind_nat_emp.get(ind_nat_emp, "") if ind_nat_emp else ""
        },
        "INF_COMP": {
            "titulo": "Informações Complementares",
            "valor": inf_comp
        }
    }
    
    return resultado


def validar_f200(linhas, dt_ini_0000=None, dt_fin_0000=None):
    """
    Valida uma ou mais linhas do registro F200 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |F200|IND_OPER|UNID_IMOB|IDENT_EMP|DESC_UNID_IMOB|NUM_CONT|CPF_CNPJ_ADQU|DT_OPER|VL_TOT_VEND|VL_REC_ACUM|VL_TOT_REC|CST_PIS|VL_BC_PIS|ALIQ_PIS|VL_PIS|CST_COFINS|VL_BC_COFINS|ALIQ_COFINS|VL_COFINS|PERC_REC_RECEB|IND_NAT_EMP|INF_COMP|
        dt_ini_0000: Data inicial do período (opcional, para validação de DT_OPER)
        dt_fin_0000: Data final do período (opcional, para validação de DT_OPER)
        
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
        resultado = _processar_linha_f200(linha, dt_ini_0000, dt_fin_0000)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
