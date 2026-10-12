import os

from src.configs.parametros import PARAMETROS

def carregar_diretorios() -> bool | None:

    """Carrega os diretórios de input e output."""

    print("--> Realizando criação dos diretórios de INPUT & OUTPUT")

    try:

        os.makedirs(PARAMETROS.diretorios.input, exist_ok=True)
        os.makedirs(PARAMETROS.diretorios.output, exist_ok=True)
    except:
        raise ValueError("Não foi possível realizar a criação dos diretórios")

    print("--> Criação dos diretórios realizada")
