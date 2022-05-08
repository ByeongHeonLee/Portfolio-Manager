const express = require("express"); // express 모듈을 가져옴
const app = express(); // 새로운 express 앱을 만듦
const port = 3000; // 포트 설정

const mongoose = require("mongoose");
mongoose
  .connect(
    "mongodb+srv://ByeongHeonLee:7760qudgjswkd@boilerplate.yaba9.mongodb.net/myFirstDatabase?retryWrites=true&w=majority",
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

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`);
});
