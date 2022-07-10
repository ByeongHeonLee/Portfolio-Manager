import Axios from 'axios'
import React, { useState } from 'react'
import { Icon, Button } from 'antd';
import { useSelector } from 'react-redux'
import SingleComment from './SingleComment'
import ReplyComment from './ReplyComment'

// const { TextArea } = Input;

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
        if(variables.content !== ""){
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
    }

  return (
    <div>
      <br />
      <p style={{fontSize: '1.5rem', fontWeight: 'bolder'}}><Icon type="aliwangwang" />  댓글</p>
      <hr />

      {/*Comment lists*/}                                                        
      
      {props.commentLists && props.commentLists.map((comment, index) => (
                (!comment.responseTo &&
                    <React.Fragment key={index}>
                        <SingleComment comment={comment} postId={postId} refreshFunction={props.refreshFunction} />                                        
                        <ReplyComment commentLists={props.commentLists} postId={postId} parentCommentId={comment._id} refreshFunction={props.refreshFunction} />
                    </React.Fragment>
                )   
                
      ))}
      
      <br />




      {/* Root Comment form */}

      <form style={{ display: 'flex' }} onSubmit={onSubmit}>
          <textarea
            style={{ width: '60%', borderRadius: '5px' }}
            onChange={handleClick}
            value={commentValue}
            placeholder="댓글을 작성해주세요"
          />
          <br />
          <Button style={{ width: '4%', fontSize: '1.5rem', height: '52px', border: 1, backgroundColor:'rgb(0, 0, 0)', color: 'white' }} onClick={onSubmit}><Icon type='message'/> </Button>
      </form>
    </div>
  )
}

export default Comment
