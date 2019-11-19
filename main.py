"""Docstring for main."""
from flask import Flask, render_template
from flask_socketio import SocketIO
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route('/')
def index():
    """."""
    return render_template('index.html')


def mensagem_recebida():
    """."""
    print('Mensagem recebida')


@socketio.on('my event')
def handle_message(json):
    """."""
    print('Mensagem recebida: ' + str(json))
    json['horario'] = datetime.now().strftime('%H:%M')
    socketio.emit('message', json, callback=mensagem_recebida)


if __name__ == '__main__':
    socketio.run(app)
