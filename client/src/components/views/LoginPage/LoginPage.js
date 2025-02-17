import React, { useState, useEffect, useRef } from "react";
import { withRouter } from "react-router-dom";
import { loginUser } from "../../../_actions/user_actions";
import { Formik } from 'formik';
import * as Yup from 'yup';
import { Form, Icon, Input, Button, Checkbox, Typography } from 'antd';
import { useDispatch } from "react-redux";
// import { KAKAO_AUTH_URL, NAVER_CLIENT_ID, NAVER_CALLBACK_URL } from "../../views/Sns/Snskey"
import './Loginbtn.css';

const { Title } = Typography;
const KAKAO_AUTH_URL = `https://kauth.kakao.com/oauth/authorize?client_id=${process.env.REACT_APP_KAKAO_CLIENT_ID}&redirect_uri=${process.env.REACT_APP_KAKAO_REDIRECT_URI}&response_type=code`;

function LoginPage(props) {
  const dispatch = useDispatch();
  const rememberMeChecked = localStorage.getItem("rememberMe") ? true : false;

  const [formErrorMessage, setFormErrorMessage] = useState('')
  const [rememberMe, setRememberMe] = useState('')

  const handleRememberMe = () => {
    setRememberMe(!rememberMe)
  };
  const naverRef = useRef();
  useEffect(() => {
      const naverScript = document.createElement("script");
      naverScript.src = "https://static.nid.naver.com/js/naveridlogin_js_sdk_2.0.0.js";
      naverScript.type = "text/javascript";
      document.head.appendChild(naverScript);

      naverScript.onload = () => {
          const naverLogin = new window.naver.LoginWithNaverId({
              clientId: process.env.REACT_APP_NAVER_CLIENT_ID,
              callbackUrl: process.env.REACT_APP_NAVER_CALLBACK_URL,
              callbackHandle: true,
              isPopup: false,
              loginButton: {
                  color: "green",
                  type: 3,
                  height: 55,
              }
          });
          naverLogin.init();
          naverLogin.logout(); //네이버 로그인이 계속 유지되는 경우가 있음, 초기화시 로그아웃
      }
  }, [])

  const handleClick = () => {
      naverRef.current.children[0].click();
  }

  //const initialEmail = localStorage.getItem("rememberMe") ? localStorage.getItem("rememberMe") : '';

  return (
    <Formik
      initialValues={{
        email: '',    //initialEmail
        password: '',
      }}
      validationSchema={Yup.object().shape({
        email: Yup.string()
          .email('이메일 형식이 올바르지 않습니다.')
          .required(''),
        password: Yup.string()
          .min(6, '6글자 이상 입력하시오.')
          .required(''),
      })}
      onSubmit={(values, { setSubmitting }) => {
        setTimeout(() => {
          let dataToSubmit = {
            email: values.email,
            password: values.password
          };

          dispatch(loginUser(dataToSubmit))
            .then(response => {
              if (response.payload.loginSuccess) {
                window.localStorage.setItem('userId', response.payload.userId);
                if (rememberMe === true) {
                  window.localStorage.setItem('rememberMe', values.id);
                } else {
                  localStorage.removeItem('rememberMe');
                }
                props.history.push("/");
              } else {
                setFormErrorMessage('이메일과 비밀번호를 다시 확인하시오.')
              }
            })
            .catch(err => {
              setFormErrorMessage('이메일과 비밀번호를 다시 확인하시오.')
              setTimeout(() => {
                setFormErrorMessage("")
              }, 3000);
            });
          setSubmitting(false);
        }, 500);
      }}
    >
      {props => {
        const {
          values,
          touched,
          errors,
          // dirty,
          isSubmitting,
          handleChange,
          handleBlur,
          handleSubmit,
          // handleReset,
        } = props;
        return (
          <div className="app">

            <Title level={2}>로그인</Title>
            <form onSubmit={handleSubmit} style={{ width: '350px' }}>

              <Form.Item required>
                <Input
                  id="email"
                  prefix={<Icon type="user" style={{ color: 'rgba(0,0,0,.25)' }} />}
                  placeholder="Enter your email"
                  type="email"
                  value={values.email}
                  onChange={handleChange}
                  onBlur={handleBlur}
                  className={
                    errors.email && touched.email ? 'text-input error' : 'text-input'
                  }
                />
                {errors.email && touched.email && (
                  <div className="input-feedback">{errors.email}</div>
                )}
              </Form.Item>

              <Form.Item required>
                <Input
                  id="password"
                  prefix={<Icon type="lock" style={{ color: 'rgba(0,0,0,.25)' }} />}
                  placeholder="Enter your password"
                  type="password"
                  value={values.password}
                  onChange={handleChange}
                  onBlur={handleBlur}
                  className={
                    errors.password && touched.password ? 'text-input error' : 'text-input'
                  }
                />
                {errors.password && touched.password && (
                  <div className="input-feedback">{errors.password}</div>
                )}
              </Form.Item>

              {formErrorMessage && (
                <label ><p style={{ color: '#ff0000bf', fontSize: '0.7rem', border: '1px solid', padding: '1rem', borderRadius: '10px' }}>{formErrorMessage}</p></label>
              )}

              <Form.Item>
                {/* <Checkbox id="rememberMe" onChange={handleRememberMe} checked={rememberMe} >Remember me</Checkbox> */}
                {/* <a className="login-form-forgot" href="/reset_user" style={{ float: 'right' }}>
                  비밀번호 찾기
                  </a> */}
                <div>
                  <Button type="primary" htmlType="submit" className="login-form-button" style={{ minWidth: '100%', height: '45px' }} disabled={isSubmitting} onSubmit={handleSubmit}>
                    로그인
                  </Button>
                  <div style={{height: '50px', textAlign: 'center', }}> ――――――――――― or ――――――――――― </div>
                  <a href={KAKAO_AUTH_URL}>
                    <div className={"kakao_btn"} />
                  </a>
                  <div ref={naverRef} id="naverIdLogin"></div>
                  <button onClick={handleClick} className={"naver_btn"}>
                  </button>
                  최초 간편로그인시, 자동으로 회원가입을 진행합니다. 회원가입 후 버튼을 다시 한번 눌러 로그인하세요🙂
                </div>
                {/* Or <a href="/register">회원가입</a> */}
              </Form.Item>
            </form>
          </div>
        );
      }}
    </Formik>
  );
};

export default withRouter(LoginPage);


