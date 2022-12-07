import React, {useContext, useEffect, useState} from "react";
import ellipse2 from "../../assets/ellipse2.svg";
import send from "../../assets/icon_send.svg";
import './homeComponents.scss';
import Loader from "../../components/loader";
import {axiosHandler, errorHandler, getToken} from "../../helper";
import {MESSAGE_URL} from "../../urls";
import moment from "moment";
import {activeChatAction} from "../../stateManagment/actions";
import {store} from "../../stateManagment/store";
import {ProfileModal} from "./homeComponents";


function Chat(props) {
    const [message, setMessage] = useState("");
    const [messages, setMessages] = useState([]);
    const [fetching, setFetching] = useState(true);
    const [nextPage, setNextPage] = useState(1);
    const [canGoNext, setCanGoNext] = useState(false);
    const [showProfileModal, setShowProfileModal] = useState(false);

    const {state:{activeChat}, dispatch} = useContext(store)

    const getMessages = async () => {
        const token = await getToken();
        setCanGoNext(false);

        const result = await axiosHandler({
            method: 'get',
            url: MESSAGE_URL + `?user_id=${props.activeUser.user.id}`,
            token,
        }).catch(e => console.log(errorHandler(e)));

        if (result) {
            setMessages(result.data.results.reverse());

            result.data.results.map(item => {
                if (item.is_read) return null
                if (item.receiver.user.id === props.loggedUser.user.id){
                    updateMessage(item.id);
                }
               return null
            });

            if (result.data.next) {
                setCanGoNext(true);
                setNextPage(nextPage + 1);
            }
            setFetching(false);
            scrollToBottom();
        }
    }

    const updateMessage = async (message_id) => {
        const token = await getToken()
        axiosHandler({
            method: "patch", url: MESSAGE_URL + `/${message_id}`, token: token, data: {
                is_read: true
            }});
    };

    useEffect(() => {
        getMessages()
    }, [])

    useEffect(() => {
        if (activeChat) {
            getMessages();
            dispatch({type:activeChatAction, payload: null})
        }
    }, [activeChat]);

    const submitMessage = async (e) => {
        setMessage("")
        scrollToBottom();

        e.preventDefault();
        let data = {
            sender_id: props.loggedUser.user.id,
            receiver_id: props.activeUser.user.id,
            message,
        };
        const lastIndex = messages.length;
        setMessages([...messages, data]);
        setMessage("");

        const token = await getToken();
        const result = await axiosHandler({
            method: 'post',
            url: MESSAGE_URL,
            token, data
        }).catch(e => console.log(errorHandler(e)));

        if (result) {
            messages[lastIndex] = result.data;

            setMessages(messages);
        }
    };

    const handleBubbleType = (item) => {
        console.log(item);
        if (item.sender_id) return "sender"
        if (item.sender.user.id === props.loggedUser.user.id) return "sender"
        else return ""
    };

    const scrollToBottom = () => {
        setTimeout(() => {
            let messageZone = document.getElementById("messageZone");
            messageZone.scrollTop = messageZone.scrollHeight;
        }, 300)
    };

    return (
        <>
            <ProfileModal {...props}
                close={() => setShowProfileModal(false)}
                visible={showProfileModal}
                closable={true}
                userDetail={props.activeUser}
                setClosable={() => null}
                view

            />
            <div className="flex user-bar">
                <div className="chat-photo" onClick={() => setShowProfileModal(true)}>
                    <img src={ellipse2}></img>
                </div>
                <div className="info-chat">
                    <p className="firststr">{props.activeUser.first_name}</p>
                    <p className="secondstr">{props.activeUser.first_name}</p>
                </div>
            </div>

            <div className="messageZone" id="messageZone">
                { fetching ? (
                    <center><Loader/></center>
                ) : messages.length < 1 ? (
                    <div>Сообщений пока нет</div>
                ) : (
                        messages.map((item, key) => (

                            <MessageBubble
                                bubbleType={handleBubbleType(item)} // item.receiver === props.loggedUser.user.id ? "" : "sender"
                                key={key}
                                message={item.message}
                                time={item.created_at ? moment(item.created_at).format("YYYY-MM-DD hh:mm a") : ""}
                            />
                        ))
                    )}
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
        <p>{props.message}</p>
        <div className="time">{props.time}</div>
      </div>
    </div>
  );
};

