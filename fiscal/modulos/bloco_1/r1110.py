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


def _validar_chave_nfe(chave_nfe):
    """
    Valida a chave da NF-e (44 dígitos) e o dígito verificador.
    
    Args:
        chave_nfe: String com a chave da NF-e (44 dígitos)
        
    Returns:
        bool: True se válida, False caso contrário
    """
    if not chave_nfe or len(chave_nfe) != 44 or not chave_nfe.isdigit():
        return False
    
    # Extrai os 43 primeiros dígitos e o dígito verificador (último dígito)
    chave_43 = chave_nfe[:43]
    dv_informado = int(chave_nfe[43])
    
    # Calcula o dígito verificador usando módulo 11
    soma = 0
    multiplicador = 2
    
    # Percorre os 43 dígitos de trás para frente
    for i in range(42, -1, -1):
        soma += int(chave_43[i]) * multiplicador
        multiplicador += 1
        if multiplicador > 9:
            multiplicador = 2
    
    # Calcula o resto da divisão por 11
    resto = soma % 11
    
    # Se o resto for 0 ou 1, o dígito verificador é 0
    # Caso contrário, é 11 - resto
    if resto < 2:
        dv_calculado = 0
    else:
        dv_calculado = 11 - resto
    
    return dv_calculado == dv_informado


def _processar_linha_1110(linha):
    """
    Processa uma única linha do registro 1110 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |1110|COD_PART|COD_MOD|SER|NUM_DOC|DT_DOC|CHV_NFE|NR_MEMO|QTD|UNID|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |1110|...|)
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
    if reg != "1110":
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
    
    # Extrai todos os campos (10 campos no total)
    cod_part = obter_campo(1)
    cod_mod = obter_campo(2)
    ser = obter_campo(3)
    num_doc = obter_campo(4)
    dt_doc = obter_campo(5)
    chv_nfe = obter_campo(6)
    nr_memo = obter_campo(7)
    qtd = obter_campo(8)
    unid = obter_campo(9)
    
    # Validações básicas dos campos obrigatórios
    # COD_PART: obrigatório, até 60 caracteres
    if not cod_part or len(cod_part) > 60:
        return None
    
    # COD_MOD: obrigatório, valores válidos [01, 1B, 04, 55]
    if not cod_mod or cod_mod not in ["01", "1B", "04", "55"]:
        return None
    
    # SER: obrigatório condicional (geralmente obrigatório, mas pode ser vazio em alguns casos)
    # Vou considerar obrigatório, mas aceitar vazio se necessário
    
    # NUM_DOC: obrigatório, numérico, deve ser maior que 0
    if not num_doc:
        return None
    try:
        num_doc_int = int(num_doc)
        if num_doc_int <= 0:
            return None
    except ValueError:
        return None
    
    # DT_DOC: obrigatório, formato DDMMAAAA
    if not dt_doc:
        return None
    dt_doc_valida, dt_doc_obj = _validar_data(dt_doc)
    if not dt_doc_valida:
        return None
    
    # CHV_NFE: obrigatório condicional (se COD_MOD = 55)
    if cod_mod == "55":
        if not chv_nfe:
            return None
        if not _validar_chave_nfe(chv_nfe):
            return None
    
    # NR_MEMO: obrigatório condicional (se informado, deve ser numérico)
    if nr_memo:
        try:
            float(nr_memo)  # Aceita números inteiros e decimais
        except ValueError:
            return None
    
    # QTD: obrigatório, numérico com até 3 decimais, deve ser maior que 0
    if not qtd:
        return None
    try:
        qtd_float = float(qtd)
        if qtd_float <= 0:
            return None
        # Verifica se tem mais de 3 casas decimais
        partes_decimal = qtd.split('.')
        if len(partes_decimal) == 2 and len(partes_decimal[1]) > 3:
            return None
    except ValueError:
        return None
    
    # UNID: obrigatório, até 6 caracteres
    if not unid or len(unid) > 6:
        return None
    
    # Mapeamento de descrições
    cod_mod_desc = {
        "01": "Nota Fiscal",
        "1B": "Nota Fiscal Avulsa",
        "04": "Nota Fiscal de Produtor",
        "55": "Nota Fiscal Eletrônica"
    }
    
    # Formatação de data para exibição
    def formatar_data(data_str):
        if len(data_str) == 8 and data_str.isdigit():
            return f"{data_str[:2]}/{data_str[2:4]}/{data_str[4:8]}"
        return data_str
    
    # Formatação de quantidade para exibição
    def formatar_qtd(qtd_str):
        try:
            qtd_float = float(qtd_str)
            # Formata com até 3 casas decimais
            return f"{qtd_float:.3f}".rstrip('0').rstrip('.')
        except ValueError:
            return qtd_str
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "COD_PART": {
            "titulo": "Código do participante-Fornecedor da Mercadoria destinada à exportação",
            "valor": cod_part
        },
        "COD_MOD": {
            "titulo": "Código do documento fiscal",
            "valor": cod_mod,
            "descricao": cod_mod_desc.get(cod_mod, "")
        },
        "NUM_DOC": {
            "titulo": "Número do documento fiscal recebido com fins específicos de exportação",
            "valor": num_doc
        },
        "DT_DOC": {
            "titulo": "Data da emissão do documento fiscal recebido com fins específicos de exportação",
            "valor": dt_doc,
            "valor_formatado": formatar_data(dt_doc)
        },
        "QTD": {
            "titulo": "Quantidade do item efetivamente exportado",
            "valor": qtd,
            "valor_formatado": formatar_qtd(qtd)
        },
        "UNID": {
            "titulo": "Unidade do item (Campo 02 do registro 0190)",
            "valor": unid
        }
    }
    
    # Adiciona SER se informado
    if ser:
        resultado["SER"] = {
            "titulo": "Série do documento fiscal recebido com fins específicos de exportação",
            "valor": ser
        }
    
    # Adiciona CHV_NFE se informado (obrigatório quando COD_MOD = 55)
    if chv_nfe:
        resultado["CHV_NFE"] = {
            "titulo": "Chave da Nota Fiscal Eletrônica",
            "valor": chv_nfe
        }
    
    # Adiciona NR_MEMO se informado
    if nr_memo:
        resultado["NR_MEMO"] = {
            "titulo": "Número do Memorando de Exportação",
            "valor": nr_memo
        }
    
    return resultado


def validar_1110_fiscal(linhas):
    """
    Valida uma ou mais linhas do registro 1110 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |1110|COD_PART|COD_MOD|SER|NUM_DOC|DT_DOC|CHV_NFE|NR_MEMO|QTD|UNID|
        
    Returns:
        String JSON com array de objetos contendo os campos validados.
        Cada objeto tem a estrutura {"CAMPO": {"titulo": "...", "valor": "...", "descricao": "..."}}.
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
        resultado = _processar_linha_1110(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
