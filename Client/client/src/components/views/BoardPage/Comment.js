import Axios from 'axios'
import React, { useState } from 'react'
import { Button, Input } from 'antd';
import { useSelector } from 'react-redux'
import SingleComment from './SingleComment'

const { TextArea } = Input;

function Comment(props) {

    const user = useSelector(state => state.user)
    const postId = props.postId
    
    const [commentValue, setcommentValue] = useState("")
    
    const handleClick = (event) => {
        setcommentValue(event.currentTarget.value)
    }
    
    const onSubmit = (event) => {
        event.preventDefault();

        const variables = {
            content: commentValue,
            writer: user.userData._id,
            postId: postId
        }

        Axios.post('/api/comment/saveComment', variables)
        .then(response => {
            if(response.data.success){
                console.log(response.data.result)
                setcommentValue("")
                props.refreshFunction(response.data.result)
            } else {
                alert( '댓글 저장 실패.')
            }
        })
    }

  return (
    <div>
      <br />
      <p>댓글</p>
      <hr />

      {/*Comment lists*/}                                                        
      
      {props.commentLists && props.commentLists.map((comment, index) => (
                //(!comment.responseTo &&
                    <React.Fragment key={index}>
                        <SingleComment comment={comment} postId={postId} refreshFunction={props.refreshFunction} />                                        
                    </React.Fragment>
                //)   
                
      ))}
      

{/* <ReplyComment CommentLists={props.CommentLists} postId={props.postId} parentCommentId={comment._id} refreshFunction={props.refreshFunction} /> */}



      {/* Root Comment form */}

      <form style={{ display: 'flex' }} onSubmit={onSubmit}>
          <TextArea
            style={{ width: '60%', borderRadius: '5px' }}
            onChange={handleClick}
            value={commentValue}
            placeholder="댓글을 작성해주세요"
          />
          <br />
          <button style={{ width: '10%', height: '52px' }} onClick={onSubmit} >등록</button>
      </form>
    </div>
  )
}

export default Comment
