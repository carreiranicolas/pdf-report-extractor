import os
import pandas as pd
from pathlib import Path
import pdfplumber

from src.configs.parametros import PARAMETROS
from src.utils.logger import obter_logger

logger = obter_logger(__name__)

def quantidade_arquivos_diretorio() -> int:

    """
    Obtém a quantidade de arquivos .pdf que tem no diretório de input

    Returns:
        int: quantidade de arquivos .pdf que tem no diretório de input

    """
    return len([
        arquivo for arquivo in os.listdir(PARAMETROS.diretorios.input)
        if os.path.isfile(os.path.join(PARAMETROS.diretorios.input, arquivo)) and ".pdf" in arquivo
    ])

def encontrar_pdf() -> Path:
    """
    Encontra o .pdf dentro do diretório de input

    Returns:
        Path: O path do arquivo .pdf no diretório de input

    Raises:
        ValueError: Se não for encontrado o .pdf ou se forem encontrados mais de um

    """

    if quantidade_arquivos_diretorio() > 1:
        raise ValueError("Mais de um pdf na pasta de input")

    if quantidade_arquivos_diretorio() < 1:
        raise ValueError("Nenhum pdf encontrado na pasta de input")

    path_pdf = next(PARAMETROS.diretorios.input.glob(pattern="*.pdf"))

    return path_pdf

def extrair_dados_pdf() -> list[pd.DataFrame]:
    """
    Extrai os dados do pdf e os transforma em DFs.

    Returns:
        list[DataFrame]: Uma lista com todos os dataframes montados a partir da extração

    Raises:
        ValueError: Se o pdf não for encontrado ou se nenhuma tabela for encontrada nele

    """
    path_pdf = encontrar_pdf()
    logger.info(f"Iniciando a extração de dados do pdf {path_pdf.name}")
    lista_dfs = []

    with pdfplumber.open(path_pdf) as pdf:
        for page in pdf.pages:
            table = page.extract_table()

            if table:
                df = pd.DataFrame(table[1:], columns=table[0])
                lista_dfs.append(df)
            else:
                logger.warning(f"Nenhuma tabela encontrada na página {page.page_number}")

    if not lista_dfs:
        raise ValueError(f"Nenhuma tabela encontrada no pdf {path_pdf.name}")

    logger.info(f"Extração finalizada: {len(lista_dfs)} tabela(s) encontrada(s)")
    return lista_dfs
