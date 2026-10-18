import os
from dotenv import load_dotenv

from src.models.parametros_execucao import ParametrosExecucaoModel
from src.utils.logger import obter_logger

logger = obter_logger(__name__)


class ParametrosExecucao:
    def __init__(self):
        """Inicializa a classe, carregando as variáveis de ambiente a partir do arquivo `.env`."""

        load_dotenv()

    def obter_parametros_execucao(self):
        """Obtém os valores da variavel ambiente e instancia ParametrosExecucaoModel"""

        return ParametrosExecucaoModel(
            remetente=self.__obter_variavel_ambiente("FROM_EMAIL"),
            destinatario=self.__obter_variavel_ambiente("TO_EMAIL"),
            app_password=self.__obter_variavel_ambiente("APP_EMAIL_PASSWORD")
        )

    def __obter_variavel_ambiente(self, nome_variavel: str, padrao: str = None) -> str:
        """
        Recupera o valor de uma variável de ambiente.
        
        Args:
            nome_variavel (str): O nome da variável de ambiente.
            padrao (str, opcional): O valor padrão a ser retornado caso a variável não esteja definida
        
        Returns:
            str: O valor da variável de ambiente ou o valor padrão, se não estiver definida.
        
        Raises:
            ValueError: Se a variável de ambiente não estiver definida e nenhum valor padrão for fornecida
        
        """

        valor = os.getenv(nome_variavel, padrao)

        if valor is None:
            raise ValueError(f"A varíavel de ambiente {nome_variavel} não está definida")

        return valor


# Mesmo motivo de PARAMETROS: o carregamento acontece na importação, então o erro é registrado aqui.
try:
    PARAMETROS_EXECUCAO = ParametrosExecucao().obter_parametros_execucao()
except Exception:
    logger.exception("Erro ao carregar as variáveis de ambiente do arquivo .env")
    raise
