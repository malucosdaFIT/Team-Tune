import win32com.client as win32
import smtplib
import schedule
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


def enviar_email():  # Função para enviar o e-mail
    smtp_server = 'smtp.gmail.com'
    smt_port = 587
    smtp_username = 'megamordex448@gmail.com'
    smtp_password = 'cpuqhszjdwjdbfwl'

    remetente = 'megamordex448@gmail.com'  # Remetente e destinatário
    destinatario = 'dnkff448@gmail.com'

    msg = MIMEMultipart()  # Constroi o conteudo do email
    msg['From'] = remetente
    msg['To'] = destinatario
    msg['Subject'] = 'TeamTune'

    corpo_email = """<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Venha dar seu Feedback</title>
</head>
<body>
    <h1>
        <p>
            <b>TeamTune!</b>
        </p>
    </h1>
        <h2>
            Venha dar seu Feedback!!
        </h2>
        <h3>Em um ambiente de trabalho saudável, a criatividade floresce, e os desafios se tornam oportunidades.<br> 
            É onde o respeito mútuo e a colaboração constroem alicerces sólidos para o sucesso.<br>
            Nesse espaço, a motivação é uma chama constante, e a confiança é o elo que nos une.<br>
            Cada dia é uma chance de aprender e crescer, enquanto a positividade contagia a todos.<br> 
            No trabalho, como em qualquer jornada, o apoio mútuo é nossa força, e a empatia, nossa bússola.<br>
            Em um ambiente saudável, sonhos se tornam realizações, e o progresso é a trilha que seguimos juntos.<br>
            Nos ajude a melhorar e criar um ambiente de trabalho mais saudavél <br> 
            <p>
                <b>Contamos com sua participação!</b>
            </p>
        </p>
</body>
</html>
"""

    msg.attach(MIMEText(corpo_email, 'html'))

    server = smtplib.SMTP(smtp_server, smt_port)  # Conecta ao servidor SMTP
    server.starttls()
    server.login(smtp_username, smtp_password)

    server.sendmail(remetente, destinatario, msg.as_string())  # Envia o e-mail

    server.quit()  # Encerra a conexão com o servidor SMTP


schedule.every().day.at('00:23').do(enviar_email)


while True:
    schedule.run_pending()  # Executa o agendamento em loop
    time.sleep(1)
