from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__) 

# Conexão com o banco de dados 
db = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='vinicius123!',
    database='teamtune'
)
@app.route('/')
def index():
    return render_template('login.html')
    
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method== 'POST':
        email = request.form['email']
        senha = request.form['senha']

        cursor = db.cursor()
        cursor.execute("SELECT * FROM colaborador WHERE email = %s AND senha = %s", (email, senha))
        resultado = cursor.fetchone()
        cursor.close()
        print(resultado)
    if resultado:
        return redirect(url_for('sucesso'))
    else:
         return render_template('login.html', error='Credenciais incorretas')
   
@app.route('/sucesso')
def sucesso():
    return render_template('feedback.html')


if __name__ == '__main__':
    app.run(port=8000,debug=True)
