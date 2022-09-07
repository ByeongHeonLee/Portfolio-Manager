import React, { useState } from "react";
import { Button, Icon } from "antd";
import './LandingPage.css'
import Search from "../KosPage/Search";
import financials_kr from "../KosPage/data/financials_kr.json";

function LandingPage() {
  // const [Search, setSearch] = useState("");

  // const handleChangeSearch = (event) => {
  //   setSearch(event.currentTarget.value);
  // };

  // const searchValue = (event) => {};

  return (
    <div>
      <div className="app">
        <h1
          id="head"
          style={{ fontSize: "4rem", marginTop: "0px", marginBottom: "300px" }}
        >
          PORTFOLIO.COM
        </h1>
      </div>

      <div className="tc bg-green ma0 pa4 min-vh-100">
        <Search details={financials_kr} />
      </div>
    </div>
  );
}

export default LandingPage;
