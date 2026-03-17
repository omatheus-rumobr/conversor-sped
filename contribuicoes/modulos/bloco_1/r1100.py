import json
from datetime import datetime


def _validar_periodo_mmaaaa(periodo_str):
    """
    Valida se o período está no formato mmaaaa e se é um período válido.
    
    Args:
        periodo_str: String com período no formato mmaaaa
        
    Returns:
        tuple: (True/False, (mes, ano) ou None)
    """
    if not periodo_str or len(periodo_str) != 6 or not periodo_str.isdigit():
        return False, None
    
    try:
        mes = int(periodo_str[:2])
        ano = int(periodo_str[2:6])
        
        if mes < 1 or mes > 12:
            return False, None
        
        return True, (mes, ano)
    except ValueError:
        return False, None


def _validar_cnpj(cnpj):
    """
    Valida o formato básico do CNPJ (14 dígitos).
    Valida também o dígito verificador (DV).
    """
    if not cnpj:
        return False
    
    # Remove formatação
    cnpj_limpo = cnpj.replace(".", "").replace("/", "").replace("-", "").replace(" ", "")
    
    if not cnpj_limpo.isdigit() or len(cnpj_limpo) != 14:
        return False
    
    # Validação do dígito verificador
    # Verifica se todos os dígitos são iguais (CNPJ inválido)
    if len(set(cnpj_limpo)) == 1:
        return False
    
    # Calcula primeiro dígito verificador
    multiplicadores1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma = sum(int(cnpj_limpo[i]) * multiplicadores1[i] for i in range(12))
    resto = soma % 11
    dv1 = 0 if resto < 2 else 11 - resto
    
    if int(cnpj_limpo[12]) != dv1:
        return False
    
    # Calcula segundo dígito verificador
    multiplicadores2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma = sum(int(cnpj_limpo[i]) * multiplicadores2[i] for i in range(13))
    resto = soma % 11
    dv2 = 0 if resto < 2 else 11 - resto
    
    if int(cnpj_limpo[13]) != dv2:
        return False
    
    return True


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


def _float_igual(a, b, tolerancia=0.01):
    """Compara dois floats com tolerância."""
    if a is None or b is None:
        return False
    return abs(a - b) <= tolerancia


def _processar_linha_1100(linha, per_apu_escrit=None):
    """
    Processa uma única linha do registro 1100 e retorna um dicionário.
    
    Formato:
      |1100|PER_APU_CRED|ORIG_CRED|CNPJ_SUC|COD_CRED|VL_CRED_APU|VL_CRED_EXT_APU|VL_TOT_CRED_APU|VL_CRED_DESC_PA_ANT|VL_CRED_PER_PA_ANT|VL_CRED_DCOMP_PA_ANT|SD_CRED_DISP_EFD|VL_CRED_DESC_EFD|VL_CRED_PER_EFD|VL_CRED_DCOMP_EFD|VL_CRED_TRANS|VL_CRED_OUT|SLD_CRED_FIM|
    
    Regras (manual 1.35):
    - REG: obrigatório, valor fixo "1100"
    - PER_APU_CRED: obrigatório, formato mmaaaa, período válido
      - Deve ser o mesmo ou anterior ao período da escrituração atual (quando informado)
    - ORIG_CRED: obrigatório, valores válidos [01, 02]
    - CNPJ_SUC: opcional, mas obrigatório se ORIG_CRED = 02, 14 dígitos, validar DV
    - COD_CRED: obrigatório, 3 dígitos (código conforme Tabela 4.3.6)
    - VL_CRED_APU: obrigatório, numérico com 2 decimais, não negativo
    - VL_CRED_EXT_APU: opcional, numérico com 2 decimais, não negativo
    - VL_TOT_CRED_APU: obrigatório, numérico com 2 decimais, não negativo
      - Deve ser igual a VL_CRED_APU + VL_CRED_EXT_APU
    - VL_CRED_DESC_PA_ANT: obrigatório, numérico com 2 decimais, não negativo
    - VL_CRED_PER_PA_ANT: opcional, numérico com 2 decimais, não negativo
      - Obrigatório se COD_CRED em [201, 202, 203, 204, 208, 301, 302, 303, 304, 307, 308]
    - VL_CRED_DCOMP_PA_ANT: opcional, numérico com 2 decimais, não negativo
      - Obrigatório se COD_CRED em [301, 302, 303, 304, 308]
    - SD_CRED_DISP_EFD: obrigatório, numérico com 2 decimais, não negativo
      - Deve ser igual a VL_TOT_CRED_APU - VL_CRED_DESC_PA_ANT - VL_CRED_PER_PA_ANT - VL_CRED_DCOMP_PA_ANT
    - VL_CRED_DESC_EFD: opcional, numérico com 2 decimais, não negativo
    - VL_CRED_PER_EFD: opcional, numérico com 2 decimais, não negativo
      - Obrigatório se COD_CRED em [201, 202, 203, 204, 208, 301, 302, 303, 304, 307, 308]
    - VL_CRED_DCOMP_EFD: opcional, numérico com 2 decimais, não negativo
      - Obrigatório se COD_CRED em [301, 302, 303, 304, 308]
    - VL_CRED_TRANS: opcional, numérico com 2 decimais, não negativo
    - VL_CRED_OUT: opcional, numérico com 2 decimais, não negativo
    - SLD_CRED_FIM: opcional, numérico com 2 decimais, não negativo
      - Deve ser igual a SD_CRED_DISP_EFD - VL_CRED_DESC_EFD - VL_CRED_PER_EFD - VL_CRED_DCOMP_EFD - VL_CRED_TRANS - VL_CRED_OUT
    
    Nota: As validações de que COD_CRED deve existir na Tabela 4.3.6, e as validações de
    correspondência com registros M100, M200, 1101, 1102, F800 devem ser feitas em uma camada superior.
    
    Args:
        linha: String com uma linha do SPED
        per_apu_escrit: Período de apuração da escrituração atual (mmaaaa) - opcional, para validação
        
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
    # Remove primeiro e último se vazios (formato padrão SPED: |1100|...|)
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
    if reg != "1100":
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
    
    # Extrai todos os campos (18 campos no total)
    per_apu_cred = obter_campo(1)
    orig_cred = obter_campo(2)
    cnpj_suc = obter_campo(3)
    cod_cred = obter_campo(4)
    vl_cred_apu = obter_campo(5)
    vl_cred_ext_apu = obter_campo(6)
    vl_tot_cred_apu = obter_campo(7)
    vl_cred_desc_pa_ant = obter_campo(8)
    vl_cred_per_pa_ant = obter_campo(9)
    vl_cred_dcomp_pa_ant = obter_campo(10)
    sd_cred_disp_efd = obter_campo(11)
    vl_cred_desc_efd = obter_campo(12)
    vl_cred_per_efd = obter_campo(13)
    vl_cred_dcomp_efd = obter_campo(14)
    vl_cred_trans = obter_campo(15)
    vl_cred_out = obter_campo(16)
    sld_cred_fim = obter_campo(17)
    
    # Validações básicas dos campos obrigatórios
    
    # PER_APU_CRED: obrigatório, formato mmaaaa, período válido
    per_apu_cred_valido, per_apu_cred_tuplo = _validar_periodo_mmaaaa(per_apu_cred)
    if not per_apu_cred_valido:
        return None
    
    # PER_APU_CRED deve ser o mesmo ou anterior ao período da escrituração atual (quando informado)
    if per_apu_escrit:
        ok_escrit, per_escrit_tuplo = _validar_periodo_mmaaaa(per_apu_escrit)
        if ok_escrit and per_apu_cred_tuplo:
            mes_cred, ano_cred = per_apu_cred_tuplo
            mes_escrit, ano_escrit = per_escrit_tuplo
            if ano_cred > ano_escrit or (ano_cred == ano_escrit and mes_cred > mes_escrit):
                return None
    
    # ORIG_CRED: obrigatório, valores válidos [01, 02]
    valores_validos_orig_cred = ["01", "02"]
    if not orig_cred or orig_cred not in valores_validos_orig_cred:
        return None
    
    # CNPJ_SUC: opcional, mas obrigatório se ORIG_CRED = 02
    if orig_cred == "02":
        if not cnpj_suc or not _validar_cnpj(cnpj_suc):
            return None
    elif cnpj_suc:
        # Se ORIG_CRED != 02, CNPJ_SUC deve estar vazio
        if cnpj_suc:
            return None
    
    # COD_CRED: obrigatório, 3 dígitos
    if not cod_cred or len(cod_cred) != 3 or not cod_cred.isdigit():
        return None
    
    cod_cred_int = int(cod_cred)
    
    # VL_CRED_APU: obrigatório, numérico com 2 decimais, não negativo
    ok1, val1, _ = validar_valor_numerico(vl_cred_apu, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok1:
        return None
    
    # VL_CRED_EXT_APU: opcional, numérico com 2 decimais, não negativo
    ok2, val2, _ = validar_valor_numerico(vl_cred_ext_apu, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok2:
        return None
    if val2 is None:
        val2 = 0.0
    
    # VL_TOT_CRED_APU: obrigatório, numérico com 2 decimais, não negativo
    ok3, val3, _ = validar_valor_numerico(vl_tot_cred_apu, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok3:
        return None
    
    # Validação: VL_TOT_CRED_APU deve ser igual a VL_CRED_APU + VL_CRED_EXT_APU
    soma_cred_apu = val1 + val2
    if not _float_igual(val3, soma_cred_apu):
        return None
    
    # VL_CRED_DESC_PA_ANT: obrigatório, numérico com 2 decimais, não negativo
    ok4, val4, _ = validar_valor_numerico(vl_cred_desc_pa_ant, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok4:
        return None
    
    # VL_CRED_PER_PA_ANT: opcional, mas obrigatório se COD_CRED em [201, 202, 203, 204, 208, 301, 302, 303, 304, 307, 308]
    codigos_per = [201, 202, 203, 204, 208, 301, 302, 303, 304, 307, 308]
    ok5, val5, _ = validar_valor_numerico(vl_cred_per_pa_ant, decimais=2, obrigatorio=(cod_cred_int in codigos_per), nao_negativo=True)
    if not ok5:
        return None
    if val5 is None:
        val5 = 0.0
    
    # VL_CRED_DCOMP_PA_ANT: opcional, mas obrigatório se COD_CRED em [301, 302, 303, 304, 308]
    codigos_dcomp = [301, 302, 303, 304, 308]
    ok6, val6, _ = validar_valor_numerico(vl_cred_dcomp_pa_ant, decimais=2, obrigatorio=(cod_cred_int in codigos_dcomp), nao_negativo=True)
    if not ok6:
        return None
    if val6 is None:
        val6 = 0.0
    
    # SD_CRED_DISP_EFD: obrigatório, numérico com 2 decimais, não negativo
    ok7, val7, _ = validar_valor_numerico(sd_cred_disp_efd, decimais=2, obrigatorio=True, nao_negativo=True)
    if not ok7:
        return None
    
    # Validação: SD_CRED_DISP_EFD deve ser igual a VL_TOT_CRED_APU - VL_CRED_DESC_PA_ANT - VL_CRED_PER_PA_ANT - VL_CRED_DCOMP_PA_ANT
    saldo_calculado = val3 - val4 - val5 - val6
    if not _float_igual(val7, saldo_calculado):
        return None
    
    # VL_CRED_DESC_EFD: opcional, numérico com 2 decimais, não negativo
    ok8, val8, _ = validar_valor_numerico(vl_cred_desc_efd, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok8:
        return None
    if val8 is None:
        val8 = 0.0
    
    # VL_CRED_PER_EFD: opcional, mas obrigatório se COD_CRED em [201, 202, 203, 204, 208, 301, 302, 303, 304, 307, 308]
    ok9, val9, _ = validar_valor_numerico(vl_cred_per_efd, decimais=2, obrigatorio=(cod_cred_int in codigos_per), nao_negativo=True)
    if not ok9:
        return None
    if val9 is None:
        val9 = 0.0
    
    # VL_CRED_DCOMP_EFD: opcional, mas obrigatório se COD_CRED em [301, 302, 303, 304, 308]
    ok10, val10, _ = validar_valor_numerico(vl_cred_dcomp_efd, decimais=2, obrigatorio=(cod_cred_int in codigos_dcomp), nao_negativo=True)
    if not ok10:
        return None
    if val10 is None:
        val10 = 0.0
    
    # VL_CRED_TRANS: opcional, numérico com 2 decimais, não negativo
    ok11, val11, _ = validar_valor_numerico(vl_cred_trans, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok11:
        return None
    if val11 is None:
        val11 = 0.0
    
    # VL_CRED_OUT: opcional, numérico com 2 decimais, não negativo
    ok12, val12, _ = validar_valor_numerico(vl_cred_out, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok12:
        return None
    if val12 is None:
        val12 = 0.0
    
    # SLD_CRED_FIM: opcional, numérico com 2 decimais, não negativo
    ok13, val13, _ = validar_valor_numerico(sld_cred_fim, decimais=2, obrigatorio=False, nao_negativo=True)
    if not ok13:
        return None
    if val13 is None:
        val13 = 0.0
    
    # Validação: SLD_CRED_FIM deve ser igual a SD_CRED_DISP_EFD - VL_CRED_DESC_EFD - VL_CRED_PER_EFD - VL_CRED_DCOMP_EFD - VL_CRED_TRANS - VL_CRED_OUT
    saldo_fim_calculado = val7 - val8 - val9 - val10 - val11 - val12
    if not _float_igual(val13, saldo_fim_calculado):
        return None
    
    # Função auxiliar para formatar período
    def fmt_periodo(p):
        if p:
            mes, ano = p
            return f"{mes:02d}/{ano}"
        return ""
    
    # Função auxiliar para formatar valores monetários
    def fmt_valor(v):
        return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    # Monta o resultado
    descricoes_orig_cred = {
        "01": "Crédito decorrente de operações próprias",
        "02": "Crédito transferido por pessoa jurídica sucedida"
    }
    
    resultado = {
        "REG": {
            "titulo": "Registro",
            "valor": reg
        },
        "PER_APU_CRED": {
            "titulo": "Período de Apuração do Crédito (MM/AAAA)",
            "valor": per_apu_cred,
            "valor_formatado": fmt_periodo(per_apu_cred_tuplo)
        },
        "ORIG_CRED": {
            "titulo": "Indicador da origem do crédito",
            "valor": orig_cred,
            "descricao": descricoes_orig_cred.get(orig_cred, "")
        },
        "COD_CRED": {
            "titulo": "Código do Tipo do Crédito, conforme Tabela 4.3.6",
            "valor": cod_cred
        },
        "VL_CRED_APU": {
            "titulo": "Valor total do crédito apurado na Escrituração Fiscal Digital ou em demonstrativo DACON",
            "valor": vl_cred_apu,
            "valor_formatado": fmt_valor(val1)
        },
        "VL_TOT_CRED_APU": {
            "titulo": "Valor Total do Crédito Apurado (06 + 07)",
            "valor": vl_tot_cred_apu,
            "valor_formatado": fmt_valor(val3)
        },
        "VL_CRED_DESC_PA_ANT": {
            "titulo": "Valor do Crédito utilizado mediante Desconto, em Período(s) Anterior(es)",
            "valor": vl_cred_desc_pa_ant,
            "valor_formatado": fmt_valor(val4)
        },
        "SD_CRED_DISP_EFD": {
            "titulo": "Saldo do Crédito Disponível para Utilização neste Período de Escrituração",
            "valor": sd_cred_disp_efd,
            "valor_formatado": fmt_valor(val7)
        }
    }
    
    # CNPJ_SUC: opcional, mas obrigatório se ORIG_CRED = 02
    if cnpj_suc:
        resultado["CNPJ_SUC"] = {
            "titulo": "CNPJ da pessoa jurídica cedente do crédito (se ORIG_CRED = 02)",
            "valor": cnpj_suc
        }
    else:
        resultado["CNPJ_SUC"] = {
            "titulo": "CNPJ da pessoa jurídica cedente do crédito (se ORIG_CRED = 02)",
            "valor": ""
        }
    
    # VL_CRED_EXT_APU: opcional
    if vl_cred_ext_apu:
        resultado["VL_CRED_EXT_APU"] = {
            "titulo": "Valor de Crédito Extemporâneo Apurado, referente a Período Anterior",
            "valor": vl_cred_ext_apu,
            "valor_formatado": fmt_valor(val2)
        }
    else:
        resultado["VL_CRED_EXT_APU"] = {
            "titulo": "Valor de Crédito Extemporâneo Apurado, referente a Período Anterior",
            "valor": "",
            "valor_formatado": ""
        }
    
    # VL_CRED_PER_PA_ANT: opcional
    if vl_cred_per_pa_ant:
        resultado["VL_CRED_PER_PA_ANT"] = {
            "titulo": "Valor do Crédito utilizado mediante Pedido de Ressarcimento, em Período(s) Anterior(es)",
            "valor": vl_cred_per_pa_ant,
            "valor_formatado": fmt_valor(val5)
        }
    else:
        resultado["VL_CRED_PER_PA_ANT"] = {
            "titulo": "Valor do Crédito utilizado mediante Pedido de Ressarcimento, em Período(s) Anterior(es)",
            "valor": "",
            "valor_formatado": ""
        }
    
    # VL_CRED_DCOMP_PA_ANT: opcional
    if vl_cred_dcomp_pa_ant:
        resultado["VL_CRED_DCOMP_PA_ANT"] = {
            "titulo": "Valor do Crédito utilizado mediante Declaração de Compensação Intermediária, em Período(s) Anterior(es)",
            "valor": vl_cred_dcomp_pa_ant,
            "valor_formatado": fmt_valor(val6)
        }
    else:
        resultado["VL_CRED_DCOMP_PA_ANT"] = {
            "titulo": "Valor do Crédito utilizado mediante Declaração de Compensação Intermediária, em Período(s) Anterior(es)",
            "valor": "",
            "valor_formatado": ""
        }
    
    # VL_CRED_DESC_EFD: opcional
    if vl_cred_desc_efd:
        resultado["VL_CRED_DESC_EFD"] = {
            "titulo": "Valor do Crédito descontado neste período de escrituração",
            "valor": vl_cred_desc_efd,
            "valor_formatado": fmt_valor(val8)
        }
    else:
        resultado["VL_CRED_DESC_EFD"] = {
            "titulo": "Valor do Crédito descontado neste período de escrituração",
            "valor": "",
            "valor_formatado": ""
        }
    
    # VL_CRED_PER_EFD: opcional
    if vl_cred_per_efd:
        resultado["VL_CRED_PER_EFD"] = {
            "titulo": "Valor do Crédito objeto de Pedido de Ressarcimento (PER) neste período de escrituração",
            "valor": vl_cred_per_efd,
            "valor_formatado": fmt_valor(val9)
        }
    else:
        resultado["VL_CRED_PER_EFD"] = {
            "titulo": "Valor do Crédito objeto de Pedido de Ressarcimento (PER) neste período de escrituração",
            "valor": "",
            "valor_formatado": ""
        }
    
    # VL_CRED_DCOMP_EFD: opcional
    if vl_cred_dcomp_efd:
        resultado["VL_CRED_DCOMP_EFD"] = {
            "titulo": "Valor do Crédito utilizado mediante Declaração de Compensação Intermediária neste período de escrituração",
            "valor": vl_cred_dcomp_efd,
            "valor_formatado": fmt_valor(val10)
        }
    else:
        resultado["VL_CRED_DCOMP_EFD"] = {
            "titulo": "Valor do Crédito utilizado mediante Declaração de Compensação Intermediária neste período de escrituração",
            "valor": "",
            "valor_formatado": ""
        }
    
    # VL_CRED_TRANS: opcional
    if vl_cred_trans:
        resultado["VL_CRED_TRANS"] = {
            "titulo": "Valor do crédito transferido em evento de cisão, fusão ou incorporação",
            "valor": vl_cred_trans,
            "valor_formatado": fmt_valor(val11)
        }
    else:
        resultado["VL_CRED_TRANS"] = {
            "titulo": "Valor do crédito transferido em evento de cisão, fusão ou incorporação",
            "valor": "",
            "valor_formatado": ""
        }
    
    # VL_CRED_OUT: opcional
    if vl_cred_out:
        resultado["VL_CRED_OUT"] = {
            "titulo": "Valor do crédito utilizado por outras formas",
            "valor": vl_cred_out,
            "valor_formatado": fmt_valor(val12)
        }
    else:
        resultado["VL_CRED_OUT"] = {
            "titulo": "Valor do crédito utilizado por outras formas",
            "valor": "",
            "valor_formatado": ""
        }
    
    # SLD_CRED_FIM: opcional
    if sld_cred_fim:
        resultado["SLD_CRED_FIM"] = {
            "titulo": "Saldo de créditos a utilizar em período de apuração futuro",
            "valor": sld_cred_fim,
            "valor_formatado": fmt_valor(val13)
        }
    else:
        resultado["SLD_CRED_FIM"] = {
            "titulo": "Saldo de créditos a utilizar em período de apuração futuro",
            "valor": "",
            "valor_formatado": ""
        }
    
    return resultado


def validar_1100(linhas, per_apu_escrit=None):
    """
    Valida uma ou mais linhas do registro 1100 do SPED EFD-Contribuições.
    
    Args:
        linhas: String com uma linha, string com múltiplas linhas separadas por \\n,
                ou lista de strings. Cada linha deve estar no formato:
                |1100|PER_APU_CRED|ORIG_CRED|CNPJ_SUC|COD_CRED|VL_CRED_APU|VL_CRED_EXT_APU|VL_TOT_CRED_APU|VL_CRED_DESC_PA_ANT|VL_CRED_PER_PA_ANT|VL_CRED_DCOMP_PA_ANT|SD_CRED_DISP_EFD|VL_CRED_DESC_EFD|VL_CRED_PER_EFD|VL_CRED_DCOMP_EFD|VL_CRED_TRANS|VL_CRED_OUT|SLD_CRED_FIM|
        per_apu_escrit: Período de apuração da escrituração atual (mmaaaa) - opcional, para validação
        
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
        resultado = _processar_linha_1100(linha, per_apu_escrit=per_apu_escrit)
        if resultado is not None:
            resultados.append(resultado)
    
    return json.dumps(resultados, ensure_ascii=False, indent=2)
