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

        try:
        
            return ParametrosModel(
                colunas_numericas=self.__obter_colunas_numericas(),
                diretorios=self.__obter_diretorios(),
                arquivo=self.__obter_arquivo(),
                sheets=self.__obter_sheets(),
            )
        except Exception as error:
            print(f"Erro ao obter dados de Parametros | {type(error)}: {error}")

    def __obter_colunas_numericas(self) -> list[ColunasNumericasModel]:
        
        colunas = self.__configs.get("COLUNAS_NUMERICAS", "")

        lista = []

        if colunas:
            try:
                for _, nome_coluna in colunas.items():
                    coluna = ColunasNumericasModel(nome_coluna)
                    lista.append(coluna)
                return lista
            except Exception as error:
                print(f"Erro {type(error)}: {error}")
        else:
            raise ValueError("Não foi possível obter as colunas numéricas")

    def __obter_diretorios(self):
        diretorios = self.__configs.get("DIRETORIOS", "")

        if diretorios:
            try:
                return DiretoriosModel(
                    input=self.caminho_absoluto / diretorios["INPUT"],
                    output=self.caminho_absoluto / diretorios["OUTPUT"]
                )
            except Exception as error:
                print(f"Erro {type(error)}: {error}")
        else:
            raise ValueError("Não foi possível obter os diretórios")

    def __obter_arquivo(self):
        arquivo = self.__configs.get("ARQUIVO_FINAL", "")
        diretorio_output = self.caminho_absoluto / self.__configs["DIRETORIOS"]["OUTPUT"]
        data_hoje = datetime.now().strftime(format="%d%m%Y")

        if arquivo:
            try:
                return ArquivoModel(
                    caminho=diretorio_output / f"{arquivo}_{data_hoje}.xlsx"
                )
            except Exception as error:
                print(f"Erro {type(error)}: {error}")

        else:
            raise ValueError(f"Não foi possível obter o nome do arquivo final")

    def __obter_sheets(self):
        sheets = self.__configs.get("SHEETS", "")

        if sheets:
            try:
                return SheetModel(
                    tabela_itens=sheets["SHEET_1"],
                    valores_finais=sheets["SHEET_2"]
                )
            except Exception as error:
                print(f"Erro {type(error)}: {error}")
        else:
            raise ValueError(f"Não foi possível obter os nomes das sheets")


PARAMETROS = Parametros().obter_parametros()