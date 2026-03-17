import json


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
    if valor_str is None:
        valor_str = ""

    if not valor_str:
        if obrigatorio:
            return False, None, "Campo obrigatório não preenchido"
        return True, 0.0, None

    try:
        valor_float = float(valor_str)

        # Verifica precisão decimal (quando houver ponto decimal)
        partes_decimal = valor_str.split(".")
        if len(partes_decimal) == 2 and len(partes_decimal[1]) > decimais:
            return False, None, f"Valor com mais de {decimais} casas decimais"

        if positivo and valor_float <= 0:
            return False, None, "Valor deve ser maior que zero"
        if nao_negativo and valor_float < 0:
            return False, None, "Valor não pode ser negativo"

        return True, valor_float, None
    except ValueError:
        return False, None, "Valor não é numérico válido"


def _processar_linha_0200(linha):
    """
    Processa uma única linha do registro 0200 e retorna um dicionário.
    
    Formato:
      |0200|COD_ITEM|DESCR_ITEM|COD_BARRA|COD_ANT_ITEM|UNID_INV|TIPO_ITEM|COD_NCM|EX_IPI|COD_GEN|COD_LST|ALIQ_ICMS|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "0200"
    - COD_ITEM: obrigatório, até 60 caracteres
    - DESCR_ITEM: obrigatório, descrição do item
    - COD_BARRA: opcional, código de barra
    - COD_ANT_ITEM: opcional, até 60 caracteres
    - UNID_INV: opcional, até 6 caracteres (se informado, deve existir no registro 0190 - validação externa)
    - TIPO_ITEM: obrigatório, valores válidos [00, 01, 02, 03, 04, 05, 06, 07, 08, 09, 10, 99]
    - COD_NCM: opcional, 8 caracteres (obrigatório em algumas situações - validação externa)
    - EX_IPI: opcional, 3 caracteres
    - COD_GEN: opcional, 2 dígitos (obrigatório para produtos primários - validação externa)
    - COD_LST: opcional, 4 ou 5 caracteres (pode ter formato "XX.XX")
    - ALIQ_ICMS: opcional, numérico com 2 decimais, não negativo
    
    Args:
        linha: String com uma linha do SPED
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |0200|...|)
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
    if reg != "0200":
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
    
    # Extrai todos os campos (12 campos no total)
    cod_item = obter_campo(1)
    descr_item = obter_campo(2)
    cod_barra = obter_campo(3)
    cod_ant_item = obter_campo(4)
    unid_inv = obter_campo(5)
    tipo_item = obter_campo(6)
    cod_ncm = obter_campo(7)
    ex_ipi = obter_campo(8)
    cod_gen = obter_campo(9)
    cod_lst = obter_campo(10)
    aliq_icms = obter_campo(11)
    
    # Validações básicas dos campos obrigatórios
    
    # COD_ITEM: obrigatório, até 60 caracteres
    if not cod_item or len(cod_item) > 60:
        return None
    
    # DESCR_ITEM: obrigatório
    if not descr_item:
        return None
    
    # COD_BARRA: opcional, sem validação específica de formato
    
    # COD_ANT_ITEM: opcional, até 60 caracteres
    if cod_ant_item and len(cod_ant_item) > 60:
        return None
    
    # UNID_INV: opcional, até 6 caracteres
    if unid_inv and len(unid_inv) > 6:
        return None
    
    # TIPO_ITEM: obrigatório, valores válidos [00, 01, 02, 03, 04, 05, 06, 07, 08, 09, 10, 99]
    valores_validos_tipo_item = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "99"]
    if not tipo_item or tipo_item not in valores_validos_tipo_item:
        return None
    
    # COD_NCM: opcional, 8 caracteres
    if cod_ncm and len(cod_ncm) != 8:
        return None
    
    # EX_IPI: opcional, 3 caracteres
    if ex_ipi and len(ex_ipi) != 3:
        return None
    
    # COD_GEN: opcional, 2 dígitos
    if cod_gen:
        if not cod_gen.isdigit() or len(cod_gen) != 2:
            return None
    
    # COD_LST: opcional, 4 ou 5 caracteres (pode ter formato "XX.XX")
    if cod_lst:
        # Remove pontos para verificar se são apenas dígitos
        cod_lst_sem_ponto = cod_lst.replace(".", "")
        if not cod_lst_sem_ponto.isdigit():
            return None
        # Deve ter 4 ou 5 caracteres (com ou sem ponto)
        if len(cod_lst) not in [4, 5]:
            return None
        # Se tiver 5 caracteres, deve ter formato "XX.XX"
        if len(cod_lst) == 5 and cod_lst[2] != ".":
            return None
    
    # ALIQ_ICMS: opcional, numérico com 2 decimais, não negativo
    if aliq_icms:
        ok_aliq, val_aliq, _ = validar_valor_numerico(aliq_icms, decimais=2, obrigatorio=False, nao_negativo=True)
        if not ok_aliq:
            return None
    
    # Monta o resultado
    descricoes_tipo_item = {
        "00": "Mercadoria para Revenda",
        "01": "Matéria-Prima",
        "02": "Embalagem",
        "03": "Produto em Processo",
        "04": "Produto Acabado",
        "05": "Subproduto",
        "06": "Produto Intermediário",
        "07": "Material de Uso e Consumo",
        "08": "Ativo Imobilizado",
        "09": "Serviços",
        "10": "Outros insumos",
        "99": "Outras"
    }
    
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "COD_ITEM": {
            "titulo": "Código do item",
            "valor": cod_item
        },
        "DESCR_ITEM": {
            "titulo": "Descrição do item",
            "valor": descr_item
        },
        "TIPO_ITEM": {
            "titulo": "Tipo do item",
            "valor": tipo_item,
            "descricao": descricoes_tipo_item.get(tipo_item, "")
        }
    }
    
    # COD_BARRA: opcional
    if cod_barra:
        resultado["COD_BARRA"] = {
            "titulo": "Representação alfanumérica do código de barra do produto",
            "valor": cod_barra
        }
    else:
        resultado["COD_BARRA"] = {
            "titulo": "Representação alfanumérica do código de barra do produto",
            "valor": ""
        }
    
    # COD_ANT_ITEM: opcional
    if cod_ant_item:
        resultado["COD_ANT_ITEM"] = {
            "titulo": "Código anterior do item com relação à última informação apresentada",
            "valor": cod_ant_item
        }
    else:
        resultado["COD_ANT_ITEM"] = {
            "titulo": "Código anterior do item com relação à última informação apresentada",
            "valor": ""
        }
    
    # UNID_INV: opcional
    if unid_inv:
        resultado["UNID_INV"] = {
            "titulo": "Unidade de medida utilizada na quantificação de estoques",
            "valor": unid_inv
        }
    else:
        resultado["UNID_INV"] = {
            "titulo": "Unidade de medida utilizada na quantificação de estoques",
            "valor": ""
        }
    
    # COD_NCM: opcional
    if cod_ncm:
        resultado["COD_NCM"] = {
            "titulo": "Código da Nomenclatura Comum do Mercosul",
            "valor": cod_ncm
        }
    else:
        resultado["COD_NCM"] = {
            "titulo": "Código da Nomenclatura Comum do Mercosul",
            "valor": ""
        }
    
    # EX_IPI: opcional
    if ex_ipi:
        resultado["EX_IPI"] = {
            "titulo": "Código EX, conforme a TIPI",
            "valor": ex_ipi
        }
    else:
        resultado["EX_IPI"] = {
            "titulo": "Código EX, conforme a TIPI",
            "valor": ""
        }
    
    # COD_GEN: opcional
    if cod_gen:
        resultado["COD_GEN"] = {
            "titulo": "Código do gênero do item, conforme a Tabela 4.2.1",
            "valor": cod_gen
        }
    else:
        resultado["COD_GEN"] = {
            "titulo": "Código do gênero do item, conforme a Tabela 4.2.1",
            "valor": ""
        }
    
    # COD_LST: opcional
    if cod_lst:
        resultado["COD_LST"] = {
            "titulo": "Código do serviço conforme lista do Anexo I da Lei Complementar Federal nº 116/03",
            "valor": cod_lst
        }
    else:
        resultado["COD_LST"] = {
            "titulo": "Código do serviço conforme lista do Anexo I da Lei Complementar Federal nº 116/03",
            "valor": ""
        }
    
    # ALIQ_ICMS: opcional
    if aliq_icms:
        ok_aliq, val_aliq, _ = validar_valor_numerico(aliq_icms, decimais=2, obrigatorio=False, nao_negativo=True)
        def fmt_valor(v):
            return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        
        resultado["ALIQ_ICMS"] = {
            "titulo": "Alíquota de ICMS aplicável ao item nas operações internas",
            "valor": aliq_icms,
            "valor_formatado": fmt_valor(val_aliq) if val_aliq is not None else ""
        }
    else:
        resultado["ALIQ_ICMS"] = {
            "titulo": "Alíquota de ICMS aplicável ao item nas operações internas",
            "valor": "",
            "valor_formatado": ""
        }
    
    return resultado


def validar_0200(linhas):
    """
    Valida uma ou mais linhas do registro 0200 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |0200|COD_ITEM|DESCR_ITEM|COD_BARRA|COD_ANT_ITEM|UNID_INV|TIPO_ITEM|COD_NCM|EX_IPI|COD_GEN|COD_LST|ALIQ_ICMS|
        
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
        resultado = _processar_linha_0200(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
