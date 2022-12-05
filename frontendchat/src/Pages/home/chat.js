import React, {useState} from "react";
import ellipse2 from "../../assets/ellipse2.svg";
import send from "../../assets/icon_send.svg";
import './homeComponents.scss';


function Chat(props) {
    const [message, setMessage] = useState("");
    const [messages, setMessages] = useState([]);

    const submitMessage = (e) => {
        e.preventDefault();
        setMessage("")
    };


    return (
        <>
            <div className="flex user-bar">
                <div className="chat-photo">
                    <img src={ellipse2}></img>
                </div>
                <div className="info-chat">
                    <p className="firststr">{props.activeUser.first_name}</p>
                    <p className="secondstr"></p>
                </div>
            </div>

            <div className="messageZone">
                <MessageBubble bubbleType="sender"/>
                <MessageBubble bubbleType="sender"/>
                <MessageBubble bubbleType=""/>
                <MessageBubble bubbleType="sender"/>
                <MessageBubble bubbleType="sender"/>
                <MessageBubble bubbleType="sender"/>
                <MessageBubble bubbleType=""/>
                <MessageBubble bubbleType=""/>
                <MessageBubble bubbleType="sender"/>
                <MessageBubble bubbleType="sender"/>
                <MessageBubble bubbleType=""/>
                <MessageBubble bubbleType="sender"/>
                <MessageBubble bubbleType="sender"/>
                <MessageBubble bubbleType=""/>
            </div>

            <form onSubmit={submitMessage} className="flex interface">
                <input placeholder="Сообщение"
                       value={message}
                       onChange={ e => setMessage(e.target.value)}/>
                <button type="submit">
                    <img src={send}/>
                </button>
            </form>
        </>
    )
}

export default Chat


export const MessageBubble = (props) => {
  return (
    <div className={`chatbubbleCon ${props.bubbleType}`}>
      <div className="chatbubble">
        <p>ssdfdsfsdfsdfdsfsdfsdfsdf</p>
        <div className="time">{props.time}</div>
      </div>
    </div>
  );
};

