import React, {useContext, useEffect, useState} from "react";
import ellipse2 from "../../assets/ellipse2.svg";
import ellipse1 from "../../assets/ellipse1.svg";
import {axiosHandler, getToken, LastUserChat} from "../../helper";
import {PROFILE_URL} from "../../urls";
import Loader from "../../components/loader";
import {store} from "../../stateManagment/store";
import {activeChatUserAction, triggerRefreshUserListAction} from "../../stateManagment/actions";
import searchSvg from "../../assets/search.svg"


let goneNext = false;

function UsersList() {

    const [users, setUsers] = useState([]);
    const [fetching, setFetching] = useState(true);
    const [nextPage, setNextPage] = useState(1);
    const [canGoNext, setCanGoNext] = useState(false);
    const [search, setSearch] = useState("");

    const { state:{triggerRefreshUserList}, dispatch} = useContext(store);

    useEffect(() =>{
       getUserList();
    }, [search]);

      useEffect(() => {
    if(triggerRefreshUserList){
      getUserList()
      dispatch({type: triggerRefreshUserListAction, payload: false})
    }

  }, [triggerRefreshUserList])

    const getUserList = async (append=false) => {
        let extra = "";
        if (search !== "") {
            extra += `&keyword${search}`
        }

        setCanGoNext(false);
        const _token = await getToken();
        const _users = await axiosHandler({
            method: "get",
            url: PROFILE_URL + `?page=${nextPage}${extra}`,
            token: _token,
        }).catch((e) => null);
        if (_users) {

            // Удаляем доверенных лиц
            // for (var i = 0; i < _users.data.results.length; i++)
            // {
            //     if (_users.data.results[i].user.is_staff)
            //         delete _users.data.results[i]
            // }
            _users.data.count = _users.data.results.length
            // console.log('_USERS', _users)

            if (_users.data.next){
                setNextPage(nextPage+1)
                setCanGoNext(true);
            }
            if (append){
                setUsers(...users, ..._users.data.results)
                goneNext = false;
            }
            else {
                setUsers(_users.data.results)
            }
                setFetching(false)
        }

        // checkLastChat(_users.data.results);
    };

    // Включает последний выбранный при загрузке чат
    const checkLastChat = (users) => {
        let lastUserChat = localStorage.getItem(LastUserChat)
        if (lastUserChat){
            lastUserChat = JSON.parse(lastUserChat);
            if (users.filter(item => item.id === lastUserChat.id).length){
                dispatch({type: activeChatUserAction, payload: lastUserChat});
            }
        }
    }

    const setActiveUser = (user_data, elem) => {
        localStorage.setItem(LastUserChat, JSON.stringify(user_data));
        dispatch({type: activeChatUserAction, payload: user_data});
    };

    const handleScroll = (e) => {
        if (e.target.scrollTop >= (e.target.scrollHeight = (e.target.offsetHeight + 200))) {
            if (canGoNext && !goneNext) {
                getUserList(true);
            }
        }
    };

    return (

        <div className="flex users-list" onScroll={handleScroll}>
            {
                fetching ? (<center><Loader/></center>) :
                    (users.map((item, i) => <User
                        key={i}
                        name={item.first_name}
                        profilePictire={item.profile_picture}
                        message={item.last_name}
                        count={item.message_count}
                        clickable
                        onClick={() => setActiveUser(item, 'test')}
                    />))
            }
        </div>

    )
}

export default UsersList;

let debounceTimeout;
export const SearchDebounce = (props) => {
     const [search, setSearch] = useState("");

    useEffect(() => {
        clearTimeout(debounceTimeout);
        debounceTimeout = setTimeout(() => {
            props.setSearch(search)
        }, 1000)
    }, [search]);


     return (
          <div className="flex search-bar_button">
             <img src={searchSvg}></img>
             <input placeholder="Поиск" type="text" value={search} onChange={e => setSearch(e.target.value)}></input>
         </div>
     )
}


export const User = (props) => {
    return (
        <div className={`flex user ${props.clickable ? "clickable" : ""}`}
        onClick={() => props.clickable && props.onClick()}>
            <div className="imag-user">
                <img src={!props.profilePictire ? ellipse2 : props.profilePictire}></img>
            </div>
            <div className="info">
                <p class="firststr">{props.name}</p>
                <p class="secondstr">{props.message}</p>
            </div>
            <div className="social-network">
                <p></p>
            </div>
            <div className="unread-user">
                <img src={props.count > 0 && ellipse1}></img>
            </div>
        </div>
    );
};