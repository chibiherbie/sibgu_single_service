import React, {useEffect, useState} from "react";
import ellipse2 from "../../assets/ellipse2.svg";
import ellipse1 from "../../assets/ellipse1.svg";
import {axiosHandler, getToken} from "../../helper";
import {PROFILE_URL} from "../../urls";
import Loader from "../../components/loader";

function UsersList() {

    const [users, setUsers] = useState([]);
    const [fetching, setFetching] = useState(true);
    const [nextPage, setNextPage] = useState(1);

    useEffect(() =>{
       getUserList()
    }, []);

    const getUserList = async () => {
        const _token = await getToken();
        const _users = await axiosHandler({
            method: "get",
            url: PROFILE_URL + `?page=${nextPage}`,
            token: _token,
        }).catch((e) => null);
        if (_users) {
            if (_users.data.next){
                setNextPage(nextPage+1)
            }
            setUsers(_users.data.results)
            setFetching(false)
        }
    };

    return (

        <div className="flex users-list">
            {
                fetching ? (<center><Loader/></center>) :
                    (users.map((item, i) => <User
                        key={i}
                        name={item.first_name}
                        profilePictire={item.profile_picture}
                        message={item.last_name}
                        count={item.message_count}
                    />))
            }
        </div>

    )
}

export default UsersList;

export const User = (props) => {
    return (
        <div className="flex user">
            <div className="imag-user">
                <img src={!props.profilePictire ? ellipse2 : props.profilePictire}></img>
            </div>
            <div className="info">
                <p class="firststr">{props.name}</p>
                <p class="secondstr">{props.message}</p>
            </div>
            <div className="social-network">
                <p>TG</p>
            </div>
            <div className="unread-user">
                <img src={props.count > 0 && ellipse1}></img>
            </div>
        </div>
    );
};