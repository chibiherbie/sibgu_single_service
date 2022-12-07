import React, { useEffect, useContext } from "react";
import openSocket from "socket.io-client"
import {store} from "./stateManagment/store";
import {activeChatUserAction} from "./stateManagment/actions";

const SOCKET_URL = "http://localhost:9000";
let socket;

const SocketService = () => {
    const { dispatch, state: {userDetail} } = useContext(store)

    const setupSocket = () => {
        socket = openSocket(SOCKET_URL)
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

const sendSocket = data => {
    socket.emit("command", {
        type: data.type,
        id: data.id,
        content: data.content,
    });
};

export const sendTestSocket = data => {
    socket.emit("command", data);
};
