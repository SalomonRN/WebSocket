import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useSocket, SOCKET_URL, registryEvents } from "../context/SocketContext";
import { io } from "socket.io-client";

function Login() {
  const { socket, setSocket } = useSocket();
  const navigate = useNavigate();
  const [name, setName] = useState("");
  const [pass, setPass] = useState("");
 

  useEffect(() => {
    if (socket?.connected) {
      navigate('dashboard/')
    }
  }, [socket]);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const socket = io(SOCKET_URL, { auth: { username: name, password: pass } })
    socket.on("connect", () => { navigate("dashboard/") })
    setSocket(socket);
    registryEvents(socket)

  };

  return (
    <div>
      <h1>Login</h1>
      <form onSubmit={handleSubmit}>
        <label>Usuario</label>
        <input type="text" value={name} onChange={(e) => setName(e.target.value)} />
        <label>Contraseña</label>
        <input type="password" value={pass} onChange={(e) => setPass(e.target.value)} />
        <button type="submit">Ingresar</button>
      </form>
    </div>
  );
}

export default Login;
