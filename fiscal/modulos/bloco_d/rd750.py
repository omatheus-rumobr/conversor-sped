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


def _processar_linha_d750(linha):
    """
    Processa uma única linha do registro D750 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |D750|COD_MOD|SER|DT_DOC|QTD_CONS|IND_PREPAGO|VL_DOC|VL_SERV|VL_SERV_NT|VL_TERC|VL_DESC|VL_DA|VL_BC_ICMS|VL_ICMS|VL_PIS|VL_COFINS|DED|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |D750|...|)
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
    if reg != "D750":
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
    
    # Extrai todos os campos (17 campos no total)
    cod_mod = obter_campo(1)
    ser = obter_campo(2)
    dt_doc = obter_campo(3)
    qtd_cons = obter_campo(4)
    ind_prepago = obter_campo(5)
    vl_doc = obter_campo(6)
    vl_serv = obter_campo(7)
    vl_serv_nt = obter_campo(8)
    vl_terc = obter_campo(9)
    vl_desc = obter_campo(10)
    vl_da = obter_campo(11)
    vl_bc_icms = obter_campo(12)
    vl_icms = obter_campo(13)
    vl_pis = obter_campo(14)
    vl_cofins = obter_campo(15)
    ded = obter_campo(16)
    
    # Validações dos campos obrigatórios
    
    # COD_MOD: obrigatório, valor válido: "62"
    if not cod_mod or cod_mod != "62":
        return None
    
    # SER: obrigatório, até 3 caracteres
    if not ser or len(ser) > 3:
        return None
    
    # DT_DOC: obrigatório, formato ddmmaaaa
    dt_doc_valido, dt_doc_obj = _validar_data(dt_doc)
    if not dt_doc_valido:
        return None
    
    # QTD_CONS: obrigatório, numérico, maior que zero
    if not qtd_cons or not qtd_cons.isdigit() or int(qtd_cons) <= 0:
        return None
    
    # IND_PREPAGO: obrigatório, valores válidos: ["0", "1"]
    if not ind_prepago or ind_prepago not in ["0", "1"]:
        return None
    
    # VL_DOC: obrigatório, numérico com 2 decimais, maior que zero
    vl_doc_valido, vl_doc_float, _ = validar_valor_numerico(vl_doc, decimais=2, obrigatorio=True, positivo=True)
    if not vl_doc_valido:
        return None
    
    # VL_SERV: obrigatório, numérico com 2 decimais, maior que zero
    vl_serv_valido, vl_serv_float, _ = validar_valor_numerico(vl_serv, decimais=2, obrigatorio=True, positivo=True)
    if not vl_serv_valido:
        return None
    
    # VL_SERV_NT: obrigatório, numérico com 2 decimais, não negativo
    vl_serv_nt_valido, vl_serv_nt_float, _ = validar_valor_numerico(vl_serv_nt, decimais=2, obrigatorio=True, nao_negativo=True)
    if not vl_serv_nt_valido:
        return None
    
    # VL_TERC: obrigatório, numérico com 2 decimais, não negativo
    vl_terc_valido, vl_terc_float, _ = validar_valor_numerico(vl_terc, decimais=2, obrigatorio=True, nao_negativo=True)
    if not vl_terc_valido:
        return None
    
    # VL_DESC: obrigatório, numérico com 2 decimais, não negativo
    vl_desc_valido, vl_desc_float, _ = validar_valor_numerico(vl_desc, decimais=2, obrigatorio=True, nao_negativo=True)
    if not vl_desc_valido:
        return None
    
    # VL_DA: obrigatório, numérico com 2 decimais, não negativo
    vl_da_valido, vl_da_float, _ = validar_valor_numerico(vl_da, decimais=2, obrigatorio=True, nao_negativo=True)
    if not vl_da_valido:
        return None
    
    # VL_BC_ICMS: obrigatório, numérico com 2 decimais, não negativo
    # O valor constante neste campo deve corresponder à soma dos valores do campo VL_BC_ICMS do registro D760
    vl_bc_icms_valido, vl_bc_icms_float, _ = validar_valor_numerico(vl_bc_icms, decimais=2, obrigatorio=True, nao_negativo=True)
    if not vl_bc_icms_valido:
        return None
    
    # VL_ICMS: obrigatório, numérico com 2 decimais, não negativo
    # O valor constante neste campo deve corresponder à soma dos valores do campo VL_ICMS do registro D760
    vl_icms_valido, vl_icms_float, _ = validar_valor_numerico(vl_icms, decimais=2, obrigatorio=True, nao_negativo=True)
    if not vl_icms_valido:
        return None
    
    # VL_PIS: opcional condicional, numérico com 2 decimais, não negativo
    # Os contribuintes que entregarem a EFD-Contribuições relativa ao mesmo período de apuração do registro 0000 estão dispensados do preenchimento deste campo
    vl_pis_valido, vl_pis_float, _ = validar_valor_numerico(vl_pis, decimais=2, obrigatorio=False, nao_negativo=True)
    if not vl_pis_valido:
        return None
    
    # VL_COFINS: opcional condicional, numérico com 2 decimais, não negativo
    # Os contribuintes que entregarem a EFD-Contribuições relativa ao mesmo período de apuração do registro 0000 estão dispensados do preenchimento deste campo
    vl_cofins_valido, vl_cofins_float, _ = validar_valor_numerico(vl_cofins, decimais=2, obrigatorio=False, nao_negativo=True)
    if not vl_cofins_valido:
        return None
    
    # DED: opcional condicional, numérico com 2 decimais, não negativo
    # Deve ser informado quando houver itens lançados com código do grupo 590, conforme Tabela de classificação de produtos da NFCom (cClass)
    ded_valido, ded_float, _ = validar_valor_numerico(ded, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ded_valido:
        return None
    
    # Formatação de valores monetários
    def formatar_valor_monetario(valor_float):
        if valor_float is None:
            return ""
        return f"R$ {valor_float:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
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
            "descricao": "NFCom"
        },
        "SER": {
            "titulo": "Série do documento fiscal",
            "valor": ser
        },
        "DT_DOC": {
            "titulo": "Data da emissão dos documentos",
            "valor": dt_doc,
            "valor_formatado": formatar_data(dt_doc_obj)
        },
        "QTD_CONS": {
            "titulo": "Quantidade de documentos consolidados neste registro",
            "valor": qtd_cons
        },
        "IND_PREPAGO": {
            "titulo": "Forma de pagamento: 0 – pré pago; 1 – pós pago",
            "valor": ind_prepago,
            "descricao": {"0": "Pré pago", "1": "Pós pago"}.get(ind_prepago, "")
        },
        "VL_DOC": {
            "titulo": "Valor total dos documentos",
            "valor": vl_doc,
            "valor_formatado": formatar_valor_monetario(vl_doc_float)
        },
        "VL_SERV": {
            "titulo": "Valor dos serviços tributados pelo ICMS",
            "valor": vl_serv,
            "valor_formatado": formatar_valor_monetario(vl_serv_float)
        },
        "VL_SERV_NT": {
            "titulo": "Valores cobrados em nome do prestador sem destaque de ICMS",
            "valor": vl_serv_nt,
            "valor_formatado": formatar_valor_monetario(vl_serv_nt_float)
        },
        "VL_TERC": {
            "titulo": "Valor total cobrado em nome de terceiros",
            "valor": vl_terc,
            "valor_formatado": formatar_valor_monetario(vl_terc_float)
        },
        "VL_DESC": {
            "titulo": "Valor total dos descontos",
            "valor": vl_desc,
            "valor_formatado": formatar_valor_monetario(vl_desc_float)
        },
        "VL_DA": {
            "titulo": "Valor total das despesas acessórias",
            "valor": vl_da,
            "valor_formatado": formatar_valor_monetario(vl_da_float)
        },
        "VL_BC_ICMS": {
            "titulo": "Valor total da base de cálculo do ICMS",
            "valor": vl_bc_icms,
            "valor_formatado": formatar_valor_monetario(vl_bc_icms_float)
        },
        "VL_ICMS": {
            "titulo": "Valor total do ICMS",
            "valor": vl_icms,
            "valor_formatado": formatar_valor_monetario(vl_icms_float)
        },
        "VL_PIS": {
            "titulo": "Valor total do PIS",
            "valor": vl_pis if vl_pis else "",
            "valor_formatado": formatar_valor_monetario(vl_pis_float) if vl_pis else ""
        },
        "VL_COFINS": {
            "titulo": "Valor total da COFINS",
            "valor": vl_cofins if vl_cofins else "",
            "valor_formatado": formatar_valor_monetario(vl_cofins_float) if vl_cofins else ""
        },
        "DED": {
            "titulo": "Deduções",
            "valor": ded if ded else "",
            "valor_formatado": formatar_valor_monetario(ded_float) if ded else ""
        }
    }
    
    return resultado


def validar_d750_fiscal(linhas):
    """
    Valida uma ou mais linhas do registro D750 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |D750|COD_MOD|SER|DT_DOC|QTD_CONS|IND_PREPAGO|VL_DOC|VL_SERV|VL_SERV_NT|VL_TERC|VL_DESC|VL_DA|VL_BC_ICMS|VL_ICMS|VL_PIS|VL_COFINS|DED|
        
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
        resultado = _processar_linha_d750(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
