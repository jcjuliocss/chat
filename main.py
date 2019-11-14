"""Docstring for main."""
from flask import Flask, render_template
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route('/')
def index():
    """."""
    return render_template('index.html')


@socketio.on('message')
def handle_message(message):
    """."""
    print('Mensagem recebida: ' + message)
    send(message, broadcast=True)


if __name__ == '__main__':
    socketio.run(app)
