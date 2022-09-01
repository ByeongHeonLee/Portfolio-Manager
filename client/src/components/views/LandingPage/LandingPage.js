import React, { useState } from "react";
import { Button, Icon } from "antd";
import "./LandingPage.css";

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
          //style={{ fontSize: "4rem", marginTop: "-200px", marginBottom: "5px" }}
        >
          PortFolio.com
        </h1>
        <span id="fullimg" style={{ height: "400px" }}></span>
      </div>

      <div className="tc bg-green ma0 pa4 min-vh-100">
        <Search details={financials_kr} />
      </div>
    </div>
  );
}

export default LandingPage;
