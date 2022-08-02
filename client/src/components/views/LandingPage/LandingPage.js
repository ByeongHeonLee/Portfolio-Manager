import React, { useState } from 'react'
import { Button, Icon } from 'antd'
import './LandingPage.css'

function LandingPage() {
    
    const [Search, setSearch] = useState("");

    const handleChangeSearch = (event) => {
        setSearch(event.currentTarget.value)
    }
    
    const searchValue = (event) => {

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
                        <Button type="primary" class="searchButton" href="/kos"
                            style={{ width: '80px', height: '80px', border: '1px solid #000000', textAlign: 'center',
                               color: '#fff', backgroundColor: '#000000', borderRadius: '0 5px 5px 0', cursor: 'pointer', fontSize: '30px'}}>
                            <Icon type='search' style={{ padding: '23px 0 0 0' }}/>
                        </Button>       
                    </div>
                </div>
            </div>
        </>
    )
}

export default LandingPage