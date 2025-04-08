from socketio import ASGIApp
from api.app import app as flask_app
from web_socket.websocket import sio as socket
from utils.mongo import init_connection

if __name__ == "__main__":
    init_connection()
    print("INICIANDO WEBSOCKET :))")
    PORT = 5000
    print(f"🚀 Servidor corriendo en http://localhost:{PORT}")
    import uvicorn
    uvicorn.run(ASGIApp(socket, flask_app), host='0.0.0.0', port=5000)
    