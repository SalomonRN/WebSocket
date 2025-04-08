import { createContext, useState, useContext, ReactNode } from "react";

// 1️⃣ Definir el tipo de datos para el contexto
interface User {
  name: string;
}

interface AuthContextType {
  user: User | null;
  login: (username: string) => void;
  logout: () => void;
}

// 2️⃣ Crear el contexto con valores iniciales
const AuthContext = createContext<AuthContextType | undefined>(undefined);

// 3️⃣ Definir el tipo de las props del `AuthProvider`
interface AuthProviderProps {
  children: ReactNode; // ReactNode permite cualquier contenido JSX
}

// 4️⃣ Crear el `AuthProvider`
export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);

  // Función para iniciar sesión
  const login = (username: string) => {
    const newUser = { name: username };
    setUser(newUser);
    localStorage.setItem("user", JSON.stringify(newUser));
  };

  // Función para cerrar sesión
  const logout = () => {
    setUser(null);
    localStorage.removeItem("user");
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

// 5️⃣ Hook personalizado para acceder al contexto
export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth debe usarse dentro de un AuthProvider");
  }
  return context;
};
