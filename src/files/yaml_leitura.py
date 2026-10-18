from pathlib import Path
from yaml import safe_load

def ler_arquivo_yaml(path_yaml: str | Path) -> dict:
    """

    Lê um arquivo YAML e retorna os dados contidos nele.

    Args:
        path_yaml (str | Path): O caminho completo para o arquivo YAML.

    Returns:
        dict: Um dicionário contendo os dados do arquivo YAML.

    Raises:
        FileNotFoundError: Se o arquivo YAML não existir.
        YAMLError: Se o conteúdo do arquivo não for um YAML válido.
        ValueError: Se o arquivo estiver vazio ou não for um dicionário.
    """

    with open(path_yaml, mode="r", encoding="utf-8") as arquivo_yaml:
        dados = safe_load(arquivo_yaml)

    if not isinstance(dados, dict):
        raise ValueError(f"O arquivo YAML {path_yaml} está vazio ou não possui o formato chave: valor")

    return dados
