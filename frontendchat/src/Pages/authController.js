import React, { useEffect, useState, useContext } from "react";
import Loader from "../components/loader";
import {axiosHandler} from "../helper";
import {PROFILE_URL, REFRESH_URL} from "../urls";

export const tokenName = "tokenName";

const AuthController = (props) => {
    const [checking, setChecking] = useState(true);

    const checkAuthState = async () => {
        let token = localStorage.getItem(tokenName);
        if (!token) {
            props.history.push("/login");
            return;
        }

        token = JSON.parse(token);
        const userProfile = await axiosHandler({
            method: "get",
            url: PROFILE_URL,
            token: token.access,
        }).catch((e) => null);
        if (userProfile) {
            setChecking(false);
        }
        else {
            const getNewAccess = await axiosHandler({
               method: "post",
                url: REFRESH_URL,
                data: {
                   refresh: token.refresh,
                },
            }).catch((e) => null);
            if (getNewAccess) {
                localStorage.setItem(tokenName, JSON.stringify(getNewAccess.data));
                checkAuthState();
            }
            else {
                props.history.push("/login");
            }
        }
    };

    useEffect(() => {
        checkAuthState();
    }, []);

    return (
        <div className="authContainer">
            {checking ? <div className="centerLoader">
             <Loader />
            </div>: props.children}
        </div>
    );
};

export default AuthController;
