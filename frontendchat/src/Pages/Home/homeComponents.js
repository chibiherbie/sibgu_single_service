import close from "../../assets/close.svg"
import React, { useState } from "react";
import Loader from "../../components/loader";
import {axiosHandler, errorHandler, getToken} from "../../helper";
import {PROFILE_URL} from "../../urls";

export const ProfileModal = (props) => {

  const [profileData, setProfileData] = useState({
    ...props.userDetail, user_id: props.userDetail.user.id
  });
  const [submitted, setSubmitted] = useState(false);

  const submit = async (e) => {
    e.preventDefault();
    setSubmitted(true);
    const token = await getToken(props);
    const profile = await axiosHandler({
      method: props.userDetail.first_name ? "patch" : "post",
      url: PROFILE_URL + `${props.userDetail.first_name ? `/${profileData.user_id}` : ""}`,
      data: profileData,
      token,
    }).catch(e => alert(errorHandler(e)));
    setSubmitted(false);
    if (profile) {
        props.setClosable(true);
        console.log(profile.data)
      }
  };

  const onChange = (e) => {
    setProfileData({
      ...profileData,
      [e.target.name]: e.target.value,
    });
  };

  return (
    <div className={`modalContain ${props.visible ? "open" : ""}`}>
      <div className="content-inner">
        <div className="header">
          <div className="title">Профиль</div>
          {props.closable && <img src={close} onClick={props.close} />}
        </div>
        <form className="content" onSubmit={submit}>
          <div className="inner">
            <div className="leftHook">
              <div
                className="imageCon"
              />
              <div className="point">
                Изменить фото
                {/*<img src={edit} />*/}
              </div>
            </div>
            <div className="dataInput">
              <label>
                <span>First name</span>
                <input
                  name="first_name"
                  value={profileData.first_name}
                  onChange={onChange}
                  required
                />
              </label>
              <label>
                <span>Фамилия</span>
                <input
                    name="last_name"
                    value={profileData.last_name}
                    onChange={onChange}
                    required
                />
              </label>
            </div>
          </div>
          <button type="submit" disabled={submitted}>{submitted ? (<center><Loader/></center>) :
                        (props.visible ? "Завершить регистрацию" : "Обновить данные")}</button>
        </form>
      </div>
    </div>
  );
};