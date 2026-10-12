import pandas as pd

from src.configs.parametros import PARAMETROS
from src.files.extrair_dados_pdf import extrair_dados_pdf
from src.tasks.carregar_diretorios import carregar_diretorios
from src.tasks.disparar_email import disparar_email
from src.tasks.tratamento_dfs import tratamento_dfs


def main():

    # Carregando os diretórios INPUT e OUTPUT

    carregar_diretorios()


    # Extraindo dados do pdf

    lista_dfs = extrair_dados_pdf()
    
    # Tratamento dos DFs:

    df_valores = lista_dfs.pop()

    df_merged = pd.concat(lista_dfs, ignore_index=True)

    df_tratado = tratamento_dfs(df_merged)

    # Montagem do arquivo Excel

    with pd.ExcelWriter(PARAMETROS.arquivo.caminho) as writer:

        df_valores.to_excel(writer, sheet_name=PARAMETROS.sheets.tabela_itens, index=False)
        df_tratado.to_excel(writer, sheet_name=PARAMETROS.sheets.valores_finais, index=False)


    # Disparo do email

    disparar_email("Teste", "Email de teste")

if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"Erro {type(error)}: {error}")
