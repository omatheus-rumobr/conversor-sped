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


def _processar_linha_d737(linha):
    """
    Processa uma única linha do registro D737 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |D737|COD_AJ|DESCR_COMPL_AJ|COD_ITEM|VL_BC_ICMS|ALIQ_ICMS|VL_ICMS|VL_OUTROS|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |D737|...|)
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
    if reg != "D737":
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
    
    # Extrai todos os campos (8 campos no total)
    cod_aj = obter_campo(1)
    descr_compl_aj = obter_campo(2)
    cod_item = obter_campo(3)
    vl_bc_icms = obter_campo(4)
    aliq_icms = obter_campo(5)
    vl_icms = obter_campo(6)
    vl_outros = obter_campo(7)
    
    # Validações dos campos obrigatórios
    
    # COD_AJ: obrigatório, até 10 caracteres
    # Verifica se o COD_AJ está de acordo com a Tabela 5.3 da UF do informante do arquivo (validação não pode ser feita aqui)
    if not cod_aj:
        return None
    if len(cod_aj) > 10:
        return None
    
    # DESCR_COMPL_AJ: opcional condicional
    # Sem prejuízo de outras situações definidas em legislação específica, o contribuinte deverá fazer a descrição complementar de ajustes (tabela 5.3) sempre que informar códigos genéricos
    if descr_compl_aj and not descr_compl_aj.strip():
        return None
    
    # COD_ITEM: opcional condicional, até 60 caracteres
    # Pode ser informado se o ajuste/benefício for relacionado ao serviço constante na nota fiscal de serviço de comunicação
    # O COD_ITEM deverá ser informado no registro 0200 (validação não pode ser feita aqui)
    if cod_item and len(cod_item) > 60:
        return None
    
    # VL_BC_ICMS: opcional condicional, numérico com 2 decimais, não negativo
    vl_bc_icms_valido, vl_bc_icms_float, _ = validar_valor_numerico(vl_bc_icms, decimais=2, obrigatorio=False, nao_negativo=True)
    if not vl_bc_icms_valido:
        return None
    
    # ALIQ_ICMS: opcional condicional, numérico com 2 decimais, não negativo
    aliq_icms_valido, aliq_icms_float, _ = validar_valor_numerico(aliq_icms, decimais=2, obrigatorio=False, nao_negativo=True)
    if not aliq_icms_valido:
        return None
    
    # VL_ICMS: opcional condicional, numérico com 2 decimais, não negativo
    # Valor do montante do ajuste do imposto. Os dados que gerarem crédito ou débito serão somados na apuração
    vl_icms_valido, vl_icms_float, _ = validar_valor_numerico(vl_icms, decimais=2, obrigatorio=False, nao_negativo=True)
    if not vl_icms_valido:
        return None
    
    # VL_OUTROS: opcional condicional, numérico com 2 decimais, não negativo
    # Preencher com outros valores, quando o código do ajuste for informativo, conforme Tabela 5.3
    vl_outros_valido, vl_outros_float, _ = validar_valor_numerico(vl_outros, decimais=2, obrigatorio=False, nao_negativo=True)
    if not vl_outros_valido:
        return None
    
    # Formatação de valores monetários
    def formatar_valor_monetario(valor_float):
        if valor_float is None:
            return ""
        return f"R$ {valor_float:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    # Formatação de percentual
    def formatar_percentual(valor_float):
        if valor_float is None:
            return ""
        return f"{valor_float:.2f}%"
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "COD_AJ": {
            "titulo": "Código do ajustes/benefício/incentivo, conforme tabela indicada no item 5.3",
            "valor": cod_aj
        },
        "DESCR_COMPL_AJ": {
            "titulo": "Descrição complementar do ajuste do documento fiscal",
            "valor": descr_compl_aj if descr_compl_aj else ""
        },
        "COD_ITEM": {
            "titulo": "Código do item (campo 02 do Registro 0200)",
            "valor": cod_item if cod_item else ""
        },
        "VL_BC_ICMS": {
            "titulo": "Base de cálculo do ICMS",
            "valor": vl_bc_icms if vl_bc_icms else "",
            "valor_formatado": formatar_valor_monetario(vl_bc_icms_float) if vl_bc_icms else ""
        },
        "ALIQ_ICMS": {
            "titulo": "Alíquota do ICMS",
            "valor": aliq_icms if aliq_icms else "",
            "valor_formatado": formatar_percentual(aliq_icms_float) if aliq_icms else ""
        },
        "VL_ICMS": {
            "titulo": "Valor do ICMS",
            "valor": vl_icms if vl_icms else "",
            "valor_formatado": formatar_valor_monetario(vl_icms_float) if vl_icms else ""
        },
        "VL_OUTROS": {
            "titulo": "Outros valores",
            "valor": vl_outros if vl_outros else "",
            "valor_formatado": formatar_valor_monetario(vl_outros_float) if vl_outros else ""
        }
    }
    
    return resultado


def validar_d737_fiscal(linhas):
    """
    Valida uma ou mais linhas do registro D737 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |D737|COD_AJ|DESCR_COMPL_AJ|COD_ITEM|VL_BC_ICMS|ALIQ_ICMS|VL_ICMS|VL_OUTROS|
        
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
        resultado = _processar_linha_d737(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
