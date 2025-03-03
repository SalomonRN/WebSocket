from socketio import Server, WSGIApp
import eventlet
from socketio.exceptions import ConnectionRefusedError
from auth import authenticate_user, validate_token, create_token
from mongo import init_connection
from dotenv import load_dotenv
 
load_dotenv()

sio = Server(cors_allowed_origins="*")
app = WSGIApp(sio)

@sio.event
def connect(sid, environ, auth):
    if auth is None:
        raise ConnectionRefusedError("No se enviaron credenciales")
    print(auth)
    if 'token' in auth:
        print("SI HAY TOKEN")
        token, message = validate_token(auth.get('token'))
        if not token:
            raise ConnectionRefusedError(message)
        return 
    
    user: dict = authenticate_user(auth)
    if not user:
        raise ConnectionRefusedError("Credenciales erróneas")
    
    token = create_token(user)
    # sio.save_session(sid, token)
    print("EMITIMOS TOKEN -------------------------")
    sio.emit("JWT", token, to=sid)

@sio.event
def my_message(sid, data):
    session = sio.get_session(sid)
    print(f"📩 Mensaje de {session['name']} ({sid}): {data}")
    sio.emit("message", f"Echo: {data}", to=sid)

@sio.event
def disconnect(sid):
    print(f"❌ Cliente desconectado: {sid}")

if __name__ == "__main__":
    print("INICIANDO WEBSOCKET")
    init_connection()
    print("🚀 Servidor corriendo en http://localhost:5000")
    eventlet.wsgi.server(eventlet.listen(("0.0.0.0", 5000)), app)
