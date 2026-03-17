import re
import json
from datetime import datetime


def _validar_cnpj(cnpj):
    """
    Valida o formato básico do CNPJ (14 dígitos).
    Não valida o dígito verificador completo, apenas o formato.
    """
    if not cnpj:
        return False
    # Remove formatação
    cnpj_limpo = cnpj.replace(".", "").replace("/", "").replace("-", "").replace(" ", "")
    if not cnpj_limpo.isdigit() or len(cnpj_limpo) != 14:
        return False
    return True


def _validar_cpf(cpf):
    """
    Valida o formato básico do CPF (11 dígitos).
    Não valida o dígito verificador completo, apenas o formato.
    """
    if not cpf:
        return False
    # Remove formatação
    cpf_limpo = cpf.replace(".", "").replace("-", "").replace(" ", "")
    if not cpf_limpo.isdigit() or len(cpf_limpo) != 11:
        return False
    return True


def _processar_linha_1320(linha):
    """
    Processa uma única linha do registro 1320 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |1320|NUM_BICO|NR_INTERV|MOT_INTERV|NOM_INTERV|CNPJ_INTERV|CPF_INTERV|VAL_FECHA|VAL_ABERT|VOL_AFERI|VOL_VENDAS|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |1320|...|)
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
    if reg != "1320":
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
    
    # Extrai todos os campos (11 campos no total, incluindo REG)
    # Após remover primeiro e último vazios, REG está em partes[0]
    # Então os campos começam do índice 1
    num_bico = obter_campo(1)
    nr_interv = obter_campo(2)
    mot_interv = obter_campo(3)
    nom_interv = obter_campo(4)
    cnpj_interv = obter_campo(5)
    cpf_interv = obter_campo(6)
    val_fecha = obter_campo(7)
    val_abert = obter_campo(8)
    vol_aferi = obter_campo(9)
    vol_vendas = obter_campo(10)
    
    # Validações básicas dos campos obrigatórios
    # NUM_BICO: obrigatório, numérico
    if not num_bico:
        return None
    try:
        num_bico_int = int(num_bico)
        if num_bico_int <= 0:
            return None
    except ValueError:
        return None
    
    # Campos de intervenção: se NR_INTERV estiver preenchido, os outros campos relacionados devem estar preenchidos
    tem_intervencao = bool(nr_interv)
    
    if tem_intervencao:
        # MOT_INTERV: obrigatório condicional (se NR_INTERV preenchido)
        if not mot_interv or len(mot_interv) > 50:
            return None
        
        # NOM_INTERV: obrigatório condicional (se NR_INTERV preenchido)
        if not nom_interv or len(nom_interv) > 30:
            return None
        
        # CNPJ_INTERV: obrigatório condicional (se NR_INTERV preenchido)
        if cnpj_interv and not _validar_cnpj(cnpj_interv):
            return None
        
        # CPF_INTERV: obrigatório condicional (se NR_INTERV preenchido)
        if cpf_interv and not _validar_cpf(cpf_interv):
            return None
    
    # VAL_FECHA: obrigatório, numérico com 3 decimais
    if not val_fecha:
        return None
    try:
        val_fecha_float = float(val_fecha)
        # Verifica se tem mais de 3 casas decimais
        partes_decimal = val_fecha.split('.')
        if len(partes_decimal) == 2 and len(partes_decimal[1]) > 3:
            return None
    except ValueError:
        return None
    
    # VAL_ABERT: obrigatório, numérico com 3 decimais
    if not val_abert:
        return None
    try:
        val_abert_float = float(val_abert)
        # Verifica se tem mais de 3 casas decimais
        partes_decimal = val_abert.split('.')
        if len(partes_decimal) == 2 and len(partes_decimal[1]) > 3:
            return None
    except ValueError:
        return None
    
    # VOL_AFERI: obrigatório condicional (se informado, deve ser numérico com 3 decimais)
    vol_aferi_float = 0.0
    if vol_aferi:
        try:
            vol_aferi_float = float(vol_aferi)
            # Verifica se tem mais de 3 casas decimais
            partes_decimal = vol_aferi.split('.')
            if len(partes_decimal) == 2 and len(partes_decimal[1]) > 3:
                return None
        except ValueError:
            return None
    
    # VOL_VENDAS: obrigatório, numérico com 3 decimais
    if not vol_vendas:
        return None
    try:
        vol_vendas_float = float(vol_vendas)
        # Verifica se tem mais de 3 casas decimais
        partes_decimal = vol_vendas.split('.')
        if len(partes_decimal) == 2 and len(partes_decimal[1]) > 3:
            return None
    except ValueError:
        return None
    
    # Validação: VOL_VENDAS deve ser igual a VAL_FECHA - VAL_ABERT - VOL_AFERI
    vol_vendas_calculado = val_fecha_float - val_abert_float - vol_aferi_float
    # Usa uma tolerância pequena para comparação de ponto flutuante
    if abs(vol_vendas_float - vol_vendas_calculado) > 0.001:
        return None
    
    # Formatação de valores para exibição
    def formatar_volume(valor_str):
        try:
            valor_float = float(valor_str)
            # Formata com até 3 casas decimais
            return f"{valor_float:,.3f}".rstrip('0').rstrip('.').replace(',', 'X').replace('.', ',').replace('X', '.')
        except ValueError:
            return valor_str
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "NUM_BICO": {
            "titulo": "Bico Ligado à Bomba",
            "valor": num_bico
        },
        "VAL_FECHA": {
            "titulo": "Valor da leitura final do contador, no fechamento do bico",
            "valor": val_fecha,
            "valor_formatado": formatar_volume(val_fecha)
        },
        "VAL_ABERT": {
            "titulo": "Valor da leitura inicial do contador, na abertura do bico",
            "valor": val_abert,
            "valor_formatado": formatar_volume(val_abert)
        },
        "VOL_VENDAS": {
            "titulo": "Vendas (VAL_FECHA – VAL_ABERT - VOL_AFERI) do bico, em litros",
            "valor": vol_vendas,
            "valor_formatado": formatar_volume(vol_vendas)
        }
    }
    
    # Adiciona campos de intervenção se informados
    if nr_interv:
        resultado["NR_INTERV"] = {
            "titulo": "Número da intervenção",
            "valor": nr_interv
        }
    
    if mot_interv:
        resultado["MOT_INTERV"] = {
            "titulo": "Motivo da Intervenção",
            "valor": mot_interv
        }
    
    if nom_interv:
        resultado["NOM_INTERV"] = {
            "titulo": "Nome do Interventor",
            "valor": nom_interv
        }
    
    if cnpj_interv:
        resultado["CNPJ_INTERV"] = {
            "titulo": "CNPJ da empresa responsável pela intervenção",
            "valor": cnpj_interv
        }
    
    if cpf_interv:
        resultado["CPF_INTERV"] = {
            "titulo": "CPF do técnico responsável pela intervenção",
            "valor": cpf_interv
        }
    
    if vol_aferi:
        resultado["VOL_AFERI"] = {
            "titulo": "Aferições da Bomba, em litros",
            "valor": vol_aferi,
            "valor_formatado": formatar_volume(vol_aferi)
        }
    
    return resultado


def validar_1320(linhas):
    """
    Valida uma ou mais linhas do registro 1320 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |1320|NUM_BICO|NR_INTERV|MOT_INTERV|NOM_INTERV|CNPJ_INTERV|CPF_INTERV|VAL_FECHA|VAL_ABERT|VOL_AFERI|VOL_VENDAS|
        
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
        resultado = _processar_linha_1320(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
