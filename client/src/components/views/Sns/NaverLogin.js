import React, { useEffect } from 'react'
import { useDispatch } from "react-redux";
import { loginUser } from "../../../_actions/user_actions";
import { registerUser } from '../../../_actions/user_actions';
import { message } from 'antd';
import {NAVER_CLIENT_ID, NAVER_CALLBACK_URL} from '../Sns/Snskey'

function NaverLogin(props){
    const dispatch = useDispatch();
    
    const { naver } = window;
    const naverLogin = new naver.LoginWithNaverId({
        clientId: REACT_APP_NAVER_CLIENT_ID,
        callbackUrl: REACT_APP_NAVER_CALLBACK_URL,
        callbackHandle: true,
        isPopup: false,
    });
    naverLogin.init();

    useEffect(() => {
        window.location.href.includes("access_token");
        //const token = (window.location.href.split('=')[1]).split('&')[0];
        
        console.log(naverLogin)
        window.addEventListener('load', function () {
            naverLogin.getLoginStatus(function (status) {
                if (status) {
                    let dataToSubmit = {
                        email: naverLogin.user.getId(),
                        name: naverLogin.user.getName(),
                        image: naverLogin.user.getProfileImage(),
                        sns: 2,
                    };
                    dispatch(loginUser(dataToSubmit))
                    .then(response => {

                    if (response.payload.loginSuccess) {
                        window.localStorage.setItem('userId', response.payload.userId);
                        message.success("네이버 간편 로그인 성공")
                        props.history.push('/')
                    } else {
                        dispatch(registerUser(dataToSubmit)).then(response => {
                            if (response.payload.success) {
                                message.success("네이버 간편 가입 성공! 다시 한번 네이버로 시작하기를 눌러주세요.")
                                
                            } else {
                                message.error("이미 등록되어 있는 계정입니다.")
                            }
                            props.history.push('/')
                        })   
                    }
                    })
                    .catch(err => {
                        // message.error("간편로그인 실패")
                        // console.log("간편로그인 실패")
                    });
                }
            });
        });
        
    }, []);

    return (
        <div>
            <div className='app'>
                <span style={{ fontSize: '2rem' }}>네이버계정으로 로그인 중입니다. 잠시만 기다려주세요 ...</span>
            </div>
        </div>
    )

}

export default NaverLogin;
