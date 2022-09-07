import React from 'react'
import './HomePage.css'
import Search from "../KosPage/Search";
import financials_kr from "../KosPage/data/financials_kr.json";

function HomePage() {

  return (
    <div>
      <div className="app">
        <h1
          id="head"
          style={{ fontSize: "4rem", marginTop: "0px", marginBottom: "0px" }}
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

export default HomePage
