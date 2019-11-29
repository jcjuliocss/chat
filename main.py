"""Docstring for main."""
from flask import Flask, render_template, session, request, redirect
from flask_socketio import SocketIO
from flask_sslify import SSLify
from datetime import datetime
import psycopg2

app = Flask(__name__)
sslify = SSLify(app)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


def conectar():
        """."""
        p = 'f58a406d6ec66146ad5701f458108c0c35c1997dcbc7826eb7fb75161c2a9257'
        conn = \
            psycopg2.connect(
                user="bwciolhujcnndr",
                password=p,
                host="ec2-174-129-238-192.compute-1.amazonaws.com",
                port="5432",
                database="d6n4gbdm74cfr6")

        return conn


def monta_retorno(colunas, valores):
        """."""
        retorno = []
        for i in range(len(valores)):
            dict = {}
            for j in range(len(colunas)):
                dict[colunas[j][0]] = valores[i][j]
            retorno.append(dict)

        return retorno

conn = conectar()
cursor = conn.cursor()


@app.route("/")
def login():
    """."""
    return render_template("login.html")


@app.route("/logar", methods=['POST'])
def logar():
    """."""
    dados = request.form
    session['nome'] = dados.get("login")

    query = "INSERT INTO usuarios_temp(nome) " \
            + "VALUES('%s');" % (session['nome'])
    cursor.execute(query)
    conn.commit()

    return redirect("/index")


@app.route('/index', methods=['GET'])
def index():
    """."""
    if 'nome' not in session:
        return redirect('/')
    return render_template('index.html', nome=session['nome'])


@socketio.on('send message')
def handle_message(json):
    """."""
    hora = datetime.now().strftime('%H')
    minutos = datetime.now().strftime('%M')
    json['horario'] = str(int(hora) - 3) + ':' + minutos
    json['nome'] = session['nome']
    if 'texto' in json and len(json['texto']) > 300:
        json['texto'] = json['texto'][:300]
    print('Mensagem recebida: ' + str(json))
    socketio.emit('message', json)


@socketio.on('connect message')
def handle_connect(json):
    """."""
    hora = datetime.now().strftime('%H')
    minutos = datetime.now().strftime('%M')
    json['horario'] = str(int(hora) - 3) + ':' + minutos
    json['nome'] = session['nome']
    json['texto'] = ' conectado.'
    print("Usuario conectado")
    query = 'select column_name from ' +\
            'information_schema.columns where table_name ' +\
            '= \'' + 'usuarios_temp' + '\';'

    cursor.execute(query)
    q = cursor.fetchall()
    cursor.execute("SELECT * FROM usuarios_temp;")
    usuarios = cursor.fetchall()
    m = monta_retorno(q, usuarios)
    json['lista_usuarios'] = m
    socketio.emit('connection', json)


@socketio.on('disconnect message')
def handle_disconnect(json):
    """."""
    hora = datetime.now().strftime('%H')
    minutos = datetime.now().strftime('%M')
    json['horario'] = str(int(hora) - 3) + ':' + minutos
    json['nome'] = session['nome']
    json['texto'] = ' desconectado.'
    print("Usuario desconectado")
    deleta_usuario(json['nome'])
    cursor.execute("SELECT * FROM usuarios_temp;")
    usuarios = cursor.fetchall()
    query = 'select column_name from ' +\
            'information_schema.columns where table_name ' +\
            '= \'' + 'usuarios_temp' + '\';'

    cursor.execute(query)
    q = cursor.fetchall()
    m = monta_retorno(q, usuarios)
    json['lista_usuarios'] = m
    del(session['nome'])
    socketio.emit('connection', json)


def deleta_usuario(nome):
    """."""
    query = "DELETE FROM usuarios_temp WHERE nome = '%s';" % (nome)
    cursor.execute(query)
    conn.commit()


if __name__ == '__main__':
    socketio.run(app)
