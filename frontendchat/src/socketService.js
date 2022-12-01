import React, { useEffect } from "react";
import openSocket from "socket.io-client"

const SOCKET_URL = "http://localhost:9000";
let socket;

const SocketService = () => {
    const setupSocket = () => {
        socket = openSocket(SOCKET_URL)
        socket.on("command", (data) => {
            console.log(data);
        });
    };

    useEffect(setupSocket, []);

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
