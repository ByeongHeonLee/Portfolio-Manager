import React, { Suspense } from 'react';
import { Route, Switch } from "react-router-dom";
import Auth from "../hoc/auth";
// pages for this product
import LandingPage from "./views/LandingPage/LandingPage.js";
import LoginPage from "./views/LoginPage/LoginPage.js";
import RegisterPage from "./views/RegisterPage/RegisterPage.js";
import NavBar from "./views/NavBar/NavBar";
// import Footer from "./views/Footer/Footer"
import HomePage from './views/HomePage/HomePage';
import BoardPage from './views/BoardPage/BoardPage';
import TablePage from './views/BoardPage/TablePage';
import SimulatePage from './views/SimulatePage/SimulatePage';
import Postdetailpage from './views/BoardPage/PostDetailpage';
import MyaccountPage from './views/MyaccountPage/MyaccountPage';
import KosPage from './views/KosPage/KosPage';
import Index from './views/Index/Index';
//import Percent from './views/Percent/Percent';
import NewsPage from './views/NewsPage/NewsPage';
import KakaoLogin from './views/Sns/KakaoLogin';
import NaverLogin from './views/Sns/NaverLogin';

import './App.css'

//null   Anyone Can go inside
//true   only logged in user can go inside
//false  logged in user can't go inside

function App() {
  return (
    <Suspense fallback={(<div>Loading...</div>)}>
      <NavBar />
      <div style={{ paddingTop: '69px', minHeight: 'calc(100vh - 80px)' }}>
        <Switch>
          <Route exact path="/home" component={Auth(HomePage, null)} />
          <Route exact path="/" component={Auth(LandingPage, true)} />
          <Route exact path="/board" component={Auth(TablePage, true)} />
          <Route exact path="/board/post" component={Auth(BoardPage, true)} />
          <Route exact path="/board/:postId" component={Auth(Postdetailpage, true)} />
          <Route exact path="/simulate" component={Auth(SimulatePage, true)} />
          <Route exact path="/login" component={Auth(LoginPage, false)} />
          <Route exact path="/register" component={Auth(RegisterPage, false)} />
          <Route exact path="/myAccount" component={Auth(MyaccountPage, true)} />
          <Route exact path="/index" component={Auth(Index, null)} />
          <Route exact path="/news" component={Auth(NewsPage, null)} />
          <Route exact path="/oauth/callback/kakao" component={Auth(KakaoLogin, false)} />
          <Route exact path="/oauth/callback/naver" component={Auth(NaverLogin, false)} />
        </Switch>
      </div>
    </Suspense>
  );
}

export default App;
