import { useLocation } from 'react-router';
import { useSocket } from '../context/SocketContext.tsx';
import React, { useState, useEffect } from 'react';
import FormChat from "./templates/FormChat.tsx";
import { MessageInterface } from "./templates/FormChat.tsx";
import { arrayBufferToFile, handleUpload } from "../utils/fileHandling.ts";

const Chat = () => {
  const { socket } = useSocket();
  const [message, setMessage] = useState("");
  const [file, setFile] = useState<File | null>();
  const [messages, setMessages] = useState<MessageInterface[]>([]);
  const location = useLocation();

  useEffect(() => {

    socket?.on('chat_message', (msg: string, username: string, date: any, file: any | null, fileType: any | null) => {
      const URL = arrayBufferToFile(file, fileType);
      const newMessage: MessageInterface = {
        message: msg,
        username: username,
        date: {
          day: date['day'],
          hour: date['hour'],
          min: date['min'],
          month: date['month']
        },
        url: URL
      }
      setMessages((messages) => [...messages, newMessage])
    });

    return () => {
      socket?.emit("exit_chat", location.state.room);
      socket?.off("chat_message");
    };

  }, [socket]);

  const handleFormChat = async (e: React.FormEvent) => {
    e.preventDefault();
    const label = document.getElementById("label-id");
    if (!message && !file) return

    let buffer = await handleUpload(file);
    socket?.emit("chat_message", message, buffer, location.state.room);
    setMessage("");
    setFile(null);
    label!.innerText = "Upload File"
  };


  const handleSetFile = (e: React.ChangeEvent<HTMLInputElement>) => {
    const label = document.getElementById("label-id")

    if (!e.target.files) return
    label!.innerText = e.target.files[0].name

    setFile(e.target.files[0])
  }

  return (<>
    <h1>{location.state.room}</h1>
    <FormChat messages={messages} message={message} setMessage={setMessage} handleFormChat={handleFormChat} handleSetFile={handleSetFile} />
  </>
  )
}

export default Chat;
