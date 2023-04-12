    import React, {useState, useContext, useEffect} from "react";
import iconMenu from "../../assets/iconMenu.svg"
import close from "../../assets/close.svg"
import { ProfileModal } from "./homeComponents";
import './home.scss';
import {store} from "../../stateManagment/store";
import Loader from "../../components/loader";
import { logout } from "../authController"
import UsersList, {SearchDebounce} from "./userList";
import Chat from "./chat";
import menu from "../../assets/menu.svg";
import ellipse2 from "../../assets/ellipse2.svg";

const Home = (props) => {
    const [showProfile, setShowProfile] = useState(false);
    const [profileClosable, setProfileClosable] = useState(true);
    const [dropdown, setDropdown] = useState(false);
    const [userdetail, setUserDetail] = useState(null);
    const [activeUser, setActiveUser] = useState(null);

    const [search, setSearch] = useState("");

    const {
        state: { userDetail, activeChatUser },
    } = useContext(store);


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
            closeSideBar();
        }

    }, [userDetail, activeChatUser])

    if (!userdetail) {
        return (
            <div className="centerLoader">
                <Loader />
            </div>
        );
    }

    const toggleSideBar = () => {
    const sideBar = document.getElementById("sideBar")
    if(sideBar.classList.contains("close")){
      sideBar.classList.remove("close")
    }
    else{
      sideBar.classList.add("close")
    }
    }

    const closeSideBar = () => {
    const sideBar = document.getElementById("sideBar")
    if(!sideBar.classList.contains("close")){
      sideBar.classList.add("close")
        }
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
                <div className="left-side close" id="sideBar">
                    <div className="flex search-bar">
                        <div className="dropdown">
                            <button onClick={() => setDropdown(!dropdown)}
                                    className="dropdown_btn"><img src={iconMenu}/></button>
                            <div id="myDropdown" className={`dropdown-content ${dropdown ? "show" : ""}`}>
                                <p onClick={() => {
                                    setShowProfile(true);
                                    setDropdown(!dropdown);
                                closeSideBar();}
                                }>Аккаунт</p>
                                <p>FAQ</p>
                                <p className="logout" onClick={() => logout(props)}>Выйти</p>
                            </div>
                        </div>
                        {/*<div onClick={() => logout(props)}></div>*/}
                        <SearchDebounce setSearch={setSearch} />
                        <div className="mobile">
                          <img className='close-left-side' src={close} alt="" onClick={toggleSideBar}/>
                        </div>
                    </div>

                <UsersList />

                </div>

                <div className="right-side">
                    {
                        activeUser ? (<Chat activeUser={activeUser}
                                             loggedUser={userdetail}
                                             toggleSideBar={toggleSideBar}/>
                        ) : (
                            <div>
                                <div className="flex user-bar">
                                    <div className="mobile">
                                        <img src={menu} className='hamburger-lines' alt="" onClick={toggleSideBar}/>
                                    </div>
                                </div>
                            </div>
                        )}
                </div>
            </div>
        </>
    );
};

export default Home;