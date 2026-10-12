def formatar_numerais(texto: str):
    """
    Função resposnsável pela formatação dos numerais presentes na tabela extraida do .pdf

    Args:
        texto (str): Texto a ser formatado para numeral
    
    Returns:
        str: String do númeral formatada

    Raises:
        ...
    """

    texto_formatado = texto.replace(".", "").replace(",", ".")

    return texto_formatado