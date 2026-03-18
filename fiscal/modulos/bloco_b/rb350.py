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


def _processar_linha_b350(linha):
    """
    Processa uma única linha do registro B350 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |B350|COD_CTD|CTA_ISS|CTA_COSIF|QTD_OCOR|COD_SERV|VL_CONT|VL_BC_ISS|ALIQ_ISS|VL_ISS|COD_INF_OBS|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |B350|...|)
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
    if reg != "B350":
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
    cod_ctd = obter_campo(1)
    cta_iss = obter_campo(2)
    cta_cosif = obter_campo(3)
    qtd_ocor = obter_campo(4)
    cod_serv = obter_campo(5)
    vl_cont = obter_campo(6)
    vl_bc_iss = obter_campo(7)
    aliq_iss = obter_campo(8)
    vl_iss = obter_campo(9)
    cod_inf_obs = obter_campo(10)
    
    # Validações dos campos obrigatórios
    
    # COD_CTD: obrigatório (sem limite de tamanho especificado)
    if not cod_ctd:
        return None
    
    # CTA_ISS: obrigatório (sem limite de tamanho especificado)
    if not cta_iss:
        return None
    
    # CTA_COSIF: obrigatório, 8 dígitos numéricos
    if not cta_cosif:
        return None
    if len(cta_cosif) != 8 or not cta_cosif.isdigit():
        return None
    # Nota: Validação contra Tabela 4.6.2 não pode ser feita diretamente
    
    # QTD_OCOR: obrigatório, numérico, >= 1
    if not qtd_ocor:
        return None
    qtd_ocor_valido, qtd_ocor_int, qtd_ocor_erro = validar_valor_numerico(qtd_ocor, decimais=0, obrigatorio=True, positivo=True)
    if not qtd_ocor_valido:
        return None
    
    # COD_SERV: obrigatório, 4 dígitos numéricos
    if not cod_serv:
        return None
    if len(cod_serv) != 4 or not cod_serv.isdigit():
        return None
    # Nota: Validação contra Tabela 4.6.3 não pode ser feita diretamente
    
    # VL_CONT: obrigatório, numérico com 2 decimais, não negativo
    if not vl_cont:
        return None
    vl_cont_valido, vl_cont_float, vl_cont_erro = validar_valor_numerico(vl_cont, decimais=2, obrigatorio=True, nao_negativo=True)
    if not vl_cont_valido:
        return None
    
    # VL_BC_ISS: obrigatório, numérico com 2 decimais, não negativo
    if not vl_bc_iss:
        return None
    vl_bc_iss_valido, vl_bc_iss_float, vl_bc_iss_erro = validar_valor_numerico(vl_bc_iss, decimais=2, obrigatorio=True, nao_negativo=True)
    if not vl_bc_iss_valido:
        return None
    
    # ALIQ_ISS: obrigatório, numérico com 2 decimais, não negativo, <= 5
    if not aliq_iss:
        return None
    aliq_iss_valido, aliq_iss_float, aliq_iss_erro = validar_valor_numerico(aliq_iss, decimais=2, obrigatorio=True, nao_negativo=True)
    if not aliq_iss_valido:
        return None
    if aliq_iss_float > 5.0:
        return None
    
    # VL_ISS: obrigatório, numérico com 2 decimais, não negativo
    if not vl_iss:
        return None
    vl_iss_valido, vl_iss_float, vl_iss_erro = validar_valor_numerico(vl_iss, decimais=2, obrigatorio=True, nao_negativo=True)
    if not vl_iss_valido:
        return None
    
    # Validação de cálculo: VL_ISS = VL_BC_ISS * ALIQ_ISS
    # Nota: ALIQ_ISS é um percentual, então precisa dividir por 100
    aliq_iss_percentual = aliq_iss_float / 100.0
    vl_iss_calculado = vl_bc_iss_float * aliq_iss_percentual
    if abs(vl_iss_float - vl_iss_calculado) > 0.01:  # Tolerância para arredondamento
        return None
    
    # COD_INF_OBS: opcional condicional, até 60 caracteres
    # Nota: Validação contra registro 0460 não pode ser feita diretamente
    if cod_inf_obs and len(cod_inf_obs) > 60:
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
    
    # Formatação de percentual para exibição
    def formatar_percentual(valor_str):
        if not valor_str:
            return ""
        try:
            valor_float = float(valor_str)
            return f"{valor_float:,.2f}%".replace(',', 'X').replace('.', ',').replace('X', '.')
        except ValueError:
            return valor_str
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "COD_CTD": {
            "titulo": "Código da conta do plano de contas",
            "valor": cod_ctd
        },
        "CTA_ISS": {
            "titulo": "Descrição da conta no plano de contas",
            "valor": cta_iss
        },
        "CTA_COSIF": {
            "titulo": "Código COSIF a que está subordinada a conta do ISS das instituições financeiras",
            "valor": cta_cosif
        },
        "QTD_OCOR": {
            "titulo": "Quantidade de ocorrências na conta",
            "valor": qtd_ocor
        },
        "COD_SERV": {
            "titulo": "Item da lista de serviços, conforme Tabela 4.6.3",
            "valor": cod_serv
        },
        "VL_CONT": {
            "titulo": "Valor contábil",
            "valor": vl_cont,
            "valor_formatado": formatar_valor(vl_cont)
        },
        "VL_BC_ISS": {
            "titulo": "Valor da base de cálculo do ISS",
            "valor": vl_bc_iss,
            "valor_formatado": formatar_valor(vl_bc_iss)
        },
        "ALIQ_ISS": {
            "titulo": "Alíquota do ISS",
            "valor": aliq_iss,
            "valor_formatado": formatar_percentual(aliq_iss)
        },
        "VL_ISS": {
            "titulo": "Valor do ISS",
            "valor": vl_iss,
            "valor_formatado": formatar_valor(vl_iss)
        },
        "COD_INF_OBS": {
            "titulo": "Código da observação do lançamento fiscal (campo 02 do Registro 0460)",
            "valor": cod_inf_obs if cod_inf_obs else ""
        }
    }
    
    return resultado


def validar_b350_fiscal(linhas):
    """
    Valida uma ou mais linhas do registro B350 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |B350|COD_CTD|CTA_ISS|CTA_COSIF|QTD_OCOR|COD_SERV|VL_CONT|VL_BC_ISS|ALIQ_ISS|VL_ISS|COD_INF_OBS|
        
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
        resultado = _processar_linha_b350(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
