import re
import json
from datetime import datetime


# Lista de siglas válidas de UF brasileiras
UFS_VALIDAS = [
    'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA',
    'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN',
    'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
]


def _processar_linha_c112(linha):
    """
    Processa uma única linha do registro C112 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |C112|COD_DA|UF|NUM_DA|COD_AUT|VL_DA|DT_VCTO|DT_PGTO|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |C112|...|)
    if partes and not partes[0]:
        partes = partes[1:]
    if partes and not partes[-1]:
        partes = partes[:-1]
    
    # Verifica se tem pelo menos o campo REG
    if len(partes) < 1:
        return None
    
    # Extrai o campo REG
    reg = partes[0].strip().upper() if partes else ""
    
    # Validação do campo REG
    if reg != "C112":
        return None
    
    # Função auxiliar para obter campo ou string vazia
    def obter_campo(indice):
        if indice < len(partes):
            valor = partes[indice].strip()
            return valor if valor else ""
        return ""
    
    # Extrai todos os campos (8 campos no total)
    cod_da = obter_campo(1)
    uf = obter_campo(2)
    num_da = obter_campo(3)
    cod_aut = obter_campo(4)
    vl_da = obter_campo(5)
    dt_vcto = obter_campo(6)
    dt_pgto = obter_campo(7)
    
    # Validação do campo COD_DA: valores válidos [0, 1]
    if not cod_da or cod_da not in ["0", "1"]:
        return None
    
    # Validação do campo UF: deve ser uma sigla válida de UF
    if not uf:
        return None
    
    uf_upper = uf.upper()
    if uf_upper not in UFS_VALIDAS:
        return None
    
    # Validação condicional: se NUM_DA não for informado, COD_AUT deve ser informado
    if not num_da and not cod_aut:
        return None
    
    # Validação de formato de data (ddmmaaaa)
    def validar_data(data_str):
        if not data_str:
            return False  # Datas são obrigatórias
        if len(data_str) != 8 or not data_str.isdigit():
            return False
        try:
            dia = int(data_str[0:2])
            mes = int(data_str[2:4])
            ano = int(data_str[4:8])
            datetime(ano, mes, dia)
            return True
        except (ValueError, IndexError):
            return False
    
    # Valida formato das datas (obrigatórias)
    if not validar_data(dt_vcto):
        return None
    if not validar_data(dt_pgto):
        return None
    
    # Validação de valores numéricos
    def validar_valor(valor_str):
        if not valor_str:
            return False  # VL_DA é obrigatório
        try:
            valor_float = float(valor_str.replace(",", "."))
            return valor_float > 0  # Deve ser maior que 0
        except ValueError:
            return False
    
    # Valida VL_DA (obrigatório e maior que 0)
    if not validar_valor(vl_da):
        return None
    
    # Monta o dicionário com título e valor
    descricoes_cod_da = {
        "0": "Documento estadual de arrecadação",
        "1": "GNRE"
    }
    
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "COD_DA": {
            "titulo": "Código do Modelo do Documento de Arrecadação",
            "valor": cod_da,
            "descricao": descricoes_cod_da.get(cod_da, "")
        },
        "UF": {
            "titulo": "Unidade Federada Beneficiária do Recolhimento",
            "valor": uf_upper
        },
        "NUM_DA": {
            "titulo": "Número do Documento de Arrecadação",
            "valor": num_da
        },
        "COD_AUT": {
            "titulo": "Código Completo da Autenticação Bancária",
            "valor": cod_aut
        },
        "VL_DA": {
            "titulo": "Valor do Total do Documento de Arrecadação",
            "valor": vl_da
        },
        "DT_VCTO": {
            "titulo": "Data de Vencimento do Documento de Arrecadação",
            "valor": dt_vcto
        },
        "DT_PGTO": {
            "titulo": "Data de Pagamento do Documento de Arrecadação",
            "valor": dt_pgto
        }
    }
    
    return resultado


def validar_c112(linhas):
    """
    Valida e processa uma ou múltiplas linhas do registro C112 (Documento de Arrecadação Referenciado) do SPED.
    
    Este registro deve ser apresentado, obrigatoriamente, quando no campo "Informações Complementares" da nota
    fiscal constar a identificação de um documento de arrecadação.
    
    Args:
        linhas: Pode ser:
                - Uma string com uma linha do SPED
                - Uma lista de strings (cada string é uma linha)
                - Uma string com múltiplas linhas separadas por \\n
                Formato: |C112|COD_DA|UF|NUM_DA|COD_AUT|VL_DA|DT_VCTO|DT_PGTO|
        
    Returns:
        str: JSON com um array contendo os campos validados de cada linha processada.
             Retorna um array vazio [] se nenhuma linha válida for encontrada.
             Retorna None se o input for inválido.
        
    Validações principais:
        - Campo REG deve ser exatamente "C112"
        - COD_DA: obrigatório, valores válidos [0, 1]
          - 0: Documento estadual de arrecadação
          - 1: GNRE
        - UF: obrigatório, sigla válida de unidade da federação brasileira
        - NUM_DA: opcional condicional (se não informado, COD_AUT deve ser informado)
        - COD_AUT: opcional condicional (se NUM_DA não for informado, deve ser informado)
        - VL_DA: obrigatório, valor numérico maior que 0
        - DT_VCTO: obrigatório, data no formato ddmmaaaa
        - DT_PGTO: obrigatório, data no formato ddmmaaaa
    """
    if linhas is None:
        return None
    
    # Lista para armazenar as linhas a processar
    linhas_para_processar = []
    
    # Se for uma lista, processa cada item
    if isinstance(linhas, list):
        linhas_para_processar = linhas
    # Se for uma string, verifica se tem múltiplas linhas
    elif isinstance(linhas, str):
        # Se contém \n, divide em linhas
        if '\n' in linhas:
            linhas_para_processar = linhas.split('\n')
        else:
            # String única
            linhas_para_processar = [linhas]
    else:
        return None
    
    # Lista para armazenar os resultados válidos
    resultados = []
    
    # Processa cada linha
    for linha in linhas_para_processar:
        resultado = _processar_linha_c112(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    # Retorna JSON com array de resultados
    return json.dumps(resultados, ensure_ascii=False, indent=2)