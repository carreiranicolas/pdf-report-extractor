from yaml import safe_load

def ler_arquivo_yaml(path_yaml: str):
    """
     
    Lê um arquivo YAML e retorna os dados contidos nele.

    Args:
        caminho_arquivo_yaml (str): O caminho completo para o arquivo YAML.

    Returns:
        dict: Um dicionário contendo os dados do arquivo YAML.

    Raises:
        Exibirá o erro se ocorrer um erro ao ler o arquivo YAML.
    """

    
    try:
        with open(path_yaml, mode="r", encoding="utf-8") as arquivo_yaml:
            return safe_load(arquivo_yaml)
    except Exception as error:
        print(f"Erro ao ler arquivo YAML! | {type(error)}: {error}, linha {error.__traceback__.tb_lineno}")