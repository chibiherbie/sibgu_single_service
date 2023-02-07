import React, { useState } from "react";
import { AuthForm, loginRequest } from "./login";
import { Link } from "react-router-dom";
import { axiosHandler, errorHandler } from "../helper";
import { REGISTER_URL } from "../urls";

const Register = (props) => {
    const [registerData, setRegisterData] = useState({});
    const [loading, setLoading] = useState(false);
    const [showPassword, setShowPassword] = useState(false);
    const [error, setError] = useState(null);

    const submit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);

        registerData['is_staff'] = true;

        // Проверка пароля
        if (registerData['password'].length < 8){
            setError(errorHandler('password Пароль должен быть длиньше 8 символов', true))
            setLoading(false);
            return
        }
        if (registerData['password2'] !== registerData['password']) {
            setError(errorHandler('password Пароли не совпадают', true))
            setLoading(false);
            return
        }

        const result = await axiosHandler({
            method: "post",
            url: REGISTER_URL,
            data: registerData
        }).catch(e => setError(errorHandler(e)));
        if (result) {
            await loginRequest(registerData, setError, props);
        }
        setLoading(false);
    };

    const onChange = (e) => {
        setRegisterData({
                ...registerData,
                [e.target.name]: e.target.value,
            });
    };

    return (
        <div className="loginContainer">
            <div className="inner">
                <div className="logo">SIBGU</div>
                <div className="title">Регистрация</div>

                <AuthForm
                    data={registerData}
                    onSubmit={submit}
                    onChange={onChange}
                    showPassword={showPassword}
                    setShowPassword={setShowPassword}
                    error={error}
                    loading={loading}
                    setError={setError}/>

                <div className="switchOption">
                    Уже есть аккаунт? <Link to="/login">Войти</Link>
                </div>

            </div>
        </div>
    );
};

export default Register;
