import React from "react";
import eyeopen from "../assets/eyeopen.png"
import eyeclose from "../assets/eyeclose.png"
import { Link } from "react-router-dom"

const Login = (props) => {
    return (
        <div className="loginContainer">
            <div className="inner">
                <div className="logo">SIBGU</div>
                <div className="title">Войти</div>

                <AuthForm login/>

                <div className="switchOption">
                    Нет аккаунта? <Link to="/register">Зарегистрироваться</Link>
                </div>

            </div>
        </div>
    );
};

export const AuthForm = (props) => {
    return (
                        <form>
                    <input className="input-field" placeholder="Имя пользователя" />
                    <div className="input-container">
                        <input className="input-field" placeholder="Пароль" type="password" autoComplete="new-password"/>
                        <img src={eyeopen}/>
                        <img src={eyeclose} />
                    </div>
                    <button type="submit">Войти</button>
                </form>
    );
};

export default Login;
