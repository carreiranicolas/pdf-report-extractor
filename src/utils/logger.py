import logging

from datetime import datetime
from pathlib import Path


DIRETORIO_LOGS = Path().absolute() / "logs"
FORMATO_LOG = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
FORMATO_DATA = "%d/%m/%Y %H:%M:%S"


def __configurar_logging():
    """
    Configura o logging da aplicação uma única vez.

    Os logs são exibidos no terminal e gravados em um arquivo diário dentro do diretório `logs`.
    Se o logging já estiver configurado, a função não faz nada.
    """

    logger_raiz = logging.getLogger()

    if logger_raiz.handlers:
        return

    DIRETORIO_LOGS.mkdir(exist_ok=True)
    arquivo_log = DIRETORIO_LOGS / f"execucao_{datetime.now():%Y-%m-%d}.log"

    formatador = logging.Formatter(FORMATO_LOG, datefmt=FORMATO_DATA)

    handler_terminal = logging.StreamHandler()
    handler_terminal.setFormatter(formatador)

    handler_arquivo = logging.FileHandler(arquivo_log, encoding="utf-8")
    handler_arquivo.setFormatter(formatador)

    logger_raiz.setLevel(logging.INFO)
    logger_raiz.addHandler(handler_terminal)
    logger_raiz.addHandler(handler_arquivo)

    # Bibliotecas de terceiros que geram muitos logs: só exibe avisos e erros
    logging.getLogger("pdfminer").setLevel(logging.WARNING)


def obter_logger(nome: str) -> logging.Logger:
    """
    Obtém um logger já configurado.

    Args:
        nome (str): Nome do logger, normalmente `__name__` do módulo que o utiliza.

    Returns:
        Logger: O logger pronto para uso.
    """

    __configurar_logging()

    return logging.getLogger(nome)
