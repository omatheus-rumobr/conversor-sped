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


def _processar_linha_1925(linha):
    """
    Processa uma única linha do registro 1925 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |1925|COD_INF_ADIC|VL_INF_ADIC|DESCR_COMPL_AJ|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |1925|...|)
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
    if reg != "1925":
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
    cod_inf_adic = obter_campo(1)
    vl_inf_adic = obter_campo(2)
    descr_compl_aj = obter_campo(3)
    
    # Validações dos campos obrigatórios
    
    # COD_INF_ADIC: obrigatório, até 8 caracteres
    if not cod_inf_adic or len(cod_inf_adic) > 8:
        return None
    
    # VL_INF_ADIC: obrigatório, numérico com 2 decimais
    if not vl_inf_adic:
        return None
    vl_inf_adic_valido, vl_inf_adic_float, vl_inf_adic_erro = validar_valor_numerico(vl_inf_adic, decimais=2, obrigatorio=True)
    if not vl_inf_adic_valido:
        return None
    
    # DESCR_COMPL_AJ: obrigatório condicional (sem limite de tamanho especificado)
    # Não há validação específica além de verificar se está presente quando necessário
    
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
        "COD_INF_ADIC": {
            "titulo": "Código da informação adicional conforme tabela a ser definida pelas SEFAZ, conforme tabela definida no item 5.2",
            "valor": cod_inf_adic
        },
        "VL_INF_ADIC": {
            "titulo": "Valor referente à informação adicional",
            "valor": vl_inf_adic,
            "valor_formatado": formatar_valor(vl_inf_adic)
        },
        "DESCR_COMPL_AJ": {
            "titulo": "Descrição complementar do ajuste",
            "valor": descr_compl_aj if descr_compl_aj else ""
        }
    }
    
    return resultado


def validar_1925(linhas):
    """
    Valida uma ou mais linhas do registro 1925 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |1925|COD_INF_ADIC|VL_INF_ADIC|DESCR_COMPL_AJ|
        
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
        resultado = _processar_linha_1925(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
