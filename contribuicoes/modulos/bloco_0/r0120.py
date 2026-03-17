import json
from datetime import datetime


def _validar_mes_referencia(mes_ref_str):
    """
    Valida se o mês de referência está no formato mmaaaa e se é válido.
    
    Args:
        mes_ref_str: String com mês/ano no formato mmaaaa
        
    Returns:
        tuple: (True/False, dict com mes e ano ou None)
    """
    if not mes_ref_str or len(mes_ref_str) != 6 or not mes_ref_str.isdigit():
        return False, None
    
    try:
        mes = int(mes_ref_str[:2])
        ano = int(mes_ref_str[2:6])
        
        # Valida se o mês está entre 01 e 12
        if mes < 1 or mes > 12:
            return False, None
        
        # Valida se o ano é razoável (ex: entre 1900 e 2100)
        if ano < 1900 or ano > 2100:
            return False, None
        
        # Valida se a data é válida (ex: 31/02 não existe)
        try:
            datetime(ano, mes, 1)
        except ValueError:
            return False, None
        
        return True, {"mes": mes, "ano": ano}
    except (ValueError, IndexError):
        return False, None


def _processar_linha_0120(linha):
    """
    Processa uma única linha do registro 0120 e retorna um dicionário.
    
    Formato:
      |0120|MES_REFER|INF_COMP|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "0120"
    - MES_REFER: obrigatório, formato "mmaaaa" (6 caracteres)
    - INF_COMP: obrigatório, até 90 caracteres, valores válidos [01, 02, 03, 04, 05, 06, 07, 99]
    
    Nota: Este registro é obrigatório em dezembro e no mês de encerramento de atividades,
    ou quando a escrituração não contém dados representativos de operações geradoras de receitas
    ou de créditos (para fatos geradores a partir de 01/08/2017).
    Esta validação deve ser feita em uma camada superior.
    
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
    # Remove primeiro e último se vazios (formato padrão SPED: |0120|...|)
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
    if reg != "0120":
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
    mes_refer = obter_campo(1)
    inf_comp = obter_campo(2)
    
    # Validações básicas dos campos obrigatórios
    
    # MES_REFER: obrigatório, formato "mmaaaa"
    mes_refer_valido, mes_refer_obj = _validar_mes_referencia(mes_refer)
    if not mes_refer_valido:
        return None
    
    # INF_COMP: obrigatório, até 90 caracteres, valores válidos [01, 02, 03, 04, 05, 06, 07, 99]
    if not inf_comp or len(inf_comp) > 90:
        return None
    
    # Valida se INF_COMP é um dos valores válidos
    valores_validos_inf_comp = ["01", "02", "03", "04", "05", "06", "07", "99"]
    
    # Verifica se INF_COMP começa com um dos valores válidos (pode ter texto adicional)
    # Mas conforme o manual, parece que deve ser exatamente o código de 2 dígitos
    # Vou validar se começa com um dos códigos válidos ou se é exatamente um deles
    inf_comp_valido = False
    codigo_inf_comp = None
    
    # Se INF_COMP tem exatamente 2 caracteres, deve ser um dos códigos válidos
    if len(inf_comp) == 2 and inf_comp in valores_validos_inf_comp:
        inf_comp_valido = True
        codigo_inf_comp = inf_comp
    # Se tem mais de 2 caracteres, deve começar com um dos códigos válidos seguido de espaço ou hífen
    elif len(inf_comp) > 2:
        for codigo in valores_validos_inf_comp:
            if inf_comp.startswith(codigo):
                # Verifica se após o código há espaço, hífen ou fim da string
                if len(inf_comp) == len(codigo) or inf_comp[len(codigo)] in [' ', '-', '–']:
                    inf_comp_valido = True
                    codigo_inf_comp = codigo
                    break
    
    if not inf_comp_valido:
        return None
    
    # Monta o resultado
    descricoes_inf_comp = {
        "01": "Pessoa jurídica imune ou isenta do IRPJ",
        "02": "Órgãos públicos, autarquias e fundações públicas",
        "03": "Pessoa jurídica inativa",
        "04": "Pessoa jurídica em geral, que não realizou operações geradoras de receitas (tributáveis ou não) ou de créditos",
        "05": "Sociedade em Conta de Participação - SCP, que não realizou operações geradoras de receitas (tributáveis ou não) ou de créditos",
        "06": "Sociedade Cooperativa, que não realizou operações geradoras de receitas (tributáveis ou não) ou de créditos",
        "07": "Escrituração decorrente de incorporação, fusão ou cisão, sem operações geradoras de receitas (tributáveis ou não) ou de créditos",
        "99": "Demais hipóteses de dispensa de escrituração, relacionadas no art. 5º, da IN RFB nº 1.252, de 2012"
    }
    
    # Formata mês/ano para exibição
    def fmt_mes_ano(mes_ano_obj):
        if mes_ano_obj:
            return f"{mes_ano_obj['mes']:02d}/{mes_ano_obj['ano']}"
        return ""
    
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "MES_REFER": {
            "titulo": "Mês de referência do ano-calendário da escrituração sem dados, dispensada da entrega",
            "valor": mes_refer,
            "valor_formatado": fmt_mes_ano(mes_refer_obj)
        },
        "INF_COMP": {
            "titulo": "Informação complementar do registro",
            "valor": inf_comp,
            "codigo": codigo_inf_comp,
            "descricao": descricoes_inf_comp.get(codigo_inf_comp, "")
        }
    }
    
    return resultado


def validar_0120(linhas):
    """
    Valida uma ou mais linhas do registro 0120 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |0120|MES_REFER|INF_COMP|
        
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
        resultado = _processar_linha_0120(linha)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
