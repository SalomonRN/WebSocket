import { io, Socket } from "socket.io-client";
import { DefaultEventsMap } from "@socket.io/component-emitter";

const createConnection = () => {
    const token = localStorage.getItem("JWT");
    if (token) {
      console.log("TOKEN :)");
      const newSocket = io("http://localhost:5000", { auth: { token } });
      socket = newSocket;
      setupSocketEvents(newSocket);
    }
}

const setupSocketEvents = (newSocket: Socket<DefaultEventsMap, DefaultEventsMap>) => {
    newSocket.on("connect", () => console.log("Conectado al WebSocket"));
    newSocket.on("connect_error", (error) =>
      console.error("Error:", error.message)
    );
    newSocket.on("message", (data) => console.log("Mensaje recibido:", data));

    // Si el servidor emite un nuevo token
    newSocket.on("JWT", (newToken) => {
      console.log("Token recibido:", newToken);
      localStorage.setItem("JWT", newToken);
      navigate("/dashboard");
    });

    return () => {
      newSocket.off("message");
      newSocket.off("JWT");
      newSocket.close();
    };
  };

export default setupSocketEvents