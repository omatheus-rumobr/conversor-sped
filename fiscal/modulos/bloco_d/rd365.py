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


def _processar_linha_d365(linha):
    """
    Processa uma única linha do registro D365 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |D365|COD_TOT_PAR|VLR_ACUM_TOT|NR_TOT|DESCR_NR_TOT|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |D365|...|)
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
    if reg != "D365":
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
    
    # Extrai todos os campos (5 campos no total)
    cod_tot_par = obter_campo(1)
    vlr_acum_tot = obter_campo(2)
    nr_tot = obter_campo(3)
    descr_nr_tot = obter_campo(4)
    
    # Validações dos campos obrigatórios
    
    # COD_TOT_PAR: obrigatório, até 7 caracteres
    if not cod_tot_par or len(cod_tot_par) > 7:
        return None
    
    # VLR_ACUM_TOT: obrigatório, numérico com 2 decimais, não negativo
    vlr_acum_tot_valido, vlr_acum_tot_float, _ = validar_valor_numerico(vlr_acum_tot, decimais=2, obrigatorio=True, nao_negativo=True)
    if not vlr_acum_tot_valido:
        return None
    
    # NR_TOT: opcional condicional, numérico, até 2 dígitos, maior que zero
    if nr_tot:
        if not nr_tot.isdigit() or len(nr_tot) > 2 or int(nr_tot) <= 0:
            return None
    
    # DESCR_NR_TOT: opcional condicional, só deve ser preenchido se NR_TOT estiver preenchido
    if descr_nr_tot and not nr_tot:
        return None
    
    # Formatação de valores monetários
    def formatar_valor_monetario(valor_float):
        if valor_float is None:
            return ""
        return f"R$ {valor_float:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "COD_TOT_PAR": {
            "titulo": "Código do totalizador, conforme Tabela 4.4.6",
            "valor": cod_tot_par
        },
        "VLR_ACUM_TOT": {
            "titulo": "Valor acumulado no totalizador, relativo à respectiva Redução Z",
            "valor": vlr_acum_tot,
            "valor_formatado": formatar_valor_monetario(vlr_acum_tot_float)
        },
        "NR_TOT": {
            "titulo": "Número do totalizador quando ocorrer mais de uma situação com a mesma carga tributária efetiva",
            "valor": nr_tot if nr_tot else ""
        },
        "DESCR_NR_TOT": {
            "titulo": "Descrição da situação tributária relativa ao totalizador parcial, quando houver mais de um com a mesma carga tributária efetiva",
            "valor": descr_nr_tot if descr_nr_tot else ""
        }
    }
    
    return resultado


def validar_d365_fiscal(linhas):
    """
    Valida uma ou mais linhas do registro D365 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |D365|COD_TOT_PAR|VLR_ACUM_TOT|NR_TOT|DESCR_NR_TOT|
        
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
        resultado = _processar_linha_d365(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
