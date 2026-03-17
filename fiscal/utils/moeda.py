def formatar_valor_monetario(valor_str):
    """
    Formata valor monetário substituindo vírgula por ponto para compatibilidade com Excel.
    
    Args:
        valor_str: String com valor monetário (formato brasileiro com vírgula)
        
    Returns:
        String formatada ou a string original se inválida
    """
    if not valor_str:
        return valor_str
    
    try:
        return valor_str.replace(',', '.')
    except:
        return valor_str
