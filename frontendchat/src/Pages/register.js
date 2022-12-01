import React from "react";
import {AuthForm} from "./login";
import {Link} from "react-router-dom";

const Register = (props) => {
    return (
        <div className="loginContainer">
            <div className="inner">
                <div className="logo">SIBGU</div>
                <div className="title">Регистрация</div>

                <AuthForm />

                <div className="switchOption">
                    Уже есть аккаунт? <Link to="/login">Войти</Link>
                </div>

            </div>
        </div>
    );
};

export default Register;
