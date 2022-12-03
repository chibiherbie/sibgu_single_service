import React from "react";
import search from "../assets/search.svg"

const Home = (props) => {
    // const [ShowProfile, setShowProfile]

    return (
        <div className="container">
            <div className="flex wrapper">
                <div class="left-side">
                    <div class="flex search-bar">
                        <div class="flex search-bar_button">
                            <img src={search}></img>
                            <p>Поиск</p>
                        </div>
                    </div>

                    <div class="flex users-list">
                        <User/>
                        <User/>
                        <User/>
                        <User/>
                        
                    </div>

                </div>

                <div class="right-side">
                    <div class="flex user-bar"></div>
                    <div class="intarface">
                        <div class="messages">
                            <Message/>
                        </div>
                        <div class="">

                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Home;


export const User = (props) => {

    return (
        <div class="flex user">
            <div class="">img</div>
            <div class="info">
                <p>name</p>
                <p>message</p>
            </div>
        </div>
    );
}


export const Message = (props) => {

    return (
        <div class="message">
            
        </div>
    );
}
