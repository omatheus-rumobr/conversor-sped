import re
import json
from datetime import datetime


def _processar_linha_0400(linha):
    """
    Processa uma única linha do registro 0400 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |0400|COD_NAT|DESCR_NAT|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |0400|...|)
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
    if reg != "0400":
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
    
    # Extrai todos os campos (3 campos no total)
    cod_nat = obter_campo(1)
    descr_nat = obter_campo(2)
    
    # Validações básicas dos campos obrigatórios
    # COD_NAT: obrigatório, até 10 caracteres
    # Validação: o valor informado no campo COD_NAT deve existir em pelo menos um registro dos demais blocos
    # (validação básica de formato implementada; validação completa requer acesso aos demais blocos)
    if not cod_nat or len(cod_nat) > 10:
        return None
    
    # DESCR_NAT: obrigatório
    if not descr_nat:
        return None
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "COD_NAT": {
            "titulo": "Código da Natureza da Operação/Prestação",
            "valor": cod_nat
        },
        "DESCR_NAT": {
            "titulo": "Descrição da Natureza da Operação/Prestação",
            "valor": descr_nat
        }
    }
    
    return resultado


def validar_0400(linhas):
    """
    Valida uma ou mais linhas do registro 0400 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |0400|COD_NAT|DESCR_NAT|
        
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
        resultado = _processar_linha_0400(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
