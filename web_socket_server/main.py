from eventlet import wsgi, listen
from web_socket.websocket import app as socket
from utils.mongo import init_connection

if __name__ == "__main__":
    init_connection()
    print("INICIANDO WEBSOCKET :))")
    PORT = 5000
    print(f"🚀 Servidor corriendo en http://localhost:{PORT}")
    wsgi.server(listen(("0.0.0.0", PORT)), socket)
