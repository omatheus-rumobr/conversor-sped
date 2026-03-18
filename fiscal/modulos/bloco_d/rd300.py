import re
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
    if not valor_str:
        if obrigatorio:
            return False, None, f"Campo obrigatório não preenchido"
        return True, 0.0, None
    
    try:
        valor_float = float(valor_str)
        
        # Verifica precisão decimal
        partes_decimal = valor_str.split('.')
        if len(partes_decimal) == 2 and len(partes_decimal[1]) > decimais:
            return False, None, f"Valor com mais de {decimais} casas decimais"
        
        # Validações de sinal
        if positivo and valor_float <= 0:
            return False, None, "Valor deve ser maior que zero"
        if nao_negativo and valor_float < 0:
            return False, None, "Valor não pode ser negativo"
        
        return True, valor_float, None
    except ValueError:
        return False, None, "Valor não é numérico válido"


def _processar_linha_d300(linha):
    """
    Processa uma única linha do registro D300 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |D300|COD_MOD|SER|SUB|NUM_DOC_INI|NUM_DOC_FIN|CST_ICMS|CFOP|ALIQ_ICMS|DT_DOC|VL_OPR|VL_DESC|VL_SERV|VL_SEG|VL_OUT_DESP|VL_BC_ICMS|VL_ICMS|VL_RED_BC|COD_OBS|COD_CTA|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |D300|...|)
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
    if reg != "D300":
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
    
    # Extrai todos os campos (20 campos no total)
    cod_mod = obter_campo(1)
    ser = obter_campo(2)
    sub = obter_campo(3)
    num_doc_ini = obter_campo(4)
    num_doc_fin = obter_campo(5)
    cst_icms = obter_campo(6)
    cfop = obter_campo(7)
    aliq_icms = obter_campo(8)
    dt_doc = obter_campo(9)
    vl_opr = obter_campo(10)
    vl_desc = obter_campo(11)
    vl_serv = obter_campo(12)
    vl_seg = obter_campo(13)
    vl_out_desp = obter_campo(14)
    vl_bc_icms = obter_campo(15)
    vl_icms = obter_campo(16)
    vl_red_bc = obter_campo(17)
    cod_obs = obter_campo(18)
    cod_cta = obter_campo(19)
    
    # Validações dos campos obrigatórios
    
    # COD_MOD: obrigatório, valores válidos: ["13", "14", "15", "16"]
    if not cod_mod or cod_mod not in ["13", "14", "15", "16"]:
        return None
    
    # SER: obrigatório, até 4 caracteres
    if not ser or len(ser) > 4:
        return None
    
    # SUB: opcional condicional, numérico, até 4 dígitos
    if sub and (not sub.isdigit() or len(sub) > 4):
        return None
    
    # NUM_DOC_INI: obrigatório, numérico, maior que zero
    if not num_doc_ini or not num_doc_ini.isdigit() or int(num_doc_ini) <= 0:
        return None
    
    # NUM_DOC_FIN: obrigatório, numérico, maior que zero
    if not num_doc_fin or not num_doc_fin.isdigit() or int(num_doc_fin) <= 0:
        return None
    
    # Validação: NUM_DOC_FIN deve ser maior ou igual a NUM_DOC_INI
    if int(num_doc_fin) < int(num_doc_ini):
        return None
    
    # CST_ICMS: obrigatório, 3 dígitos, primeiro dígito sempre 0
    if not cst_icms or len(cst_icms) != 3 or not cst_icms.isdigit() or cst_icms[0] != '0':
        return None
    
    # Extrai os dois últimos dígitos do CST_ICMS
    cst_icms_ultimos_2 = cst_icms[1:]
    
    # CFOP: obrigatório, 4 dígitos, primeiro caractere = 5, não pode terminar em 00 ou 50
    if not cfop or len(cfop) != 4 or not cfop.isdigit() or cfop[0] != '5' or cfop.endswith("00") or cfop.endswith("50"):
        return None
    
    # DT_DOC: obrigatório, formato ddmmaaaa
    dt_doc_valido, dt_doc_obj = _validar_data(dt_doc)
    if not dt_doc_valido:
        return None
    
    # VL_SERV: obrigatório, numérico com 2 decimais, maior que zero
    vl_serv_valido, vl_serv_float, _ = validar_valor_numerico(vl_serv, decimais=2, obrigatorio=True, positivo=True)
    if not vl_serv_valido:
        return None
    
    # VL_DESC: opcional condicional, numérico com 2 decimais, não negativo
    vl_desc_valido, vl_desc_float, _ = validar_valor_numerico(vl_desc, decimais=2, obrigatorio=False, nao_negativo=True)
    if not vl_desc_valido:
        return None
    
    # VL_SEG: opcional condicional, numérico com 2 decimais, não negativo
    vl_seg_valido, vl_seg_float, _ = validar_valor_numerico(vl_seg, decimais=2, obrigatorio=False, nao_negativo=True)
    if not vl_seg_valido:
        return None
    
    # VL_OUT_DESP: opcional condicional, numérico com 2 decimais, não negativo
    vl_out_desp_valido, vl_out_desp_float, _ = validar_valor_numerico(vl_out_desp, decimais=2, obrigatorio=False, nao_negativo=True)
    if not vl_out_desp_valido:
        return None
    
    # VL_OPR: obrigatório, numérico com 2 decimais, maior que zero
    # Deve ser igual a VL_SERV + VL_SEG + VL_OUT_DESP - VL_DESC
    vl_opr_valido, vl_opr_float, _ = validar_valor_numerico(vl_opr, decimais=2, obrigatorio=True, positivo=True)
    if not vl_opr_valido:
        return None
    
    # Validação: VL_OPR deve ser igual a VL_SERV + VL_SEG + VL_OUT_DESP - VL_DESC
    vl_opr_calculado = vl_serv_float + vl_seg_float + vl_out_desp_float - vl_desc_float
    if abs(vl_opr_float - vl_opr_calculado) > 0.01:  # Tolerância para diferenças de arredondamento
        return None
    
    # Validações condicionais baseadas nos dois últimos dígitos do CST_ICMS
    # Para CST_ICMS terminando em 30, 40, 41, 50 ou 60: VL_BC_ICMS, ALIQ_ICMS e VL_ICMS devem ser 0
    if cst_icms_ultimos_2 in ["30", "40", "41", "50", "60"]:
        vl_bc_icms_valido, vl_bc_icms_float, _ = validar_valor_numerico(vl_bc_icms, decimais=2, obrigatorio=True, nao_negativo=True)
        if not vl_bc_icms_valido or abs(vl_bc_icms_float) > 0.001:
            return None
        
        aliq_icms_valido, aliq_icms_float, _ = validar_valor_numerico(aliq_icms, decimais=2, obrigatorio=True, nao_negativo=True)
        if not aliq_icms_valido or abs(aliq_icms_float) > 0.001:
            return None
        
        vl_icms_valido, vl_icms_float, _ = validar_valor_numerico(vl_icms, decimais=2, obrigatorio=True, nao_negativo=True)
        if not vl_icms_valido or abs(vl_icms_float) > 0.001:
            return None
    # Para CST_ICMS diferente de 30, 40, 41, 50, 60, 51, 90: VL_BC_ICMS, ALIQ_ICMS e VL_ICMS devem ser > 0
    elif cst_icms_ultimos_2 not in ["51", "90"]:
        vl_bc_icms_valido, vl_bc_icms_float, _ = validar_valor_numerico(vl_bc_icms, decimais=2, obrigatorio=True, positivo=True)
        if not vl_bc_icms_valido:
            return None
        
        aliq_icms_valido, aliq_icms_float, _ = validar_valor_numerico(aliq_icms, decimais=2, obrigatorio=True, positivo=True)
        if not aliq_icms_valido:
            return None
        
        vl_icms_valido, vl_icms_float, _ = validar_valor_numerico(vl_icms, decimais=2, obrigatorio=True, positivo=True)
        if not vl_icms_valido:
            return None
    # Para CST_ICMS terminando em 51 ou 90: VL_BC_ICMS, ALIQ_ICMS e VL_ICMS devem ser >= 0
    else:  # cst_icms_ultimos_2 in ["51", "90"]
        vl_bc_icms_valido, vl_bc_icms_float, _ = validar_valor_numerico(vl_bc_icms, decimais=2, obrigatorio=True, nao_negativo=True)
        if not vl_bc_icms_valido:
            return None
        
        aliq_icms_valido, aliq_icms_float, _ = validar_valor_numerico(aliq_icms, decimais=2, obrigatorio=True, nao_negativo=True)
        if not aliq_icms_valido:
            return None
        
        vl_icms_valido, vl_icms_float, _ = validar_valor_numerico(vl_icms, decimais=2, obrigatorio=True, nao_negativo=True)
        if not vl_icms_valido:
            return None
    
    # VL_RED_BC: obrigatório condicional; só pode ser preenchido se CST_ICMS terminar em 20, 70 ou 90
    if cst_icms_ultimos_2 in ["20", "70", "90"]:
        vl_red_bc_valido, vl_red_bc_float, _ = validar_valor_numerico(vl_red_bc, decimais=2, obrigatorio=True, nao_negativo=True)
        if not vl_red_bc_valido:
            return None
    elif vl_red_bc and float(vl_red_bc) != 0.0:  # Se não for 20, 70 ou 90, deve ser vazio ou zero
        return None
    else:
        vl_red_bc_float = 0.0
    
    # COD_OBS: opcional condicional, até 6 caracteres
    if cod_obs and len(cod_obs) > 6:
        return None
    
    # COD_CTA: opcional condicional (sem validação específica de formato no manual)
    
    # Formatação de valores monetários
    def formatar_valor_monetario(valor_float):
        if valor_float is None:
            return ""
        return f"R$ {valor_float:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    # Formatação de percentual
    def formatar_percentual(valor_float):
        if valor_float is None:
            return ""
        return f"{valor_float:.2f}%"
    
    # Formatação de data
    def formatar_data(data_obj):
        if data_obj is None:
            return ""
        return data_obj.strftime("%d/%m/%Y")
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "COD_MOD": {
            "titulo": "Código do modelo do documento fiscal, conforme a Tabela 4.1.1",
            "valor": cod_mod,
            "descricao": {
                "13": "Bilhete Consolidado de Passagem Rodoviário",
                "14": "Bilhete Consolidado de Passagem Aquaviário",
                "15": "Bilhete Consolidado de Passagem e Nota de Bagagem",
                "16": "Bilhete Consolidado de Passagem Ferroviário"
            }.get(cod_mod, "")
        },
        "SER": {
            "titulo": "Série do documento fiscal",
            "valor": ser
        },
        "SUB": {
            "titulo": "Subsérie do documento fiscal",
            "valor": sub if sub else ""
        },
        "NUM_DOC_INI": {
            "titulo": "Número do primeiro documento fiscal emitido (mesmo modelo, série e subsérie)",
            "valor": num_doc_ini
        },
        "NUM_DOC_FIN": {
            "titulo": "Número do último documento fiscal emitido (mesmo modelo, série e subsérie)",
            "valor": num_doc_fin
        },
        "CST_ICMS": {
            "titulo": "Código da Situação Tributária, conforme a Tabela indicada no item 4.3.1",
            "valor": cst_icms
        },
        "CFOP": {
            "titulo": "Código Fiscal de Operação e Prestação conforme tabela indicada no item 4.2.2",
            "valor": cfop
        },
        "ALIQ_ICMS": {
            "titulo": "Alíquota do ICMS",
            "valor": aliq_icms if aliq_icms else "",
            "valor_formatado": formatar_percentual(aliq_icms_float) if aliq_icms else ""
        },
        "DT_DOC": {
            "titulo": "Data da emissão dos documentos fiscais",
            "valor": dt_doc,
            "valor_formatado": formatar_data(dt_doc_obj)
        },
        "VL_OPR": {
            "titulo": "Valor total acumulado das operações correspondentes à combinação de CST_ICMS, CFOP e alíquota do ICMS, incluídas as despesas acessórias e acréscimos",
            "valor": vl_opr,
            "valor_formatado": formatar_valor_monetario(vl_opr_float)
        },
        "VL_DESC": {
            "titulo": "Valor total dos descontos",
            "valor": vl_desc if vl_desc else "",
            "valor_formatado": formatar_valor_monetario(vl_desc_float) if vl_desc else ""
        },
        "VL_SERV": {
            "titulo": "Valor total da prestação de serviço",
            "valor": vl_serv,
            "valor_formatado": formatar_valor_monetario(vl_serv_float)
        },
        "VL_SEG": {
            "titulo": "Valor de seguro",
            "valor": vl_seg if vl_seg else "",
            "valor_formatado": formatar_valor_monetario(vl_seg_float) if vl_seg else ""
        },
        "VL_OUT_DESP": {
            "titulo": "Valor de outras despesas",
            "valor": vl_out_desp if vl_out_desp else "",
            "valor_formatado": formatar_valor_monetario(vl_out_desp_float) if vl_out_desp else ""
        },
        "VL_BC_ICMS": {
            "titulo": "Valor total da base de cálculo do ICMS",
            "valor": vl_bc_icms if vl_bc_icms else "",
            "valor_formatado": formatar_valor_monetario(vl_bc_icms_float) if vl_bc_icms else ""
        },
        "VL_ICMS": {
            "titulo": "Valor total do ICMS",
            "valor": vl_icms if vl_icms else "",
            "valor_formatado": formatar_valor_monetario(vl_icms_float) if vl_icms else ""
        },
        "VL_RED_BC": {
            "titulo": "Valor não tributado em função da redução da base de cálculo do ICMS, referente à combinação de CST_ICMS, CFOP e alíquota do ICMS",
            "valor": vl_red_bc if vl_red_bc else "",
            "valor_formatado": formatar_valor_monetario(vl_red_bc_float) if vl_red_bc else ""
        },
        "COD_OBS": {
            "titulo": "Código da observação do lançamento fiscal (campo 02 do Registro 0460)",
            "valor": cod_obs if cod_obs else ""
        },
        "COD_CTA": {
            "titulo": "Código da conta analítica contábil debitada/creditada",
            "valor": cod_cta if cod_cta else ""
        }
    }
    
    return resultado


def validar_d300_fiscal(linhas):
    """
    Valida uma ou mais linhas do registro D300 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |D300|COD_MOD|SER|SUB|NUM_DOC_INI|NUM_DOC_FIN|CST_ICMS|CFOP|ALIQ_ICMS|DT_DOC|VL_OPR|VL_DESC|VL_SERV|VL_SEG|VL_OUT_DESP|VL_BC_ICMS|VL_ICMS|VL_RED_BC|COD_OBS|COD_CTA|
        
    Returns:
        String JSON com array de objetos contendo os campos validados.
        Cada objeto tem a estrutura {"CAMPO": {"titulo": "...", "valor": "...", "valor_formatado": "..."}}.
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
        resultado = _processar_linha_d300(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
