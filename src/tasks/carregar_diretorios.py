import os

from src.configs.parametros import PARAMETROS
from src.utils.logger import obter_logger

logger = obter_logger(__name__)

def carregar_diretorios() -> bool | None:

    """Carrega os diretórios de input e output."""

    logger.info("Realizando criação dos diretórios de INPUT & OUTPUT")

    os.makedirs(PARAMETROS.diretorios.input, exist_ok=True)
    os.makedirs(PARAMETROS.diretorios.output, exist_ok=True)

    logger.info("Criação dos diretórios realizada")
