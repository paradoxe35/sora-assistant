import eventlet
import socketio
from dotenv import load_dotenv

load_dotenv()

from env import APP_SERVER_PORT  # noqa

sio = socketio.Server(async_mode='eventlet')
app = socketio.WSGIApp(sio, static_files=None)


@sio.event
def connect(sid, environ):
    print('connect ', sid)


@sio.on('recording')
def recording(sid, data):
    print('message ', data)


@sio.event
def disconnect(sid):
    print('disconnect ', sid)


# run app
if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', APP_SERVER_PORT)), app)
