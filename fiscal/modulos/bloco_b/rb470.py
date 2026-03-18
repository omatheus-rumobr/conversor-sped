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


def _processar_linha_b470(linha):
    """
    Processa uma única linha do registro B470 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |B470|VL_CONT|VL_MAT_TERC|VL_MAT_PROP|VL_SUB|VL_ISNT|VL_DED_BC|VL_BC_ISS|VL_BC_ISS_RT|VL_ISS|VL_ISS_RT|VL_DED|VL_ISS_REC|VL_ISS_ST|VL_ISS_REC_UNI|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |B470|...|)
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
    if reg != "B470":
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
    
    # Extrai todos os campos (15 campos no total)
    vl_cont = obter_campo(1)
    vl_mat_terc = obter_campo(2)
    vl_mat_prop = obter_campo(3)
    vl_sub = obter_campo(4)
    vl_isnt = obter_campo(5)
    vl_ded_bc = obter_campo(6)
    vl_bc_iss = obter_campo(7)
    vl_bc_iss_rt = obter_campo(8)
    vl_iss = obter_campo(9)
    vl_iss_rt = obter_campo(10)
    vl_ded = obter_campo(11)
    vl_iss_rec = obter_campo(12)
    vl_iss_st = obter_campo(13)
    vl_iss_rec_uni = obter_campo(14)
    
    # Todos os campos são obrigatórios e numéricos com 2 decimais, não negativos
    campos_valor = {
        "VL_CONT": vl_cont,
        "VL_MAT_TERC": vl_mat_terc,
        "VL_MAT_PROP": vl_mat_prop,
        "VL_SUB": vl_sub,
        "VL_ISNT": vl_isnt,
        "VL_DED_BC": vl_ded_bc,
        "VL_BC_ISS": vl_bc_iss,
        "VL_BC_ISS_RT": vl_bc_iss_rt,
        "VL_ISS": vl_iss,
        "VL_ISS_RT": vl_iss_rt,
        "VL_DED": vl_ded,
        "VL_ISS_REC": vl_iss_rec,
        "VL_ISS_ST": vl_iss_st,
        "VL_ISS_REC_UNI": vl_iss_rec_uni
    }
    
    valores = {}
    for campo_nome, campo_valor in campos_valor.items():
        if not campo_valor:
            return None
        campo_valido, campo_float, campo_erro = validar_valor_numerico(campo_valor, decimais=2, obrigatorio=True, nao_negativo=True)
        if not campo_valido:
            return None
        valores[campo_nome] = campo_float
    
    # Validações de cálculos
    
    # VL_DED_BC = VL_MAT_TERC + VL_MAT_PROP + VL_SUB + VL_ISNT
    vl_ded_bc_calculado = valores["VL_MAT_TERC"] + valores["VL_MAT_PROP"] + valores["VL_SUB"] + valores["VL_ISNT"]
    if abs(valores["VL_DED_BC"] - vl_ded_bc_calculado) > 0.01:  # Tolerância para arredondamento
        return None
    
    # VL_ISS_REC = VL_ISS - VL_ISS_RT - VL_DED (se >= 0, senão 0)
    vl_iss_rec_calculado = valores["VL_ISS"] - valores["VL_ISS_RT"] - valores["VL_DED"]
    if vl_iss_rec_calculado < 0:
        vl_iss_rec_calculado = 0.0
    if abs(valores["VL_ISS_REC"] - vl_iss_rec_calculado) > 0.01:  # Tolerância para arredondamento
        return None
    
    # Nota: As outras validações requerem acesso a outros registros:
    # - VL_CONT contra registros B420
    # - VL_ISNT contra registros B420
    # - VL_BC_ISS contra registros B420
    # - VL_BC_ISS_RT contra registros B440 com IND_OPER=1
    # - VL_ISS contra registros B420
    # - VL_ISS_RT contra registros B440 com IND_OPER=1
    # - VL_DED contra registros B460 com IND_OBR=0
    # - VL_ISS_ST contra registros B440 com IND_OPER=0 e B460 com IND_OBR=1
    # - VL_ISS_REC_UNI contra registro B500 e B460 com IND_OBR=2
    
    # Formatação de valores monetários para exibição
    def formatar_valor(valor_str):
        if not valor_str:
            return ""
        try:
            valor_float = float(valor_str)
            return f"{valor_float:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        except ValueError:
            return valor_str
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "VL_CONT": {
            "titulo": "A - Valor total referente às prestações de serviço do período",
            "valor": vl_cont,
            "valor_formatado": formatar_valor(vl_cont)
        },
        "VL_MAT_TERC": {
            "titulo": "B - Valor total do material fornecido por terceiros na prestação do serviço",
            "valor": vl_mat_terc,
            "valor_formatado": formatar_valor(vl_mat_terc)
        },
        "VL_MAT_PROP": {
            "titulo": "C - Valor do material próprio utilizado na prestação do serviço",
            "valor": vl_mat_prop,
            "valor_formatado": formatar_valor(vl_mat_prop)
        },
        "VL_SUB": {
            "titulo": "D - Valor total das subempreitadas",
            "valor": vl_sub,
            "valor_formatado": formatar_valor(vl_sub)
        },
        "VL_ISNT": {
            "titulo": "E - Valor total das operações isentas ou não-tributadas pelo ISS",
            "valor": vl_isnt,
            "valor_formatado": formatar_valor(vl_isnt)
        },
        "VL_DED_BC": {
            "titulo": "F - Valor total das deduções da base de cálculo (B + C + D + E)",
            "valor": vl_ded_bc,
            "valor_formatado": formatar_valor(vl_ded_bc)
        },
        "VL_BC_ISS": {
            "titulo": "G - Valor total da base de cálculo do ISS",
            "valor": vl_bc_iss,
            "valor_formatado": formatar_valor(vl_bc_iss)
        },
        "VL_BC_ISS_RT": {
            "titulo": "H - Valor total da base de cálculo de retenção do ISS referente às prestações do declarante",
            "valor": vl_bc_iss_rt,
            "valor_formatado": formatar_valor(vl_bc_iss_rt)
        },
        "VL_ISS": {
            "titulo": "I - Valor total do ISS destacado",
            "valor": vl_iss,
            "valor_formatado": formatar_valor(vl_iss)
        },
        "VL_ISS_RT": {
            "titulo": "J - Valor total do ISS retido pelo tomador nas prestações do declarante",
            "valor": vl_iss_rt,
            "valor_formatado": formatar_valor(vl_iss_rt)
        },
        "VL_DED": {
            "titulo": "K - Valor total das deduções do ISS próprio",
            "valor": vl_ded,
            "valor_formatado": formatar_valor(vl_ded)
        },
        "VL_ISS_REC": {
            "titulo": "L - Valor total apurado do ISS próprio a recolher (I - J - K)",
            "valor": vl_iss_rec,
            "valor_formatado": formatar_valor(vl_iss_rec)
        },
        "VL_ISS_ST": {
            "titulo": "M - Valor total do ISS substituto a recolher pelas aquisições do declarante (tomador)",
            "valor": vl_iss_st,
            "valor_formatado": formatar_valor(vl_iss_st)
        },
        "VL_ISS_REC_UNI": {
            "titulo": "N - Valor do ISS próprio a recolher pela Sociedade Uniprofissional",
            "valor": vl_iss_rec_uni,
            "valor_formatado": formatar_valor(vl_iss_rec_uni)
        }
    }
    
    return resultado


def validar_b470_fiscal(linhas):
    """
    Valida uma ou mais linhas do registro B470 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |B470|VL_CONT|VL_MAT_TERC|VL_MAT_PROP|VL_SUB|VL_ISNT|VL_DED_BC|VL_BC_ISS|VL_BC_ISS_RT|VL_ISS|VL_ISS_RT|VL_DED|VL_ISS_REC|VL_ISS_ST|VL_ISS_REC_UNI|
        
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
        resultado = _processar_linha_b470(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
