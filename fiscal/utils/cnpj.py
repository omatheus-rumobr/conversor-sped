def formatar_cnpj(cnpj_str):
    """
    Formata CNPJ para o formato XX.XXX.XXX/XXXX-XX.
    
    Args:
        cnpj_str: String com CNPJ sem formatação
        
    Returns:
        String formatada ou a string original se inválida
    """
    if not cnpj_str or len(cnpj_str) != 14:
        return cnpj_str
    
    try:
        return f"{cnpj_str[0:2]}.{cnpj_str[2:5]}.{cnpj_str[5:8]}/{cnpj_str[8:12]}-{cnpj_str[12:14]}"
    except:
        return cnpj_str
