import re
import json
from datetime import datetime


def _processar_linha_0300(linha):
    """
    Processa uma única linha do registro 0300 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |0300|COD_IND_BEM|IDENT_MERC|DESCR_ITEM|COD_PRNC|COD_CTA|NR_PARC|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |0300|...|)
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
    if reg != "0300":
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
    cod_ind_bem = obter_campo(1)
    ident_merc = obter_campo(2)
    descr_item = obter_campo(3)
    cod_prnc = obter_campo(4)
    cod_cta = obter_campo(5)
    nr_parc = obter_campo(6)
    
    # Validações básicas dos campos obrigatórios
    # COD_IND_BEM: obrigatório, até 60 caracteres
    if not cod_ind_bem or len(cod_ind_bem) > 60:
        return None
    
    # IDENT_MERC: obrigatório, valores válidos [1, 2]
    if ident_merc not in ["1", "2"]:
        return None
    
    # DESCR_ITEM: obrigatório
    if not descr_item:
        return None
    
    # COD_PRNC: opcional condicional
    # Se IDENT_MERC = "2" (componente), este campo deve obrigatoriamente estar preenchido
    if ident_merc == "2":
        if not cod_prnc or len(cod_prnc) > 60:
            return None
    else:
        # Se IDENT_MERC = "1" (bem), pode estar vazio ou preenchido
        if cod_prnc and len(cod_prnc) > 60:
            return None
    
    # COD_CTA: obrigatório, até 60 caracteres
    if not cod_cta or len(cod_cta) > 60:
        return None
    
    # NR_PARC: opcional condicional, se informado deve ter 3 dígitos numéricos
    if nr_parc:
        if not nr_parc.isdigit() or len(nr_parc) != 3:
            return None
    
    # Mapeamento de descrições do IDENT_MERC
    descricoes_ident_merc = {
        "1": "1 - Bem",
        "2": "2 - Componente"
    }
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "COD_IND_BEM": {
            "titulo": "Código Individualizado do Bem ou Componente",
            "valor": cod_ind_bem
        },
        "IDENT_MERC": {
            "titulo": "Identificação do Tipo de Mercadoria",
            "valor": ident_merc,
            "descricao": descricoes_ident_merc.get(ident_merc, f"{ident_merc} - Tipo não especificado")
        },
        "DESCR_ITEM": {
            "titulo": "Descrição do Bem ou Componente",
            "valor": descr_item
        }
    }
    
    # COD_PRNC é opcional condicional
    if cod_prnc:
        resultado["COD_PRNC"] = {
            "titulo": "Código de Cadastro do Bem Principal",
            "valor": cod_prnc
        }
    else:
        resultado["COD_PRNC"] = {
            "titulo": "Código de Cadastro do Bem Principal",
            "valor": ""
        }
    
    resultado["COD_CTA"] = {
        "titulo": "Código da Conta Analítica de Contabilização do Bem ou Componente",
        "valor": cod_cta
    }
    
    # NR_PARC é opcional condicional
    if nr_parc:
        resultado["NR_PARC"] = {
            "titulo": "Número Total de Parcelas a serem Apropriadas",
            "valor": nr_parc
        }
    else:
        resultado["NR_PARC"] = {
            "titulo": "Número Total de Parcelas a serem Apropriadas",
            "valor": ""
        }
    
    return resultado


def validar_0300(linhas):
    """
    Valida uma ou mais linhas do registro 0300 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |0300|COD_IND_BEM|IDENT_MERC|DESCR_ITEM|COD_PRNC|COD_CTA|NR_PARC|
        
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
        resultado = _processar_linha_0300(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
