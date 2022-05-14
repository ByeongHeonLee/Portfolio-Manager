import React, { useState } from 'react'
import Axios from 'axios'
import { Comment, Button, Avatar, Input } from 'antd'
import { useSelector } from 'react-redux'

const { TextArea } = Input;

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

    const onSubmit = (event) => {
        event.preventDefault();

        const variables = {
            content: CommentValue,
            writer: user.userData._id,
            postId: props.postId,
            responseTo: props.comment._id
        }

        Axios.post('/api/comment/saveComment', variables)
        .then(response => {
            if(response.data.success){
                console.log(response.data.result)
                console.log(props.comment.writer.name)
                setCommentValue("")
                // setOpenReply(!OpenReply)
                props.refreshFunction(response.data.result)
            } else {
                alert( '댓글 저장 실패.')
            }
        })
    }

    const actions = [
        <span onClick={onClickReplyOpen} key="comment-basic-reply-to">대댓글</span>
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
                    <TextArea
                        style={{ width: '60%', borderRadius: '5px' }}
                        onChange={onHandleChange}
                        value = {CommentValue}
                        placeholder="댓글을 작성해주세요"
                    />
                    <br />
                    <button style={{ width: '10%', height: '52px' }} onClick={onSubmit}>등록</button>
                </form>
            }
            

        </div>
    )
}

export default SingleComment
