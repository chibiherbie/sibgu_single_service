import React, { useEffect, useContext } from "react";
import openSocket from "socket.io-client"
import {store} from "./stateManagment/store";
import {activeChatUserAction} from "./stateManagment/actions";

const SOCKET_URL = "http://127.0.0.1:9000";
let socket;

const SocketService = () => {
    const { dispatch, state: {userDetail} } = useContext(store)

    const setupSocket = () => {
        socket = openSocket(SOCKET_URL, {
          cors: {
            origin: "*",
            withCredentials: true
          }
        })
        socket.on("command", (data) => {
            if (!userDetail) return;
            if (userDetail !== data.receiver) return;
                dispatch({type: activeChatUserAction, payload: true});
        });
    };

    useEffect(setupSocket, [userDetail]);

    return <></>;
};

export default SocketService

export const sendSocket = data => {
    console.log('Сокеты')
    socket.emit("command", {
        type: data.type,
        id: data.id,
        content: data.content,
    });
};

export const sendTestSocket = data => {
    socket.set( 'origins', '*' )
    socket.emit("command", data);
    console.log('sendTestSocket -', data)
};
