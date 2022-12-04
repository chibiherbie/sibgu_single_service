import React, {useState, useContext, useEffect} from "react";
import search from "../../assets/search.svg"
import ellipse from "../../assets/ellipse.svg"
import ellipse1 from "../../assets/ellipse1.svg"
import ellipse2 from "../../assets/ellipse2.svg"
import { ProfileModal } from "./homeComponents";

import './Home.scss';
import {store} from "../../stateManagment/store";
import Loader from "../../components/loader";

const Home = (props) => {
    const [showProfile, setShowProfile] = useState(false);
    const [profileClosable, setProfileClosable] = useState(true);
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
                            <div className="flex search-bar_button">
                                <img src={search}></img>
                                <p>Поиск</p>
                            </div>
                        </div>

                        <div className="users-list">
                            <User/>
                            <User/>
                            <User/>
                            <User/>
                            <User/>
                            <User/>
                            <User/>
                            <User/>
                            <User/>
                            <User/>
                            <User/>
                            <User/>
                            <User/>
                            <User/>
                            <User/>
                            <User/>
                        </div>

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


export const User = (props) => {

    return (
        <div className="flex user">
            <div className="imag-user">
                <img src={ellipse2}></img>
            </div>
            <div className="info">
                <p class="firststr">name</p>
                <p class="secondstr">message</p>
            </div>
            <div className="social-network">
                <p>TG</p>
            </div>
            <div className="unread-user">
                <img src={ellipse1}></img>
            </div>
        </div>
    );
}


export const Message = (props) => {

    return (
        <div className="message">
            
        </div>
    );
}
