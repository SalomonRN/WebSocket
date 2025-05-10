from socketio import Server, WSGIApp
from eventlet import wsgi, listen
from socketio.exceptions import ConnectionRefusedError
from utils.mongo import init_connection
from utils.auth import validate_token, authenticate_user, create_token
from dotenv import load_dotenv
import time
from datetime import datetime

load_dotenv()
sio = Server(max_http_buffer_size=10000000 , cors_allowed_origins='*')
app = WSGIApp(sio)
@sio.event
def connect(sid, environ, auth):
    if auth is None:
        raise ConnectionRefusedError("No se enviaron credenciales")

    if 'token' in auth:
        token, message = validate_token(auth.get('token'))
        if not token:
            raise ConnectionRefusedError(message)
        token: dict = token['payload']
        sio.save_session(sid, {"name": token.get('username')})
        return

    user: dict = authenticate_user(auth)
    if not user:
        raise ConnectionRefusedError("Credenciales erróneas")
    
    token = create_token(user)
    sio.save_session(sid, {"name": user.get('username', "NONAME")})
    sio.emit("JWT", token, to=sid)

@sio.event
def disconnect(sid):
    session = sio.get_session(sid)

# TODOS
@sio.event
def message(sid, message, file):
    if file:
        with open("received_image.jpg", "wb") as f:
            a = f.write(file)
    date = _get_date()
    session = sio.get_session(sid)
    sio.emit("message", (message, session.get('name', "NO-NAME :("), date, file, "image/png"))


@sio.event
def create_chat(sid, room: str):
    session = sio.get_session(sid)    
    sio.enter_room(sid, room=room)
    return True, room

@sio.event
def exit_chat(sid, room):
    session = sio.get_session(sid)
    sio.leave_room(sid, room)

@sio.event
def chat_message(sid, message, file, room):
    date = _get_date()
    session = sio.get_session(sid)
    sio.emit('chat_message', (message, session.get('name', "NO-NAME :("), date, file, "image/png"), room=room)


def _get_date() -> dict:
    now = datetime.now()
    return  {"month": now.strftime("%B"), "day": now.day, "hour": now.hour, "min": now.minute}

if __name__ == "__main__":
    print("INICIANDO WEBSOCKET :))")
    init_connection()
    PORT = 5000
    print(f"Servidor en http://localhost:{PORT}")
    wsgi.server(listen(("0.0.0.0", PORT)), app)
