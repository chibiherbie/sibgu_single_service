import React from "react";
import { BrowserRouter, Route, Switch } from "react-router-dom";
import Login from "./Pages/login";
import Register from "./Pages/register";
import Home from "./Pages/home/home";
import AuthController from "./Pages/authController";


const Router = () => {
    return (
        <BrowserRouter style={{height: '100%'}}>
            <Switch>
                <Route path="/login" component={Login} />
                <Route path="/register" component={Register} exact/>
                { <Route path="/" component={(props) => (
                    <AuthController {...props}>
                        <Route {...props} path="/" component={Home} exact/>
                    </AuthController>
                )} /> }
                {/*<Route path='/' component={home} />*/}

            </Switch>
        </BrowserRouter>
    );
};

export default Router;
