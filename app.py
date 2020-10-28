from flask_socketio import SocketIO, emit
from flask import Flask, render_template, url_for, request
from pubsub import pub
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG'] = True
CORS(app, resources={r'*': {'origins': '*'}})

# turn the flask app into a socketio app
socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)

def listener(arg1):
    print('Function listener1 received:')
    print('  arg1 =', arg1)
    socketio.emit('newmessage',{'message':arg1})

pub.subscribe(listener, 'rootTopic')

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/post', methods=['POST'])
def post():
    pub.sendMessage('rootTopic', arg1='post')

@socketio.on('connect')
def connect():
    pub.sendMessage('rootTopic', arg1='connected to socket')
    print('Client connected')

if __name__ == '__main__':
    socketio.run(app)