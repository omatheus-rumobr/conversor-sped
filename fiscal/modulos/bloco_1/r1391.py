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


def _processar_linha_1391(linha):
    """
    Processa uma única linha do registro 1391 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |1391|DT_REGISTRO|QTD_MOID|ESTQ_INI|QTD_PRODUZ|ENT_ANID_HID|OUTR_ENTR|PERDA|CONS|SAI_ANI_HID|SAÍDAS|ESTQ_FIN|ESTQ_INI_MEL|PROD_DIA_MEL|UTIL_MEL|PROD_ALC_MEL|OBS|COD_ITEM|TP_RESIDUO|QTD_RESIDUO|QTD_RESIDUO_DDG|QTD_RESIDUO_WDG|QTD_RESIDUO_CANA|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |1391|...|)
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
    if reg != "1391":
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
    
    # Extrai todos os campos (23 campos no total)
    dt_registro = obter_campo(1)
    qtd_moid = obter_campo(2)
    estq_ini = obter_campo(3)
    qtd_produz = obter_campo(4)
    ent_anid_hid = obter_campo(5)
    outr_entr = obter_campo(6)
    perda = obter_campo(7)
    cons = obter_campo(8)
    sai_ani_hid = obter_campo(9)
    saidas = obter_campo(10)
    estq_fin = obter_campo(11)
    estq_ini_mel = obter_campo(12)
    prod_dia_mel = obter_campo(13)
    util_mel = obter_campo(14)
    prod_alc_mel = obter_campo(15)
    obs = obter_campo(16)
    cod_item = obter_campo(17)
    tp_residuo = obter_campo(18)
    qtd_residuo = obter_campo(19)
    qtd_residuo_ddg = obter_campo(20)
    qtd_residuo_wdg = obter_campo(21)
    qtd_residuo_cana = obter_campo(22)
    
    # Validações básicas dos campos obrigatórios
    # DT_REGISTRO: obrigatório, formato DDMMAAAA
    if not dt_registro:
        return None
    dt_registro_valida, dt_registro_obj = _validar_data(dt_registro)
    if not dt_registro_valida:
        return None
    
    # Função auxiliar para validar valor numérico com 2 decimais
    def validar_valor_numerico(valor_str, obrigatorio=False):
        if not valor_str:
            return None if obrigatorio else 0.0
        try:
            valor_float = float(valor_str)
            # Verifica se tem mais de 2 casas decimais
            partes_decimal = valor_str.split('.')
            if len(partes_decimal) == 2 and len(partes_decimal[1]) > 2:
                return None
            return valor_float
        except ValueError:
            return None
    
    # ESTQ_INI: obrigatório, numérico com 2 decimais
    estq_ini_float = validar_valor_numerico(estq_ini, obrigatorio=True)
    if estq_ini_float is None:
        return None
    
    # ESTQ_FIN: obrigatório, numérico com 2 decimais
    estq_fin_float = validar_valor_numerico(estq_fin, obrigatorio=True)
    if estq_fin_float is None:
        return None
    
    # COD_ITEM: obrigatório, até 60 caracteres
    if not cod_item or len(cod_item) > 60:
        return None
    
    # TP_RESIDUO: obrigatório, valores válidos [01, 02, 03, 04]
    if not tp_residuo or tp_residuo not in ["01", "02", "03", "04"]:
        return None
    
    # QTD_RESIDUO: obrigatório, numérico com 2 decimais
    qtd_residuo_float = validar_valor_numerico(qtd_residuo, obrigatorio=True)
    if qtd_residuo_float is None:
        return None
    
    # QTD_RESIDUO_DDG: obrigatório, numérico com 2 decimais
    qtd_residuo_ddg_float = validar_valor_numerico(qtd_residuo_ddg, obrigatorio=True)
    if qtd_residuo_ddg_float is None:
        return None
    
    # Validação: QTD_RESIDUO_DDG não pode ser maior que zero quando TP_RESIDUO for 01 ou 03
    if tp_residuo in ["01", "03"] and qtd_residuo_ddg_float > 0:
        return None
    
    # QTD_RESIDUO_WDG: obrigatório, numérico com 2 decimais
    qtd_residuo_wdg_float = validar_valor_numerico(qtd_residuo_wdg, obrigatorio=True)
    if qtd_residuo_wdg_float is None:
        return None
    
    # Validação: QTD_RESIDUO_WDG não pode ser maior que zero quando TP_RESIDUO for 01 ou 02
    if tp_residuo in ["01", "02"] and qtd_residuo_wdg_float > 0:
        return None
    
    # QTD_RESIDUO_CANA: obrigatório, numérico com 2 decimais
    qtd_residuo_cana_float = validar_valor_numerico(qtd_residuo_cana, obrigatorio=True)
    if qtd_residuo_cana_float is None:
        return None
    
    # Validação: QTD_RESIDUO_CANA não pode ser maior que zero quando TP_RESIDUO for 02, 03 ou 04
    if tp_residuo in ["02", "03", "04"] and qtd_residuo_cana_float > 0:
        return None
    
    # Validação: QTD_RESIDUO deve ser igual à soma de QTD_RESIDUO_DDG + QTD_RESIDUO_WDG + QTD_RESIDUO_CANA
    qtd_residuo_calculado = qtd_residuo_ddg_float + qtd_residuo_wdg_float + qtd_residuo_cana_float
    # Usa uma tolerância pequena para comparação de ponto flutuante
    if abs(qtd_residuo_float - qtd_residuo_calculado) > 0.01:
        return None
    
    # Valida campos opcionais condicionais (se informados, devem ser numéricos com 2 decimais)
    qtd_moid_float = validar_valor_numerico(qtd_moid)
    if qtd_moid_float is None and qtd_moid:
        return None
    
    qtd_produz_float = validar_valor_numerico(qtd_produz)
    if qtd_produz_float is None and qtd_produz:
        return None
    
    ent_anid_hid_float = validar_valor_numerico(ent_anid_hid)
    if ent_anid_hid_float is None and ent_anid_hid:
        return None
    
    outr_entr_float = validar_valor_numerico(outr_entr)
    if outr_entr_float is None and outr_entr:
        return None
    
    perda_float = validar_valor_numerico(perda)
    if perda_float is None and perda:
        return None
    
    cons_float = validar_valor_numerico(cons)
    if cons_float is None and cons:
        return None
    
    sai_ani_hid_float = validar_valor_numerico(sai_ani_hid)
    if sai_ani_hid_float is None and sai_ani_hid:
        return None
    
    saidas_float = validar_valor_numerico(saidas)
    if saidas_float is None and saidas:
        return None
    
    estq_ini_mel_float = validar_valor_numerico(estq_ini_mel)
    if estq_ini_mel_float is None and estq_ini_mel:
        return None
    
    prod_dia_mel_float = validar_valor_numerico(prod_dia_mel)
    if prod_dia_mel_float is None and prod_dia_mel:
        return None
    
    util_mel_float = validar_valor_numerico(util_mel)
    if util_mel_float is None and util_mel:
        return None
    
    prod_alc_mel_float = validar_valor_numerico(prod_alc_mel)
    if prod_alc_mel_float is None and prod_alc_mel:
        return None
    
    # Formatação de valores para exibição
    def formatar_valor(valor_str):
        if not valor_str:
            return ""
        try:
            valor_float = float(valor_str)
            return f"{valor_float:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        except ValueError:
            return valor_str
    
    # Formatação de data para exibição
    def formatar_data(data_str):
        if len(data_str) == 8 and data_str.isdigit():
            return f"{data_str[:2]}/{data_str[2:4]}/{data_str[4:8]}"
        return data_str
    
    # Mapeamento de descrições
    tp_residuo_desc = {
        "01": "Bagaço de cana",
        "02": "DDG",
        "03": "WDG",
        "04": "DDG + WDG"
    }
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "DT_REGISTRO": {
            "titulo": "Data de produção",
            "valor": dt_registro,
            "valor_formatado": formatar_data(dt_registro)
        },
        "ESTQ_INI": {
            "titulo": "Estoque inicial (litros / kg)",
            "valor": estq_ini,
            "valor_formatado": formatar_valor(estq_ini)
        },
        "ESTQ_FIN": {
            "titulo": "Estoque final (litros / kg)",
            "valor": estq_fin,
            "valor_formatado": formatar_valor(estq_fin)
        },
        "COD_ITEM": {
            "titulo": "Código do insumo conforme código do item (campo 02 do Registro 0200)",
            "valor": cod_item
        },
        "TP_RESIDUO": {
            "titulo": "Tipo de resíduo produzido",
            "valor": tp_residuo,
            "descricao": tp_residuo_desc.get(tp_residuo, "")
        },
        "QTD_RESIDUO": {
            "titulo": "Quantidade de resíduo produzido (toneladas)",
            "valor": qtd_residuo,
            "valor_formatado": formatar_valor(qtd_residuo)
        },
        "QTD_RESIDUO_DDG": {
            "titulo": "Quantidade de resíduo produzido de DDG (toneladas)",
            "valor": qtd_residuo_ddg,
            "valor_formatado": formatar_valor(qtd_residuo_ddg)
        },
        "QTD_RESIDUO_WDG": {
            "titulo": "Quantidade de resíduo produzido de WDG (toneladas)",
            "valor": qtd_residuo_wdg,
            "valor_formatado": formatar_valor(qtd_residuo_wdg)
        },
        "QTD_RESIDUO_CANA": {
            "titulo": "Quantidade de resíduo produzido de bagaço de cana (toneladas)",
            "valor": qtd_residuo_cana,
            "valor_formatado": formatar_valor(qtd_residuo_cana)
        }
    }
    
    # Adiciona campos opcionais se informados
    if qtd_moid:
        resultado["QTD_MOID"] = {
            "titulo": "Quantidade de insumo esmagado (toneladas)",
            "valor": qtd_moid,
            "valor_formatado": formatar_valor(qtd_moid)
        }
    
    if qtd_produz:
        resultado["QTD_PRODUZ"] = {
            "titulo": "Quantidade produzida (litros / kg)",
            "valor": qtd_produz,
            "valor_formatado": formatar_valor(qtd_produz)
        }
    
    if ent_anid_hid:
        resultado["ENT_ANID_HID"] = {
            "titulo": "Entrada de álcool anidro decorrente da transformação do álcool hidratado ou Entrada de álcool hidratado decorrente da transformação do álcool anidro (litros)",
            "valor": ent_anid_hid,
            "valor_formatado": formatar_valor(ent_anid_hid)
        }
    
    if outr_entr:
        resultado["OUTR_ENTR"] = {
            "titulo": "Outras entradas (litros / kg)",
            "valor": outr_entr,
            "valor_formatado": formatar_valor(outr_entr)
        }
    
    if perda:
        resultado["PERDA"] = {
            "titulo": "Evaporação (litros) ou Quebra de peso (kg)",
            "valor": perda,
            "valor_formatado": formatar_valor(perda)
        }
    
    if cons:
        resultado["CONS"] = {
            "titulo": "Consumo (litros)",
            "valor": cons,
            "valor_formatado": formatar_valor(cons)
        }
    
    if sai_ani_hid:
        resultado["SAI_ANI_HID"] = {
            "titulo": "Saída para transformação (litros)",
            "valor": sai_ani_hid,
            "valor_formatado": formatar_valor(sai_ani_hid)
        }
    
    if saidas:
        resultado["SAÍDAS"] = {
            "titulo": "Saídas (litros / kg)",
            "valor": saidas,
            "valor_formatado": formatar_valor(saidas)
        }
    
    if estq_ini_mel:
        resultado["ESTQ_INI_MEL"] = {
            "titulo": "Estoque inicial de mel residual (kg)",
            "valor": estq_ini_mel,
            "valor_formatado": formatar_valor(estq_ini_mel)
        }
    
    if prod_dia_mel:
        resultado["PROD_DIA_MEL"] = {
            "titulo": "Produção de mel residual (kg) e entradas de mel (kg)",
            "valor": prod_dia_mel,
            "valor_formatado": formatar_valor(prod_dia_mel)
        }
    
    if util_mel:
        resultado["UTIL_MEL"] = {
            "titulo": "Mel residual utilizado (kg) e saídas de mel (kg)",
            "valor": util_mel,
            "valor_formatado": formatar_valor(util_mel)
        }
    
    if prod_alc_mel:
        resultado["PROD_ALC_MEL"] = {
            "titulo": "Produção de álcool (litros) ou açúcar (kg) proveniente do mel residual",
            "valor": prod_alc_mel,
            "valor_formatado": formatar_valor(prod_alc_mel)
        }
    
    if obs:
        resultado["OBS"] = {
            "titulo": "Observações",
            "valor": obs
        }
    
    return resultado


def validar_1391_fiscal(linhas):
    """
    Valida uma ou mais linhas do registro 1391 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |1391|DT_REGISTRO|QTD_MOID|ESTQ_INI|QTD_PRODUZ|ENT_ANID_HID|OUTR_ENTR|PERDA|CONS|SAI_ANI_HID|SAÍDAS|ESTQ_FIN|ESTQ_INI_MEL|PROD_DIA_MEL|UTIL_MEL|PROD_ALC_MEL|OBS|COD_ITEM|TP_RESIDUO|QTD_RESIDUO|QTD_RESIDUO_DDG|QTD_RESIDUO_WDG|QTD_RESIDUO_CANA|
        
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
        resultado = _processar_linha_1391(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
