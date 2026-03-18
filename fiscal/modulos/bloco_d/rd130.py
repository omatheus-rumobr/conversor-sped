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


def _processar_linha_d130(linha):
    """
    Processa uma única linha do registro D130 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |D130|COD_PART_CONSG|COD_PART_RED|IND_FRT_RED|COD_MUN_ORIG|COD_MUN_DEST|VEIC_ID|VL_LIQ_FRT|VL_SEC_CAT|VL_DESP|VL_PEDG|VL_OUT|VL_FRT|UF_ID|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |D130|...|)
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
    if reg != "D130":
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
    cod_part_red = obter_campo(2)
    ind_frt_red = obter_campo(3)
    cod_mun_orig = obter_campo(4)
    cod_mun_dest = obter_campo(5)
    veic_id = obter_campo(6)
    vl_liq_frt = obter_campo(7)
    vl_sec_cat = obter_campo(8)
    vl_desp = obter_campo(9)
    vl_pedg = obter_campo(10)
    vl_out = obter_campo(11)
    vl_frt = obter_campo(12)
    uf_id = obter_campo(13)
    
    # Validações dos campos obrigatórios
    
    # COD_PART_CONSG: opcional condicional, até 60 caracteres
    if cod_part_consg and len(cod_part_consg) > 60:
        return None
    
    # COD_PART_RED: opcional condicional, até 60 caracteres
    if cod_part_red and len(cod_part_red) > 60:
        return None
    
    # IND_FRT_RED: obrigatório, valores válidos: ["0", "1", "2", "9"]
    if ind_frt_red not in ["0", "1", "2", "9"]:
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
    
    # VEIC_ID: opcional condicional, até 7 caracteres
    if veic_id and len(veic_id) > 7:
        return None
    
    # VL_LIQ_FRT: obrigatório, numérico com 2 decimais, não negativo
    # Nota: A validação de "maior que zero se IND_FRT do D100 != 9" não pode ser feita aqui sem acesso ao registro D100
    vl_liq_frt_valido, vl_liq_frt_float, _ = validar_valor_numerico(vl_liq_frt, decimais=2, obrigatorio=True, nao_negativo=True)
    if not vl_liq_frt_valido:
        return None
    
    # VL_SEC_CAT: opcional, numérico com 2 decimais, não negativo
    vl_sec_cat_valido, vl_sec_cat_float, _ = validar_valor_numerico(vl_sec_cat, decimais=2, obrigatorio=False, nao_negativo=True)
    if not vl_sec_cat_valido:
        return None
    
    # VL_DESP: opcional, numérico com 2 decimais, não negativo
    vl_desp_valido, vl_desp_float, _ = validar_valor_numerico(vl_desp, decimais=2, obrigatorio=False, nao_negativo=True)
    if not vl_desp_valido:
        return None
    
    # VL_PEDG: opcional, numérico com 2 decimais, não negativo
    vl_pedg_valido, vl_pedg_float, _ = validar_valor_numerico(vl_pedg, decimais=2, obrigatorio=False, nao_negativo=True)
    if not vl_pedg_valido:
        return None
    
    # VL_OUT: opcional, numérico com 2 decimais, não negativo
    vl_out_valido, vl_out_float, _ = validar_valor_numerico(vl_out, decimais=2, obrigatorio=False, nao_negativo=True)
    if not vl_out_valido:
        return None
    
    # VL_FRT: obrigatório, numérico com 2 decimais, não negativo
    # Nota: A validação de "maior que zero se IND_FRT do D100 != 9" não pode ser feita aqui sem acesso ao registro D100
    vl_frt_valido, vl_frt_float, _ = validar_valor_numerico(vl_frt, decimais=2, obrigatorio=True, nao_negativo=True)
    if not vl_frt_valido:
        return None
    
    # UF_ID: opcional condicional, 2 caracteres
    if uf_id and len(uf_id) > 2:
        return None
    
    # Mapeamento de códigos para descrições
    ind_frt_red_desc = {
        "0": "Sem redespacho",
        "1": "Por conta do emitente",
        "2": "Por conta do destinatário",
        "9": "Outros"
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
        "COD_PART_RED": {
            "titulo": "Código do participante (redespachado)",
            "valor": cod_part_red if cod_part_red else ""
        },
        "IND_FRT_RED": {
            "titulo": "Indicador do tipo do frete da operação de redespacho",
            "valor": ind_frt_red,
            "descricao": ind_frt_red_desc.get(ind_frt_red, "")
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
            "titulo": "Placa de identificação do veículo",
            "valor": veic_id if veic_id else ""
        },
        "VL_LIQ_FRT": {
            "titulo": "Valor líquido do frete",
            "valor": vl_liq_frt,
            "valor_formatado": formatar_valor_monetario(vl_liq_frt_float)
        },
        "VL_SEC_CAT": {
            "titulo": "Soma de valores de Sec/Cat (serviços de coleta/custo adicional de transporte)",
            "valor": vl_sec_cat if vl_sec_cat else "",
            "valor_formatado": formatar_valor_monetario(vl_sec_cat_float) if vl_sec_cat else ""
        },
        "VL_DESP": {
            "titulo": "Soma de valores de despacho",
            "valor": vl_desp if vl_desp else "",
            "valor_formatado": formatar_valor_monetario(vl_desp_float) if vl_desp else ""
        },
        "VL_PEDG": {
            "titulo": "Soma dos valores de pedágio",
            "valor": vl_pedg if vl_pedg else "",
            "valor_formatado": formatar_valor_monetario(vl_pedg_float) if vl_pedg else ""
        },
        "VL_OUT": {
            "titulo": "Outros valores",
            "valor": vl_out if vl_out else "",
            "valor_formatado": formatar_valor_monetario(vl_out_float) if vl_out else ""
        },
        "VL_FRT": {
            "titulo": "Valor total do frete",
            "valor": vl_frt,
            "valor_formatado": formatar_valor_monetario(vl_frt_float)
        },
        "UF_ID": {
            "titulo": "Sigla da UF da placa do veículo",
            "valor": uf_id if uf_id else ""
        }
    }
    
    return resultado


def validar_d130_fiscal(linhas):
    """
    Valida uma ou mais linhas do registro D130 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |D130|COD_PART_CONSG|COD_PART_RED|IND_FRT_RED|COD_MUN_ORIG|COD_MUN_DEST|VEIC_ID|VL_LIQ_FRT|VL_SEC_CAT|VL_DESP|VL_PEDG|VL_OUT|VL_FRT|UF_ID|
        
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
        resultado = _processar_linha_d130(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
