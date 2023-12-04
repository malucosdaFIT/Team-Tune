from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
import mysql.connector
import smtplib
from email.mime.text import MIMEText
import string
import random

app = Flask(__name__, static_folder='static')
app.secret_key = 'chave_secreta'
# Conectar ao banco de dados
conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='vini123',
    database='cadastro_emails',
    auth_plugin='mysql_native_password'
)

cursor = conexao.cursor()


# Função para enviar e-mail
def enviar_email(destinatario, assunto, corpo):
    remetente = 'rpa.bomfim2023@gmail.com'
    senha = 'akti fxch otto stgs'
    # ATENÇÃO: Não é recomendado inserir a senha diretamente no código

    msg = MIMEText(corpo)
    msg['Subject'] = assunto
    msg['From'] = remetente
    msg['To'] = destinatario

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(remetente, senha)
        server.sendmail(remetente, destinatario, msg.as_string())


@app.route('/cadastrar', methods=['POST'])
def cadastrar_email():
    try:
        data = request.get_json()
        email = data['email']
        senha = data['senha']

        # Inserir o email no banco de dados
        cursor.execute("INSERT INTO emails (email, senha) VALUES (%s, %s)", (email, senha))
        conexao.commit()

        # Enviar e-mail automático para o usuário
        assunto = "Bem-vindo ao nosso serviço!"
        corpo = """\
Venha dar seu Feedback!!
Clique no link abaixo.
http://127.0.0.1:5500/feedback

No trabalho, como em qualquer jornada, o apoio mútuo é nossa força.
Em um ambiente saudável, sonhos se tornam realizações, 
e o progresso é a trilha que seguimos juntos.

Contamos com sua participação!
"""

        enviar_email(email, assunto, corpo)
        return jsonify({'mensagem': 'E-mail cadastrado com sucesso!'}), 200
        
    except Exception as e:
        return jsonify({'mensagem': f'Erro ao cadastrar e-mail: {e}'}), 500
    

@app.route('/lista_emails', methods=['GET'])
def listar_emails():
    try:
        cursor.execute("SELECT * FROM emails")
        emails = cursor.fetchall()
        return render_template('lista_emails.html', emails=emails)
    except Exception as e:
        return jsonify({'mensagem': f'Erro ao cadastrar e-mail: {e}'}), 500

@app.route('/excluir/<int:id>', methods=['POST'])
def excluir_email(id):
    try:
        cursor.execute("DELETE FROM emails WHERE id = %s", (id,))
        conexao.commit()
        return jsonify({'mensagem': 'E-mail excluído com sucesso!'}), 200
    except Exception as e:
        return jsonify({'mensagem': f'Erro ao excluir e-mail: {e}'}), 500


@app.route('/feedback', methods=['GET'])
def feedback_form():
    return render_template('feedback_form.html')


@app.route('/enviar_feedback', methods=['POST'])
def enviar_feedback():
    try:
        data = request.get_json()
        nome = data['nome']
        email = data['email']
        feedback = data['feedback']

        # Enviar e-mail com o feedback
        assunto = "Novo Feedback Recebido"
        corpo = f"Nome: {nome}\nE-mail: {email}\nFeedback:\n{feedback}"
        enviar_email('rpa.bomfim2023@gmail.com', assunto, corpo)

        return jsonify({'mensagem': 'Feedback enviado com sucesso!'}), 200
    except Exception as e:
        return jsonify({'mensagem': f'Erro ao enviar feedback: {e}'}), 500


#@app.route('/login', methods=['POST'])
#def fazer_login():
#    try:
#        data = request.get_json()
#        email = data['email']
#        senha = data['senha']
#
#        # Verifique se o e-mail e a senha correspondem aos registros no banco de dados
#        cursor.execute("SELECT * FROM usuarios WHERE email = %s AND senha = %s", (email, senha))
#        usuario = cursor.fetchone()
#
#        if usuario:
#            # Se as credenciais estiverem corretas, redirecione para a página de feedback
#            return jsonify({'mensagem': 'Login bem-sucedido! Redirecionando para a página de feedback...'}), 200
#        else:
#            return jsonify({'mensagem': 'Credenciais inválidas. Tente novamente.'}), 401
#
#    except Exception as e:
#        return jsonify({'mensagem': f'Erro ao fazer login: {e}'}), 500
def gerar_senha_temporaria(tamanho=8):
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choice(caracteres) for _ in range(tamanho))


@app.route('/excluir_senhas', methods=['GET'])
def excluir_senhas():
    try:
        cursor.execute("UPDATE emails SET senha = ''")
        conexao.commit()
        return jsonify({'mensagem': 'Senhas excluídas com sucesso!'}), 200
    except Exception as e:
        return jsonify({'mensagem': f'Erro ao excluir senhas: {e}'}), 500


@app.route('/excluir_senhas_pagina', methods=['GET'])
def excluir_senhas_pagina():
    return render_template('excluir_senhas.html')


@app.route('/esqueceu_senha', methods=['GET', 'POST'])
def esqueceu_senha():
    if request.method == 'POST':
        email = request.form.get('email')

        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM emails WHERE email = %s", (email,))
        resultado = cursor.fetchone()
        cursor.fetchall()
        cursor.close()

        if resultado:
            # Gera uma nova senha temporária
            nova_senha_temporaria = gerar_senha_temporaria()

            # Atualiza a senha no banco de dados
            cursor = conexao.cursor()
            cursor.execute("UPDATE emails SET senha = %s WHERE email = %s",
                           (nova_senha_temporaria, email))
            conexao.commit()
            cursor.close()

            # Envia e-mail de recuperação
            assunto = "Recuperação de Senha"
            corpo = f"Sua nova senha temporária é: {nova_senha_temporaria}\n\nVocê pode redefinir sua senha clicando no seguinte link: http://127.0.0.1:5500/alterar_senha/{email}"
            enviar_email(email, assunto, corpo)

            flash('Verifique seu e-mail para obter instruções de recuperação.', 'success')
            return render_template('recuperacao_senha_confirmacao.html')

        flash('E-mail não encontrado. Certifique-se de inserir o e-mail correto.', 'error')

    return render_template('recuperacao_senha.html')


@app.route('/alterar_senha/<email>', methods=['GET', 'POST'])
def alterar_senha(email):
    if request.method == 'POST':
        nova_senha = request.form.get('nova_senha')

        cursor = conexao.cursor()
        cursor.execute("UPDATE emails SET senha = %s WHERE email = %s",
                       (nova_senha, email))
        conexao.commit()
        cursor.close()

        flash('Senha alterada com sucesso.', 'success')
        return redirect(url_for('formulario'))

    return render_template('alterar_senha.html', email=email)

@app.route('/')
def formulario():
    return render_template('formulario.html')

if __name__ == "__main__":
    app.run(debug=True, port=5500)

























####@app.route('/esqueceu_senha', methods=['GET', 'POST'])
#def esqueceu_senha():
#    if request.method == 'POST':
#        email = request.form.get('email')
#
#        cursor = db.cursor()
#        cursor.execute("SELECT * FROM colaborador WHERE email = %s", (email,))
#        resultado = cursor.fetchone()
#        cursor.fetchall()
#        cursor.close()
#
#        if resultado:
#            return redirect(url_for('redefinir_senha', email=email))
#
#        flash('E-mail não encontrado. Certifique-se de inserir o e-mail correto.', 'error')
#
#    return render_template('redefinir_senha.html')
#
#@app.route('/redefinir_senha/<email>', methods=['GET', 'POST'])
#def redefinir_senha(email):
#    if request.method == 'POST':
#        nova_senha = request.form['novaSenha']
#        confirmar_senha = request.form['confirmarSenha']
#
#        if nova_senha == confirmar_senha:
#            # Gerar o hash da nova senha
#            nova_senha_hash = generate_password_hash(nova_senha, method='sha256')
#
#            # Atualizar a senha no banco de dados
#            with conectar_bd() as conn:
#                cursor = conn.cursor()
#                cursor.execute("UPDATE emails SET senha = %s WHERE email = %s", (nova_senha_hash, email))
#                conn.commit()
#
#            flash('Senha redefinida com sucesso!', 'success')
#            return redirect(url_for('login'))
#        else:
#            flash('As senhas não coincidem. Tente novamente.', 'error')
#
#    return render_template('redefinir_senha.html', email=email)