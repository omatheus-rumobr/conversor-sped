import re
import json
from datetime import datetime


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


def _processar_linha_1800(linha):
    """
    Processa uma única linha do registro 1800 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |1800|VL_CARGA|VL_PASS|VL_FAT|IND_RAT|VL_ICMS_ANT|VL_BC_ICMS|VL_ICMS_APUR|VL_BC_ICMS_APUR|VL_DIF|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |1800|...|)
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
    if reg != "1800":
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
    vl_carga = obter_campo(1)
    vl_pass = obter_campo(2)
    vl_fat = obter_campo(3)
    ind_rat = obter_campo(4)
    vl_icms_ant = obter_campo(5)
    vl_bc_icms = obter_campo(6)
    vl_icms_apur = obter_campo(7)
    vl_bc_icms_apur = obter_campo(8)
    vl_dif = obter_campo(9)
    
    # Validações dos campos obrigatórios
    
    # VL_CARGA: obrigatório, numérico com 2 decimais, não negativo
    if not vl_carga:
        return None
    vl_carga_valido, vl_carga_float, vl_carga_erro = validar_valor_numerico(vl_carga, decimais=2, obrigatorio=True, nao_negativo=True)
    if not vl_carga_valido:
        return None
    
    # VL_PASS: obrigatório, numérico com 2 decimais, não negativo
    if not vl_pass:
        return None
    vl_pass_valido, vl_pass_float, vl_pass_erro = validar_valor_numerico(vl_pass, decimais=2, obrigatorio=True, nao_negativo=True)
    if not vl_pass_valido:
        return None
    
    # VL_FAT: obrigatório, numérico com 2 decimais, não negativo
    # Deve ser igual a VL_CARGA + VL_PASS
    if not vl_fat:
        return None
    vl_fat_valido, vl_fat_float, vl_fat_erro = validar_valor_numerico(vl_fat, decimais=2, obrigatorio=True, nao_negativo=True)
    if not vl_fat_valido:
        return None
    
    # Validação: VL_FAT = VL_CARGA + VL_PASS (com tolerância para arredondamento)
    soma_calculada = vl_carga_float + vl_pass_float
    if abs(vl_fat_float - soma_calculada) > 0.01:
        return None
    
    # IND_RAT: obrigatório, numérico com 6 decimais
    # Deve ser igual a VL_CARGA / VL_FAT
    if not ind_rat:
        return None
    ind_rat_valido, ind_rat_float, ind_rat_erro = validar_valor_numerico(ind_rat, decimais=6, obrigatorio=True, nao_negativo=True)
    if not ind_rat_valido:
        return None
    
    # Validação: IND_RAT = VL_CARGA / VL_FAT (com tolerância para arredondamento)
    if vl_fat_float > 0:
        ind_rat_calculado = vl_carga_float / vl_fat_float
        if abs(ind_rat_float - ind_rat_calculado) > 0.000001:
            return None
    elif vl_carga_float > 0:
        # Se VL_FAT = 0 mas VL_CARGA > 0, há inconsistência
        return None
    
    # VL_ICMS_ANT: obrigatório, numérico com 2 decimais, não negativo
    if not vl_icms_ant:
        return None
    vl_icms_ant_valido, vl_icms_ant_float, vl_icms_ant_erro = validar_valor_numerico(vl_icms_ant, decimais=2, obrigatorio=True, nao_negativo=True)
    if not vl_icms_ant_valido:
        return None
    
    # VL_BC_ICMS: obrigatório, numérico com 2 decimais, não negativo
    if not vl_bc_icms:
        return None
    vl_bc_icms_valido, vl_bc_icms_float, vl_bc_icms_erro = validar_valor_numerico(vl_bc_icms, decimais=2, obrigatorio=True, nao_negativo=True)
    if not vl_bc_icms_valido:
        return None
    
    # VL_ICMS_APUR: obrigatório, numérico com 2 decimais, não negativo
    # Deve ser igual a IND_RAT * VL_ICMS_ANT
    if not vl_icms_apur:
        return None
    vl_icms_apur_valido, vl_icms_apur_float, vl_icms_apur_erro = validar_valor_numerico(vl_icms_apur, decimais=2, obrigatorio=True, nao_negativo=True)
    if not vl_icms_apur_valido:
        return None
    
    # Validação: VL_ICMS_APUR = IND_RAT * VL_ICMS_ANT (com tolerância para arredondamento)
    vl_icms_apur_calculado = ind_rat_float * vl_icms_ant_float
    if abs(vl_icms_apur_float - vl_icms_apur_calculado) > 0.01:
        return None
    
    # VL_BC_ICMS_APUR: obrigatório, numérico com 2 decimais, não negativo
    # Deve ser igual a IND_RAT * VL_BC_ICMS
    if not vl_bc_icms_apur:
        return None
    vl_bc_icms_apur_valido, vl_bc_icms_apur_float, vl_bc_icms_apur_erro = validar_valor_numerico(vl_bc_icms_apur, decimais=2, obrigatorio=True, nao_negativo=True)
    if not vl_bc_icms_apur_valido:
        return None
    
    # Validação: VL_BC_ICMS_APUR = IND_RAT * VL_BC_ICMS (com tolerância para arredondamento)
    vl_bc_icms_apur_calculado = ind_rat_float * vl_bc_icms_float
    if abs(vl_bc_icms_apur_float - vl_bc_icms_apur_calculado) > 0.01:
        return None
    
    # VL_DIF: obrigatório, numérico com 2 decimais
    # Deve ser igual a VL_ICMS_ANT - VL_ICMS_APUR
    if not vl_dif:
        return None
    vl_dif_valido, vl_dif_float, vl_dif_erro = validar_valor_numerico(vl_dif, decimais=2, obrigatorio=True)
    if not vl_dif_valido:
        return None
    
    # Validação: VL_DIF = VL_ICMS_ANT - VL_ICMS_APUR (com tolerância para arredondamento)
    vl_dif_calculado = vl_icms_ant_float - vl_icms_apur_float
    if abs(vl_dif_float - vl_dif_calculado) > 0.01:
        return None
    
    # Formatação de valores monetários para exibição
    def formatar_valor(valor_str):
        if not valor_str:
            return ""
        try:
            valor_float = float(valor_str)
            return f"{valor_float:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        except ValueError:
            return valor_str
    
    # Formatação de percentual/índice com 6 decimais
    def formatar_indice(valor_str):
        if not valor_str:
            return ""
        try:
            valor_float = float(valor_str)
            return f"{valor_float:,.6f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        except ValueError:
            return valor_str
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "VL_CARGA": {
            "titulo": "Valor das prestações cargas (Tributado)",
            "valor": vl_carga,
            "valor_formatado": formatar_valor(vl_carga)
        },
        "VL_PASS": {
            "titulo": "Valor das prestações passageiros/cargas (Não Tributado)",
            "valor": vl_pass,
            "valor_formatado": formatar_valor(vl_pass)
        },
        "VL_FAT": {
            "titulo": "Valor total do faturamento (VL_CARGA + VL_PASS)",
            "valor": vl_fat,
            "valor_formatado": formatar_valor(vl_fat)
        },
        "IND_RAT": {
            "titulo": "Índice para rateio (VL_CARGA / VL_FAT)",
            "valor": ind_rat,
            "valor_formatado": formatar_indice(ind_rat)
        },
        "VL_ICMS_ANT": {
            "titulo": "Valor total dos créditos do ICMS",
            "valor": vl_icms_ant,
            "valor_formatado": formatar_valor(vl_icms_ant)
        },
        "VL_BC_ICMS": {
            "titulo": "Valor da base de cálculo do ICMS",
            "valor": vl_bc_icms,
            "valor_formatado": formatar_valor(vl_bc_icms)
        },
        "VL_ICMS_APUR": {
            "titulo": "Valor do ICMS apurado no cálculo (IND_RAT x VL_ICMS_ANT)",
            "valor": vl_icms_apur,
            "valor_formatado": formatar_valor(vl_icms_apur)
        },
        "VL_BC_ICMS_APUR": {
            "titulo": "Valor da base de cálculo do ICMS apurada (IND_RAT x VL_BC_ICMS)",
            "valor": vl_bc_icms_apur,
            "valor_formatado": formatar_valor(vl_bc_icms_apur)
        },
        "VL_DIF": {
            "titulo": "Valor da diferença a ser levada a estorno de crédito na apuração (VL_ICMS_ANT - VL_ICMS_APUR)",
            "valor": vl_dif,
            "valor_formatado": formatar_valor(vl_dif)
        }
    }
    
    return resultado


def validar_1800_fiscal(linhas):
    """
    Valida uma ou mais linhas do registro 1800 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |1800|VL_CARGA|VL_PASS|VL_FAT|IND_RAT|VL_ICMS_ANT|VL_BC_ICMS|VL_ICMS_APUR|VL_BC_ICMS_APUR|VL_DIF|
        
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
        resultado = _processar_linha_1800(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
