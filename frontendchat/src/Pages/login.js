import React, {useState, useContext} from "react";
import eyeopen from "../assets/eyeopen.png"
import eyeclose from "../assets/eyeclose.png"
import { Link } from "react-router-dom"

const Login = (props) => {

    const [loginData, setLoginData] = useState({});
    const [loading, setLoading] = useState(false);
    const [showPassword, setShowPassword] = useState(false);
    
    const submit = (e) => {
        e.preventDefault()
        console.log(loginData)
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
                <div className="title">Войти</div>

                <AuthForm
                    login data={loginData}
                    onSubmit={submit}
                    onChange={onChange}
                    showPassword={showPassword}
                    setShowPassword={setShowPassword}/>

                <div className="switchOption">
                    Нет аккаунта? <Link to="/register">Зарегистрироваться</Link>
                </div>

            </div>
        </div>
    );
};

export const AuthForm = (props) => {
    return (
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
                <img src={!props.showPassword ? eyeopen : eyeclose} onClick={() => props.setShowPassword(!props.showPassword)}/>
                {/*<img src={eyeclose} />*/}
            </div>
            <button type="submit">Войти</button>
        </form>
    );
};

export default Login;
