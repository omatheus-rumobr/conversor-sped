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


def _processar_linha_1011(linha):
    """
    Processa uma única linha do registro 1011 e retorna um dicionário.
    
    Formato:
      |1011|REG_REF|CHAVE_DOC|COD_PART|COD_ITEM|DT_OPER|VL_OPER|CST_PIS|VL_BC_PIS|ALIQ_PIS|VL_PIS|CST_COFINS|VL_BC_COFINS|ALIQ_COFINS|VL_COFINS|CST_PIS_SUSP|VL_BC_PIS_SUSP|ALIQ_PIS_SUSP|VL_PIS_SUSP|CST_COFINS_SUSP|VL_BC_COFINS_SUSP|ALIQ_COFINS_SUSP|VL_COFINS_SUSP|COD_CTA|COD_CCUS|DESC_DOC_OPER|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "1011"
    - REG_REF: opcional, até 4 caracteres
    - CHAVE_DOC: opcional, até 90 caracteres
    - COD_PART: opcional, até 60 caracteres
    - COD_ITEM: opcional, até 60 caracteres
    - DT_OPER: obrigatório, formato ddmmaaaa, data válida
    - VL_OPER: obrigatório, numérico com 2 decimais, > 0
    - CST_PIS: obrigatório, 2 dígitos
    - VL_BC_PIS: opcional, numérico com 4 decimais, não negativo
    - ALIQ_PIS: opcional, numérico com 4 decimais, não negativo
    - VL_PIS: opcional, numérico com 2 decimais, não negativo
    - CST_COFINS: obrigatório, 2 dígitos
    - VL_BC_COFINS: opcional, numérico com 4 decimais, não negativo
    - ALIQ_COFINS: opcional, numérico com 4 decimais, não negativo
    - VL_COFINS: opcional, numérico com 2 decimais, não negativo
    - CST_PIS_SUSP: obrigatório, 2 dígitos
    - VL_BC_PIS_SUSP: opcional, numérico com 4 decimais, não negativo
    - ALIQ_PIS_SUSP: opcional, numérico com 4 decimais, não negativo
    - VL_PIS_SUSP: opcional, numérico com 2 decimais, não negativo
    - CST_COFINS_SUSP: obrigatório, 2 dígitos
    - VL_BC_COFINS_SUSP: opcional, numérico com 4 decimais, não negativo
    - ALIQ_COFINS_SUSP: opcional, numérico com 4 decimais, não negativo
    - VL_COFINS_SUSP: opcional, numérico com 2 decimais, não negativo
    - COD_CTA: opcional, até 255 caracteres (obrigatório exceto se PJ dispensada de ECD)
    - COD_CCUS: opcional, até 255 caracteres
    - DESC_DOC_OPER: opcional
    
    Nota: Este registro está disponível apenas para escriturações criadas a partir do leiaute VI
    da EFD-Contribuições, válido a partir de janeiro/2020.
    As validações de que REG_REF deve existir na escrituração, COD_PART deve existir no 0150,
    COD_ITEM deve existir no 0200, COD_CTA deve existir no 0500, e COD_CCUS deve existir no 0600
    devem ser feitas em uma camada superior.
    A validação de que COD_CTA é obrigatório exceto se a PJ estiver dispensada de ECD deve ser
    feita em uma camada superior.
    
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
    # Remove primeiro e último se vazios (formato padrão SPED: |1011|...|)
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
    if reg != "1011":
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
    
    # Extrai todos os campos (26 campos no total)
    reg_ref = obter_campo(1)
    chave_doc = obter_campo(2)
    cod_part = obter_campo(3)
    cod_item = obter_campo(4)
    dt_oper = obter_campo(5)
    vl_oper = obter_campo(6)
    cst_pis = obter_campo(7)
    vl_bc_pis = obter_campo(8)
    aliq_pis = obter_campo(9)
    vl_pis = obter_campo(10)
    cst_cofins = obter_campo(11)
    vl_bc_cofins = obter_campo(12)
    aliq_cofins = obter_campo(13)
    vl_cofins = obter_campo(14)
    cst_pis_susp = obter_campo(15)
    vl_bc_pis_susp = obter_campo(16)
    aliq_pis_susp = obter_campo(17)
    vl_pis_susp = obter_campo(18)
    cst_cofins_susp = obter_campo(19)
    vl_bc_cofins_susp = obter_campo(20)
    aliq_cofins_susp = obter_campo(21)
    vl_cofins_susp = obter_campo(22)
    cod_cta = obter_campo(23)
    cod_ccus = obter_campo(24)
    desc_doc_oper = obter_campo(25)
    
    # Validações básicas dos campos obrigatórios
    
    # REG_REF: opcional, até 4 caracteres
    if reg_ref and len(reg_ref) > 4:
        return None
    
    # CHAVE_DOC: opcional, até 90 caracteres
    if chave_doc and len(chave_doc) > 90:
        return None
    
    # COD_PART: opcional, até 60 caracteres
    if cod_part and len(cod_part) > 60:
        return None
    
    # COD_ITEM: opcional, até 60 caracteres
    if cod_item and len(cod_item) > 60:
        return None
    
    # DT_OPER: obrigatório, formato ddmmaaaa, data válida
    dt_oper_valida, dt_oper_obj = _validar_data(dt_oper)
    if not dt_oper_valida:
        return None
    
    # VL_OPER: obrigatório, numérico com 2 decimais, > 0
    ok1, val1, _ = validar_valor_numerico(vl_oper, decimais=2, obrigatorio=True, positivo=True)
    if not ok1:
        return None
    
    # CST_PIS: obrigatório, 2 dígitos
    if not cst_pis or len(cst_pis) != 2 or not cst_pis.isdigit():
        return None
    
    # VL_BC_PIS: opcional, numérico com 4 decimais, não negativo
    ok2, val2, _ = validar_valor_numerico(vl_bc_pis, decimais=4, obrigatorio=False, nao_negativo=True)
    if not ok2:
        return None
    
    # ALIQ_PIS: opcional, numérico com 4 decimais, não negativo
    ok3, val3, _ = validar_valor_numerico(aliq_pis, decimais=4, obrigatorio=False, nao_negativo=True)
    if not ok3:
        return None
    
    # VL_PIS: opcional, numérico com 2 decimais, não negativo
    ok4, val4, _ = validar_valor_numerico(vl_pis, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok4:
        return None
    
    # CST_COFINS: obrigatório, 2 dígitos
    if not cst_cofins or len(cst_cofins) != 2 or not cst_cofins.isdigit():
        return None
    
    # VL_BC_COFINS: opcional, numérico com 4 decimais, não negativo
    ok5, val5, _ = validar_valor_numerico(vl_bc_cofins, decimais=4, obrigatorio=False, nao_negativo=True)
    if not ok5:
        return None
    
    # ALIQ_COFINS: opcional, numérico com 4 decimais, não negativo
    ok6, val6, _ = validar_valor_numerico(aliq_cofins, decimais=4, obrigatorio=False, nao_negativo=True)
    if not ok6:
        return None
    
    # VL_COFINS: opcional, numérico com 2 decimais, não negativo
    ok7, val7, _ = validar_valor_numerico(vl_cofins, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok7:
        return None
    
    # CST_PIS_SUSP: obrigatório, 2 dígitos
    if not cst_pis_susp or len(cst_pis_susp) != 2 or not cst_pis_susp.isdigit():
        return None
    
    # VL_BC_PIS_SUSP: opcional, numérico com 4 decimais, não negativo
    ok8, val8, _ = validar_valor_numerico(vl_bc_pis_susp, decimais=4, obrigatorio=False, nao_negativo=True)
    if not ok8:
        return None
    
    # ALIQ_PIS_SUSP: opcional, numérico com 4 decimais, não negativo
    ok9, val9, _ = validar_valor_numerico(aliq_pis_susp, decimais=4, obrigatorio=False, nao_negativo=True)
    if not ok9:
        return None
    
    # VL_PIS_SUSP: opcional, numérico com 2 decimais, não negativo
    ok10, val10, _ = validar_valor_numerico(vl_pis_susp, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok10:
        return None
    
    # CST_COFINS_SUSP: obrigatório, 2 dígitos
    if not cst_cofins_susp or len(cst_cofins_susp) != 2 or not cst_cofins_susp.isdigit():
        return None
    
    # VL_BC_COFINS_SUSP: opcional, numérico com 4 decimais, não negativo
    ok11, val11, _ = validar_valor_numerico(vl_bc_cofins_susp, decimais=4, obrigatorio=False, nao_negativo=True)
    if not ok11:
        return None
    
    # ALIQ_COFINS_SUSP: opcional, numérico com 4 decimais, não negativo
    ok12, val12, _ = validar_valor_numerico(aliq_cofins_susp, decimais=4, obrigatorio=False, nao_negativo=True)
    if not ok12:
        return None
    
    # VL_COFINS_SUSP: opcional, numérico com 2 decimais, não negativo
    ok13, val13, _ = validar_valor_numerico(vl_cofins_susp, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok13:
        return None
    
    # COD_CTA: opcional, até 255 caracteres
    if cod_cta and len(cod_cta) > 255:
        return None
    
    # COD_CCUS: opcional, até 255 caracteres
    if cod_ccus and len(cod_ccus) > 255:
        return None
    
    # Função auxiliar para formatar data
    def fmt_data(d):
        return d.strftime("%d/%m/%Y") if d else ""
    
    # Função auxiliar para formatar valores monetários
    def fmt_valor(v):
        return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    # Função auxiliar para formatar valores com 4 decimais
    def fmt_valor_4dec(v):
        return f"{v:,.4f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "DT_OPER": {
            "titulo": "Data da Operação",
            "valor": dt_oper,
            "valor_formatado": fmt_data(dt_oper_obj)
        },
        "VL_OPER": {
            "titulo": "Valor da Operação/Item",
            "valor": vl_oper,
            "valor_formatado": fmt_valor(val1)
        },
        "CST_PIS": {
            "titulo": "Código da Situação Tributária conforme escrituração, referente ao PIS/PASEP",
            "valor": cst_pis
        },
        "CST_COFINS": {
            "titulo": "Código da Situação Tributária conforme escrituração, referente a COFINS",
            "valor": cst_cofins
        },
        "CST_PIS_SUSP": {
            "titulo": "Código da Situação Tributária conforme decisão judicial, referente ao PIS/PASEP",
            "valor": cst_pis_susp
        },
        "CST_COFINS_SUSP": {
            "titulo": "Código da Situação Tributária conforme decisão judicial, referente a COFINS",
            "valor": cst_cofins_susp
        }
    }
    
    # REG_REF: opcional
    if reg_ref:
        resultado["REG_REF"] = {
            "titulo": "Registro da escrituração que terá o detalhamento das contribuições sociais com exigibilidade suspensa",
            "valor": reg_ref
        }
    else:
        resultado["REG_REF"] = {
            "titulo": "Registro da escrituração que terá o detalhamento das contribuições sociais com exigibilidade suspensa",
            "valor": ""
        }
    
    # CHAVE_DOC: opcional
    if chave_doc:
        resultado["CHAVE_DOC"] = {
            "titulo": "Chave do documento eletrônico",
            "valor": chave_doc
        }
    else:
        resultado["CHAVE_DOC"] = {
            "titulo": "Chave do documento eletrônico",
            "valor": ""
        }
    
    # COD_PART: opcional
    if cod_part:
        resultado["COD_PART"] = {
            "titulo": "Código do participante (Campo 02 do Registro 0150)",
            "valor": cod_part
        }
    else:
        resultado["COD_PART"] = {
            "titulo": "Código do participante (Campo 02 do Registro 0150)",
            "valor": ""
        }
    
    # COD_ITEM: opcional
    if cod_item:
        resultado["COD_ITEM"] = {
            "titulo": "Código do item (campo 02 do Registro 0200)",
            "valor": cod_item
        }
    else:
        resultado["COD_ITEM"] = {
            "titulo": "Código do item (campo 02 do Registro 0200)",
            "valor": ""
        }
    
    # VL_BC_PIS: opcional
    if vl_bc_pis:
        resultado["VL_BC_PIS"] = {
            "titulo": "Base de cálculo do PIS/PASEP, conforme escrituração",
            "valor": vl_bc_pis,
            "valor_formatado": fmt_valor_4dec(val2) if val2 else ""
        }
    else:
        resultado["VL_BC_PIS"] = {
            "titulo": "Base de cálculo do PIS/PASEP, conforme escrituração",
            "valor": "",
            "valor_formatado": ""
        }
    
    # ALIQ_PIS: opcional
    if aliq_pis:
        resultado["ALIQ_PIS"] = {
            "titulo": "Alíquota do PIS/PASEP, conforme escrituração",
            "valor": aliq_pis,
            "valor_formatado": fmt_valor_4dec(val3) if val3 else ""
        }
    else:
        resultado["ALIQ_PIS"] = {
            "titulo": "Alíquota do PIS/PASEP, conforme escrituração",
            "valor": "",
            "valor_formatado": ""
        }
    
    # VL_PIS: opcional
    if vl_pis:
        resultado["VL_PIS"] = {
            "titulo": "Valor do PIS/PASEP, conforme escrituração",
            "valor": vl_pis,
            "valor_formatado": fmt_valor(val4) if val4 else ""
        }
    else:
        resultado["VL_PIS"] = {
            "titulo": "Valor do PIS/PASEP, conforme escrituração",
            "valor": "",
            "valor_formatado": ""
        }
    
    # VL_BC_COFINS: opcional
    if vl_bc_cofins:
        resultado["VL_BC_COFINS"] = {
            "titulo": "Base de cálculo da COFINS, conforme escrituração",
            "valor": vl_bc_cofins,
            "valor_formatado": fmt_valor_4dec(val5) if val5 else ""
        }
    else:
        resultado["VL_BC_COFINS"] = {
            "titulo": "Base de cálculo da COFINS, conforme escrituração",
            "valor": "",
            "valor_formatado": ""
        }
    
    # ALIQ_COFINS: opcional
    if aliq_cofins:
        resultado["ALIQ_COFINS"] = {
            "titulo": "Alíquota da COFINS, conforme escrituração",
            "valor": aliq_cofins,
            "valor_formatado": fmt_valor_4dec(val6) if val6 else ""
        }
    else:
        resultado["ALIQ_COFINS"] = {
            "titulo": "Alíquota da COFINS, conforme escrituração",
            "valor": "",
            "valor_formatado": ""
        }
    
    # VL_COFINS: opcional
    if vl_cofins:
        resultado["VL_COFINS"] = {
            "titulo": "Valor da COFINS, conforme escrituração",
            "valor": vl_cofins,
            "valor_formatado": fmt_valor(val7) if val7 else ""
        }
    else:
        resultado["VL_COFINS"] = {
            "titulo": "Valor da COFINS, conforme escrituração",
            "valor": "",
            "valor_formatado": ""
        }
    
    # VL_BC_PIS_SUSP: opcional
    if vl_bc_pis_susp:
        resultado["VL_BC_PIS_SUSP"] = {
            "titulo": "Base de cálculo do PIS/PASEP, conforme decisão judicial",
            "valor": vl_bc_pis_susp,
            "valor_formatado": fmt_valor_4dec(val8) if val8 else ""
        }
    else:
        resultado["VL_BC_PIS_SUSP"] = {
            "titulo": "Base de cálculo do PIS/PASEP, conforme decisão judicial",
            "valor": "",
            "valor_formatado": ""
        }
    
    # ALIQ_PIS_SUSP: opcional
    if aliq_pis_susp:
        resultado["ALIQ_PIS_SUSP"] = {
            "titulo": "Alíquota do PIS/PASEP, conforme decisão judicial",
            "valor": aliq_pis_susp,
            "valor_formatado": fmt_valor_4dec(val9) if val9 else ""
        }
    else:
        resultado["ALIQ_PIS_SUSP"] = {
            "titulo": "Alíquota do PIS/PASEP, conforme decisão judicial",
            "valor": "",
            "valor_formatado": ""
        }
    
    # VL_PIS_SUSP: opcional
    if vl_pis_susp:
        resultado["VL_PIS_SUSP"] = {
            "titulo": "Valor do PIS/PASEP, conforme decisão judicial",
            "valor": vl_pis_susp,
            "valor_formatado": fmt_valor(val10) if val10 else ""
        }
    else:
        resultado["VL_PIS_SUSP"] = {
            "titulo": "Valor do PIS/PASEP, conforme decisão judicial",
            "valor": "",
            "valor_formatado": ""
        }
    
    # VL_BC_COFINS_SUSP: opcional
    if vl_bc_cofins_susp:
        resultado["VL_BC_COFINS_SUSP"] = {
            "titulo": "Base de cálculo da COFINS, conforme decisão judicial",
            "valor": vl_bc_cofins_susp,
            "valor_formatado": fmt_valor_4dec(val11) if val11 else ""
        }
    else:
        resultado["VL_BC_COFINS_SUSP"] = {
            "titulo": "Base de cálculo da COFINS, conforme decisão judicial",
            "valor": "",
            "valor_formatado": ""
        }
    
    # ALIQ_COFINS_SUSP: opcional
    if aliq_cofins_susp:
        resultado["ALIQ_COFINS_SUSP"] = {
            "titulo": "Alíquota da COFINS, conforme decisão judicial",
            "valor": aliq_cofins_susp,
            "valor_formatado": fmt_valor_4dec(val12) if val12 else ""
        }
    else:
        resultado["ALIQ_COFINS_SUSP"] = {
            "titulo": "Alíquota da COFINS, conforme decisão judicial",
            "valor": "",
            "valor_formatado": ""
        }
    
    # VL_COFINS_SUSP: opcional
    if vl_cofins_susp:
        resultado["VL_COFINS_SUSP"] = {
            "titulo": "Valor da COFINS, conforme decisão judicial",
            "valor": vl_cofins_susp,
            "valor_formatado": fmt_valor(val13) if val13 else ""
        }
    else:
        resultado["VL_COFINS_SUSP"] = {
            "titulo": "Valor da COFINS, conforme decisão judicial",
            "valor": "",
            "valor_formatado": ""
        }
    
    # COD_CTA: opcional
    if cod_cta:
        resultado["COD_CTA"] = {
            "titulo": "Código da conta analítica contábil debitada/creditada",
            "valor": cod_cta
        }
    else:
        resultado["COD_CTA"] = {
            "titulo": "Código da conta analítica contábil debitada/creditada",
            "valor": ""
        }
    
    # COD_CCUS: opcional
    if cod_ccus:
        resultado["COD_CCUS"] = {
            "titulo": "Código do Centro de Custos",
            "valor": cod_ccus
        }
    else:
        resultado["COD_CCUS"] = {
            "titulo": "Código do Centro de Custos",
            "valor": ""
        }
    
    # DESC_DOC_OPER: opcional
    if desc_doc_oper:
        resultado["DESC_DOC_OPER"] = {
            "titulo": "Descrição do Documento/Operação",
            "valor": desc_doc_oper
        }
    else:
        resultado["DESC_DOC_OPER"] = {
            "titulo": "Descrição do Documento/Operação",
            "valor": ""
        }
    
    return resultado


def validar_1011(linhas):
    """
    Valida uma ou mais linhas do registro 1011 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |1011|REG_REF|CHAVE_DOC|COD_PART|COD_ITEM|DT_OPER|VL_OPER|CST_PIS|VL_BC_PIS|ALIQ_PIS|VL_PIS|CST_COFINS|VL_BC_COFINS|ALIQ_COFINS|VL_COFINS|CST_PIS_SUSP|VL_BC_PIS_SUSP|ALIQ_PIS_SUSP|VL_PIS_SUSP|CST_COFINS_SUSP|VL_BC_COFINS_SUSP|ALIQ_COFINS_SUSP|VL_COFINS_SUSP|COD_CTA|COD_CCUS|DESC_DOC_OPER|
        
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
        resultado = _processar_linha_1011(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
