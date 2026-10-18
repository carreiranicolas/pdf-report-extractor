import os

from datetime import datetime
from pathlib import Path


from src.files.yaml_leitura import ler_arquivo_yaml
from src.models.parametros import (
    ArquivoModel,
    ColunasNumericasModel,
    DiretoriosModel,
    ParametrosModel,
    SheetModel
)
from src.utils.logger import obter_logger

logger = obter_logger(__name__)

class Parametros:
    """Classe responsável por carregar os parâmetros de configuração"""

    def __init__(self):
        self.__configs = ler_arquivo_yaml(os.path.join(r"./resources/configs/geral.yaml"))
        self.caminho_absoluto = Path().absolute()

    def obter_parametros(self):
        """
        Obtém os parâmetros de configuração.

        Essa função centraliza a chamada das funções específicas para carregar
        os parâmetros de configuração.

        Returns:
            Parametros: Objeto contendo todos os parâmetroS.
        """

        return ParametrosModel(
            colunas_numericas=self.__obter_colunas_numericas(),
            diretorios=self.__obter_diretorios(),
            arquivo=self.__obter_arquivo(),
            sheets=self.__obter_sheets(),
        )

    def __obter_colunas_numericas(self) -> list[ColunasNumericasModel]:

        colunas = self.__configs.get("COLUNAS_NUMERICAS", "")

        if not colunas:
            raise ValueError("Não foi possível obter as colunas numéricas")

        return [ColunasNumericasModel(nome_coluna) for nome_coluna in colunas.values()]

    def __obter_diretorios(self):
        diretorios = self.__configs.get("DIRETORIOS", "")

        if not diretorios:
            raise ValueError("Não foi possível obter os diretórios")

        return DiretoriosModel(
            input=self.caminho_absoluto / diretorios["INPUT"],
            output=self.caminho_absoluto / diretorios["OUTPUT"]
        )

    def __obter_arquivo(self):
        arquivo = self.__configs.get("ARQUIVO_FINAL", "")

        if not arquivo:
            raise ValueError("Não foi possível obter o nome do arquivo final")

        diretorio_output = self.caminho_absoluto / self.__configs["DIRETORIOS"]["OUTPUT"]
        data_hoje = datetime.now().strftime(format="%d%m%Y")

        return ArquivoModel(
            caminho=diretorio_output / f"{arquivo}_{data_hoje}.xlsx"
        )

    def __obter_sheets(self):
        sheets = self.__configs.get("SHEETS", "")

        if not sheets:
            raise ValueError("Não foi possível obter os nomes das sheets")

        return SheetModel(
            tabela_itens=sheets["SHEET_1"],
            valores_finais=sheets["SHEET_2"]
        )


# Os parâmetros são carregados na importação, fora do try/except do main.py.
# Por isso o erro é registrado aqui antes de ser relançado: senão ele não chegaria ao arquivo de log.
try:
    PARAMETROS = Parametros().obter_parametros()
except Exception:
    logger.exception("Erro ao carregar os parâmetros do arquivo geral.yaml")
    raise
