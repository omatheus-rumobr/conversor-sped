def formatar_cpf(cpf_str):
    """
    Formata CPF para o formato XXX.XXX.XXX-XX.
    
    Args:
        cpf_str: String com CPF sem formatação
        
    Returns:
        String formatada ou a string original se inválida
    """
    if not cpf_str or len(cpf_str) != 11:
        return cpf_str
    
    try:
        return f"{cpf_str[0:3]}.{cpf_str[3:6]}.{cpf_str[6:9]}-{cpf_str[9:11]}"
    except:
        return cpf_str
