import re
import json
from datetime import datetime


def _processar_linha_c190(linha):
    """
    Processa uma única linha do registro C190 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |C190|CST_ICMS|CFOP|ALIQ_ICMS|...| (12 campos)
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |C190|...|)
    if partes and not partes[0]:
        partes = partes[1:]
    if partes and not partes[-1]:
        partes = partes[:-1]
    
    # Verifica se tem pelo menos o campo REG
    if len(partes) < 1:
        return None
    
    # Extrai o campo REG
    reg = partes[0].strip().upper() if partes else ""
    
    # Validação do campo REG
    if reg != "C190":
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
    
    # Extrai todos os campos (12 campos no total)
    cst_icms = obter_campo(1)
    cfop = obter_campo(2)
    aliq_icms = obter_campo(3)
    vl_opr = obter_campo(4)
    vl_bc_icms = obter_campo(5)
    vl_icms = obter_campo(6)
    vl_bc_icms_st = obter_campo(7)
    vl_icms_st = obter_campo(8)
    vl_red_bc = obter_campo(9)
    vl_ipi = obter_campo(10)
    cod_obs = obter_campo(11)
    
    # Validações básicas dos campos obrigatórios
    # CST_ICMS: obrigatório, numérico de até 3 dígitos
    if not cst_icms:
        return None
    try:
        int(cst_icms)
        if len(cst_icms) > 3:
            return None
    except ValueError:
        return None
    
    # CFOP: obrigatório, numérico de 4 dígitos
    if not cfop:
        return None
    try:
        int(cfop)
        if len(cfop) != 4:
            return None
    except ValueError:
        return None
    
    # Validação de valores numéricos (devem ser números válidos se preenchidos)
    def validar_valor(valor_str):
        if not valor_str:
            return True  # Campo opcional
        try:
            float(valor_str.replace(",", "."))
            return True
        except ValueError:
            return False
    
    # Valida valores monetários obrigatórios
    valores_obrigatorios = [vl_opr, vl_bc_icms, vl_icms, vl_bc_icms_st, vl_icms_st, vl_red_bc, vl_ipi]
    for valor in valores_obrigatorios:
        if not valor:
            return None
        if not validar_valor(valor):
            return None
    
    # Valida ALIQ_ICMS (opcional condicional)
    if aliq_icms and not validar_valor(aliq_icms):
        return None
    
    # Monta o dicionário com título e valor
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "CST_ICMS": {
            "titulo": "Código da Situação Tributária",
            "valor": cst_icms
        },
        "CFOP": {
            "titulo": "Código Fiscal de Operação e Prestação do Agrupamento de Itens",
            "valor": cfop
        },
        "ALIQ_ICMS": {
            "titulo": "Alíquota do ICMS",
            "valor": aliq_icms
        },
        "VL_OPR": {
            "titulo": "Valor da Operação na Combinação de CST_ICMS, CFOP e Alíquota do ICMS",
            "valor": vl_opr
        },
        "VL_BC_ICMS": {
            "titulo": "Valor da Base de Cálculo do ICMS",
            "valor": vl_bc_icms
        },
        "VL_ICMS": {
            "titulo": "Valor do ICMS",
            "valor": vl_icms
        },
        "VL_BC_ICMS_ST": {
            "titulo": "Valor da Base de Cálculo do ICMS da Substituição Tributária",
            "valor": vl_bc_icms_st
        },
        "VL_ICMS_ST": {
            "titulo": "Valor Creditado/Debitado do ICMS da Substituição Tributária",
            "valor": vl_icms_st
        },
        "VL_RED_BC": {
            "titulo": "Valor Não Tributado em Função da Redução da Base de Cálculo do ICMS",
            "valor": vl_red_bc
        },
        "VL_IPI": {
            "titulo": "Valor do IPI",
            "valor": vl_ipi
        },
        "COD_OBS": {
            "titulo": "Código da Observação do Lançamento Fiscal",
            "valor": cod_obs
        }
    }
    
    return resultado


def validar_c190(linhas):
    """
    Valida e processa uma ou múltiplas linhas do registro C190 (Registro Analítico do Documento) do SPED.
    
    Este registro tem por objetivo representar a escrituração dos documentos fiscais totalizados por CST, CFOP e Alíquota de ICMS.
    
    Args:
        linhas: Pode ser:
                - Uma string com uma linha do SPED
                - Uma lista de strings (cada string é uma linha)
                - Uma string com múltiplas linhas separadas por \\n
                Formato: |C190|CST_ICMS|CFOP|ALIQ_ICMS|VL_OPR|VL_BC_ICMS|VL_ICMS|VL_BC_ICMS_ST|VL_ICMS_ST|VL_RED_BC|VL_IPI|COD_OBS|
        
    Returns:
        str: JSON com um array contendo os campos validados de cada linha processada.
             Retorna um array vazio [] se nenhuma linha válida for encontrada.
             Retorna None se o input for inválido.
        
    Validações principais:
        - Campo REG deve ser exatamente "C190"
        - CST_ICMS: obrigatório, código de situação tributária (até 3 dígitos)
        - CFOP: obrigatório, código fiscal de operação (4 dígitos)
        - ALIQ_ICMS: opcional condicional, alíquota do ICMS
        - VL_OPR: obrigatório, valor numérico
        - VL_BC_ICMS: obrigatório, valor numérico
        - VL_ICMS: obrigatório, valor numérico
        - VL_BC_ICMS_ST: obrigatório, valor numérico
        - VL_ICMS_ST: obrigatório, valor numérico
        - VL_RED_BC: obrigatório, valor numérico
        - VL_IPI: obrigatório, valor numérico
        - COD_OBS: opcional condicional, código da observação
    """
    if linhas is None:
        return None
    
    # Lista para armazenar as linhas a processar
    linhas_para_processar = []
    
    # Se for uma lista, processa cada item
    if isinstance(linhas, list):
        linhas_para_processar = linhas
    # Se for uma string, verifica se tem múltiplas linhas
    elif isinstance(linhas, str):
        # Se contém \n, divide em linhas
        if '\n' in linhas:
            linhas_para_processar = linhas.split('\n')
        else:
            # String única
            linhas_para_processar = [linhas]
    else:
        return None
    
    # Lista para armazenar os resultados válidos
    resultados = []
    
    # Processa cada linha
    for linha in linhas_para_processar:
        resultado = _processar_linha_c190(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    # Retorna JSON com array de resultados
    return json.dumps(resultados, ensure_ascii=False, indent=2)