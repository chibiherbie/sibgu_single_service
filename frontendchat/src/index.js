import React from "react";
import ReactDom from "react-dom";
import App from "./app";
import { StoreProvider } from "./stateManagment/store";
import SocketService from "./socketService";
import Router from "./router";
import "./style.scss"

ReactDom.render(
    <StoreProvider>
        <Router />
        {/* Socket service as React Component??? */}
        <SocketService />
    </StoreProvider>,
    document.getElementById("root")
);
