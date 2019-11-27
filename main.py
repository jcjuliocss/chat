"""Docstring for main."""
from flask import Flask, render_template, session, request, redirect
from flask_socketio import SocketIO
from datetime import datetime
from Usuario import Usuario

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

usuarios = Usuario()


@app.route("/")
def login():
    """."""
    return render_template("login.html")


@app.route("/logar", methods=['POST'])
def logar():
    """."""
    dados = request.form
    session['nome'] = dados.get("login")

    return redirect("/index")


@app.route('/index', methods=['GET'])
def index():
    """."""
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
    usuarios.insere_usuario(json['nome'])
    print(id(usuarios.lista_usuarios))
    json['lista_usuarios'] = usuarios.lista_usuarios
    print(usuarios.lista_usuarios)
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
    usuarios.remove_usuario(json['nome'])
    print(id(usuarios.lista_usuarios))
    json['lista_usuarios'] = usuarios.lista_usuarios
    print(usuarios.lista_usuarios)
    socketio.emit('connection', json)


if __name__ == '__main__':
    socketio.run(app)
