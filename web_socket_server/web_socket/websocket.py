from socketio import Server, WSGIApp, AsyncServer
from eventlet import wsgi, listen
from socketio.exceptions import ConnectionRefusedError
from utils.mongo import init_connection
from utils.auth import validate_token, authenticate_user, create_token
from dotenv import load_dotenv
import time
from datetime import datetime

load_dotenv()
sio = AsyncServer(max_http_buffer_size=10000000 , cors_allowed_origins='*', async_mode='asgi')
app = WSGIApp(sio)

@sio.event
async def connect(sid, environ, auth):
    print("CONEXION ENTRANTE...")
    if auth is None:
        raise ConnectionRefusedError("No se enviaron credenciales")

    if 'token' in auth:
        token, message = validate_token(auth.get('token'))
        if not token:
            raise ConnectionRefusedError(message)
        token: dict = token['payload']
        print("CONEXION CON JWT ")
        await sio.save_session(sid, {"name": token.get('username')})
        return

    user: dict = authenticate_user(auth)
    if not user:
        raise ConnectionRefusedError("Credenciales erróneas")
    
    print("CONEXION CON USER PASS")
    token = create_token(user)
    print("IDENTIFICADOR: ", sid)
    await sio.save_session(sid, {"name": user.get('username', "NONAME")})
    await sio.emit("JWT", token, to=sid)

@sio.event
async def disconnect(sid):
    session = await sio.get_session(sid)
    print(f"❌ Cliente desconectado: {sid} {session.get('name', "NO-NAME :(")}")

# TODOS
@sio.event
async def message(sid, message, file):
    print("MENSAJE ENTRANTE.....")
    if file:
        with open("received_image.jpg", "wb") as f:
            a = f.write(file)
    date = _get_date()
    session = await sio.get_session(sid)
    await sio.emit("message", (message, session.get('name', "NO-NAME :("), date, file, "image/png"))


@sio.event
async def create_chat(sid, room: str):
    session = await sio.get_session(sid)
    print(session.get("name"), "ENTRANDO A: ", room)
    
    await sio.enter_room(sid, room=room)
    return True, room

@sio.event
async def exit_chat(sid, room):
    print("SALIENDO DEL CHAT...")
    session = await sio.get_session(sid)
    print(session.get("name"), "SALIENDO DE: ", room)
    await sio.leave_room(sid, room)

@sio.event
async def chat_message(sid, message, file):
    date = _get_date()
    session = await sio.get_session(sid)
    await sio.emit('chat_message', (message, session.get('name', "NO-NAME :("), date, file, "image/png"), room='chat_users')


def _get_date() -> dict:
    now = datetime.now()
    return  {"month": now.strftime("%B"), "day": now.day, "hour": now.hour, "min": now.minute}

if __name__ == "__main__":
    print("INICIANDO WEBSOCKET :))")
    init_connection()
    PORT = 5000
    print(f"🚀 Servidor corriendo en http://localhost:{PORT}")
    wsgi.server(listen(("0.0.0.0", PORT)), app)
