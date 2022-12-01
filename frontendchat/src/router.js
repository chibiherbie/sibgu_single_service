import React from "react";

import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./Pages/login";
import Register from "./Pages/register";
import Home from "./Pages/home";


const Router = () => {
    return (
        <BrowserRouter>
            <Routes>
                <Route path={"/login"} element={<Login/>} exact/>
                <Route path={"/register"} element={<Register/>} exact/>
                <Route path={"/"} element={<Home/>} exact/>
            </Routes>
        </BrowserRouter>
    );
}

export default Router;
