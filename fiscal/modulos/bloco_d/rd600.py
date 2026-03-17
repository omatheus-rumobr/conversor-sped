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


def _validar_codigo_municipio(cod_mun_str):
    """
    Valida o código do município IBGE (7 dígitos).
    Aceita também códigos especiais: 9999999 (Exterior) e 9999998 (CT-e simplificado).
    
    Args:
        cod_mun_str: String com o código do município
        
    Returns:
        bool: True se válido, False caso contrário
    """
    if not cod_mun_str:
        return False
    
    # Códigos especiais permitidos
    if cod_mun_str in ["9999999", "9999998"]:
        return True
    
    # Deve ter 7 dígitos numéricos
    if len(cod_mun_str) != 7 or not cod_mun_str.isdigit():
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


def _processar_linha_d600(linha):
    """
    Processa uma única linha do registro D600 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |D600|COD_MOD|COD_MUN|SER|SUB|COD_CONS|QTD_CONS|DT_DOC|VL_DOC|VL_DESC|VL_SERV|VL_SERV_NT|VL_TERC|VL_DA|VL_BC_ICMS|VL_ICMS|VL_PIS|VL_COFINS|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |D600|...|)
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
    if reg != "D600":
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
    
    # Extrai todos os campos (18 campos no total)
    cod_mod = obter_campo(1)
    cod_mun = obter_campo(2)
    ser = obter_campo(3)
    sub = obter_campo(4)
    cod_cons = obter_campo(5)
    qtd_cons = obter_campo(6)
    dt_doc = obter_campo(7)
    vl_doc = obter_campo(8)
    vl_desc = obter_campo(9)
    vl_serv = obter_campo(10)
    vl_serv_nt = obter_campo(11)
    vl_terc = obter_campo(12)
    vl_da = obter_campo(13)
    vl_bc_icms = obter_campo(14)
    vl_icms = obter_campo(15)
    vl_pis = obter_campo(16)
    vl_cofins = obter_campo(17)
    
    # Validações dos campos obrigatórios
    
    # COD_MOD: obrigatório, valores válidos: ["21", "22"]
    if not cod_mod or cod_mod not in ["21", "22"]:
        return None
    
    # COD_MUN: obrigatório, 7 dígitos, deve existir na Tabela de Municípios do IBGE
    if not _validar_codigo_municipio(cod_mun):
        return None
    
    # SER: obrigatório, até 4 caracteres
    if not ser or len(ser) > 4:
        return None
    
    # SUB: opcional condicional, até 3 dígitos
    if sub and (not sub.isdigit() or len(sub) > 3):
        return None
    
    # COD_CONS: obrigatório, 2 dígitos
    if not cod_cons or len(cod_cons) != 2 or not cod_cons.isdigit():
        return None
    
    # QTD_CONS: obrigatório, numérico, maior que zero
    if not qtd_cons or not qtd_cons.isdigit() or int(qtd_cons) <= 0:
        return None
    
    # DT_DOC: obrigatório, formato ddmmaaaa
    dt_doc_valido, dt_doc_obj = _validar_data(dt_doc)
    if not dt_doc_valido:
        return None
    
    # VL_DOC: obrigatório, numérico com 2 decimais, maior que zero
    vl_doc_valido, vl_doc_float, _ = validar_valor_numerico(vl_doc, decimais=2, obrigatorio=True, positivo=True)
    if not vl_doc_valido:
        return None
    
    # VL_DESC: opcional condicional, numérico com 2 decimais, não negativo
    vl_desc_valido, vl_desc_float, _ = validar_valor_numerico(vl_desc, decimais=2, obrigatorio=False, nao_negativo=True)
    if not vl_desc_valido:
        return None
    
    # VL_SERV: obrigatório, numérico com 2 decimais, maior que zero
    vl_serv_valido, vl_serv_float, _ = validar_valor_numerico(vl_serv, decimais=2, obrigatorio=True, positivo=True)
    if not vl_serv_valido:
        return None
    
    # VL_SERV_NT: opcional condicional, numérico com 2 decimais, não negativo
    vl_serv_nt_valido, vl_serv_nt_float, _ = validar_valor_numerico(vl_serv_nt, decimais=2, obrigatorio=False, nao_negativo=True)
    if not vl_serv_nt_valido:
        return None
    
    # VL_TERC: opcional condicional, numérico com 2 decimais, não negativo
    vl_terc_valido, vl_terc_float, _ = validar_valor_numerico(vl_terc, decimais=2, obrigatorio=False, nao_negativo=True)
    if not vl_terc_valido:
        return None
    
    # VL_DA: opcional condicional, numérico com 2 decimais, não negativo
    vl_da_valido, vl_da_float, _ = validar_valor_numerico(vl_da, decimais=2, obrigatorio=False, nao_negativo=True)
    if not vl_da_valido:
        return None
    
    # VL_BC_ICMS: opcional condicional, numérico com 2 decimais, não negativo
    vl_bc_icms_valido, vl_bc_icms_float, _ = validar_valor_numerico(vl_bc_icms, decimais=2, obrigatorio=False, nao_negativo=True)
    if not vl_bc_icms_valido:
        return None
    
    # VL_ICMS: opcional condicional, numérico com 2 decimais, não negativo
    vl_icms_valido, vl_icms_float, _ = validar_valor_numerico(vl_icms, decimais=2, obrigatorio=False, nao_negativo=True)
    if not vl_icms_valido:
        return None
    
    # VL_PIS: opcional condicional, numérico com 2 decimais, não negativo
    vl_pis_valido, vl_pis_float, _ = validar_valor_numerico(vl_pis, decimais=2, obrigatorio=False, nao_negativo=True)
    if not vl_pis_valido:
        return None
    
    # VL_COFINS: opcional condicional, numérico com 2 decimais, não negativo
    vl_cofins_valido, vl_cofins_float, _ = validar_valor_numerico(vl_cofins, decimais=2, obrigatorio=False, nao_negativo=True)
    if not vl_cofins_valido:
        return None
    
    # Formatação de valores monetários
    def formatar_valor_monetario(valor_float):
        if valor_float is None:
            return ""
        return f"R$ {valor_float:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
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
                "21": "Nota Fiscal de Serviço de Comunicação",
                "22": "Nota Fiscal de Serviço de Telecomunicação"
            }.get(cod_mod, "")
        },
        "COD_MUN": {
            "titulo": "Código do município dos terminais faturados, conforme a tabela IBGE",
            "valor": cod_mun
        },
        "SER": {
            "titulo": "Série do documento fiscal",
            "valor": ser
        },
        "SUB": {
            "titulo": "Subsérie do documento fiscal",
            "valor": sub if sub else ""
        },
        "COD_CONS": {
            "titulo": "Código de classe de consumo dos serviços de comunicação ou de telecomunicação, conforme a Tabela 4.4.4",
            "valor": cod_cons
        },
        "QTD_CONS": {
            "titulo": "Quantidade de documentos consolidados neste registro",
            "valor": qtd_cons
        },
        "DT_DOC": {
            "titulo": "Data dos documentos consolidados",
            "valor": dt_doc,
            "valor_formatado": formatar_data(dt_doc_obj)
        },
        "VL_DOC": {
            "titulo": "Valor total acumulado dos documentos fiscais",
            "valor": vl_doc,
            "valor_formatado": formatar_valor_monetario(vl_doc_float)
        },
        "VL_DESC": {
            "titulo": "Valor acumulado dos descontos",
            "valor": vl_desc if vl_desc else "",
            "valor_formatado": formatar_valor_monetario(vl_desc_float) if vl_desc else ""
        },
        "VL_SERV": {
            "titulo": "Valor acumulado das prestações de serviços tributados pelo ICMS",
            "valor": vl_serv,
            "valor_formatado": formatar_valor_monetario(vl_serv_float)
        },
        "VL_SERV_NT": {
            "titulo": "Valor acumulado dos serviços não-tributados pelo ICMS",
            "valor": vl_serv_nt if vl_serv_nt else "",
            "valor_formatado": formatar_valor_monetario(vl_serv_nt_float) if vl_serv_nt else ""
        },
        "VL_TERC": {
            "titulo": "Valores cobrados em nome de terceiros",
            "valor": vl_terc if vl_terc else "",
            "valor_formatado": formatar_valor_monetario(vl_terc_float) if vl_terc else ""
        },
        "VL_DA": {
            "titulo": "Valor acumulado das despesas acessórias",
            "valor": vl_da if vl_da else "",
            "valor_formatado": formatar_valor_monetario(vl_da_float) if vl_da else ""
        },
        "VL_BC_ICMS": {
            "titulo": "Valor acumulado da base de cálculo do ICMS",
            "valor": vl_bc_icms if vl_bc_icms else "",
            "valor_formatado": formatar_valor_monetario(vl_bc_icms_float) if vl_bc_icms else ""
        },
        "VL_ICMS": {
            "titulo": "Valor acumulado do ICMS",
            "valor": vl_icms if vl_icms else "",
            "valor_formatado": formatar_valor_monetario(vl_icms_float) if vl_icms else ""
        },
        "VL_PIS": {
            "titulo": "Valor do PIS",
            "valor": vl_pis if vl_pis else "",
            "valor_formatado": formatar_valor_monetario(vl_pis_float) if vl_pis else ""
        },
        "VL_COFINS": {
            "titulo": "Valor da COFINS",
            "valor": vl_cofins if vl_cofins else "",
            "valor_formatado": formatar_valor_monetario(vl_cofins_float) if vl_cofins else ""
        }
    }
    
    return resultado


def validar_d600(linhas):
    """
    Valida uma ou mais linhas do registro D600 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |D600|COD_MOD|COD_MUN|SER|SUB|COD_CONS|QTD_CONS|DT_DOC|VL_DOC|VL_DESC|VL_SERV|VL_SERV_NT|VL_TERC|VL_DA|VL_BC_ICMS|VL_ICMS|VL_PIS|VL_COFINS|
        
    Returns:
        String JSON com array de objetos contendo os campos validados.
        Cada objeto tem a estrutura {"CAMPO": {"titulo": "...", "valor": "...", "valor_formatado": "...", "descricao": "..."}}.
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
        resultado = _processar_linha_d600(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
