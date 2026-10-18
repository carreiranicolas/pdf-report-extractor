import mimetypes
import smtplib
import ssl

from email.message import EmailMessage
from src.configs.parametros import PARAMETROS
from src.configs.parametros_execucao import PARAMETROS_EXECUCAO
from src.utils.logger import obter_logger

logger = obter_logger(__name__)


def disparar_email(titulo: str, mensagem: str):
    """
    Realiza a conexão segura (via SSL) com o servidor do SMTP do gmail para disparar o email.
    
    Args:
        titulo (str): O titulo do email.
        mensagem (str): A mensagem inserida no email

    Raises:
        RuntimeError: Se ocorrer uma falha na comunicação com o servidor SMTP
    
    """


    msg = EmailMessage()

    msg["Subject"] = titulo
    msg["From"] = PARAMETROS_EXECUCAO.remetente
    msg["To"] = PARAMETROS_EXECUCAO.destinatario

    msg.set_content(mensagem)

    with PARAMETROS.arquivo.caminho.open("rb") as f:
        conteudo = f.read()

    tipo_mime, _ = mimetypes.guess_type(PARAMETROS.arquivo.caminho.name)

    if tipo_mime is None:
        tipo_mime = "application/octet-stream"

    tipo_principal, subtipo = tipo_mime.split("/", 1)

    msg.add_attachment(
        conteudo,
        maintype=tipo_principal,
        subtype=subtipo,
        filename=PARAMETROS.arquivo.caminho.name
    )

    context = ssl.create_default_context()

    logger.info(f"Enviando e-mail para {PARAMETROS_EXECUCAO.destinatario}")

    try:
        with smtplib.SMTP_SSL(
            "smtp.gmail.com",
            465,
            context=context
        ) as server:

            server.login(PARAMETROS_EXECUCAO.remetente, PARAMETROS_EXECUCAO.app_password)
            server.send_message(msg)

    except smtplib.SMTPException as error:
        raise RuntimeError(f"Falha ao enviar o e-mail para {PARAMETROS_EXECUCAO.destinatario}") from error

    logger.info("E-mail enviado com sucesso!")
