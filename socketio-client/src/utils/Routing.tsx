import { Routes, Route } from "react-router-dom";
import Login from "../components/Login.tsx";
import Dashboard from "../components/Dashboard.tsx";
import NoPage from "../components/templates/NoPage.tsx";
import Chat from "../components/Chat.tsx";
import GroupChat from "../components/GroupChat.tsx";
/**
 * BrowserRouter ->
 *
 * Route ->
 */
const Routing = () => {
    return (<>
        <Routes>
            <Route path="/" element={<Login />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/chat" element={<Chat />} />
            <Route path="/group" element={<GroupChat />} />
            <Route path="*" element={<NoPage />} />
        </Routes>
    </>)
}

export default Routing;