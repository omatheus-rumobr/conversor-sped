import re
import json
from datetime import datetime


def _validar_chave_doc_eletronico(chave):
    """
    Valida a chave de documento eletrônico (NF-e, CT-e, CT-e OS) - 44 dígitos e o dígito verificador.
    
    Args:
        chave: String com a chave do documento eletrônico (44 dígitos)
        
    Returns:
        bool: True se válida, False caso contrário
    """
    if not chave or len(chave) != 44 or not chave.isdigit():
        return False
    
    # Extrai os 43 primeiros dígitos e o dígito verificador (último dígito)
    chave_43 = chave[:43]
    dv_informado = int(chave[43])
    
    # Calcula o dígito verificador usando módulo 11
    soma = 0
    multiplicador = 2
    
    # Percorre os 43 dígitos de trás para frente
    for i in range(42, -1, -1):
        soma += int(chave_43[i]) * multiplicador
        multiplicador += 1
        if multiplicador > 9:
            multiplicador = 2
    
    # Calcula o resto da divisão por 11
    resto = soma % 11
    
    # Se o resto for 0 ou 1, o dígito verificador é 0
    # Caso contrário, é 11 - resto
    if resto < 2:
        dv_calculado = 0
    else:
        dv_calculado = 11 - resto
    
    return dv_calculado == dv_informado


def _processar_linha_1210(linha):
    """
    Processa uma única linha do registro 1210 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |1210|TIPO_UTIL|NR_DOC|VL_CRED_UTIL|CHV_DOCe|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |1210|...|)
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
    if reg != "1210":
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
    tipo_util = obter_campo(1)
    nr_doc = obter_campo(2)
    vl_cred_util = obter_campo(3)
    chv_doce = obter_campo(4)
    
    # Validações básicas dos campos obrigatórios
    # TIPO_UTIL: obrigatório, até 4 caracteres
    if not tipo_util or len(tipo_util) > 4:
        return None
    
    # NR_DOC: obrigatório condicional (se informado, deve ser válido)
    # Não vou validar formato específico, apenas se está presente quando necessário
    
    # VL_CRED_UTIL: obrigatório, numérico com 2 decimais, deve ser maior que 0
    if not vl_cred_util:
        return None
    try:
        vl_cred_util_float = float(vl_cred_util)
        if vl_cred_util_float <= 0:
            return None
        # Verifica se tem mais de 2 casas decimais
        partes_decimal = vl_cred_util.split('.')
        if len(partes_decimal) == 2 and len(partes_decimal[1]) > 2:
            return None
    except ValueError:
        return None
    
    # CHV_DOCe: obrigatório condicional (se informado, deve ter 44 dígitos e validar dígito verificador)
    if chv_doce:
        if not _validar_chave_doc_eletronico(chv_doce):
            return None
    
    # Formatação de valores monetários para exibição
    def formatar_valor(valor_str):
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
        "TIPO_UTIL": {
            "titulo": "Tipo de utilização do crédito, conforme tabela indicada no item 5.5",
            "valor": tipo_util
        },
        "VL_CRED_UTIL": {
            "titulo": "Total de crédito utilizado",
            "valor": vl_cred_util,
            "valor_formatado": formatar_valor(vl_cred_util)
        }
    }
    
    # Adiciona NR_DOC se informado
    if nr_doc:
        resultado["NR_DOC"] = {
            "titulo": "Número do documento utilizado na baixa de créditos",
            "valor": nr_doc
        }
    
    # Adiciona CHV_DOCe se informado
    if chv_doce:
        resultado["CHV_DOCe"] = {
            "titulo": "Chave do Documento Eletrônico",
            "valor": chv_doce
        }
    
    return resultado


def validar_1210(linhas):
    """
    Valida uma ou mais linhas do registro 1210 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |1210|TIPO_UTIL|NR_DOC|VL_CRED_UTIL|CHV_DOCe|
        
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
        resultado = _processar_linha_1210(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
