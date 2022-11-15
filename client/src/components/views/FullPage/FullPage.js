import React from 'react';
import { FullPage, Slide } from 'react-full-page';
import { Icon, Button } from 'antd';
import './FullPage.css'
import man_img from '../../../images/character.png'
import kakao_img from '../../../images/kakao_logo.png'
import naver_img from '../../../images/naver_logo.png'

export default class fullPage extends React.Component {
  render() {
    return (
        <div className='full-page'>
          <FullPage controls controlsProps={{className: 'slide-navigation'}}>
              <Slide>
              <div className="section-common section-area1">
                <h1>Portfolio.com</h1>
                <img src={man_img} className='man_img'></img>
              </div>
              </Slide>
              <Slide>
              <div className="section-common section-area2">
                <div className='search_bar'>
                  <h1>삼성전자</h1>
                </div>
                <Button type="primary" size="large" href="/search" 
                  style={{ border: '1px solid rgb(0, 88, 202)', backgroundColor:'rgb(0, 88, 202)', color: 'white', top: '75%', left: '70%',
                  borderRadius: '20px', padding: '8px', height:'60px', width: '200px', fontSize: '20px', fontWeight: 'bolder' }}>
                    검색하러 가기</Button>
              </div>
              </Slide>
              <Slide>
              <div className="section-common section-area3">
                <div className="title3">
                  <h1 style={{color:'black'}}>세계 주요지수들을<br />지금 바로 확인할 수 있어요!</h1> 
                </div>
                <div className='worldmap' />
                <Button type="primary" size="large" href="/index" 
                  style={{ border: '1px solid rgb(0, 88, 202)', backgroundColor:'rgb(0, 88, 202)', color: 'white', top: '75%', left: '70%',
                  borderRadius: '20px', padding: '8px', height:'60px', width: '200px', fontSize: '20px', fontWeight: 'bolder' }}>
                    지수 확인하기</Button>
              </div>
              </Slide>
              <Slide>
              <div className="section-common section-area5">
                <div className='postDetail'>
                  <h1>저도 다시 회복중입니다 ㅠㅠ 정말 다행!</h1>
                  <div className='like_img' />
                </div>
                <Button type="primary" size="large" href="/board" 
                  style={{ border: '1px solid rgb(0, 88, 202)', backgroundColor:'rgb(0, 88, 202)', color: 'white', top: '75%', left: '70%',
                  borderRadius: '20px', padding: '8px', height:'60px', width: '200px', fontSize: '20px', fontWeight: 'bolder' }}>
                    게시판 바로가기</Button>
              </div>
              </Slide>
              <Slide>
              <div className="section-common section-area6">
                <h1 style={{marginLeft: '10%', marginTop: '5%', fontSize: '100px', fontWeight: 'bolder', color: 'white'}}>Portfolio<br/> dot<br/> com</h1>
                <Button type="primary" size="large" href="/register" 
                  style={{ border: '1px solid rgb(0, 88, 202)', backgroundColor:'white', color: 'black', top: '20%', left: '20%',
                  borderRadius: '30px', padding: '19px', height:'80px', width: '300px', fontSize: '40px', fontWeight: '400' }}>
                    회원가입</Button>
                <h1 style={{marginLeft: '135px', marginTop: '231px', fontSize: '30px', fontWeight: 'bolder', color: 'white'}}>OR<br/></h1>
                <Button type="primary" size="large" href="/login" 
                  style={{ border: '1px solid rgb(0, 88, 202)', backgroundColor:'white', color: 'black', top: '20%', left: '20%',
                  borderRadius: '30px', padding: '19px', height:'80px', width: '300px', fontSize: '40px', fontWeight: '400', marginTop:'130px',
                  marginLeft:'-478px' }}>
                    로그인</Button>

                  <h1 style={{marginLeft: '120px', marginTop: '370px', fontSize: '20px', fontWeight: 'bolder', color: 'white'}}>
                    login with. <img src={kakao_img}></img><img src={naver_img} style={{marginLeft: '10px'}}></img>
                  </h1>
                  <h1 style={{marginLeft: '-1050px', marginTop: '580px', fontSize: '15px', fontWeight: '400', color: 'white'}}>
                    포트폴리오닷컴<br/><br/> 홍익대학교<br/> 컴퓨터공학과 졸업프로젝트<br/>
                  </h1>
                  <h1 style={{marginLeft: '100px', marginTop: '620px', fontSize: '15px', fontWeight: '400', color: 'white'}}>
                    이병헌, lww7438@gmail.com<br/> 이성혁, eseonghyeok@naver.com
                  </h1>

              </div>
              </Slide>
          </FullPage>
        </div>
    );
  }
};
