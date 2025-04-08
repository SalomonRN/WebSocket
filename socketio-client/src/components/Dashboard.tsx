import React from "react";
import { useNavigate } from "react-router";
import { useState, useEffect } from "react";
import { useSocket } from "../context/SocketContext";
import "../App.css";

function Dashboard() {
    const { socket } = useSocket();
    const navigate = useNavigate()
    const [chat, setChat] = useState<string>("");

    useEffect(() => {

        const JWT = localStorage.getItem("JWT")
        if (!JWT) {
            navigate("/")
            localStorage.removeItem("JWT")
            return
        }

        let data = JSON.parse(atob(JWT.split('.')?.[1] ?? ""))
        if (!data.username) {
            localStorage.removeItem("JWT");
            navigate('/')
        }

        // fetch(`http://localhost:8080/api/users/`, {
        fetch(`http://localhost:8080/ping/`, {
            method: "GET",
            headers: {
                token: JWT
            }
        })
            .then((res) => {
                if (res.status != 200) {
                    alert("ALGO SALIÓ MAL...")
                    return
                }
                return res.json()
            })
            .then(res => console.log(res))
            .catch((e) => { console.log(e) })


    }, [])

    const handleGroupForm = (e: React.FormEvent) => {
        e.preventDefault();
        socket?.emit('create_chat', chat, (connected: boolean, room: string) => {
            if (connected) {
                navigate('/group', { state: { room: room } })

            } else {
                console.log("ALGO SALIÓ MAL...")
            }

        })

    }
    return (
        <>
            <h1>Hola WebSocket</h1>
            <p>Lorem, ipsum dolor sit amet consectetur adipisicing elit. Vitae odio officia distinctio pariatur! Quae quisquam inventore debitis temporibus praesentium modi iure, explicabo facere illum doloribus ducimus sunt voluptates corporis blanditiis!</p>

            <p style={{ color: "#8744" }}>Click acá para unirte al chat general.</p>
            <button onClick={() => { navigate("/chat") }}>Chat Global</button>
            {/*USARÉ ESTO PARA LISTAR TODOS LOS CHATS, O MEJOR UNA COPIA DE WASA??*/}
            {/* <select name="" id="">
                <option value="chat1">Chat1</option>
                <option value="chat2">Chat2</option>
            </select> */}
            <form onSubmit={handleGroupForm} >
                <label htmlFor="">Nombre del chat: </label>
                <input type="text" name="" id="" value={chat} onChange={(e) => { setChat(e.target.value) }} />
                <input type="submit" value="Unirse al chat" />
            </form>
        </>
    )

}

export default Dashboard;
