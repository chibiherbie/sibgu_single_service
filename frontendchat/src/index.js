import React from "react";
import ReactDom from "react-dom";
import App from "./app";

ReactDom.render(
    <div>
        <h1>Hello world</h1>
        <h1>Hello react</h1>
        <App />
    </div>,
    document.getElementById("root")
);


