def formatar_data(data_str):
    """
    Formata data do formato DDMMYYYY para DD/MM/YYYY.
    
    Args:
        data_str: String com data no formato DDMMYYYY
        
    Returns:
        String formatada como DD/MM/YYYY ou a string original se inválida
    """
    if not data_str or len(data_str) != 8:
        return data_str
    
    try:
        return f"{data_str[0:2]}/{data_str[2:4]}/{data_str[4:8]}"
    except:
        return data_str
