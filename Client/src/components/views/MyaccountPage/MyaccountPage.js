import React from 'react'
import { useSelector } from "react-redux";
import { Avatar ,List, Typography, Button, Icon } from 'antd'

const { Title } = Typography;

function MyaccountPage() {

    const user = useSelector(state => state.user)
    
    if (!user.userData) return null; 
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
            <br /><br /><br />

            <Title level={2}>나의 관심 종목</Title>
        </div>
    )

}

export default MyaccountPage