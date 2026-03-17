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


def _processar_linha_b440(linha):
    """
    Processa uma única linha do registro B440 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |B440|IND_OPER|COD_PART|VL_CONT_RT|VL_BC_ISS_RT|VL_ISS_RT|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |B440|...|)
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
    if reg != "B440":
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
    
    # Extrai todos os campos (6 campos no total)
    ind_oper = obter_campo(1)
    cod_part = obter_campo(2)
    vl_cont_rt = obter_campo(3)
    vl_bc_iss_rt = obter_campo(4)
    vl_iss_rt = obter_campo(5)
    
    # Validações dos campos obrigatórios
    
    # IND_OPER: obrigatório, valores válidos: ["0", "1"]
    if ind_oper not in ["0", "1"]:
        return None
    
    # COD_PART: obrigatório, até 60 caracteres
    if not cod_part:
        return None
    if len(cod_part) > 60:
        return None
    # Nota: Validação contra registro 0150 não pode ser feita diretamente
    
    # VL_CONT_RT: obrigatório, numérico com 2 decimais, não negativo
    if not vl_cont_rt:
        return None
    vl_cont_rt_valido, vl_cont_rt_float, vl_cont_rt_erro = validar_valor_numerico(vl_cont_rt, decimais=2, obrigatorio=True, nao_negativo=True)
    if not vl_cont_rt_valido:
        return None
    
    # VL_BC_ISS_RT: obrigatório, numérico com 2 decimais, não negativo
    if not vl_bc_iss_rt:
        return None
    vl_bc_iss_rt_valido, vl_bc_iss_rt_float, vl_bc_iss_rt_erro = validar_valor_numerico(vl_bc_iss_rt, decimais=2, obrigatorio=True, nao_negativo=True)
    if not vl_bc_iss_rt_valido:
        return None
    
    # VL_ISS_RT: obrigatório, numérico com 2 decimais, não negativo
    if not vl_iss_rt:
        return None
    vl_iss_rt_valido, vl_iss_rt_float, vl_iss_rt_erro = validar_valor_numerico(vl_iss_rt, decimais=2, obrigatorio=True, nao_negativo=True)
    if not vl_iss_rt_valido:
        return None
    
    # Mapeamento de códigos para descrições
    ind_oper_desc = {
        "0": "Aquisição",
        "1": "Prestação"
    }
    
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
        "IND_OPER": {
            "titulo": "Indicador do tipo de operação",
            "valor": ind_oper,
            "descricao": ind_oper_desc.get(ind_oper, "")
        },
        "COD_PART": {
            "titulo": "Código do participante (campo 02 do Registro 0150)",
            "valor": cod_part
        },
        "VL_CONT_RT": {
            "titulo": "Totalização do Valor Contábil das prestações e/ou aquisições do declarante pela combinação de tipo de operação e participante",
            "valor": vl_cont_rt,
            "valor_formatado": formatar_valor(vl_cont_rt)
        },
        "VL_BC_ISS_RT": {
            "titulo": "Totalização do Valor da base de cálculo de retenção do ISS das prestações e/ou aquisições do declarante pela combinação de tipo de operação e participante",
            "valor": vl_bc_iss_rt,
            "valor_formatado": formatar_valor(vl_bc_iss_rt)
        },
        "VL_ISS_RT": {
            "titulo": "Totalização do Valor do ISS retido pelo tomador das prestações e/ou aquisições do declarante pela combinação de tipo de operação e participante",
            "valor": vl_iss_rt,
            "valor_formatado": formatar_valor(vl_iss_rt)
        }
    }
    
    return resultado


def validar_b440(linhas):
    """
    Valida uma ou mais linhas do registro B440 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |B440|IND_OPER|COD_PART|VL_CONT_RT|VL_BC_ISS_RT|VL_ISS_RT|
        
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
        resultado = _processar_linha_b440(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
