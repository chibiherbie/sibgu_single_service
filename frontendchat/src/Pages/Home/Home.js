import React, {useState, useContext, useEffect} from "react";
import search from "../../assets/search.svg"
import ellipse2 from "../../assets/ellipse2.svg"
import iconMenu from "../../assets/iconMenu.svg"
import { ProfileModal } from "./homeComponents";

import './Home.scss';
import {store} from "../../stateManagment/store";
import Loader from "../../components/loader";
import { logout } from "../authController"
import UsersList from "./userList";

const Home = (props) => {
    const [showProfile, setShowProfile] = useState(false);
    const [profileClosable, setProfileClosable] = useState(true);
    const [dropdown, setDropdown] = useState(false);
    const [userdetail, setUserDetail] = useState(null);

    const {state: {userDetail}} = useContext(store);

    useEffect(() => {
        if (userDetail !== userdetail) {
            setUserDetail(userDetail);
            if (!userDetail.first_name) {
                setShowProfile(true);
                setProfileClosable(false);
            }
        }
    }, [userDetail])

    if (!userdetail) {
        return (
            <div className="centerLoader">
                <Loader />
            </div>
        );
    }

    return (
        <>
            <ProfileModal {...props}
                close={() => setShowProfile(false)}
                visible={showProfile}
                closable={profileClosable}
                userDetail={userdetail}
                setClosable={() => setProfileClosable(true)}
            />
            <div className="container">
                    <div className="left-side">
                        <div className="flex search-bar">
                            <div className="dropdown">
                                <button onClick={() => setDropdown(!dropdown)}
                                        className="dropdown_btn"><img src={iconMenu}/></button>
                                <div id="myDropdown" className={`dropdown-content ${dropdown ? "show" : ""}`}>
                                    <p>Аккаунт</p>
                                    <p className="logout" onClick={() => logout(props)}>Выйти</p>
                                </div>
                            </div>
                            {/*<div onClick={() => logout(props)}></div>*/}
                            <div className="flex search-bar_button">
                                <img src={search}></img>
                                <input placeholder="Поиск" type="text"></input>
                            </div>
                        </div>

                    <UsersList/>

                    </div>

                    <div className="right-side">
                        <div className="user-bar">
                            <div className="chat-photo">
                                <img src={ellipse2}></img>
                            </div>
                            <div className="info-chat">
                                <p class="firststr">name</p>
                                <p class="secondstr">TG</p>
                            </div>
                        </div>


                        <div className="interface">

                        </div>

                    </div>
            </div>
        </>
    );
};

export default Home;

export const Message = (props) => {

    return (
        <div className="message">
            
        </div>
    );
}
