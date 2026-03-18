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


def _processar_linha_1920(linha):
    """
    Processa uma única linha do registro 1920 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |1920|VL_TOT_TRANSF_DEBITOS_OA|VL_TOT_AJ_DEBITOS_OA|...|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |1920|...|)
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
    if reg != "1920":
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
    
    # Extrai todos os campos (13 campos no total)
    vl_tot_transf_debitos_oa = obter_campo(1)
    vl_tot_aj_debitos_oa = obter_campo(2)
    vl_estornos_cred_oa = obter_campo(3)
    vl_tot_transf_creditos_oa = obter_campo(4)
    vl_tot_aj_creditos_oa = obter_campo(5)
    vl_estornos_deb_oa = obter_campo(6)
    vl_sld_credor_ant_oa = obter_campo(7)
    vl_sld_apurado_oa = obter_campo(8)
    vl_tot_ded = obter_campo(9)
    vl_icms_recolher_oa = obter_campo(10)
    vl_sld_credor_transp_oa = obter_campo(11)
    deb_esp_oa = obter_campo(12)
    
    # Validações dos campos obrigatórios - todos são numéricos com 2 decimais
    
    # VL_TOT_TRANSF_DEBITOS_OA: obrigatório, numérico com 2 decimais, não negativo
    if not vl_tot_transf_debitos_oa:
        return None
    vl_tot_transf_debitos_oa_valido, vl_tot_transf_debitos_oa_float, _ = validar_valor_numerico(vl_tot_transf_debitos_oa, decimais=2, obrigatorio=True, nao_negativo=True)
    if not vl_tot_transf_debitos_oa_valido:
        return None
    
    # VL_TOT_AJ_DEBITOS_OA: obrigatório, numérico com 2 decimais, não negativo
    if not vl_tot_aj_debitos_oa:
        return None
    vl_tot_aj_debitos_oa_valido, vl_tot_aj_debitos_oa_float, _ = validar_valor_numerico(vl_tot_aj_debitos_oa, decimais=2, obrigatorio=True, nao_negativo=True)
    if not vl_tot_aj_debitos_oa_valido:
        return None
    
    # VL_ESTORNOS_CRED_OA: obrigatório, numérico com 2 decimais, não negativo
    if not vl_estornos_cred_oa:
        return None
    vl_estornos_cred_oa_valido, vl_estornos_cred_oa_float, _ = validar_valor_numerico(vl_estornos_cred_oa, decimais=2, obrigatorio=True, nao_negativo=True)
    if not vl_estornos_cred_oa_valido:
        return None
    
    # VL_TOT_TRANSF_CREDITOS_OA: obrigatório, numérico com 2 decimais, não negativo
    if not vl_tot_transf_creditos_oa:
        return None
    vl_tot_transf_creditos_oa_valido, vl_tot_transf_creditos_oa_float, _ = validar_valor_numerico(vl_tot_transf_creditos_oa, decimais=2, obrigatorio=True, nao_negativo=True)
    if not vl_tot_transf_creditos_oa_valido:
        return None
    
    # VL_TOT_AJ_CREDITOS_OA: obrigatório, numérico com 2 decimais, não negativo
    if not vl_tot_aj_creditos_oa:
        return None
    vl_tot_aj_creditos_oa_valido, vl_tot_aj_creditos_oa_float, _ = validar_valor_numerico(vl_tot_aj_creditos_oa, decimais=2, obrigatorio=True, nao_negativo=True)
    if not vl_tot_aj_creditos_oa_valido:
        return None
    
    # VL_ESTORNOS_DEB_OA: obrigatório, numérico com 2 decimais, não negativo
    if not vl_estornos_deb_oa:
        return None
    vl_estornos_deb_oa_valido, vl_estornos_deb_oa_float, _ = validar_valor_numerico(vl_estornos_deb_oa, decimais=2, obrigatorio=True, nao_negativo=True)
    if not vl_estornos_deb_oa_valido:
        return None
    
    # VL_SLD_CREDOR_ANT_OA: obrigatório, numérico com 2 decimais, não negativo
    if not vl_sld_credor_ant_oa:
        return None
    vl_sld_credor_ant_oa_valido, vl_sld_credor_ant_oa_float, _ = validar_valor_numerico(vl_sld_credor_ant_oa, decimais=2, obrigatorio=True, nao_negativo=True)
    if not vl_sld_credor_ant_oa_valido:
        return None
    
    # VL_SLD_APURADO_OA: obrigatório, numérico com 2 decimais, não negativo
    if not vl_sld_apurado_oa:
        return None
    vl_sld_apurado_oa_valido, vl_sld_apurado_oa_float, _ = validar_valor_numerico(vl_sld_apurado_oa, decimais=2, obrigatorio=True, nao_negativo=True)
    if not vl_sld_apurado_oa_valido:
        return None
    
    # VL_TOT_DED: obrigatório, numérico com 2 decimais, não negativo
    if not vl_tot_ded:
        return None
    vl_tot_ded_valido, vl_tot_ded_float, _ = validar_valor_numerico(vl_tot_ded, decimais=2, obrigatorio=True, nao_negativo=True)
    if not vl_tot_ded_valido:
        return None
    
    # VL_ICMS_RECOLHER_OA: obrigatório, numérico com 2 decimais
    if not vl_icms_recolher_oa:
        return None
    vl_icms_recolher_oa_valido, vl_icms_recolher_oa_float, _ = validar_valor_numerico(vl_icms_recolher_oa, decimais=2, obrigatorio=True)
    if not vl_icms_recolher_oa_valido:
        return None
    
    # VL_SLD_CREDOR_TRANSP_OA: obrigatório, numérico com 2 decimais, não negativo
    if not vl_sld_credor_transp_oa:
        return None
    vl_sld_credor_transp_oa_valido, vl_sld_credor_transp_oa_float, _ = validar_valor_numerico(vl_sld_credor_transp_oa, decimais=2, obrigatorio=True, nao_negativo=True)
    if not vl_sld_credor_transp_oa_valido:
        return None
    
    # DEB_ESP_OA: obrigatório, numérico com 2 decimais, não negativo
    if not deb_esp_oa:
        return None
    deb_esp_oa_valido, deb_esp_oa_float, _ = validar_valor_numerico(deb_esp_oa, decimais=2, obrigatorio=True, nao_negativo=True)
    if not deb_esp_oa_valido:
        return None
    
    # Validações de cálculos
    
    # Cálculo do saldo apurado:
    # VL_SLD_APURADO_OA = (VL_TOT_TRANSF_DEBITOS_OA + VL_TOT_AJ_DEBITOS_OA + VL_ESTORNOS_CRED_OA) 
    #                    - (VL_TOT_TRANSF_CREDITOS_OA + VL_TOT_AJ_CREDITOS_OA + VL_ESTORNOS_DEB_OA + VL_SLD_CREDOR_ANT_OA)
    total_debitos = vl_tot_transf_debitos_oa_float + vl_tot_aj_debitos_oa_float + vl_estornos_cred_oa_float
    total_creditos = vl_tot_transf_creditos_oa_float + vl_tot_aj_creditos_oa_float + vl_estornos_deb_oa_float + vl_sld_credor_ant_oa_float
    saldo_calculado = total_debitos - total_creditos
    
    # Se saldo_calculado >= 0, então VL_SLD_APURADO_OA = saldo_calculado e VL_SLD_CREDOR_TRANSP_OA = 0
    # Se saldo_calculado < 0, então VL_SLD_APURADO_OA = 0 e VL_SLD_CREDOR_TRANSP_OA = abs(saldo_calculado)
    if saldo_calculado >= 0:
        if abs(vl_sld_apurado_oa_float - saldo_calculado) > 0.01:
            return None
        if abs(vl_sld_credor_transp_oa_float - 0.0) > 0.01:
            return None
    else:
        if abs(vl_sld_apurado_oa_float - 0.0) > 0.01:
            return None
        if abs(vl_sld_credor_transp_oa_float - abs(saldo_calculado)) > 0.01:
            return None
    
    # Validação: VL_ICMS_RECOLHER_OA = VL_SLD_APURADO_OA - VL_TOT_DED
    vl_icms_recolher_oa_calculado = vl_sld_apurado_oa_float - vl_tot_ded_float
    if abs(vl_icms_recolher_oa_float - vl_icms_recolher_oa_calculado) > 0.01:
        return None
    
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
        "VL_TOT_TRANSF_DEBITOS_OA": {
            "titulo": "Valor total dos débitos por \"Saídas e prestações com débito do imposto\"",
            "valor": vl_tot_transf_debitos_oa,
            "valor_formatado": formatar_valor(vl_tot_transf_debitos_oa)
        },
        "VL_TOT_AJ_DEBITOS_OA": {
            "titulo": "Valor total de \"Ajustes a débito\"",
            "valor": vl_tot_aj_debitos_oa,
            "valor_formatado": formatar_valor(vl_tot_aj_debitos_oa)
        },
        "VL_ESTORNOS_CRED_OA": {
            "titulo": "Valor total de Ajustes \"Estornos de créditos\"",
            "valor": vl_estornos_cred_oa,
            "valor_formatado": formatar_valor(vl_estornos_cred_oa)
        },
        "VL_TOT_TRANSF_CREDITOS_OA": {
            "titulo": "Valor total dos créditos por \"Entradas e aquisições com crédito do imposto\"",
            "valor": vl_tot_transf_creditos_oa,
            "valor_formatado": formatar_valor(vl_tot_transf_creditos_oa)
        },
        "VL_TOT_AJ_CREDITOS_OA": {
            "titulo": "Valor total de \"Ajustes a crédito\"",
            "valor": vl_tot_aj_creditos_oa,
            "valor_formatado": formatar_valor(vl_tot_aj_creditos_oa)
        },
        "VL_ESTORNOS_DEB_OA": {
            "titulo": "Valor total de Ajustes \"Estornos de Débitos\"",
            "valor": vl_estornos_deb_oa,
            "valor_formatado": formatar_valor(vl_estornos_deb_oa)
        },
        "VL_SLD_CREDOR_ANT_OA": {
            "titulo": "Valor total de \"Saldo credor do período anterior\"",
            "valor": vl_sld_credor_ant_oa,
            "valor_formatado": formatar_valor(vl_sld_credor_ant_oa)
        },
        "VL_SLD_APURADO_OA": {
            "titulo": "Valor do saldo devedor apurado",
            "valor": vl_sld_apurado_oa,
            "valor_formatado": formatar_valor(vl_sld_apurado_oa)
        },
        "VL_TOT_DED": {
            "titulo": "Valor total de \"Deduções\"",
            "valor": vl_tot_ded,
            "valor_formatado": formatar_valor(vl_tot_ded)
        },
        "VL_ICMS_RECOLHER_OA": {
            "titulo": "Valor total de \"ICMS a recolher (VL_SLD_APURADO_OA - VL_TOT_DED)\"",
            "valor": vl_icms_recolher_oa,
            "valor_formatado": formatar_valor(vl_icms_recolher_oa)
        },
        "VL_SLD_CREDOR_TRANSP_OA": {
            "titulo": "Valor total de \"Saldo credor a transportar para o período seguinte\"",
            "valor": vl_sld_credor_transp_oa,
            "valor_formatado": formatar_valor(vl_sld_credor_transp_oa)
        },
        "DEB_ESP_OA": {
            "titulo": "Valores recolhidos ou a recolher, extra-apuração",
            "valor": deb_esp_oa,
            "valor_formatado": formatar_valor(deb_esp_oa)
        }
    }
    
    return resultado


def validar_1920_fiscal(linhas):
    """
    Valida uma ou mais linhas do registro 1920 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |1920|VL_TOT_TRANSF_DEBITOS_OA|...|
        
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
        resultado = _processar_linha_1920(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
