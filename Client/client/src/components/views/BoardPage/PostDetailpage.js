import React, { useEffect, useState } from 'react'
import Axios from 'axios'
import { Avatar ,List, Typography, Button } from 'antd'
import moment from 'moment';
import Comment from './Comment'
import './BoardPage.css'

const { Title } = Typography;



function Postdetailpage(props) {
    
    const postId = props.match.params.postId
    const variable = { postId: postId }
    
    const [PostDetail, setPostDetail] = useState([])
    const [Comments, setComments] = useState([])
    useEffect(() => {
      Axios.post('/api/users/getPostDetail', variable)
      .then(response => {
          if(response.data.success) {
            setPostDetail(response.data.postDetail)
          } else {
              alert('게시글 정보를 가져오지 못했습니다.')
          }
        })

        Axios.post('/api/comment/getComments', variable)
        .then(response => {
            if(response.data.success){
                setComments(response.data.comments)
                console.log(response.data.comments)
            } else {
                alert('댓글 정보를 가져오지 못했습니다.')
            }
            
        })

    }, [])
    
    const refreshFunction = (newComment) => {
        setComments(Comments.concat(newComment))
    }

    if(PostDetail.writer) {
        if(PostDetail.filePath){
            return (
                        <div style={{ width: '100%', margin: '3rem 4rem' }}>
                            <Title level={2}>{PostDetail.title}</Title>
                            <List.Item>
                                <List.Item.Meta
                                    avatar={<Avatar src={PostDetail.writer && PostDetail.writer.image} />} 
                                    title={PostDetail.writer.name}
                                    description={moment(PostDetail.updatedAt).calendar('')}
                                />
                            </List.Item>
                            
                            <hr />
                            <img style={{ width: '50%' }} src={`http://localhost:5000/${PostDetail.filePath}`} />
                            <p style={{ fontSize: '2.3rem' }}>
                                {PostDetail.description}
                            </p>

                            <Button type="primary" size="large" href="/board" style={{left: '50%'}}>목록</Button>
                            <Comment commentLists={Comments} postId={PostDetail._id} refreshFunction={refreshFunction}/>
                        </div>
                    )
        } else {
            return (
                <div style={{ width: '100%', margin: '3rem 4rem' }}>
                    <Title level={2}>{PostDetail.title}</Title>
                    <List.Item>
                        <List.Item.Meta 
                            title={PostDetail.writer.name}
                            description={moment(PostDetail.updatedAt).calendar('')}
                        />
                    </List.Item>
                    
                    <hr />
                   
                    <p style={{ fontSize: '2.3rem' }}>
                        {PostDetail.description}
                    </p>
 
                    <Button type="primary" size="large" href="/board" style={{left: '50%'}}>목록</Button>
                    <Comment commentLists={Comments} postId={PostDetail._id} refreshFunction={refreshFunction}/>
                </div>
            )
        }
        
    } else {
        return (
            <div>...loading </div>
        )
    }
   
}

export default Postdetailpage
