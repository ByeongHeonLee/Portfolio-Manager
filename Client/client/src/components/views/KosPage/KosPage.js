//코스피 코스닥 주가정보 페이지

import { React, useState } from "react";
import TextField from "@mui/material/TextField";
import List from "./Components/KosPage"
import "./App.css";

function App() {
  return (
    <div className="main">
      <h1>KOSPI Search</h1>
      <div className="search">
        <TextField
          id="outlined-basic"
          variant="outlined"
          fullWidth
          label="Search"
        />
      </div>
      <List />
    </div>
  );
}

export default KosPage
