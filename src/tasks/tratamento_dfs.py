import pandas as pd

from src.configs.parametros import PARAMETROS
from src.utils.formatar_numerais import formatar_numerais
from src.utils.logger import obter_logger

logger = obter_logger(__name__)

def converter_para_numeral(df: pd.DataFrame):
    """
    Realiza a conversão de colunas para numeral.
    
    Args:
        df (DataFrame): o dataframe recebido para ter a coluna convertida
    
    Returns:
        DataFrame: O dataframe com as colunas convertidas para numeral
    """

    df = df.copy()
    logger.info("Convertendo colunas do df para numeral")
    for coluna in PARAMETROS.colunas_numericas:
        df[coluna.nome] = pd.to_numeric(df[coluna.nome].map(formatar_numerais), errors='coerce')

    return df

def tratamento_dfs(df: pd.DataFrame):
    """
    Função que centraliza as funções de tratamento.
    
    Args:
        df(DataFrame): Recebe o DataFrame que será tratado
    
    Returns:
        DataFrame: retorna o DataFrame tratado
    
    """
    logger.info("Iniciando tratamento do df extraído")
    df_numeral_convertido = converter_para_numeral(df)

    return df_numeral_convertido