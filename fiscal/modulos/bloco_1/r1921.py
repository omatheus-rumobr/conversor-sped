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


def _processar_linha_1921(linha):
    """
    Processa uma única linha do registro 1921 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |1921|COD_AJ_APUR|DESCR_COMPL_AJ|VL_AJ_APUR|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |1921|...|)
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
    if reg != "1921":
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
    
    # Extrai todos os campos (4 campos no total)
    cod_aj_apur = obter_campo(1)
    descr_compl_aj = obter_campo(2)
    vl_aj_apur = obter_campo(3)
    
    # Validações dos campos obrigatórios
    
    # COD_AJ_APUR: obrigatório, até 8 caracteres
    # O terceiro caractere deve ser "0" (zero)
    # O quarto caractere deve ser: "0", "1", "2", "3", "4" ou "5"
    if not cod_aj_apur:
        return None
    if len(cod_aj_apur) > 8:
        return None
    
    # Validação do terceiro caractere (índice 2)
    if len(cod_aj_apur) < 3:
        return None
    if cod_aj_apur[2] != "0":
        return None
    
    # Validação do quarto caractere (índice 3)
    if len(cod_aj_apur) < 4:
        return None
    quarto_caractere_validos = ["0", "1", "2", "3", "4", "5"]
    if cod_aj_apur[3] not in quarto_caractere_validos:
        return None
    
    # DESCR_COMPL_AJ: obrigatório condicional (pode estar vazio)
    # Não há validação específica além de verificar se está presente
    
    # VL_AJ_APUR: obrigatório, numérico com 2 decimais
    if not vl_aj_apur:
        return None
    vl_aj_apur_valido, vl_aj_apur_float, vl_aj_apur_erro = validar_valor_numerico(vl_aj_apur, decimais=2, obrigatorio=True)
    if not vl_aj_apur_valido:
        return None
    
    # Mapeamento do quarto caractere para descrição
    quarto_caractere_desc = {
        "0": "Outros débitos",
        "1": "Estorno de créditos",
        "2": "Outros créditos",
        "3": "Estorno de débitos",
        "4": "Deduções do imposto apurado",
        "5": "Débitos Especiais"
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
        "COD_AJ_APUR": {
            "titulo": "Código do ajuste da SUB-APURAÇÃO e dedução, conforme a Tabela indicada no item 5.1.1",
            "valor": cod_aj_apur,
            "descricao": quarto_caractere_desc.get(cod_aj_apur[3], "") if len(cod_aj_apur) > 3 else ""
        },
        "DESCR_COMPL_AJ": {
            "titulo": "Descrição complementar do ajuste da apuração",
            "valor": descr_compl_aj if descr_compl_aj else ""
        },
        "VL_AJ_APUR": {
            "titulo": "Valor do ajuste da apuração",
            "valor": vl_aj_apur,
            "valor_formatado": formatar_valor(vl_aj_apur)
        }
    }
    
    return resultado


def validar_1921(linhas):
    """
    Valida uma ou mais linhas do registro 1921 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |1921|COD_AJ_APUR|DESCR_COMPL_AJ|VL_AJ_APUR|
        
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
        resultado = _processar_linha_1921(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
