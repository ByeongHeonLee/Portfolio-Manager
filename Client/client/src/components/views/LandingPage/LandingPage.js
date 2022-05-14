import React, { useState } from 'react'
import { FaCode } from "react-icons/fa";
import './LandingPage.css'

function LandingPage() {
    
    const [Search, setSearch] = useState("");

    const handleChangeSearch = (event) => {
        setSearch(event.currentTarget.value)
    }
    
    
    return (
        <>
            <div className="app">
                <h1 id="head" style={{ fontSize: '4rem', marginTop: '-200px', marginBottom: '5px'}}>PortFolio Manager</h1>
                <span id="fullimg" style={{ height:'400px'}}></span>
            
                
                <div className="wrap" style={{marginTop: '-80px'}}>
                    <div className="search">
                        <input type="text" id="searchStocks" autocomplete="off" name="searchStocksName" 
                            value={Search} placeholder="종목 이름 또는 코드를 입력하세요" box-sizing="border-box" class="searchTerm" onChange={handleChangeSearch}>
                        </input>
                        <button type="submit" class="searchButton">
                            검색<i class="fa fa-search"></i>
                        </button>       
                    </div>
                </div>
            </div>
        </>
    )
}

export default LandingPage
