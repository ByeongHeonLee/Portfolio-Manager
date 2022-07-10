import React from 'react'
import './HomePage.css'

function HomePage() {
    return (
        <div className="app">
            <h1 id="head" style={{ fontSize: '4rem', marginTop: '10px', marginBottom: '5px'}}>PortFolio Manager</h1>
            <span id="fullimg" style={{ height:'390px'}}></span>
            <div id="content">                                
                <h1 style={{ fontSize: '1.5rem', marginTop:'20px', marginBottom: '40px'}}>아직도 손해만 보고 계시나요?</h1>                
                <p style={{ fontSize: '0.8rem', marginTop:'10px', marginBottom: '10px'}}>개인투자자들이 주식 시장에서 고전하는 이유 중 하나는 기관·외국인과 개인투자자 사이의 상당한 "정보의 격차"입니다.</p>
                <p style={{ fontSize: '0.8rem', marginTop:'10px', marginBottom: '10px'}}>우리는 이 정보의 격차를 조금이나마 줄여보기 위해 개인투자자들이 기본적인 투자 공부를 무료로 할 수 있는 서비스입니다.</p>
                <p style={{ fontSize: '1rem', marginTop:'10px', marginBottom: '30px'}}>학습 없는 투자는 투기에 불과합니다.</p>               
                <p style={{ fontSize: '0.8rem', marginTop:'10px', marginBottom: '10px'}}>지금 바로 무료 회원가입을 통해 회원이 되어보세요.</p>
                <p style={{ fontSize: '0.8rem', marginTop:'10px', marginBottom: '10px'}}>주식 종목에 대한 관련 공시 및 재무제표 정보를 열람 및 안내받을 수 있고</p>
                <p style={{ fontSize: '0.8rem', marginTop:'10px', marginBottom: '10px'}}>개인별 투자 성향을 분석하여 적합한 종목을 추천받고 그 추천이유 또한 안내받을 수 있으며</p>
                <p style={{ fontSize: '0.8rem', marginTop:'10px', marginBottom: '10px'}}>여태껏 배운 내용을 모의 투자 기능을 통해 주식 시장에 적용해 볼 수 있고</p>
                <p style={{ fontSize: '0.8rem', marginTop:'10px', marginBottom: '70px', marginLeft:'0px'}}>회원들 간의 주식 관련 토론도 자유로이 할 수 있습니다.</p>
            </div>            
        </div>

    )
}

export default HomePage
