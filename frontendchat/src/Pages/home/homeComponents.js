import close from "../../assets/close.svg"
import React, {useContext, useState} from "react";
import Loader from "../../components/loader";
import {axiosHandler, errorHandler, getToken} from "../../helper";
import {PROFILE_URL} from "../../urls";
import './homeComponents.scss';
import {store} from "../../stateManagment/store";
import {userDetailAction} from "../../stateManagment/actions";

let profileRef;

export const ProfileModal = (props) => {

  const [profileData, setProfileData] = useState({
    ...props.userDetail, user_id: props.userDetail.user.id
  });
  const [submitted, setSubmitted] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [photoProfile, setPhotoProfile] = useState("");

  const { dispatch } = useContext(store);

  const submit = async (e) => {
    e.preventDefault();
    setSubmitted(true);
    const token = await getToken(props);

    const url =
      PROFILE_URL +
      `${props.userDetail.first_name ? `/${props.userDetail.id}` : ""}`;
    const method = props.userDetail.first_name ? "patch" : "post";
    const profile = await axiosHandler({
      method,
      url,
      data: profileData,
      token,
    }).catch((e) => alert(errorHandler(e)));
    setSubmitted(false);
    if (profile) {
        props.setClosable();
        dispatch({ type: userDetailAction, payload: profile.data });
      }
  };

  const onChange = (e) => {
    setProfileData({
      ...profileData,
      [e.target.name]: e.target.value,
    });
  };

  const handleOnChange = async (e) => {
    let data = new FormData()
    data.append("file_upload", e.target.files[0])
    setUploading(true);
    console.log(e)
    setUploading(false);
    // setProfileData(...profileData, prof)
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
              <input type="file" style={{display: "none"}} ref={e => profileRef = e} onChange={handleOnChange}/>
              <div className="point" onClick={() => profileRef.click()}>
                {!props.view && <p>Изменить фото</p>}

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
                    disabled={props.view}
                    required
                />
              </label>
              <label>
                <span>Фамилия</span>
                <input
                    name="last_name"
                    value={profileData.last_name}
                    onChange={onChange}
                    disabled={props.view}
                    required
                />
              </label>
            </div>
          </div>
          {
          !props.view && <button type="submit" disabled={submitted}>{submitted ? (<center><Loader/></center>) :
                        (!props.visible ? "Завершить регистрацию" : "Обновить данные")}</button>
          }
        </form>
      </div>
    </div>
  );
};