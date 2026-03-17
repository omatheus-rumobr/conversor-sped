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


def _processar_linha_a100(linha, dt_ini_0000=None, dt_fin_0000=None):
    """
    Processa uma única linha do registro A100 e retorna um dicionário.
    
    Formato:
      |A100|IND_OPER|IND_EMIT|COD_PART|COD_SIT|SER|SUB|NUM_DOC|CHV_NFSE|DT_DOC|DT_EXE_SERV|VL_DOC|IND_PGTO|VL_DESC|VL_BC_PIS|VL_PIS|VL_BC_COFINS|VL_COFINS|VL_PIS_RET|VL_COFINS_RET|VL_ISS|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "A100"
    - IND_OPER: obrigatório, valores válidos [0, 1]
    - IND_EMIT: obrigatório, valores válidos [0, 1]
    - COD_PART: opcional, máximo 60 caracteres
      - Obrigatório na escrituração das operações de contratação de serviços (IND_OPER=0)
      - Não obrigatório quando serviço prestado para consumidor final
    - COD_SIT: obrigatório, valores válidos [00, 02]
    - SER: opcional, máximo 20 caracteres
    - SUB: opcional, máximo 20 caracteres
    - NUM_DOC: obrigatório, máximo 60 caracteres
    - CHV_NFSE: opcional, máximo 60 caracteres
    - DT_DOC: obrigatório, formato ddmmaaaa, data válida
      - Deve estar compreendida no período da escrituração (quando informado)
    - DT_EXE_SERV: opcional, formato ddmmaaaa, data válida
      - Deve estar compreendida no período da escrituração (quando informado)
    - VL_DOC: obrigatório, numérico com 2 decimais
    - IND_PGTO: obrigatório, valores válidos [0, 1, 9]
    - VL_DESC: opcional, numérico com 2 decimais
    - VL_BC_PIS: obrigatório, numérico com 2 decimais
    - VL_PIS: obrigatório, numérico com 2 decimais
    - VL_BC_COFINS: obrigatório, numérico com 2 decimais
    - VL_COFINS: obrigatório, numérico com 2 decimais
    - VL_PIS_RET: opcional, numérico com 2 decimais
    - VL_COFINS_RET: opcional, numérico com 2 decimais
    - VL_ISS: opcional, numérico com 2 decimais
    
    Nota: Para documento fiscal de serviço cancelado (COD_SIT=02), somente podem ser preenchidos os campos
    de código da situação, indicador de operação, emitente, número do documento, série, subsérie e código
    do participante. Esta validação deve ser feita em uma camada superior.
    A validação de que a soma dos valores do campo VL_PIS dos registros filhos A170 deve ser igual ao
    valor informado no campo VL_PIS deve ser feita em uma camada superior.
    A validação de que a soma dos valores do campo VL_COFINS dos registros filhos A170 deve ser igual
    ao valor informado no campo VL_COFINS deve ser feita em uma camada superior.
    A validação de que COD_PART deve existir no campo COD_PART do registro 0150 deve ser feita em uma
    camada superior.
    
    Args:
        linha: String com uma linha do SPED
        dt_ini_0000: Data inicial da escrituração (ddmmaaaa) - opcional, para validação
        dt_fin_0000: Data final da escrituração (ddmmaaaa) - opcional, para validação
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |A100|...|)
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
    if reg != "A100":
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
    
    # Extrai todos os campos (21 campos no total)
    ind_oper = obter_campo(1)
    ind_emit = obter_campo(2)
    cod_part = obter_campo(3)
    cod_sit = obter_campo(4)
    ser = obter_campo(5)
    sub = obter_campo(6)
    num_doc = obter_campo(7)
    chv_nfse = obter_campo(8)
    dt_doc = obter_campo(9)
    dt_exe_serv = obter_campo(10)
    vl_doc = obter_campo(11)
    ind_pgto = obter_campo(12)
    vl_desc = obter_campo(13)
    vl_bc_pis = obter_campo(14)
    vl_pis = obter_campo(15)
    vl_bc_cofins = obter_campo(16)
    vl_cofins = obter_campo(17)
    vl_pis_ret = obter_campo(18)
    vl_cofins_ret = obter_campo(19)
    vl_iss = obter_campo(20)
    
    # Validações básicas dos campos obrigatórios
    
    # IND_OPER: obrigatório, valores válidos [0, 1]
    if not ind_oper or ind_oper not in ["0", "1"]:
        return None
    
    # IND_EMIT: obrigatório, valores válidos [0, 1]
    if not ind_emit or ind_emit not in ["0", "1"]:
        return None
    
    # COD_PART: opcional, máximo 60 caracteres
    # Obrigatório na escrituração das operações de contratação de serviços (IND_OPER=0)
    # Não obrigatório quando serviço prestado para consumidor final
    if cod_part and len(cod_part) > 60:
        return None
    # Nota: A validação de obrigatoriedade condicional deve ser feita em camada superior
    
    # COD_SIT: obrigatório, valores válidos [00, 02]
    if not cod_sit or cod_sit not in ["00", "02"]:
        return None
    
    # SER: opcional, máximo 20 caracteres
    if ser and len(ser) > 20:
        return None
    
    # SUB: opcional, máximo 20 caracteres
    if sub and len(sub) > 20:
        return None
    
    # NUM_DOC: obrigatório, máximo 60 caracteres
    if not num_doc or len(num_doc) > 60:
        return None
    
    # CHV_NFSE: opcional, máximo 60 caracteres
    if chv_nfse and len(chv_nfse) > 60:
        return None
    
    # DT_DOC: obrigatório, formato ddmmaaaa, data válida
    dt_doc_valido, dt_doc_obj = _validar_data(dt_doc)
    if not dt_doc_valido:
        return None
    
    # DT_DOC deve estar compreendida no período da escrituração (quando informado)
    if dt_ini_0000 and dt_fin_0000:
        ok_ini, dt_ini_obj = _validar_data(dt_ini_0000)
        ok_fin, dt_fin_obj = _validar_data(dt_fin_0000)
        if ok_ini and ok_fin and dt_doc_obj:
            if dt_doc_obj < dt_ini_obj or dt_doc_obj > dt_fin_obj:
                # Se DT_DOC estiver fora do período, verifica DT_EXE_SERV
                if dt_exe_serv:
                    dt_exe_serv_valido, dt_exe_serv_obj = _validar_data(dt_exe_serv)
                    if not dt_exe_serv_valido or not dt_exe_serv_obj:
                        return None
                    if dt_exe_serv_obj < dt_ini_obj or dt_exe_serv_obj > dt_fin_obj:
                        return None
                else:
                    return None
    
    # DT_EXE_SERV: opcional, formato ddmmaaaa, data válida
    dt_exe_serv_obj = None
    if dt_exe_serv:
        dt_exe_serv_valido, dt_exe_serv_obj = _validar_data(dt_exe_serv)
        if not dt_exe_serv_valido:
            return None
        
        # DT_EXE_SERV deve estar compreendida no período da escrituração (quando informado)
        if dt_ini_0000 and dt_fin_0000:
            ok_ini, dt_ini_obj = _validar_data(dt_ini_0000)
            ok_fin, dt_fin_obj = _validar_data(dt_fin_0000)
            if ok_ini and ok_fin and dt_exe_serv_obj:
                if dt_exe_serv_obj < dt_ini_obj or dt_exe_serv_obj > dt_fin_obj:
                    # Se DT_EXE_SERV estiver fora do período, verifica DT_DOC
                    if dt_doc_obj:
                        if dt_doc_obj < dt_ini_obj or dt_doc_obj > dt_fin_obj:
                            return None
                    else:
                        return None
    
    # VL_DOC: obrigatório, numérico com 2 decimais
    ok1, val1, _ = validar_valor_numerico(vl_doc, decimais=2, obrigatorio=True)
    if not ok1:
        return None
    
    # IND_PGTO: obrigatório, valores válidos [0, 1, 9]
    if not ind_pgto or ind_pgto not in ["0", "1", "9"]:
        return None
    
    # VL_DESC: opcional, numérico com 2 decimais
    ok2, val2, _ = validar_valor_numerico(vl_desc, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok2:
        return None
    
    # VL_BC_PIS: obrigatório, numérico com 2 decimais
    ok3, val3, _ = validar_valor_numerico(vl_bc_pis, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok3:
        return None
    
    # VL_PIS: obrigatório, numérico com 2 decimais
    ok4, val4, _ = validar_valor_numerico(vl_pis, decimais=2, obrigatorio=True)
    if not ok4:
        return None
    
    # VL_BC_COFINS: obrigatório, numérico com 2 decimais
    ok5, val5, _ = validar_valor_numerico(vl_bc_cofins, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok5:
        return None
    
    # VL_COFINS: obrigatório, numérico com 2 decimais
    ok6, val6, _ = validar_valor_numerico(vl_cofins, decimais=2, obrigatorio=True)
    if not ok6:
        return None
    
    # VL_PIS_RET: opcional, numérico com 2 decimais
    ok7, val7, _ = validar_valor_numerico(vl_pis_ret, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok7:
        return None
    
    # VL_COFINS_RET: opcional, numérico com 2 decimais
    ok8, val8, _ = validar_valor_numerico(vl_cofins_ret, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok8:
        return None
    
    # VL_ISS: opcional, numérico com 2 decimais
    ok9, val9, _ = validar_valor_numerico(vl_iss, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok9:
        return None
    
    # Função auxiliar para formatar valores monetários
    def fmt_valor(v):
        return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    # Função auxiliar para formatar data
    def fmt_data(dt):
        if dt:
            return dt.strftime("%d/%m/%Y")
        return ""
    
    # Monta o resultado
    descricoes_ind_oper = {
        "0": "Serviço Contratado pelo Estabelecimento",
        "1": "Serviço Prestado pelo Estabelecimento"
    }
    
    descricoes_ind_emit = {
        "0": "Emissão Própria",
        "1": "Emissão de Terceiros"
    }
    
    descricoes_cod_sit = {
        "00": "Documento regular",
        "02": "Documento cancelado"
    }
    
    descricoes_ind_pgto = {
        "0": "À vista",
        "1": "A prazo",
        "9": "Sem pagamento"
    }
    
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "IND_OPER": {
            "titulo": "Indicador do tipo de operação",
            "valor": ind_oper,
            "descricao": descricoes_ind_oper.get(ind_oper, "")
        },
        "IND_EMIT": {
            "titulo": "Indicador do emitente do documento fiscal",
            "valor": ind_emit,
            "descricao": descricoes_ind_emit.get(ind_emit, "")
        },
        "COD_PART": {
            "titulo": "Código do participante (campo 02 do Registro 0150)",
            "valor": cod_part
        },
        "COD_SIT": {
            "titulo": "Código da situação do documento fiscal",
            "valor": cod_sit,
            "descricao": descricoes_cod_sit.get(cod_sit, "")
        },
        "SER": {
            "titulo": "Série do documento fiscal",
            "valor": ser
        },
        "SUB": {
            "titulo": "Subsérie do documento fiscal",
            "valor": sub
        },
        "NUM_DOC": {
            "titulo": "Número do documento fiscal ou documento internacional equivalente",
            "valor": num_doc
        },
        "CHV_NFSE": {
            "titulo": "Chave/Código de Verificação da nota fiscal de serviço eletrônica",
            "valor": chv_nfse
        },
        "DT_DOC": {
            "titulo": "Data da emissão do documento fiscal",
            "valor": dt_doc,
            "valor_formatado": fmt_data(dt_doc_obj)
        },
        "DT_EXE_SERV": {
            "titulo": "Data de Execução / Conclusão do Serviço",
            "valor": dt_exe_serv,
            "valor_formatado": fmt_data(dt_exe_serv_obj) if dt_exe_serv_obj else ""
        },
        "VL_DOC": {
            "titulo": "Valor total do documento",
            "valor": vl_doc,
            "valor_formatado": fmt_valor(val1)
        },
        "IND_PGTO": {
            "titulo": "Indicador do tipo de pagamento",
            "valor": ind_pgto,
            "descricao": descricoes_ind_pgto.get(ind_pgto, "")
        },
        "VL_DESC": {
            "titulo": "Valor total do desconto",
            "valor": vl_desc,
            "valor_formatado": fmt_valor(val2) if vl_desc else ""
        },
        "VL_BC_PIS": {
            "titulo": "Valor da base de cálculo do PIS/PASEP",
            "valor": vl_bc_pis,
            "valor_formatado": fmt_valor(val3)
        },
        "VL_PIS": {
            "titulo": "Valor total do PIS",
            "valor": vl_pis,
            "valor_formatado": fmt_valor(val4)
        },
        "VL_BC_COFINS": {
            "titulo": "Valor da base de cálculo da COFINS",
            "valor": vl_bc_cofins,
            "valor_formatado": fmt_valor(val5)
        },
        "VL_COFINS": {
            "titulo": "Valor total da COFINS",
            "valor": vl_cofins,
            "valor_formatado": fmt_valor(val6)
        },
        "VL_PIS_RET": {
            "titulo": "Valor total do PIS retido na fonte",
            "valor": vl_pis_ret,
            "valor_formatado": fmt_valor(val7) if vl_pis_ret else ""
        },
        "VL_COFINS_RET": {
            "titulo": "Valor total da COFINS retido na fonte",
            "valor": vl_cofins_ret,
            "valor_formatado": fmt_valor(val8) if vl_cofins_ret else ""
        },
        "VL_ISS": {
            "titulo": "Valor do ISS",
            "valor": vl_iss,
            "valor_formatado": fmt_valor(val9) if vl_iss else ""
        }
    }
    
    return resultado


def validar_a100(linhas, dt_ini_0000=None, dt_fin_0000=None):
    """
    Valida uma ou mais linhas do registro A100 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |A100|IND_OPER|IND_EMIT|COD_PART|COD_SIT|SER|SUB|NUM_DOC|CHV_NFSE|DT_DOC|DT_EXE_SERV|VL_DOC|IND_PGTO|VL_DESC|VL_BC_PIS|VL_PIS|VL_BC_COFINS|VL_COFINS|VL_PIS_RET|VL_COFINS_RET|VL_ISS|
        dt_ini_0000: Data inicial da escrituração (ddmmaaaa) - opcional, para validação
        dt_fin_0000: Data final da escrituração (ddmmaaaa) - opcional, para validação
        
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
        resultado = _processar_linha_a100(linha, dt_ini_0000=dt_ini_0000, dt_fin_0000=dt_fin_0000)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
