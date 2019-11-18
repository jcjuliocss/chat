"""Docstring for main."""
from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = '4&f5y4l156'
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
    socketio.emit('message', json, broadcast=True,
                  callback=mensagem_recebida)


if __name__ == '__main__':
    socketio.run(app)
