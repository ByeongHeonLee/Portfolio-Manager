import React, { useState } from 'react'
import { Typography, Button, Form, message, Input, Icon } from 'antd';
import Dropzone from 'react-dropzone';
import axios from 'axios';
import { useSelector } from "react-redux";

//글쓰기페이지임 나중에 이름 바꿀것.
const { Title } = Typography;
const { TextArea } = Input;

function BoardPage(props) {
    const user = useSelector(state => state.user)
    const [title, setTitle] = useState("");
    const [Description, setDescription] = useState("");
    const [FilePath, setFilePath] = useState("")

    const handleChangeTitle = (event) => {
        setTitle(event.currentTarget.value)
    }

    const handleChangeDecsription = (event) => {
        setDescription(event.currentTarget.value)
    }

    const onSubmit = (event) => {

        event.preventDefault();

        if (user.userData && !user.userData.isAuth) {
            return alert('Please Log in First')
        }

        if (title === "" || Description === "" /*||FilePath === ""*/) {
            return alert('제목, 내용은 필수 입력란 입니다.')
        }

        const variables = {
            writer: user.userData._id,
            title: title,
            description: Description,
            // privacy: privacy,
            filePath: FilePath
        }

        axios.post('/api/users/post', variables)
            .then(response => {
                if (response.data.success) {
                     alert('글쓰기에 성공하셨습니다.')
                    props.history.push('/board')

                    // setTimeout(() => {
                    //     props.history.push('/board')
                    // }, 2000); 타이머 자동 넘어가기기능 대신 alert->message.success
                    
                } else {
                    alert('글쓰기에 실패하셨습니다.')
                }
            }) 

    }


    const onDrop = (files) => {

        let formData = new FormData();
        const config = {
            header: { 'content-type': 'multipart/form-data' }
        }
        formData.append("file", files[0])

        axios.post('/api/users/uploadfiles', formData, config)
            .then(response => {
                if (response.data.success) {
                    console.log(response.data)

                    // let variables = {
                    //     filePath: response.data.filePath,
                    //     fileName: response.data.fileName
                    // }

                    setFilePath(response.data.filePath)

                } else {
                    alert('파일 업로드를 실패하였습니다.')
                }
            })

    }


  return (
    <div style={{ maxWidth: '700px', margin: '2rem auto' }}>
        <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
            <Title level={2} > 게시판 글쓰기</Title>
        </div>
        <label>제목</label>
        <Input
            onChange={handleChangeTitle}
            value={title}
        />
        <br /><br />

        <label>첨부파일</label>
        <Form onSubmit={onSubmit}>  
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <Dropzone
                onDrop={onDrop}
                multiple={false}
                maxSize={800000000}
                >
                {({ getRootProps, getInputProps }) => (
                    <div style={{ width: '50px', height: '40px', border: '1px solid lightgray', display: 'flex', alignItems: 'center', justifyContent: 'center' }} {...getRootProps()}>                   
                        <input {...getInputProps()} />
                        <Icon type="plus" style={{ fontSize: '1.2rem' }} />
                    </div>
                )}
                </Dropzone>               
            </div>
            <br />
                {FilePath&&
                    <div>
                        <img src={`http://localhost:5000/${FilePath}`} style={{ width: '400px', height: '300px'}} alt="미리보기"></img>
                    </div>
                }
            <br />
            <label>내용</label>
            <TextArea style={{height: '100px'}}
                onChange={handleChangeDecsription}
                value={Description}
            />
            <br /><br />

            <Button type="primary" href="/board">
                취소
            </Button>
            <Button type="primary" style={{marginLeft: '2px'}} onClick={onSubmit}>
                등록
            </Button>

        </Form>
    </div>
  )
}


export default BoardPage
