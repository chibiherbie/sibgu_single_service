import React, {useState, useContext, useEffect} from "react";
import search from "../../assets/search.svg"
import iconMenu from "../../assets/iconMenu.svg"
import { ProfileModal } from "./homeComponents";
import './home.scss';
import {store} from "../../stateManagment/store";
import Loader from "../../components/loader";
import { logout } from "../authController"
import UsersList from "./userList";
import Chat from "./chat";

const Home = (props) => {
    const [showProfile, setShowProfile] = useState(false);
    const [profileClosable, setProfileClosable] = useState(true);
    const [dropdown, setDropdown] = useState(false);
    const [userdetail, setUserDetail] = useState(null);
    const [activeUser, setActiveUser] = useState(null);

    const {state: {userDetail, activeChatUser}} = useContext(store);

    useEffect(() => {
        if (userDetail !== userdetail) {
            setUserDetail(userDetail);
            if (!userDetail.first_name) {
                setShowProfile(true);
                setProfileClosable(false);
            }
        }

        if (activeUser !== activeChatUser) {
            setActiveUser(activeChatUser);
        }

    }, [userDetail, activeChatUser])

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
                        {
                            activeUser ? <Chat activeUser={activeUser}/> : <div></div>
                        }
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
