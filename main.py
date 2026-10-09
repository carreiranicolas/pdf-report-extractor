from datetime import datetime
import os
import pandas as pd
from pathlib import Path
import pdfplumber


DATE =  datetime.now().strftime(format="%d%m%Y")



BASE_DIR = Path(__file__).parent
INPUT_DIR = BASE_DIR / 'input'
OUTPUT_DIR = BASE_DIR / 'output'

os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

PDF_FILE = next(INPUT_DIR.glob(pattern="*.pdf"))

with pdfplumber.open(PDF_FILE) as pdf:

    # Extrair tabelas
    dfs = []
    for page in pdf.pages:
        table = page.extract_table()

        if table:
            df = pd.DataFrame(table[1:], columns=table[0])
            dfs.append(df)

        else:
            print("Nenhuma tabela encontrada para esta página")

 
    # Montar o excel:
    
    df_valores = dfs.pop()

    df_merged = pd.concat(dfs, ignore_index=True)

    with pd.ExcelWriter(OUTPUT_DIR/ f'relatorio_pedido_{DATE}.xlsx') as writer:

        df_valores.to_excel(writer, sheet_name="Tabela de Itens", index=False)
        df_merged.to_excel(writer, sheet_name="Valores Finais", index=False)

