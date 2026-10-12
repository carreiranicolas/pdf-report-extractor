import os
import pandas as pd
from pathlib import PosixPath
import pdfplumber

from src.configs.parametros import PARAMETROS

def quantidade_arquivos_diretorio() -> int:

    """
    Obtém a quantidade de arquivos .pdf que tem no diretório de input
    
    Returns:
        int: quantidade de arquivos .pdf que tem no diretório de input

    """
    try:
        return len([
            arquivo for arquivo in os.listdir(PARAMETROS.diretorios.input)
            if os.path.isfile(os.path.join(PARAMETROS.diretorios.input, arquivo)) and ".pdf" in arquivo
        ])
    except Exception as error:
        print(f"Não foi possível obter a quantidade de arquivos .pdf {type(error)}: {error}")

def encontrar_pdf() -> PosixPath:
    """
    Encontra o .pdf dentro do diretório de input

    Returns:
        PosixPath: O path do arquivo .pdf no diretório de input
    
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
        ValueError: Se a variável de ambiente não estiver definida e nenhum valor padrão for fornecida
    
    """
    print("Iniciando a extração de dados do .pdf")
    path_pdf = encontrar_pdf()
    lista_dfs = []
    try:
        with pdfplumber.open(path_pdf) as pdf:
            for page in pdf.pages:
                table = page.extract_table()

                if table:
                    df = pd.DataFrame(table[1:], columns=table[0])
                    lista_dfs.append(df)
                else:
                    print(f"Nenhuma tabela encontrada para a página {page.page_number}")
        print("Extração finaliza.")
    except Exception as error:
        print(f"Não foi possível extrair os dados do pdf: {type(error)}: {error}")
    return lista_dfs