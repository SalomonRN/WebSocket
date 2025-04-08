import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import { ThemeProvider } from './context/ThemeContext.tsx';
import { SocketProvider } from './context/SocketContext.tsx';
import Routing from "./utils/Routing.tsx"
import { BrowserRouter } from "react-router";

createRoot(document.getElementById("root")!).render(
  // <StrictMode>
    <BrowserRouter>
      <SocketProvider>
        <ThemeProvider>
          <Routing />
        </ThemeProvider>
      </SocketProvider>
    </BrowserRouter>
  // </StrictMode>
);
