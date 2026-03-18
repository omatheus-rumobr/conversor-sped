import re
import json
from datetime import datetime


def _validar_codigo_municipio(cod_mun_str):
    """
    Valida o código do município IBGE (7 dígitos).
    Aceita também códigos especiais: 9999999 (Exterior) e 9999998 (CT-e simplificado).
    
    Args:
        cod_mun_str: String com o código do município
        
    Returns:
        bool: True se válido, False caso contrário
    """
    if not cod_mun_str:
        return False
    
    # Códigos especiais permitidos
    if cod_mun_str in ["9999999", "9999998"]:
        return True
    
    # Deve ter 7 dígitos numéricos
    if len(cod_mun_str) != 7 or not cod_mun_str.isdigit():
        return False
    
    return True


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


def _processar_linha_d150(linha):
    """
    Processa uma única linha do registro D150 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |D150|COD_MUN_ORIG|COD_MUN_DEST|VEIC_ID|VIAGEM|IND_TFA|VL_PESO_TX|VL_TX_TERR|VL_TX_RED|VL_OUT|VL_TX_ADV|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |D150|...|)
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
    if reg != "D150":
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
    cod_mun_orig = obter_campo(1)
    cod_mun_dest = obter_campo(2)
    veic_id = obter_campo(3)
    viagem = obter_campo(4)
    ind_tfa = obter_campo(5)
    vl_peso_tx = obter_campo(6)
    vl_tx_terr = obter_campo(7)
    vl_tx_red = obter_campo(8)
    vl_out = obter_campo(9)
    vl_tx_adv = obter_campo(10)
    
    # Validações dos campos obrigatórios
    
    # COD_MUN_ORIG: obrigatório, 7 dígitos, deve existir na Tabela de Municípios do IBGE (ou 9999999 para Exterior)
    if not cod_mun_orig:
        return None
    if not _validar_codigo_municipio(cod_mun_orig):
        return None
    
    # COD_MUN_DEST: obrigatório, 7 dígitos, deve existir na Tabela de Municípios do IBGE (ou 9999999 para Exterior)
    if not cod_mun_dest:
        return None
    if not _validar_codigo_municipio(cod_mun_dest):
        return None
    
    # VEIC_ID: opcional condicional (sem validação específica de formato no manual)
    
    # VIAGEM: opcional condicional (sem validação específica de formato no manual)
    
    # IND_TFA: obrigatório, valores válidos: ["0", "1", "2", "9"]
    if ind_tfa not in ["0", "1", "2", "9"]:
        return None
    
    # VL_PESO_TX: obrigatório, numérico com 2 decimais, não negativo
    vl_peso_tx_valido, vl_peso_tx_float, _ = validar_valor_numerico(vl_peso_tx, decimais=2, obrigatorio=True, nao_negativo=True)
    if not vl_peso_tx_valido:
        return None
    
    # VL_TX_TERR: opcional, numérico com 2 decimais, não negativo
    vl_tx_terr_valido, vl_tx_terr_float, _ = validar_valor_numerico(vl_tx_terr, decimais=2, obrigatorio=False, nao_negativo=True)
    if not vl_tx_terr_valido:
        return None
    
    # VL_TX_RED: opcional, numérico com 2 decimais, não negativo
    vl_tx_red_valido, vl_tx_red_float, _ = validar_valor_numerico(vl_tx_red, decimais=2, obrigatorio=False, nao_negativo=True)
    if not vl_tx_red_valido:
        return None
    
    # VL_OUT: opcional, numérico com 2 decimais, não negativo
    vl_out_valido, vl_out_float, _ = validar_valor_numerico(vl_out, decimais=2, obrigatorio=False, nao_negativo=True)
    if not vl_out_valido:
        return None
    
    # VL_TX_ADV: opcional, numérico com 2 decimais, não negativo
    vl_tx_adv_valido, vl_tx_adv_float, _ = validar_valor_numerico(vl_tx_adv, decimais=2, obrigatorio=False, nao_negativo=True)
    if not vl_tx_adv_valido:
        return None
    
    # Mapeamento de códigos para descrições
    ind_tfa_desc = {
        "0": "Exp.",
        "1": "Enc.",
        "2": "C.I.",
        "9": "Outra"
    }
    
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
        "COD_MUN_ORIG": {
            "titulo": "Código do município de origem do serviço",
            "valor": cod_mun_orig
        },
        "COD_MUN_DEST": {
            "titulo": "Código do município de destino",
            "valor": cod_mun_dest
        },
        "VEIC_ID": {
            "titulo": "Identificação da aeronave (DAC)",
            "valor": veic_id if veic_id else ""
        },
        "VIAGEM": {
            "titulo": "Número do vôo",
            "valor": viagem if viagem else ""
        },
        "IND_TFA": {
            "titulo": "Indicador do tipo de tarifa aplicada",
            "valor": ind_tfa,
            "descricao": ind_tfa_desc.get(ind_tfa, "")
        },
        "VL_PESO_TX": {
            "titulo": "Peso taxado",
            "valor": vl_peso_tx,
            "valor_formatado": formatar_valor_monetario(vl_peso_tx_float)
        },
        "VL_TX_TERR": {
            "titulo": "Valor da taxa terrestre",
            "valor": vl_tx_terr if vl_tx_terr else "",
            "valor_formatado": formatar_valor_monetario(vl_tx_terr_float) if vl_tx_terr else ""
        },
        "VL_TX_RED": {
            "titulo": "Valor da taxa de redespacho",
            "valor": vl_tx_red if vl_tx_red else "",
            "valor_formatado": formatar_valor_monetario(vl_tx_red_float) if vl_tx_red else ""
        },
        "VL_OUT": {
            "titulo": "Outros valores",
            "valor": vl_out if vl_out else "",
            "valor_formatado": formatar_valor_monetario(vl_out_float) if vl_out else ""
        },
        "VL_TX_ADV": {
            "titulo": "Valor da taxa \"ad valorem\"",
            "valor": vl_tx_adv if vl_tx_adv else "",
            "valor_formatado": formatar_valor_monetario(vl_tx_adv_float) if vl_tx_adv else ""
        }
    }
    
    return resultado


def validar_d150_fiscal(linhas):
    """
    Valida uma ou mais linhas do registro D150 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |D150|COD_MUN_ORIG|COD_MUN_DEST|VEIC_ID|VIAGEM|IND_TFA|VL_PESO_TX|VL_TX_TERR|VL_TX_RED|VL_OUT|VL_TX_ADV|
        
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
        resultado = _processar_linha_d150(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
