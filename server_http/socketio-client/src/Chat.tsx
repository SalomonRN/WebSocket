function Message(message: string) {
  return (
    <>
      <div className="message">
        <p>{message}</p>
      </div>
    </>
  );
}
function Chat() {
  socket.on("2");
  return (
    <>
      <h1>Chat</h1>
      <div className="container-messages">
        <Message message = "asd"/>
      </div>
    </>
  );
}
export default Chat;
