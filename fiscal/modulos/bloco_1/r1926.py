import re
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


def _validar_mes_ref(mes_ref_str):
    """
    Valida se o mês de referência está no formato mmaaaa e se é válido.
    
    Args:
        mes_ref_str: String com mês de referência no formato mmaaaa
        
    Returns:
        tuple: (True/False, (mes, ano) ou None)
    """
    if not mes_ref_str or len(mes_ref_str) != 6 or not mes_ref_str.isdigit():
        return False, None
    
    try:
        mes = int(mes_ref_str[:2])
        ano = int(mes_ref_str[2:6])
        
        # Valida se o mês está entre 01 e 12
        if mes < 1 or mes > 12:
            return False, None
        
        return True, (mes, ano)
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
    if not valor_str:
        if obrigatorio:
            return False, None, f"Campo obrigatório não preenchido"
        return True, 0.0, None
    
    try:
        valor_float = float(valor_str)
        
        # Verifica precisão decimal
        partes_decimal = valor_str.split('.')
        if len(partes_decimal) == 2 and len(partes_decimal[1]) > decimais:
            return False, None, f"Valor com mais de {decimais} casas decimais"
        
        # Validações de sinal
        if positivo and valor_float <= 0:
            return False, None, "Valor deve ser maior que zero"
        if nao_negativo and valor_float < 0:
            return False, None, "Valor não pode ser negativo"
        
        return True, valor_float, None
    except ValueError:
        return False, None, "Valor não é numérico válido"


def _processar_linha_1926(linha):
    """
    Processa uma única linha do registro 1926 e retorna um dicionário.
    
    Args:
        linha: String com uma linha do SPED no formato |1926|COD_OR|VL_OR|DT_VCTO|COD_REC|NUM_PROC|IND_PROC|PROC|TXT_COMPL|MES_REF|
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |1926|...|)
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
    if reg != "1926":
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
    
    # Extrai todos os campos (10 campos no total)
    # Nota: após split('|') e remoção do primeiro e último vazio,
    # os índices começam em 0 para REG, então:
    # 0=REG, 1=COD_OR, 2=VL_OR, 3=DT_VCTO, 4=COD_REC, 5=NUM_PROC, 6=IND_PROC, 7=PROC, 8=TXT_COMPL, 9=MES_REF
    # Mas quando há campos vazios consecutivos no meio, o MES_REF pode estar em posição diferente
    # Primeiro, identifica onde está o MES_REF procurando pelo último campo com formato mmaaaa (6 dígitos)
    mes_ref = ""
    mes_ref_pos = -1
    for i in range(len(partes) - 1, 4, -1):  # Procura do último campo para trás até COD_REC
        campo_teste = obter_campo(i)
        if campo_teste and len(campo_teste) == 6 and campo_teste.isdigit():
            mes_ref_valido_teste, _ = _validar_mes_ref(campo_teste)
            if mes_ref_valido_teste:
                mes_ref = campo_teste
                mes_ref_pos = i
                break
    
    # Se não encontrou MES_REF, tenta no índice 9 (posição esperada)
    if not mes_ref:
        mes_ref = obter_campo(9)
        if mes_ref and len(mes_ref) == 6 and mes_ref.isdigit():
            mes_ref_valido_teste, _ = _validar_mes_ref(mes_ref)
            if mes_ref_valido_teste:
                mes_ref_pos = 9
            else:
                mes_ref = ""
        else:
            mes_ref = ""
    
    # Extrai os campos obrigatórios fixos
    cod_or = obter_campo(1)
    vl_or = obter_campo(2)
    dt_vcto = obter_campo(3)
    cod_rec = obter_campo(4)
    
    # Extrai os campos opcionais baseado na posição do MES_REF
    if mes_ref_pos == 5:
        # MES_REF está na posição 5, então NUM_PROC, IND_PROC, PROC, TXT_COMPL estão vazios
        num_proc = ""
        ind_proc = ""
        proc = ""
        txt_compl = ""
    elif mes_ref_pos == 6:
        # MES_REF está na posição 6, então NUM_PROC está preenchido, mas IND_PROC, PROC, TXT_COMPL estão vazios
        num_proc = obter_campo(5)
        ind_proc = ""
        proc = ""
        txt_compl = ""
    elif mes_ref_pos == 7:
        # MES_REF está na posição 7, então NUM_PROC e IND_PROC estão preenchidos, mas PROC e TXT_COMPL estão vazios
        num_proc = obter_campo(5)
        ind_proc = obter_campo(6)
        proc = ""
        txt_compl = ""
    elif mes_ref_pos == 8:
        # MES_REF está na posição 8, então NUM_PROC, IND_PROC e PROC estão preenchidos, mas TXT_COMPL está vazio
        num_proc = obter_campo(5)
        ind_proc = obter_campo(6)
        proc = obter_campo(7)
        txt_compl = ""
    elif mes_ref_pos == 9:
        # MES_REF está na posição correta (9), todos os campos anteriores podem estar preenchidos
        num_proc = obter_campo(5)
        ind_proc = obter_campo(6)
        proc = obter_campo(7)
        txt_compl = obter_campo(8)
    else:
        # Se não encontrou MES_REF, assume posições padrão
        num_proc = obter_campo(5)
        ind_proc = obter_campo(6)
        proc = obter_campo(7)
        txt_compl = obter_campo(8)
    
    # Validações dos campos obrigatórios
    
    # COD_OR: obrigatório, valores válidos: ["000", "003", "004", "005", "006", "090"]
    cod_or_validos = ["000", "003", "004", "005", "006", "090"]
    if cod_or not in cod_or_validos:
        return None
    
    # VL_OR: obrigatório, numérico com 2 decimais, não negativo
    if not vl_or:
        return None
    vl_or_valido, vl_or_float, vl_or_erro = validar_valor_numerico(vl_or, decimais=2, obrigatorio=True, nao_negativo=True)
    if not vl_or_valido:
        return None
    
    # DT_VCTO: obrigatório, formato DDMMAAAA
    if not dt_vcto:
        return None
    dt_vcto_valida, dt_vcto_obj = _validar_data(dt_vcto)
    if not dt_vcto_valida:
        return None
    
    # COD_REC: obrigatório (sem limite de tamanho especificado)
    if not cod_rec:
        return None
    
    # NUM_PROC: obrigatório condicional, até 60 caracteres
    # Se preenchido, IND_PROC e PROC também devem estar preenchidos
    if num_proc:
        if len(num_proc) > 60:
            return None
        # Se NUM_PROC está preenchido, IND_PROC e PROC também devem estar preenchidos
        if not ind_proc or not proc:
            return None
    
    # IND_PROC: obrigatório condicional, valores válidos: ["0", "1", "2", "9"]
    if ind_proc:
        ind_proc_validos = ["0", "1", "2", "9"]
        if ind_proc not in ind_proc_validos:
            return None
    
    # PROC: obrigatório condicional (sem limite de tamanho especificado)
    # Não há validação específica além de verificar se está presente quando necessário
    
    # TXT_COMPL: obrigatório condicional (sem limite de tamanho especificado)
    # Não há validação específica além de verificar se está presente quando necessário
    
    # MES_REF: obrigatório, formato mmaaaa (6 caracteres)
    # Nota: MES_REF é o último campo (índice 9), mas pode haver campos vazios antes dele
    # Se não encontrou MES_REF no índice 9, tenta encontrar no último campo não vazio
    if not mes_ref:
        # Tenta encontrar MES_REF no último campo não vazio da linha
        for i in range(len(partes) - 1, 4, -1):  # Começa do último e vai até COD_REC
            campo_teste = obter_campo(i)
            if campo_teste and len(campo_teste) == 6 and campo_teste.isdigit():
                mes_ref_valido_teste, _ = _validar_mes_ref(campo_teste)
                if mes_ref_valido_teste:
                    mes_ref = campo_teste
                    # Ajusta os campos intermediários se necessário
                    if i == 5 and not num_proc:
                        num_proc = ""
                    if i == 6 and not ind_proc:
                        ind_proc = ""
                    if i == 7 and not proc:
                        proc = ""
                    if i == 8 and not txt_compl:
                        txt_compl = ""
                    break
    
    if not mes_ref:
        return None
    mes_ref_valido, mes_ref_tuple = _validar_mes_ref(mes_ref)
    if not mes_ref_valido:
        return None
    
    # Mapeamento de códigos para descrições
    cod_or_desc = {
        "000": "ICMS a recolher",
        "003": "ICMS a recolher - Diferencial de Alíquota",
        "004": "ICMS a recolher - Substituição Tributária",
        "005": "ICMS a recolher - Diferimento",
        "006": "ICMS a recolher - Antecipação",
        "090": "ICMS a recolher - Outros"
    }
    
    ind_proc_desc = {
        "0": "SEFAZ",
        "1": "Justiça Federal",
        "2": "Justiça Estadual",
        "9": "Outros"
    }
    
    # Formatação de valores monetários para exibição
    def formatar_valor(valor_str):
        if not valor_str:
            return ""
        try:
            valor_float = float(valor_str)
            return f"{valor_float:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        except ValueError:
            return valor_str
    
    # Formatação de data para exibição
    def formatar_data(data_str):
        if not data_str or len(data_str) != 8:
            return ""
        try:
            return f"{data_str[:2]}/{data_str[2:4]}/{data_str[4:8]}"
        except:
            return data_str
    
    # Formatação de mês de referência para exibição
    def formatar_mes_ref(mes_ref_str):
        if not mes_ref_str or len(mes_ref_str) != 6:
            return ""
        try:
            return f"{mes_ref_str[:2]}/{mes_ref_str[2:6]}"
        except:
            return mes_ref_str
    
    # Monta o resultado
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "COD_OR": {
            "titulo": "Código da obrigação a recolher, conforme a Tabela 5.4",
            "valor": cod_or,
            "descricao": cod_or_desc.get(cod_or, "")
        },
        "VL_OR": {
            "titulo": "Valor da obrigação a recolher",
            "valor": vl_or,
            "valor_formatado": formatar_valor(vl_or)
        },
        "DT_VCTO": {
            "titulo": "Data de vencimento da obrigação",
            "valor": dt_vcto,
            "valor_formatado": formatar_data(dt_vcto)
        },
        "COD_REC": {
            "titulo": "Código de receita referente à obrigação, próprio da unidade da federação, conforme legislação estadual",
            "valor": cod_rec
        },
        "NUM_PROC": {
            "titulo": "Número do processo ou auto de infração ao qual a obrigação está vinculada, se houver",
            "valor": num_proc if num_proc else ""
        },
        "IND_PROC": {
            "titulo": "Indicador da origem do processo",
            "valor": ind_proc if ind_proc else "",
            "descricao": ind_proc_desc.get(ind_proc, "") if ind_proc else ""
        },
        "PROC": {
            "titulo": "Descrição resumida do processo que embasou o lançamento",
            "valor": proc if proc else ""
        },
        "TXT_COMPL": {
            "titulo": "Descrição complementar das obrigações a recolher",
            "valor": txt_compl if txt_compl else ""
        },
        "MES_REF": {
            "titulo": "Mês de referência",
            "valor": mes_ref,
            "valor_formatado": formatar_mes_ref(mes_ref)
        }
    }
    
    return resultado


def validar_1926_fiscal(linhas):
    """
    Valida uma ou mais linhas do registro 1926 do SPED EFD Fiscal.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato |1926|COD_OR|VL_OR|DT_VCTO|COD_REC|NUM_PROC|IND_PROC|PROC|TXT_COMPL|MES_REF|
        
    Returns:
        String JSON com array de objetos contendo os campos validados.
        Cada objeto tem a estrutura {"CAMPO": {"titulo": "...", "valor": "...", "valor_formatado": "...", "descricao": "..."}}.
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
        resultado = _processar_linha_1926(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
