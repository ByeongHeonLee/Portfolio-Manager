const express = require("express"); // express 모듈을 가져옴
const app = express(); // 새로운 express 앱을 만듦
const port = 3000; // 포트 설정
const bodyParser = require("body-parser");

const config = require('./config/key')

const { User } = require("./models/User");

// application/x-www-form-urlencoded
app.use(bodyParser.urlencoded({ entended: true }));

// application/json
app.use(bodyParser.json());

const mongoose = require("mongoose");
mongoose
  .connect(config.mongoURI,
    {
      //useNewUrlParser: true, useUnifiedTopology: true, useCreateIndex: true, useFindAndModify:false (Default Options on Mongoose Version 6)
    }
  )
  .then(() => console.log("MongoDB Connected..."))
  .catch((err) => console.log(err));

app.get("/", (req, res) => {
  // 루트에 문자열을 출력하게 함
  res.send("Hello World! 안녕하세요!");
});

app.post("/register", (req, res) => {
  //회원가입시 필요한 정보들을 client에서 가져오면
  // 그것들을 DB에 저장한다.

  const user = new User(req.body);
  user.save((err, userInfo) => {
    if (err) return res.json({ success: false, err });
    return res.status(200).json({ success: true });
  });
});

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`);
});
