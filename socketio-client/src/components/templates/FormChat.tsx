import { ChangeEventHandler, FormEventHandler, SetStateAction } from "react";


interface MessageInterface {
    message: string,
    username: string,
    date: {
        month: string,
        day: number,
        hour: number,
        min: number,
    },
    url: string | null
}

interface FormChatProps {
    messages: MessageInterface[];
    message: string;
    setMessage: SetStateAction<any>;
    handleFormChat: FormEventHandler<HTMLFormElement>;
    handleSetFile: ChangeEventHandler<HTMLInputElement>;
}

const Message: React.FC<MessageInterface> = ({ message, username, date, url }) => {
    return (
        <li>
            <p>{message}</p>
            {url ? <img src={url} alt="" /> : null}
            <small className='username'>{username} </small>
            <small>{date.day}/{date.month} {date.hour}:{date.min >= 10 ? date.min : "".concat("0", date.min.toString())}</small>
        </li>
    );
};

const FormChat: React.FC<FormChatProps> = ({ messages, message, setMessage, handleFormChat, handleSetFile }) => {
    
    return (<section id="chat">
        <ul id="messages">
            {messages.map((msg, index) => {
                return <Message key={index} message={msg.message} username={msg.username} date={msg.date} url={msg.url} />
            })}
        </ul>
        <form id="form" onSubmit={handleFormChat}>
            <input type="text" name="message" id="input" placeholder="Type a message...." value={message}
                onChange={(e) => setMessage(e.target.value)} />
            <label id="label-id" htmlFor="file-upload" className="custom-file-upload">
                Upload File
            </label>
            <input type="file" id="file-upload" onChange={handleSetFile} />
            <button type="submit">Enviar</button>
        </form>
    </section>)
}
export default FormChat;
export type { MessageInterface }
