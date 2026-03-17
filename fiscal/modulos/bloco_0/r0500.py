import re
import json
from datetime import datetime


def _validar_data(data_str):
    """
    Valida se a data está no formato ddmmaaaa e se é uma data válida.
    
    Args:
        data_str: String com data no formato ddmmaaaa
        
    Returns:
        tuple: (True/False, datetime object ou None)
    """
    if not data_str or len(data_str) != 8 or not data_str.isdigit():
        return False, None
    
    try:
        dia = int(data_str[:2])
        mes = int(data_str[2:4])
        ano = int(data_str[4:8])
        data_obj = datetime(ano, mes, dia)
        return True, data_obj
    except ValueError:
        return False, None


def _processar_linha_0500(linha):
    """
    Processa uma única linha do registro 0500 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |0500|DT_ALT|COD_NAT_CC|IND_CTA|NÍVEL|COD_CTA|NOME_CTA|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |0500|...|)
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
    if reg != "0500":
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
    dt_alt = obter_campo(1)
    cod_nat_cc = obter_campo(2)
    ind_cta = obter_campo(3)
    nivel = obter_campo(4)
    cod_cta = obter_campo(5)
    nome_cta = obter_campo(6)
    
    # Validações básicas dos campos obrigatórios
    # DT_ALT: obrigatório, formato ddmmaaaa, data válida
    dt_alt_valida, dt_alt_obj = _validar_data(dt_alt)
    if not dt_alt_valida:
        return None
    
    # COD_NAT_CC: obrigatório, valores válidos [01, 02, 03, 04, 05, 09]
    cod_nat_cc_validos = ["01", "02", "03", "04", "05", "09"]
    if cod_nat_cc not in cod_nat_cc_validos:
        return None
    
    # IND_CTA: obrigatório, valores válidos [S, A]
    if ind_cta not in ["S", "A"]:
        return None
    
    # NÍVEL: obrigatório, numérico, 5 dígitos
    if not nivel or not nivel.isdigit() or len(nivel) != 5:
        return None
    
    # COD_CTA: obrigatório, até 60 caracteres
    if not cod_cta or len(cod_cta) > 60:
        return None
    
    # NOME_CTA: obrigatório, até 60 caracteres
    if not nome_cta or len(nome_cta) > 60:
        return None
    
    # Mapeamento de descrições do COD_NAT_CC
    descricoes_cod_nat_cc = {
        "01": "01 - Contas de ativo",
        "02": "02 - Contas de passivo",
        "03": "03 - Patrimônio líquido",
        "04": "04 - Contas de resultado",
        "05": "05 - Contas de compensação",
        "09": "09 - Outras"
    }
    
    # Mapeamento de descrições do IND_CTA
    descricoes_ind_cta = {
        "S": "S - Sintética (grupo de contas)",
        "A": "A - Analítica (conta)"
    }
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "DT_ALT": {
            "titulo": "Data da Inclusão/Alteração",
            "valor": dt_alt
        },
        "COD_NAT_CC": {
            "titulo": "Código da Natureza da Conta/Grupo de Contas",
            "valor": cod_nat_cc,
            "descricao": descricoes_cod_nat_cc.get(cod_nat_cc, f"{cod_nat_cc} - Natureza não identificada")
        },
        "IND_CTA": {
            "titulo": "Indicador do Tipo de Conta",
            "valor": ind_cta,
            "descricao": descricoes_ind_cta.get(ind_cta, f"{ind_cta} - Tipo não identificado")
        },
        "NÍVEL": {
            "titulo": "Nível da Conta Analítica/Grupo de Contas",
            "valor": nivel
        },
        "COD_CTA": {
            "titulo": "Código da Conta Analítica/Grupo de Contas",
            "valor": cod_cta
        },
        "NOME_CTA": {
            "titulo": "Nome da Conta Analítica/Grupo de Contas",
            "valor": nome_cta
        }
    }
    
    return resultado


def validar_0500(linhas):
    """
    Valida uma ou mais linhas do registro 0500 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |0500|DT_ALT|COD_NAT_CC|IND_CTA|NÍVEL|COD_CTA|NOME_CTA|
        
    Returns:
        String JSON com array de objetos contendo os campos validados.
        Cada objeto tem a estrutura {"CAMPO": {"titulo": "...", "valor": "..."}}.
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
        resultado = _processar_linha_0500(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
