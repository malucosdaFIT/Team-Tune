from flask import Flask, render_template, request, redirect, url_for, flash
import bcrypt
#from passlib.hash import bcrypt
import mysql.connector

app = Flask(__name__)
app.secret_key = 'hello word' 

# Conexão com o banco de dados 
db = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='vinicius123!',
    database='teamtune'
)

cursor = db.cursor()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome=request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        # Select
        cursor.execute("SELECT * FROM users WHERE username = %s", (nome,email))
        user = cursor.fetchone()

        if user:
            if bcrypt.checkpw(senha.encode('utf-8'), user[2].encode('utf-8')):
                return redirect('/sucesso')
            else:
                flash('Senha incorreta', 'error')
        else:
            flash('Usuário não encontrado', 'error')

    return render_template('login.html')


@app.route('/sucesso')
def sucesso():
    return render_template('sucesso.html')


if __name__ == '__main__':
    app.run(debug=True)
    
#pip install bcrypt