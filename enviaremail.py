import win32com.client as win32
import smtplib
import schedule
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# Função para enviar o e-mail


def enviar_email():
    smtp_server = 'smtp.gmail.com'
    smt_port = 587
    smtp_username = 'megamordex448@gmail.com'
    smtp_password = 'cpuqhszjdwjdbfwl'

    # Remetente e destinatário
    remetente = 'megamordex448@gmail.com'
    destinatario = 'dnkff448@gmail.com'

    # Construa a mensagem de e-mail
    msg = MIMEMultipart()
    msg['From'] = remetente
    msg['To'] = destinatario
    msg['Subject'] = 'Envio mensal de emails TeamTune'

    corpo_email = "To usando esse email aqui para testes."

    msg.attach(MIMEText(corpo_email, 'plain'))

    # Conecte-se ao servidor SMTP
    server = smtplib.SMTP(smtp_server, smt_port)
    server.starttls()
    server.login(smtp_username, smtp_password)

    # Envie o e-mail
    server.sendmail(remetente, destinatario, msg.as_string())

    # Encerre a conexão com o servidor SMTP
    server.quit()


# Agende o envio do e-mail mensalmente
schedule.every().month.at('09:00').do(enviar_email)


# Execute o agendamento em um loop
while True:
    schedule.run_pending()
    time.sleep(1)


