import React, { useEffect, useState } from 'react'
import { Table, Card, Typography, Button, Row, Col, Avatar } from 'antd';
import Axios from 'axios';
import moment from 'moment';

const { Title } = Typography;
const { Meta } = Card;
//글목록 테이블 페이지임.
function TablePage() {
  
 const [Post, setPost] = useState([])

  useEffect(() => {
    
    Axios.get('/api/users/getPosts')
    .then(response => {
      if(response.data.success) {
        console.log(response.data)
        setPost(response.data.posts)
      } else {
        alert('게시글 가져오기를 실패하였습니다.')
      }
    })
  
  }, [])

  const columns = [
    {
      title: '#',
      dataIndex: 'number',
      key: 'number',
      align: 'center',
      width: '10%',
    },
    {
      title: '제목',
      dataIndex: 'title',
      key: 'title',
      align: 'center',
      width: '40%',
      render: (text, record) => {
        return <a href={`/board/${record._id}`}>{record.title}</a>
      }
    },
    {
      title: '글쓴이',
      dataIndex: 'writer',
      key: 'writer',
      align: 'center',
      width: '15%',
    },
    {
      title: '날짜',
      dataIndex: 'date',
      key: 'date',
      align: 'center',
    },
    {
      title: '조회수',
      dataIndex: 'views',
      key: 'views',
      align: 'center',
    },
  ];

  const data = [];
  Post.map((post, index) => {
    data.push({
        key: index.toString(),
        number: `${index+1}`,
        title: `${post.title}`,
        writer: `${post.writer.name}`,
        views: `${post.views}`,
        date: `${moment(post.createdAt).calendar('')}`,
        _id: `${post._id}`,   
    })
  })
  



  
  
//반응형으로 만드는법
  // const renderCards = Post.map((post, index) => { 

  //     // var minutes = Math.floor(post.duration / 60);
  //     // var seconds = Math.floor(post.duration - minutes * 60);


  //     return <Col lg={6} md={8} xs={24}>
  //           <div style={{ position: 'relative' }}>
  //               <a href={`/video/${post._id}`} >
  //               <img style={{ width: '100%' }} alt="thumbnail" src={`http://localhost:5000/${post.FilePath}`} />
  //               {/* <div className=" duration"
  //                   style={{ bottom: 0, right:0, position: 'absolute', margin: '4px', 
  //                   color: '#fff', backgroundColor: 'rgba(17, 17, 17, 0.8)', opacity: 0.8, 
  //                   padding: '2px 4px', borderRadius:'2px', letterSpacing:'0.5px', fontSize:'12px',
  //                   fontWeight:'500', lineHeight:'12px' }}>
  //                   <span>{minutes} : {seconds}</span>
  //               </div> */}
  //               </a>
  //           </div><br />
  //           <Meta
  //               avatar={
  //                   <Avatar src={post.writer.image} />
  //               }
  //               title={post.title}
  //           />
  //           <span>{post.writer.name} </span><br />
  //           <span style={{ marginLeft: '3rem' }}> {post.views}</span>
  //           - <span> {moment(post.createdAt).format("MMM Do YY")} </span>
  //       </Col>
      
  // })
  
  

  
  
  
  
  return (
    <div style={{width: '85%', margin: '3rem auto'}}>
      <Title level={2}>종목 토론 게시판</Title>
      <hr />
      <Table dataSource={data} columns={columns} />
      <Button type="primary" size="large" href="/board/post">글쓰기</Button>
    
    </div>
    
  )
}

export default TablePage
