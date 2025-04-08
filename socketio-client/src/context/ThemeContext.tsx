import { createContext, useContext, useState } from "react";

// Definimos el tipo del contexto
interface ThemeContextType {
  theme: "light" | "dark";
  toggleTheme: () => void;
}

// Creamos el contexto con valor inicial (undefined para TypeScript)
const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

// Proveedor del contexto
export const ThemeProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [theme, setTheme] = useState<"light" | "dark">("light");

  const toggleTheme = () => {
    setTheme((prev) => (prev === "light" ? "dark" : "light"));
  };

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
};

// Hook personalizado para acceder al contexto
export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (!context) throw new Error("useTheme debe usarse dentro de un ThemeProvider");
  return context;
};