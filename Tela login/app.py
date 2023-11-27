from flask import Flask, render_template, request, redirect, url_for, flash
import smtplib
from email.mime.text import MIMEText
import random
import string
import mysql.connector

app = Flask(__name__)
app.secret_key = 'chave_secreta'

# Conexão com o banco de dados
db = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='vinicius123!',
    database='teamtune'
)


def enviar_email(destinatario, assunto, corpo):
    remetente = 'vinicius.rcunha.rpa@gmail.com'
    senha = 'ydfp ikpy grfg yken'

    msg = MIMEText(corpo)
    msg['Subject'] = assunto
    msg['From'] = remetente
    msg['To'] = destinatario

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(remetente, senha)
        server.sendmail(remetente, destinatario, msg.as_string())


def gerar_senha(tamanho=8):
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choice(caracteres) for _ in range(tamanho))


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        cursor = db.cursor()
        cursor.execute(
            "SELECT * FROM colaborador WHERE email = %s AND senha = %s", (email, senha))
        resultado = cursor.fetchone()
        cursor.fetchall()
        cursor.close()

        if resultado:
            return redirect(url_for('feedback_form'))
        else:
            flash('Credenciais incorretas', 'error')

    return render_template('login.html')


@app.route('/esqueceu_senha', methods=['GET', 'POST'])
def esqueceu_senha():
    if request.method == 'POST':
        email = request.form.get('email')

        cursor = db.cursor()
        cursor.execute("SELECT * FROM colaborador WHERE email = %s", (email,))
        resultado = cursor.fetchone()
        cursor.fetchall()
        cursor.close()

        if resultado:
            return redirect(url_for('alterar_senha', email=email))

        flash('E-mail não encontrado. Certifique-se de inserir o e-mail correto.', 'error')

    return render_template('recuperacao_senha.html')

@app.route('/alterar_senha/<email>', methods=['GET', 'POST'])
def alterar_senha(email):
    if request.method == 'POST':
        nova_senha = request.form.get('nova_senha')

        cursor = db.cursor()
        cursor.execute("UPDATE colaborador SET senha = %s WHERE email = %s",
                       (nova_senha, email))
        db.commit()
        cursor.close()

        flash('Senha alterada com sucesso.', 'success')
        return redirect(url_for('login'))

    return render_template('alterar_senha.html', email=email)

@app.route('/feedback', methods=['GET'])
def feedback_form():
    return render_template('feedback_form.html')


if __name__ == '__main__':
    app.run(port=8000, debug=True)
