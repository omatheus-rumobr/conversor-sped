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


def _processar_linha_p100(linha):
    """
    Processa uma única linha do registro P100 e retorna um dicionário.
    
    Formato:
      |P100|DT_INI|DT_FIN|VL_REC_TOT_EST|COD_ATIV_ECON|VL_REC_ATIV_ESTAB|VL_EXC|VL_BC_CONT|ALIQ_CONT|VL_CONT_APU|COD_CTA|INFO_COMPL|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "P100"
    - DT_INI: obrigatório, data inicial a que a apuração se refere (formato ddmmaaaa)
    - DT_FIN: obrigatório, data final a que a apuração se refere (formato ddmmaaaa)
    - VL_REC_TOT_EST: obrigatório, valor da receita bruta total do estabelecimento (numérico, 2 decimais)
    - COD_ATIV_ECON: obrigatório, código de atividade econômica conforme Tabela 5.1.1 (8 caracteres)
    - VL_REC_ATIV_ESTAB: obrigatório, valor da receita bruta do estabelecimento (numérico, 2 decimais)
      - Deve ser MENOR ou IGUAL ao valor do Campo 04 (VL_REC_TOT_EST)
    - VL_EXC: opcional, valor das exclusões da receita bruta (numérico, 2 decimais)
    - VL_BC_CONT: obrigatório, valor da base de cálculo (numérico, 2 decimais)
      - Validação: VL_BC_CONT = VL_REC_ATIV_ESTAB - VL_EXC
    - ALIQ_CONT: obrigatório, alíquota da contribuição previdenciária (8 dígitos, 4 decimais)
    - VL_CONT_APU: obrigatório, valor da contribuição previdenciária apurada (numérico, 2 decimais)
      - Validação: VL_CONT_APU = VL_BC_CONT * ALIQ_CONT
    - COD_CTA: opcional, código da conta contábil (máximo 255 caracteres)
    - INFO_COMPL: opcional, informação complementar (texto livre)
    
    Nota: Registro específico da escrituração da contribuição previdenciária incidente sobre o valor
    da receita bruta, prevista na legislação tributária, conforme a Tabela "5.1.1- Atividades, Produtos
    e Serviços Sujeitos à Contribuição Previdenciária sobre a Receita Bruta".
    
    Poderão ser gerados um ou vários registros "P100" para o mesmo estabelecimento, de acordo com as
    chaves definidas para o registro. (Chaves: DT_INI + DT_FIN + COD_ATIV_ECON + ALIQ_CONT + COD_CTA).
    
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
    # Remove primeiro e último se vazios (formato padrão SPED: |P100|...|)
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
    if reg != "P100":
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
    dt_ini = obter_campo(1)
    dt_fin = obter_campo(2)
    vl_rec_tot_est = obter_campo(3)
    cod_ativ_econ = obter_campo(4)
    vl_rec_ativ_estab = obter_campo(5)
    vl_exc = obter_campo(6)
    vl_bc_cont = obter_campo(7)
    aliq_cont = obter_campo(8)
    vl_cont_apu = obter_campo(9)
    cod_cta = obter_campo(10)
    info_compl = obter_campo(11)
    
    # Validações básicas dos campos obrigatórios
    
    # DT_INI: obrigatório, formato ddmmaaaa
    ok_dt_ini, dt_ini_obj = _validar_data(dt_ini)
    if not ok_dt_ini:
        return None
    
    # DT_FIN: obrigatório, formato ddmmaaaa
    ok_dt_fin, dt_fin_obj = _validar_data(dt_fin)
    if not ok_dt_fin:
        return None
    
    # Validação: DT_FIN deve ser maior ou igual a DT_INI
    if dt_fin_obj < dt_ini_obj:
        return None
    
    # VL_REC_TOT_EST: obrigatório, numérico com 2 decimais
    ok1, val1, _ = validar_valor_numerico(vl_rec_tot_est, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok1:
        return None
    
    # COD_ATIV_ECON: obrigatório, código de atividade econômica (8 caracteres)
    if not cod_ativ_econ or len(cod_ativ_econ) != 8:
        return None
    
    # VL_REC_ATIV_ESTAB: obrigatório, numérico com 2 decimais
    ok2, val2, _ = validar_valor_numerico(vl_rec_ativ_estab, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok2:
        return None
    
    # Validação: VL_REC_ATIV_ESTAB deve ser MENOR ou IGUAL ao VL_REC_TOT_EST
    if val2 > val1:
        return None
    
    # VL_EXC: opcional, numérico com 2 decimais
    ok3, val3, _ = validar_valor_numerico(vl_exc, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok3:
        return None
    
    # VL_BC_CONT: obrigatório, numérico com 2 decimais
    ok4, val4, _ = validar_valor_numerico(vl_bc_cont, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok4:
        return None
    
    # Validação: VL_BC_CONT = VL_REC_ATIV_ESTAB - VL_EXC
    vl_bc_cont_calculado = round(val2 - val3, 2)
    # Permite pequena diferença devido a arredondamentos (tolerância de 0.01)
    if abs(val4 - vl_bc_cont_calculado) > 0.01:
        return None
    
    # ALIQ_CONT: obrigatório, alíquota da contribuição previdenciária (8 dígitos, 4 decimais)
    # Normaliza vírgula para ponto
    aliq_cont_normalizada = aliq_cont.replace(",", ".") if aliq_cont else ""
    ok5, val5, _ = validar_valor_numerico(aliq_cont_normalizada, decimais=4, obrigatorio=True, nao_negativo=True)
    if not ok5:
        return None
    # Valida se tem no máximo 8 dígitos na parte inteira
    if aliq_cont_normalizada:
        partes_aliq = aliq_cont_normalizada.split(".")
        if len(partes_aliq[0]) > 8:
            return None
    
    # VL_CONT_APU: obrigatório, numérico com 2 decimais
    ok6, val6, _ = validar_valor_numerico(vl_cont_apu, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok6:
        return None
    
    # Validação: VL_CONT_APU = VL_BC_CONT * ALIQ_CONT
    vl_cont_apu_calculado = round(val4 * val5, 2)
    # Permite pequena diferença devido a arredondamentos (tolerância de 0.01)
    if abs(val6 - vl_cont_apu_calculado) > 0.01:
        return None
    
    # COD_CTA: opcional, código da conta contábil (máximo 255 caracteres)
    if cod_cta and len(cod_cta) > 255:
        return None
    
    # INFO_COMPL: opcional, informação complementar (texto livre)
    # Não há validação específica além de ser texto livre
    
    # Função auxiliar para formatar valores monetários
    def fmt_valor(v):
        if v is None:
            return ""
        return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    # Função auxiliar para formatar percentual
    def fmt_percentual(v):
        if v is None:
            return ""
        return f"{v:,.4f}".replace(",", "X").replace(".", ",").replace("X", ".") + "%"
    
    # Função auxiliar para formatar data
    def fmt_data(data_str):
        if not data_str or len(data_str) != 8:
            return ""
        return f"{data_str[:2]}/{data_str[2:4]}/{data_str[4:]}"
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "DT_INI": {
            "titulo": "Data inicial a que a apuração se refere",
            "valor": dt_ini,
            "valor_formatado": fmt_data(dt_ini)
        },
        "DT_FIN": {
            "titulo": "Data final a que a apuração se refere",
            "valor": dt_fin,
            "valor_formatado": fmt_data(dt_fin)
        },
        "VL_REC_TOT_EST": {
            "titulo": "Valor da Receita Bruta Total do Estabelecimento no Período",
            "valor": vl_rec_tot_est,
            "valor_formatado": fmt_valor(val1)
        },
        "COD_ATIV_ECON": {
            "titulo": "Código indicador correspondente à atividade sujeita a incidência da Contribuição Previdenciária sobre a Receita Bruta, conforme Tabela 5.1.1",
            "valor": cod_ativ_econ
        },
        "VL_REC_ATIV_ESTAB": {
            "titulo": "Valor da Receita Bruta do Estabelecimento, correspondente às atividades/produtos referidos no Campo 05 (COD_ATIV_ECON)",
            "valor": vl_rec_ativ_estab,
            "valor_formatado": fmt_valor(val2)
        },
        "VL_EXC": {
            "titulo": "Valor das Exclusões da Receita Bruta informada no Campo 06",
            "valor": vl_exc,
            "valor_formatado": fmt_valor(val3) if vl_exc else ""
        },
        "VL_BC_CONT": {
            "titulo": "Valor da Base de Cálculo da Contribuição Previdenciária sobre a Receita Bruta (Campo 08 = Campo 06 – Campo 07)",
            "valor": vl_bc_cont,
            "valor_formatado": fmt_valor(val4)
        },
        "ALIQ_CONT": {
            "titulo": "Alíquota da Contribuição Previdenciária sobre a Receita Bruta",
            "valor": aliq_cont,
            "valor_formatado": fmt_percentual(val5)
        },
        "VL_CONT_APU": {
            "titulo": "Valor da Contribuição Previdenciária Apurada sobre a Receita Bruta",
            "valor": vl_cont_apu,
            "valor_formatado": fmt_valor(val6)
        },
        "COD_CTA": {
            "titulo": "Código da conta analítica contábil referente à Contribuição Previdenciária sobre a Receita Bruta",
            "valor": cod_cta
        },
        "INFO_COMPL": {
            "titulo": "Informação complementar do registro",
            "valor": info_compl
        }
    }
    
    return resultado


def validar_p100(linhas):
    """
    Valida uma ou mais linhas do registro P100 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |P100|DT_INI|DT_FIN|VL_REC_TOT_EST|COD_ATIV_ECON|VL_REC_ATIV_ESTAB|VL_EXC|VL_BC_CONT|ALIQ_CONT|VL_CONT_APU|COD_CTA|INFO_COMPL|
        
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
        resultado = _processar_linha_p100(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
