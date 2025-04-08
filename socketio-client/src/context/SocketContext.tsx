import { createContext, useContext, useEffect, useState } from "react";
import { io, Socket } from "socket.io-client";

export const SOCKET_URL = "ws://localhost:5000";

interface SocketType {
  socket: Socket | null | undefined,
  setSocket: (socket: Socket) => void;
}
const SocketContext = createContext<SocketType | undefined>(undefined);

// Crear el proveedor del contexto
export const SocketProvider = ({ children }: { children: React.ReactNode }) => {
  const [socket, setSocket] = useState<Socket | null | undefined>(null);

  useEffect(() => {
    let newSocket: Socket;
    const JWT = localStorage.getItem('JWT')
    if (!JWT) { return }
    newSocket = io(SOCKET_URL, { auth: { token: JWT } });
    newSocket.on("connect", () => {
      console.log("Conectado al servidor CON JWT");
      setSocket(newSocket);
    });

    return () => {
      newSocket.disconnect();
    };
  }, []);

  return (
    <SocketContext.Provider value={{ socket, setSocket }}>
      {children}
    </SocketContext.Provider>
  );
};

// Hook para acceder al socket desde cualquier componente
export const useSocket = () => {
  const context = useContext(SocketContext);
  if (!context) {
    throw new Error("useSocket debe usarse dentro de un SocketProvider");
  }
  return context;
};


export const registryEvents = (socket: Socket) => {
  socket.on('connect', () => {
    console.log("CONETADOSSSS")

  })

  socket.on('connect_error', (message) => { console.error("ERROR :C", message) })

  socket.on("JWT", (newToken: string) => {
    console.log("Token recibido:", newToken);
    localStorage.setItem("JWT", newToken);
  });

}
