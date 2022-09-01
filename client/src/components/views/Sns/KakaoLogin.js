import React, { useEffect } from "react";
import { useDispatch } from "react-redux";
import { loginUser } from "../../../_actions/user_actions";
import { registerUser } from '../../../_actions/user_actions';
import { message } from 'antd';
//import { KAKAO_CLIENT_ID, KAKAO_REDIRECT_URI } from './Snskey'

function KakaoLogin(props) {
    const dispatch = useDispatch();
    
    const code = new URL(window.location.href).searchParams.get("code");
    const tokenbodyData = {
        grant_type : "authorization_code",
        client_id : REACT_APP_KAKAO_CLIENT_ID,                  //process.env.REACT_APP_REST_API_KEY,
        redirect_uri : REACT_APP_KAKAO_REDIRECT_URI,            //process.env.REACT_APP_REDIRECTURI_DEVELOP,
        code : code
    }
    const tokenqueryStringBody = Object.keys(tokenbodyData)
        .map(k=> encodeURIComponent(k)+"="+encodeURI(tokenbodyData[k]))
        .join("&")

    const getKakaoToken = () => {
        fetch("https://kauth.kakao.com/oauth/token",{
            method : "POST",
            headers : {
                'content-type' : 'application/x-www-form-urlencoded;charset=utf-8',
            },
            body : tokenqueryStringBody
        })
        .then(res => res.json())
        .then((data)=>{
            console.log(data)
            if (data.access_token) {
                console.log("토큰받기성공")
                localStorage.setItem('token', data.access_token);
                getKakaoInfo(data);
            } else {
                console.log("토큰받기실패")
                props.history.push('/')
            }
        })
    };

    const getKakaoInfo = (data) => {
        console.log(data.access_token)
        fetch("https://kapi.kakao.com/v2/user/me",{
            method : "POST",
            headers : {
                'Authorization': `Bearer ${data.access_token}`,
                'content-type' : 'application/x-www-form-urlencoded;charset=utf-8',
            }
        })
        .then(res => res.json())
        .then((data)=>{

            let dataToSubmit = {
                email: data.id,
                name: data.properties.nickname,
                image: data.properties.profile_image,
                sns: 1,
            };
            console.log(dataToSubmit)

            dispatch(loginUser(dataToSubmit))
            .then(response => {

              if (response.payload.loginSuccess) {
                window.localStorage.setItem('userId', response.payload.userId);
                message.success("카카오 간편 로그인 성공")
                props.history.push('/')
              } else {
                dispatch(registerUser(dataToSubmit)).then(response => {
                    if (response.payload.success) {
                        message.success("카카오 간편 가입 성공! 다시 한번 카카오로 시작하기를 눌러주세요.")
                        
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
            
        })
    }

    useEffect(() => {
        if (!window.location.search) return;
        getKakaoToken();
    }, []);

    return(
        <div className='app'>
            <span style={{ fontSize: '2rem' }}>카카오계정으로 로그인 중입니다. 잠시만 기다려주세요 ...</span>
        </div>
    )

}

export default KakaoLogin
