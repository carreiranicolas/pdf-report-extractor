import mimetypes
import os
import pdfplumber
import smtplib
import ssl


from dotenv import load_dotenv
from datetime import datetime
from email.message import EmailMessage
import pandas as pd
from pathlib import Path
from src.utils.formatar_numerais import formatar_numerais



load_dotenv()


BASE_DIR = Path(__file__).parent
INPUT_DIR = BASE_DIR / 'input'
OUTPUT_DIR = BASE_DIR / 'output'

DATE =  datetime.now().strftime(format="%d%m%Y")

os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

PDF_FILE = next(INPUT_DIR.glob(pattern="*.pdf"))


dfs = []
with pdfplumber.open(PDF_FILE) as pdf:

    # Extrair tabelas
    
    for page in pdf.pages:
        table = page.extract_table()

        if table:
            df = pd.DataFrame(table[1:], columns=table[0])
            dfs.append(df)

        else:
            print("Nenhuma tabela encontrada para esta página")



colunas_valores = [
    "Qtd",
    "Valor unit. (R$)",
    "Valor total (R$)"

]
 
# Tratamento e montagem do arquivo excel:

df_valores = dfs.pop()

df_merged = pd.concat(dfs, ignore_index=True)


for coluna in colunas_valores:
    df_merged[coluna] = pd.to_numeric(df_merged[coluna].map(formatar_numerais), errors='coerce')


with pd.ExcelWriter(OUTPUT_DIR/ f'relatorio_pedido_{DATE}.xlsx') as writer:

    df_valores.to_excel(writer, sheet_name="Tabela de Itens", index=False)
    df_merged.to_excel(writer, sheet_name="Valores Finais", index=False)

# disparo do email

SENDER_EMAIL = os.getenv("FROM_EMAIL", "")
RECEIVER_EMAIL = os.getenv("TO_EMAIL", "")
APP_EMAIL_PASSWORD = os.getenv("APP_EMAIL_PASSWORD", "")

msg = EmailMessage()
msg["Subject"] = "Relatório gerado pelo Python"
msg["From"] = SENDER_EMAIL
msg["To"] = RECEIVER_EMAIL

msg.set_content("""
Olá!

Segue em anexo o relatório solicitado.

Atenciosamente,
Nicolas
""")

arquivo = OUTPUT_DIR/ f'relatorio_pedido_{DATE}.xlsx'

with arquivo.open("rb") as f:
    conteudo = f.read()

tipo_mime, _ = mimetypes.guess_type(arquivo)

if tipo_mime is None:
    tipo_mime = "application/octet-stream"

tipo_principal, subtipo = tipo_mime.split("/", 1)

msg.add_attachment(
    conteudo,
    maintype=tipo_principal,
    subtype=subtipo,
    filename=arquivo.name
)

context = ssl.create_default_context()

try:
    with smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465,
        context=context
    ) as server:

        server.login(SENDER_EMAIL, APP_EMAIL_PASSWORD)
        server.send_message(msg)

    print("E-mail enviado com sucesso!")

except Exception as e:
    print(f"Falha ao enviar o e-mail: {e}")
