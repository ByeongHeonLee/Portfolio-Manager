import React, { useEffect, useState } from 'react'
import SingleComment from './SingleComment'

function ReplyComment(props) {

    const [ChildCommentNumber, setChildCommentNumber] = useState(0)
    const [OpenReplyComments, setOpenReplyComments] = useState(false)
    
    useEffect(() => {

        let commentNumber = 0
        props.commentLists.map((comment) => {

            if(comment.responseTo === props.parentCommentId){
                commentNumber++
            }
        })
        setChildCommentNumber(commentNumber)
    }, [])
   
    

    const renderReplyComment = (parentCommentId) => 
        props.commentLists.map((comment, index) => (
            
            <React.Fragment key={index}>
                {
                    comment.responseTo === parentCommentId && (
                        <div style={ {width: '80%', marginLeft: '40px'} }>
                            <SingleComment comment={comment} postId={props.postId} refreshFunction={props.refreshFunction} />                                        
                            <ReplyComment commentLists={props.commentLists} postId={props.postId} parentCommentId={comment._id} refreshFunction={props.refreshFunction} />
                        </div>
                    )
                }   
            </React.Fragment>
        )
    )

    const onHandleChange = () => {
        setOpenReplyComments(!OpenReplyComments)
    }
    

    return (

        <div>
            {ChildCommentNumber > 0 && (
                    <p style={{ marginLeft: '40px', fontSize : 12, color: 'gray' }} onClick={onHandleChange} >
                        답글 {ChildCommentNumber}개 더보기..
                    </p>
                )
            } 

            {OpenReplyComments && 
                renderReplyComment(props.parentCommentId)
            }
            
        </div>
    )
}

export default ReplyComment
