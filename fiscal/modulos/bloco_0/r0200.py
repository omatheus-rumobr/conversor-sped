import re
import json
from datetime import datetime


def _processar_linha_0200(linha):
    """
    Processa uma única linha do registro 0200 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |0200|COD_ITEM|DESCR_ITEM|COD_BARRA|COD_ANT_ITEM|UNID_INV|TIPO_ITEM|COD_NCM|EX_IPI|COD_GEN|COD_LST|ALIQ_ICMS|CEST|
        
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
    
    # Extrai todos os campos (13 campos no total)
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
    cest = obter_campo(12)
    
    # Validações básicas dos campos obrigatórios
    # COD_ITEM: obrigatório, até 60 caracteres
    if not cod_item or len(cod_item) > 60:
        return None
    
    # DESCR_ITEM: obrigatório
    if not descr_item:
        return None
    
    # COD_ANT_ITEM: não deve ser preenchido (deve ser informado no registro 0205)
    # Se estiver preenchido, não é erro, mas não é o padrão recomendado
    
    # UNID_INV: obrigatório, até 6 caracteres
    # Validação: Deve existir no registro 0190, campo UNID (validação básica de formato)
    if not unid_inv or len(unid_inv) > 6:
        return None
    
    # TIPO_ITEM: obrigatório, valores válidos [00, 01, 02, 03, 04, 05, 06, 07, 08, 09, 10, 99]
    valores_validos_tipo_item = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "99"]
    if not tipo_item or tipo_item not in valores_validos_tipo_item:
        return None
    
    # COD_NCM: opcional condicional, se informado deve ter 8 dígitos
    if cod_ncm and (not cod_ncm.isdigit() or len(cod_ncm) != 8):
        return None
    
    # EX_IPI: opcional condicional, se informado deve ter 3 caracteres
    if ex_ipi and len(ex_ipi) > 3:
        return None
    
    # COD_GEN: opcional condicional, se informado deve ter 2 dígitos
    if cod_gen and (not cod_gen.isdigit() or len(cod_gen) != 2):
        return None
    
    # COD_LST: opcional condicional, se informado deve ter 5 caracteres
    if cod_lst and len(cod_lst) > 5:
        return None
    
    # ALIQ_ICMS: opcional condicional, se informado deve ser numérico com até 6 dígitos e 2 decimais
    if aliq_icms:
        # Remove vírgula e ponto para validar
        aliq_limpa = aliq_icms.replace(",", ".").replace(" ", "")
        try:
            aliq_float = float(aliq_limpa)
            # Valida se tem no máximo 6 dígitos totais (incluindo decimais)
            if len(aliq_limpa.replace(".", "")) > 6:
                return None
        except ValueError:
            return None
    
    # CEST: opcional condicional, se informado deve ter 7 dígitos
    if cest and (not cest.isdigit() or len(cest) != 7):
        return None
    
    # Mapeamento de descrições do TIPO_ITEM
    descricoes_tipo_item = {
        "00": "00 - Mercadoria para Revenda",
        "01": "01 - Matéria-prima",
        "02": "02 - Embalagem",
        "03": "03 - Produto em Processo",
        "04": "04 - Produto Acabado",
        "05": "05 - Subproduto",
        "06": "06 - Produto Intermediário",
        "07": "07 - Material de Uso e Consumo",
        "08": "08 - Ativo Imobilizado",
        "09": "09 - Serviços",
        "10": "10 - Outros insumos",
        "99": "99 - Outras"
    }
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "COD_ITEM": {
            "titulo": "Código do Item",
            "valor": cod_item
        },
        "DESCR_ITEM": {
            "titulo": "Descrição do Item",
            "valor": descr_item
        }
    }
    
    # COD_BARRA é opcional
    if cod_barra:
        resultado["COD_BARRA"] = {
            "titulo": "Representação Alfanumérica do Código de Barra do Produto",
            "valor": cod_barra
        }
    else:
        resultado["COD_BARRA"] = {
            "titulo": "Representação Alfanumérica do Código de Barra do Produto",
            "valor": ""
        }
    
    # COD_ANT_ITEM não deve ser preenchido (mas incluímos no resultado se estiver)
    if cod_ant_item:
        resultado["COD_ANT_ITEM"] = {
            "titulo": "Código Anterior do Item",
            "valor": cod_ant_item
        }
    else:
        resultado["COD_ANT_ITEM"] = {
            "titulo": "Código Anterior do Item",
            "valor": ""
        }
    
    resultado["UNID_INV"] = {
        "titulo": "Unidade de Medida Utilizada na Quantificação de Estoques",
        "valor": unid_inv
    }
    
    resultado["TIPO_ITEM"] = {
        "titulo": "Tipo do Item",
        "valor": tipo_item,
        "descricao": descricoes_tipo_item.get(tipo_item, f"{tipo_item} - Tipo não especificado")
    }
    
    # COD_NCM é opcional
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
    
    # EX_IPI é opcional
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
    
    # COD_GEN é opcional
    if cod_gen:
        resultado["COD_GEN"] = {
            "titulo": "Código do Gênero do Item",
            "valor": cod_gen
        }
    else:
        resultado["COD_GEN"] = {
            "titulo": "Código do Gênero do Item",
            "valor": ""
        }
    
    # COD_LST é opcional
    if cod_lst:
        resultado["COD_LST"] = {
            "titulo": "Código do Serviço conforme Lista do Anexo I da Lei Complementar Federal nº 116/03",
            "valor": cod_lst
        }
    else:
        resultado["COD_LST"] = {
            "titulo": "Código do Serviço conforme Lista do Anexo I da Lei Complementar Federal nº 116/03",
            "valor": ""
        }
    
    # ALIQ_ICMS é opcional
    if aliq_icms:
        resultado["ALIQ_ICMS"] = {
            "titulo": "Alíquota de ICMS Aplicável ao Item nas Operações Internas",
            "valor": aliq_icms
        }
    else:
        resultado["ALIQ_ICMS"] = {
            "titulo": "Alíquota de ICMS Aplicável ao Item nas Operações Internas",
            "valor": ""
        }
    
    # CEST é opcional
    if cest:
        resultado["CEST"] = {
            "titulo": "Código Especificador da Substituição Tributária",
            "valor": cest
        }
    else:
        resultado["CEST"] = {
            "titulo": "Código Especificador da Substituição Tributária",
            "valor": ""
        }
    
    return resultado


def validar_0200_fiscal(linhas):
    """
    Valida uma ou mais linhas do registro 0200 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |0200|COD_ITEM|DESCR_ITEM|COD_BARRA|COD_ANT_ITEM|UNID_INV|TIPO_ITEM|COD_NCM|EX_IPI|COD_GEN|COD_LST|ALIQ_ICMS|CEST|
        
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
