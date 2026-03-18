import re
import json
from datetime import datetime


def _processar_linha_1010(linha):
    """
    Processa uma única linha do registro 1010 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |1010|IND_EXP|IND_CCRF|IND_COMB|IND_USINA|IND_VA|IND_EE|IND_CART|IND_FORM|IND_AER|IND_GIAF1|IND_GIAF3|IND_GIAF4|IND_REST_RESSARC_COMPL_ICMS|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |1010|...|)
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
    if reg != "1010":
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
    ind_exp = obter_campo(1)
    ind_ccrf = obter_campo(2)
    ind_comb = obter_campo(3)
    ind_usina = obter_campo(4)
    ind_va = obter_campo(5)
    ind_ee = obter_campo(6)
    ind_cart = obter_campo(7)
    ind_form = obter_campo(8)
    ind_aer = obter_campo(9)
    ind_giaf1 = obter_campo(10)
    ind_giaf3 = obter_campo(11)
    ind_giaf4 = obter_campo(12)
    ind_rest_ressarc_compl_icms = obter_campo(13)
    
    # Validações básicas dos campos obrigatórios
    # Todos os campos devem ser "S" ou "N"
    valores_validos = {"S", "N"}
    
    if ind_exp not in valores_validos:
        return None
    if ind_ccrf not in valores_validos:
        return None
    if ind_comb not in valores_validos:
        return None
    if ind_usina not in valores_validos:
        return None
    if ind_va not in valores_validos:
        return None
    if ind_ee not in valores_validos:
        return None
    if ind_cart not in valores_validos:
        return None
    if ind_form not in valores_validos:
        return None
    if ind_aer not in valores_validos:
        return None
    if ind_giaf1 not in valores_validos:
        return None
    if ind_giaf3 not in valores_validos:
        return None
    if ind_giaf4 not in valores_validos:
        return None
    if ind_rest_ressarc_compl_icms not in valores_validos:
        return None
    
    # Monta o resultado com descrições para campos codificados
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "IND_EXP": {
            "titulo": "Reg. 1100 - Ocorreu averbação (conclusão) de exportação no período",
            "valor": ind_exp,
            "descricao": "Sim" if ind_exp == "S" else "Não"
        },
        "IND_CCRF": {
            "titulo": "Reg 1200 – Existem informações acerca de créditos de ICMS a serem controlados, definidos pela Sefaz",
            "valor": ind_ccrf,
            "descricao": "Sim" if ind_ccrf == "S" else "Não"
        },
        "IND_COMB": {
            "titulo": "Reg. 1300 – É comércio varejista de combustíveis com movimentação e/ou estoque no período",
            "valor": ind_comb,
            "descricao": "Sim" if ind_comb == "S" else "Não"
        },
        "IND_USINA": {
            "titulo": "Reg. 1390 – Usinas de açúcar e/álcool – O estabelecimento é produtor de açúcar e/ou álcool carburante com movimentação e/ou estoque no período",
            "valor": ind_usina,
            "descricao": "Sim" if ind_usina == "S" else "Não"
        },
        "IND_VA": {
            "titulo": "Reg 1400 - Sendo o registro obrigatório em sua Unidade de Federação, existem informações a serem prestadas neste registro",
            "valor": ind_va,
            "descricao": "Sim" if ind_va == "S" else "Não"
        },
        "IND_EE": {
            "titulo": "Reg 1500 - A empresa é distribuidora de energia e ocorreu fornecimento de energia elétrica para consumidores de outra UF",
            "valor": ind_ee,
            "descricao": "Sim" if ind_ee == "S" else "Não"
        },
        "IND_CART": {
            "titulo": "Reg 1601 - Realizou vendas com instrumentos eletrônicos de pagamento",
            "valor": ind_cart,
            "descricao": "Sim" if ind_cart == "S" else "Não"
        },
        "IND_FORM": {
            "titulo": "Reg. 1700 - Foram emitidos documentos fiscais em papel no período em unidade da federação que exija o controle de utilização de documentos fiscais",
            "valor": ind_form,
            "descricao": "Sim" if ind_form == "S" else "Não"
        },
        "IND_AER": {
            "titulo": "Reg 1800 - A empresa prestou serviços de transporte aéreo de cargas e de passageiros",
            "valor": ind_aer,
            "descricao": "Sim" if ind_aer == "S" else "Não"
        },
        "IND_GIAF1": {
            "titulo": "Reg. 1960 - Possui informações GIAF1?",
            "valor": ind_giaf1,
            "descricao": "Sim" if ind_giaf1 == "S" else "Não"
        },
        "IND_GIAF3": {
            "titulo": "Reg. 1970 - Possui informações GIAF3?",
            "valor": ind_giaf3,
            "descricao": "Sim" if ind_giaf3 == "S" else "Não"
        },
        "IND_GIAF4": {
            "titulo": "Reg. 1980 - Possui informações GIAF4?",
            "valor": ind_giaf4,
            "descricao": "Sim" if ind_giaf4 == "S" else "Não"
        },
        "IND_REST_RESSARC_COMPL_ICMS": {
            "titulo": "Reg. 1250 – Possui informações consolidadas de saldos de restituição, ressarcimento e complementação do ICMS?",
            "valor": ind_rest_ressarc_compl_icms,
            "descricao": "Sim" if ind_rest_ressarc_compl_icms == "S" else "Não"
        }
    }
    
    return resultado


def validar_1010_fiscal(linhas):
    """
    Valida uma ou mais linhas do registro 1010 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |1010|IND_EXP|IND_CCRF|IND_COMB|IND_USINA|IND_VA|IND_EE|IND_CART|IND_FORM|IND_AER|IND_GIAF1|IND_GIAF3|IND_GIAF4|IND_REST_RESSARC_COMPL_ICMS|
        
    Returns:
        String JSON com array de objetos contendo os campos validados.
        Cada objeto tem a estrutura {"CAMPO": {"titulo": "...", "valor": "...", "descricao": "..."}}.
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
        resultado = _processar_linha_1010(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
