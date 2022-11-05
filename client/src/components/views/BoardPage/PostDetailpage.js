import React, { useEffect, useState } from 'react'
import Axios from 'axios'
import { useSelector } from "react-redux";
import { Avatar ,List, Typography, Button, Icon } from 'antd'
import moment from 'moment';
import Comment from './Comment'
import LikeDislikes from './LikeDislikes';


const { Title } = Typography;



function Postdetailpage(props) {

    const user = useSelector(state => state.user)
    const postId = props.match.params.postId
    const variable = { postId: postId }
    const [PostDetail, setPostDetail] = useState([])
    const [Comments, setComments] = useState([])
    console.log(postId)
    useEffect(() => {
         Axios.post('/api/users/getPostDetail', variable)
        .then(response => {
            if(response.data.success) {
                console.log(response.data.postDetail)
                const vari = { postId: response.data.postDetail._id, views: response.data.postDetail.views}
                Axios.post('/api/users/upViews', vari)
                .then(response => {
                    if(response.data.success) {
                        console.log()
                    } else {
                        alert('조회수 증가 실패')
                    }
                })
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

    const variables ={
        writer: PostDetail.writer,
        title: PostDetail.title,
        description: PostDetail.description,
        filePath: PostDetail.filePath,
        views: PostDetail.views
    }

    const onPostDelete = () => {

        if(window.confirm('게시물을 삭제하시겠습니까?') === true){
            Axios.post('/api/users/DeletePost', variables)
            .then(response => {
                if(response.data.success) {
                    alert('게시물을 삭제했습니다.')
                    props.history.push('/board')
                } else {
                    alert('게시글 삭제에 실패하였습니다.')
                }
            })
        } else {
            return false;
        }
        
    }

    const refreshFunction = (newComment) => {
        setComments(Comments.concat(newComment))
    }

    if(PostDetail.writer) {
        if(PostDetail.filePath){
            return (
                        <div style={{ width: '100%', margin: '3rem 4rem'}}>
                            <Title level={1}>{PostDetail.title}</Title>
                            <List.Item
                                actions={[ <LikeDislikes post userId={localStorage.getItem('userId')}
                                postId={postId}/> ]
                                }>
                                <List.Item.Meta 
                                    avatar={<Avatar src={PostDetail.writer && PostDetail.writer.image} />} 
                                    title={PostDetail.writer.name}
                                    description={moment(PostDetail.updatedAt).calendar('')}
                                />
                            </List.Item>
                            
                            <hr />
                            {/*<img style={{ width: '50%' }} src={`http://localhost:5000/${PostDetail.filePath}`} />*/}
                            <img style={{ width: '400px', height: '700px' }} src={`https://portfolio-dot-com.herokuapp.com/${PostDetail.filePath}`} />
                            <p style={{ fontSize: '1.5rem' }}>
                                {PostDetail.description}
                            </p>
                            <br /><br /><br />
                            <br /><br /><br />
                            <Button type="primary" size="large" href="/board" style={{ border: '1px solid #d7d7da', backgroundColor:'white', color: 'Black', left: '42%'}}><Icon type='menu-fold'/>목록</Button>
                            
                            {user.userData && user.userData._id === PostDetail.writer._id &&
                                <Button type="primary" size="large" style={{ border: '1px solid #d7d7da', backgroundColor:'white', color: 'Black', left: '42.2%'}} onClick={onPostDelete}><Icon type='delete'/>삭제</Button>
                            }
                            <br />
                            <Comment commentLists={Comments} postId={PostDetail._id} refreshFunction={refreshFunction}/>
                        </div>
                    )
        } else {
            return (
                <div style={{ width: '100%', margin: '3rem 4rem' }}>
                    
                    <Title level={1}>{PostDetail.title}</Title>
                    <List.Item
                        actions={[ <LikeDislikes post userId={localStorage.getItem('userId')}
                        postId={postId}/>]}>
                        <List.Item.Meta 
                            avatar={<Avatar src={PostDetail.writer && PostDetail.writer.image} />}
                            title={PostDetail.writer.name}
                            description={moment(PostDetail.updatedAt).calendar('')}
                        />
                    </List.Item>
                    
                    <hr />
                   
                    <p style={{ fontSize: '1.5rem' }}>
                        {PostDetail.description}
                    </p>
                    <br /><br /><br />
                    <br /><br /><br />
                    <Button type="primary" size="large" href="/board" style={{ border: '1px solid #d7d7da', backgroundColor:'white', color: 'Black', left: '42%'}}><Icon type='menu-fold'/>목록</Button>
                    {user.userData && user.userData._id === PostDetail.writer._id &&
                        <Button type="primary" size="large" style={{ border: '1px solid #d7d7da', backgroundColor:'white', color: 'Black', left: '42.2%'}} onClick={onPostDelete}><Icon type='delete'/>삭제</Button>
                    }
                    
                    <br/>
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
