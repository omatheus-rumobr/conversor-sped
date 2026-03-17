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


def _processar_linha_d140(linha):
    """
    Processa uma única linha do registro D140 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |D140|COD_PART_CONSG|COD_MUN_ORIG|COD_MUN_DEST|IND_VEIC|VEIC_ID|IND_NAV|VIAGEM|VL_FRT_LIQ|VL_DESP_PORT|VL_DESP_CAR_DESC|VL_OUT|VL_FRT_BRT|VL_FRT_MM|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |D140|...|)
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
    if reg != "D140":
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
    
    # Extrai todos os campos (14 campos no total)
    cod_part_consg = obter_campo(1)
    cod_mun_orig = obter_campo(2)
    cod_mun_dest = obter_campo(3)
    ind_veic = obter_campo(4)
    veic_id = obter_campo(5)
    ind_nav = obter_campo(6)
    viagem = obter_campo(7)
    vl_frt_liq = obter_campo(8)
    vl_desp_port = obter_campo(9)
    vl_desp_car_desc = obter_campo(10)
    vl_out = obter_campo(11)
    vl_frt_brt = obter_campo(12)
    vl_frt_mm = obter_campo(13)
    
    # Validações dos campos obrigatórios
    
    # COD_PART_CONSG: opcional condicional, até 60 caracteres
    if cod_part_consg and len(cod_part_consg) > 60:
        return None
    
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
    
    # IND_VEIC: obrigatório, valores válidos: ["0", "1"]
    if ind_veic not in ["0", "1"]:
        return None
    
    # VEIC_ID: opcional condicional (sem validação específica de formato no manual)
    
    # IND_NAV: obrigatório, valores válidos: ["0", "1"]
    if ind_nav not in ["0", "1"]:
        return None
    
    # VIAGEM: opcional condicional (sem validação específica de formato no manual)
    
    # VL_FRT_LIQ: obrigatório, numérico com 2 decimais, não negativo
    vl_frt_liq_valido, vl_frt_liq_float, _ = validar_valor_numerico(vl_frt_liq, decimais=2, obrigatorio=True, nao_negativo=True)
    if not vl_frt_liq_valido:
        return None
    
    # VL_DESP_PORT: opcional, numérico com 2 decimais, não negativo
    vl_desp_port_valido, vl_desp_port_float, _ = validar_valor_numerico(vl_desp_port, decimais=2, obrigatorio=False, nao_negativo=True)
    if not vl_desp_port_valido:
        return None
    
    # VL_DESP_CAR_DESC: opcional, numérico com 2 decimais, não negativo
    vl_desp_car_desc_valido, vl_desp_car_desc_float, _ = validar_valor_numerico(vl_desp_car_desc, decimais=2, obrigatorio=False, nao_negativo=True)
    if not vl_desp_car_desc_valido:
        return None
    
    # VL_OUT: opcional, numérico com 2 decimais, não negativo
    vl_out_valido, vl_out_float, _ = validar_valor_numerico(vl_out, decimais=2, obrigatorio=False, nao_negativo=True)
    if not vl_out_valido:
        return None
    
    # VL_FRT_BRT: obrigatório, numérico com 2 decimais, não negativo
    vl_frt_brt_valido, vl_frt_brt_float, _ = validar_valor_numerico(vl_frt_brt, decimais=2, obrigatorio=True, nao_negativo=True)
    if not vl_frt_brt_valido:
        return None
    
    # VL_FRT_MM: opcional, numérico com 2 decimais, não negativo
    vl_frt_mm_valido, vl_frt_mm_float, _ = validar_valor_numerico(vl_frt_mm, decimais=2, obrigatorio=False, nao_negativo=True)
    if not vl_frt_mm_valido:
        return None
    
    # Mapeamento de códigos para descrições
    ind_veic_desc = {
        "0": "Embarcação",
        "1": "Empurrador/rebocador"
    }
    
    ind_nav_desc = {
        "0": "Interior",
        "1": "Cabotagem"
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
        "COD_PART_CONSG": {
            "titulo": "Código do participante (consignatário)",
            "valor": cod_part_consg if cod_part_consg else ""
        },
        "COD_MUN_ORIG": {
            "titulo": "Código do município de origem do serviço",
            "valor": cod_mun_orig
        },
        "COD_MUN_DEST": {
            "titulo": "Código do município de destino",
            "valor": cod_mun_dest
        },
        "IND_VEIC": {
            "titulo": "Indicador do tipo do veículo transportador",
            "valor": ind_veic,
            "descricao": ind_veic_desc.get(ind_veic, "")
        },
        "VEIC_ID": {
            "titulo": "Identificação da embarcação (IRIM ou Registro CPP)",
            "valor": veic_id if veic_id else ""
        },
        "IND_NAV": {
            "titulo": "Indicador do tipo da navegação",
            "valor": ind_nav,
            "descricao": ind_nav_desc.get(ind_nav, "")
        },
        "VIAGEM": {
            "titulo": "Número da viagem",
            "valor": viagem if viagem else ""
        },
        "VL_FRT_LIQ": {
            "titulo": "Valor líquido do frete",
            "valor": vl_frt_liq,
            "valor_formatado": formatar_valor_monetario(vl_frt_liq_float)
        },
        "VL_DESP_PORT": {
            "titulo": "Valor das despesas portuárias",
            "valor": vl_desp_port if vl_desp_port else "",
            "valor_formatado": formatar_valor_monetario(vl_desp_port_float) if vl_desp_port else ""
        },
        "VL_DESP_CAR_DESC": {
            "titulo": "Valor das despesas com carga e descarga",
            "valor": vl_desp_car_desc if vl_desp_car_desc else "",
            "valor_formatado": formatar_valor_monetario(vl_desp_car_desc_float) if vl_desp_car_desc else ""
        },
        "VL_OUT": {
            "titulo": "Outros valores",
            "valor": vl_out if vl_out else "",
            "valor_formatado": formatar_valor_monetario(vl_out_float) if vl_out else ""
        },
        "VL_FRT_BRT": {
            "titulo": "Valor bruto do frete",
            "valor": vl_frt_brt,
            "valor_formatado": formatar_valor_monetario(vl_frt_brt_float)
        },
        "VL_FRT_MM": {
            "titulo": "Valor adicional do frete para renovação da Marinha Mercante",
            "valor": vl_frt_mm if vl_frt_mm else "",
            "valor_formatado": formatar_valor_monetario(vl_frt_mm_float) if vl_frt_mm else ""
        }
    }
    
    return resultado


def validar_d140(linhas):
    """
    Valida uma ou mais linhas do registro D140 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |D140|COD_PART_CONSG|COD_MUN_ORIG|COD_MUN_DEST|IND_VEIC|VEIC_ID|IND_NAV|VIAGEM|VL_FRT_LIQ|VL_DESP_PORT|VL_DESP_CAR_DESC|VL_OUT|VL_FRT_BRT|VL_FRT_MM|
        
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
        resultado = _processar_linha_d140(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
