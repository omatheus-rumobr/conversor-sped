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


def _processar_linha_b420(linha):
    """
    Processa uma única linha do registro B420 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |B420|VL_CONT|VL_BC_ISS|ALIQ_ISS|VL_ISNT_ISS|VL_ISS|COD_SERV|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |B420|...|)
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
    if reg != "B420":
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
    
    # Extrai todos os campos (7 campos no total)
    vl_cont = obter_campo(1)
    vl_bc_iss = obter_campo(2)
    aliq_iss = obter_campo(3)
    vl_isnt_iss = obter_campo(4)
    vl_iss = obter_campo(5)
    cod_serv = obter_campo(6)
    
    # Validações dos campos obrigatórios
    
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
    
    # VL_ISNT_ISS: obrigatório, numérico com 2 decimais, não negativo
    if not vl_isnt_iss:
        return None
    vl_isnt_iss_valido, vl_isnt_iss_float, vl_isnt_iss_erro = validar_valor_numerico(vl_isnt_iss, decimais=2, obrigatorio=True, nao_negativo=True)
    if not vl_isnt_iss_valido:
        return None
    
    # VL_ISS: obrigatório, numérico com 2 decimais, não negativo
    if not vl_iss:
        return None
    vl_iss_valido, vl_iss_float, vl_iss_erro = validar_valor_numerico(vl_iss, decimais=2, obrigatorio=True, nao_negativo=True)
    if not vl_iss_valido:
        return None
    
    # COD_SERV: obrigatório (sem limite de tamanho especificado)
    if not cod_serv:
        return None
    # Nota: Validação contra Tabela 4.6.3 não pode ser feita diretamente
    
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
        "VL_CONT": {
            "titulo": "Totalização do Valor Contábil das prestações do declarante referente à combinação da alíquota e item da lista",
            "valor": vl_cont,
            "valor_formatado": formatar_valor(vl_cont)
        },
        "VL_BC_ISS": {
            "titulo": "Totalização do Valor da base de cálculo do ISS das prestações do declarante referente à combinação da alíquota e item da lista",
            "valor": vl_bc_iss,
            "valor_formatado": formatar_valor(vl_bc_iss)
        },
        "ALIQ_ISS": {
            "titulo": "Alíquota do ISS",
            "valor": aliq_iss,
            "valor_formatado": formatar_percentual(aliq_iss)
        },
        "VL_ISNT_ISS": {
            "titulo": "Totalização do valor das operações isentas ou não-tributadas pelo ISS referente à combinação da alíquota e item da lista",
            "valor": vl_isnt_iss,
            "valor_formatado": formatar_valor(vl_isnt_iss)
        },
        "VL_ISS": {
            "titulo": "Totalização, por combinação da alíquota e item da lista, do Valor do ISS",
            "valor": vl_iss,
            "valor_formatado": formatar_valor(vl_iss)
        },
        "COD_SERV": {
            "titulo": "Item da lista de serviços, conforme Tabela 4.6.3",
            "valor": cod_serv
        }
    }
    
    return resultado


def validar_b420(linhas):
    """
    Valida uma ou mais linhas do registro B420 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |B420|VL_CONT|VL_BC_ISS|ALIQ_ISS|VL_ISNT_ISS|VL_ISS|COD_SERV|
        
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
        resultado = _processar_linha_b420(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
