import React, {useState, useContext} from "react";
import eyeopen from "../assets/eyeopen.png"
import eyeclose from "../assets/eyeclose.png"
import closeWhite from "../assets/close-white.png"
import { Link } from "react-router-dom"
import {axiosHandler, errorHandler} from "../helper";
import { LOGIN_URL } from "../urls";
import Loader from "../components/loader";
import { tokenName } from "./authController";

export const loginRequest = async (data, setError, props) => {
    const result = await axiosHandler({
            method: "post",
            url: LOGIN_URL,
            data: data,
        }).catch(e => setError(errorHandler(e)));
    if (result) {
        localStorage.setItem(tokenName, JSON.stringify(result.data));
        props.history.push("/");
    }
};

const Login = (props) => {

    const [loginData, setLoginData] = useState({});
    const [loading, setLoading] = useState(false);
    const [showPassword, setShowPassword] = useState(false);
    const [error, setError] = useState(null);

    const submit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        await loginRequest(loginData, setError, props);
        setLoading(false);
    };

    const onChange = (e) => {
        setLoginData({
            ...loginData,
            [e.target.name]: e.target.value,
        });
    };
    
    return (
        <div className="loginContainer">
            <div className="inner">
                <div className="logo">SIBGU</div>
                <div className="title">Авторизация</div>

                <AuthForm
                    login
                    data={loginData}
                    onSubmit={submit}
                    onChange={onChange}
                    showPassword={showPassword}
                    setShowPassword={setShowPassword}
                    error={error}
                    loading={loading}
                    setError={setError}/>

                <div className="switchOption">
                    Нет аккаунта? <Link to="/register">Зарегистрироваться</Link>
                </div>

            </div>
        </div>
    );
};

export const AuthForm = (props) => {
    return (
        <>
            {props.error && (
                <div className="errorHandler">
                    <div dangerouslySetInnerHTML={{ __html: props.error }} />
                    <img alt="" src={closeWhite} onClick={() => props.setError(null)} />
                </div>
            )}

            <form onSubmit={props.onSubmit}>
                <input value={props.data.username}
                       name={"username"}
                       onChange={props.onChange}
                       className="input-field"
                       placeholder="Имя пользователя"
                       required/>
                <div className="input-container">
                    <input
                        className="input-field"
                        placeholder="Пароль"
                        value={props.data.password}
                        name={"password"}
                        onChange={props.onChange}
                        type={!props.showPassword ? "password" : "text"}
                        autoComplete="new-password"
                        required/>
                    <img alt="" src={!props.showPassword ? eyeopen : eyeclose} onClick={() => props.setShowPassword(!props.showPassword)}/>
                    {/*<img src={eyeclose} />*/}
                </div>
                <button type="submit" disabled={props.loading}>
                    {props.loading ? (<center><Loader/></center>) :
                        (props.login ? "Войти" : "Зарегистрироваться")}
                </button>
            </form>
        </>
    );
};

export default Login;
