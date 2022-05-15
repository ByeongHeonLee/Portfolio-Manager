import React, { useState } from 'react'
import Axios from 'axios'
import { Icon, Comment, Button, Avatar, message } from 'antd'
import { useSelector } from 'react-redux'
import LikeDislikes from './LikeDislikes'
//const { TextArea } = Input;

function SingleComment(props) {
    const user = useSelector(state => state.user)

    const [OpenReply, setOpenReply] = useState(false)
    const [CommentValue, setCommentValue] = useState("")
    
    const onClickReplyOpen = () => {
        setOpenReply(!OpenReply)
    }

    const onHandleChange = (event) => {
        setCommentValue(event.currentTarget.value)
    }

    
    const onCommentDelete = () => {

        const variables = {
            content: props.comment.content,
            writer: user.userData._id,
            postId: props.postId,
            responseTo: props.comment.responseTo
        }
        
        if(window.confirm('정말 삭제하시겠습니까?') === true){
            Axios.post('/api/comment/DeleteComment', variables)
            .then(response => {
                if(response.data.success) {
                    message.success("삭제하였습니다.")
                    window.location.reload()
                } else {
                    alert('삭제에 실패하였습니다.')
                }
            })
        } else {
            return false;
        }
        
    }


    const onSubmit = (event) => {
        event.preventDefault();
        
        const variables = {
            content: CommentValue,
            writer: user.userData._id,
            postId: props.postId,
            responseTo: props.comment._id
        }
        if(variables.content !== ""){

             Axios.post('/api/comment/saveComment', variables)
            .then(response => {
                if(response.data.success){
                    console.log(response.data.result)
                    setCommentValue("")
                    window.location.reload()
                    // setOpenReply(!OpenReply)
                    props.refreshFunction(response.data.result)
                } else {
                    alert( '댓글 저장 실패.')
                }
            })
        }
          
    }


    const actions = [
        <LikeDislikes userId={localStorage.getItem('userId')} commentId={props.comment._id}/>,
        <span style={{marginLeft: '-690px'}} onClick={onClickReplyOpen} key="comment-basic-reply-to">답글 달기</span>,
        (
            props.comment.writer._id === user.userData._id &&
            <Button type="primary" size='small' style={{ border: '1px solid #d7d7da', backgroundColor:'white', color: 'Black', marginLeft: '-600px'}} onClick={onCommentDelete}><Icon type='delete'/></Button>
        )
    ]

    
    return (
        
        <div>
            <Comment
                actions={actions}
                author={props.comment.writer.name}
                avatar={
                    <Avatar 
                        src={props.comment.writer.image}
                        alt="image" 
                    />
                }
                content={
                    <p>
                        {props.comment.content}
                    </p>
                }
            />

            {OpenReply && 
                <form style={{ display: 'flex' }} onSubmit={onSubmit}>
                    <textarea
                        style={{ width: '60%', borderRadius: '5px' }}
                        onChange={onHandleChange}
                        value = {CommentValue}
                        placeholder="답글을 작성해주세요"
                    />
                    <br />
                    <Button style={{ width: '4%', fontSize: '1.5rem', height: '52px', border: 1, backgroundColor:'rgb(0, 0, 0)', color: 'white' }} onClick={onSubmit}><Icon type='message' style={{width: '100%'}}/> </Button>
                </form>
            }
            

        </div>
    )
}

export default SingleComment
