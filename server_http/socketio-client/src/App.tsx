import { BaseSyntheticEvent, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

function App() {
  let socket;
  const [name, setName] = useState("");
  const [pass, setPass] = useState("");
  const navigate = useNavigate();

  useEffect(() => {

  }, []);
  //
  const handleSubmit = (event: BaseSyntheticEvent) => {
    event.preventDefault();
    if (!name || !pass) {
      alert("Ingrese usuario y contraseña");
      return;
    }

    const newSocket = io("http://localhost:5000", {
      auth: { username: name, password: pass },
    });

    socket = newSocket;
    setupSocketEvents(newSocket);
  };

  return (
    <div>
      <h1>Inicio de sesión</h1>
      <form onSubmit={handleSubmit}>
        <label>Usuario</label>
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />

        <label>Contraseña</label>
        <input
          type="password"
          value={pass}
          onChange={(e) => setPass(e.target.value)}
        />

        <button type="submit">Iniciar sesión</button>
      </form>
    </div>
  );
}

export default App;
