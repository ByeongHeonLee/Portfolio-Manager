import React from 'react'
import { useSelector } from "react-redux";
import { Avatar ,List, Typography, Button, Icon } from 'antd'

const { Title } = Typography;

function MyaccountPage() {

    const user = useSelector(state => state.user)
    
    if (!user.userData) return null; 
    else if(user.userData.sns === 1){ //카카오 회원정보
        return (
            <div style={{ width: '100%', margin: '3rem 4rem'}}>
                <Title level={2}>내 정보</Title>
                    <List.Item style={{ display: 'flex', alignItems : 'center', justifyContent: 'space-between',
                    padding: '21px', backgroundColor: 'white', border: '1px solid black', borderWidth: '2px',
                    marginRight: '85px', borderRadius: '20px'
                    }}>
                        <List.Item.Meta 
                            avatar={<Avatar src={user.userData.image} style={{
                                width: '100px', height: '100px', lineHeight : '40px', marginRight: '27px', borderRadius: '50%'
                            }} />} 
                            title={<p style={{ 
                                marginBottom : '42px', marginTop: '3px', color: 'rgba(0, 0, 0, 0.8)', fontSize: '29px', lineHeight: '22px'
                            }}><Icon type='user'/>  {user.userData.name} </p> }
                            description={<p style={{ 
                            color: 'rgba(0, 0, 0, 0.8)', fontSize: '27px', lineHeight: '22px'
                            }}><Icon type='mail'/>  {user.userData.email+" (KAKAO)"}</p>}
                        />
                    </List.Item>
                    
                    ♠ 카카오, 네이버 간편회원은 이메일 대신 랜덤아이디로 표기됩니다.
    
                <br /><br /><br />
               <Title level={2}>개인정보 처리방침</Title>
                「개인정보 보호법」 제30조에 따라 정보주체의 개인정보를 보호하고 이와 관련한 고충을 신속하고 원활하게 처리할 수 있도록 하기 위하여 다음과 같이 개인정보 처리방침을 수립·공개합니다.
                    <br/>
                    <br/>제1조(개인정보의 처리 목적)<br/>
                    <br/> 졸업프로젝트 '포트폴리오 닷컴'은(는) 다음의 목적을 위하여 개인정보를 처리합니다. 처리하고 있는 개인정보는 다음의 목적 이외의 용도로는 이용되지 않으며 <br/>이용 목적이 변경되는 경우에는 「개인정보 보호법」 제18조에 따라 별도의 동의를 받는 등 필요한 조치를 이행할 예정입니다.
                    <br/>1. 홈페이지 회원가입 및 관리
                    <br/>회원 가입의사 확인, 회원제 서비스 제공에 따른 본인 식별·인증 목적으로 개인정보를 처리합니다.
                    <br/><br/>2. 재화 또는 서비스 제공
                    <br/>서비스 제공, 콘텐츠 제공을 목적으로 개인정보를 처리합니다.
            </div>
        )
    }
    else if(user.userData.sns === 2){ //네이버 회원정보
        return (
            <div style={{ width: '100%', margin: '3rem 4rem'}}>
                <Title level={2}>내 정보</Title>
                    <List.Item style={{ display: 'flex', alignItems : 'center', justifyContent: 'space-between',
                    padding: '21px', backgroundColor: 'white', border: '1px solid black', borderWidth: '2px',
                    marginRight: '85px', borderRadius: '20px'
                    }}>
                        <List.Item.Meta 
                            avatar={<Avatar src={user.userData.image} style={{
                                width: '100px', height: '100px', lineHeight : '40px', marginRight: '27px', borderRadius: '50%'
                            }} />} 
                            title={<p style={{ 
                                marginBottom : '42px', marginTop: '3px', color: 'rgba(0, 0, 0, 0.8)', fontSize: '29px', lineHeight: '22px'
                            }}><Icon type='user'/>  {user.userData.name} </p> }
                            description={<p style={{ 
                            color: 'rgba(0, 0, 0, 0.8)', fontSize: '27px', lineHeight: '22px'
                            }}><Icon type='mail'/>  {user.userData.email+" (NAVER)"}</p>}
                        />
                    </List.Item>
                    
                    ♠ 카카오, 네이버 간편회원은 이메일 대신 랜덤아이디로 표기됩니다.
    
                <br /><br /><br />
                <Title level={2}>개인정보 처리방침</Title>
                「개인정보 보호법」 제30조에 따라 정보주체의 개인정보를 보호하고 이와 관련한 고충을 신속하고 원활하게 처리할 수 있도록 하기 위하여 다음과 같이 개인정보 처리방침을 수립·공개합니다.
                    <br/>
                    <br/>제1조(개인정보의 처리 목적)<br/>
                    <br/> 졸업프로젝트 '포트폴리오 닷컴'은(는) 다음의 목적을 위하여 개인정보를 처리합니다. 처리하고 있는 개인정보는 다음의 목적 이외의 용도로는 이용되지 않으며 <br/>이용 목적이 변경되는 경우에는 「개인정보 보호법」 제18조에 따라 별도의 동의를 받는 등 필요한 조치를 이행할 예정입니다.
                    <br/>1. 홈페이지 회원가입 및 관리
                    <br/>회원 가입의사 확인, 회원제 서비스 제공에 따른 본인 식별·인증 목적으로 개인정보를 처리합니다.
                    <br/><br/>2. 재화 또는 서비스 제공
                    <br/>서비스 제공, 콘텐츠 제공을 목적으로 개인정보를 처리합니다.
            </div>
        )
    }
    else{
        return (
            <div style={{ width: '100%', margin: '3rem 4rem'}}>
                <Title level={2}>내 정보</Title>
                    <List.Item style={{ display: 'flex', alignItems : 'center', justifyContent: 'space-between',
                    padding: '21px', backgroundColor: 'white', border: '1px solid black', borderWidth: '2px',
                    marginRight: '85px', borderRadius: '20px'
                    }}>
                        <List.Item.Meta 
                            avatar={<Avatar src={user.userData.image} style={{
                                width: '100px', height: '100px', lineHeight : '40px', marginRight: '27px', borderRadius: '50%'
                            }} />} 
                            title={<p style={{ 
                                marginBottom : '42px', marginTop: '3px', color: 'rgba(0, 0, 0, 0.8)', fontSize: '29px', lineHeight: '22px'
                            }}><Icon type='user'/>  {user.userData.name} </p> }
                            description={<p style={{ 
                            color: 'rgba(0, 0, 0, 0.8)', fontSize: '27px', lineHeight: '22px'
                            }}><Icon type='mail'/>  {user.userData.email}</p>}
                        />
                    </List.Item>
                    
                    ♠ 카카오, 네이버 간편회원은 이메일 대신 랜덤아이디로 표기됩니다.
    
                <br /><br /><br />
                <Title level={2}>개인정보 처리방침</Title>
                「개인정보 보호법」 제30조에 따라 정보주체의 개인정보를 보호하고 이와 관련한 고충을 신속하고 원활하게 처리할 수 있도록 하기 위하여 다음과 같이 개인정보 처리방침을 수립·공개합니다.
                    <br/>
                    <br/>제1조(개인정보의 처리 목적)<br/>
                    <br/> 졸업프로젝트 '포트폴리오 닷컴'은(는) 다음의 목적을 위하여 개인정보를 처리합니다. 처리하고 있는 개인정보는 다음의 목적 이외의 용도로는 이용되지 않으며 <br/>이용 목적이 변경되는 경우에는 「개인정보 보호법」 제18조에 따라 별도의 동의를 받는 등 필요한 조치를 이행할 예정입니다.
                    <br/>1. 홈페이지 회원가입 및 관리
                    <br/>회원 가입의사 확인, 회원제 서비스 제공에 따른 본인 식별·인증 목적으로 개인정보를 처리합니다.
                    <br/><br/>2. 재화 또는 서비스 제공
                    <br/>서비스 제공, 콘텐츠 제공을 목적으로 개인정보를 처리합니다.
            </div>
        )
    }
}

export default MyaccountPage
