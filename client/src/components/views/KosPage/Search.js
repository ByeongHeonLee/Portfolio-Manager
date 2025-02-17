import React, { useState } from 'react';
import { Icon, Button } from 'antd';
import Scroll from './Scroll';
import SearchList from './SearchList';

function Search({ details }) {

  const [searchField, setSearchField] = useState("");

  const filteredStocks = details.filter(
    stock => {
      return (
        stock
        .item_name
        .toLowerCase()
        .includes(searchField.toLowerCase()) ||
        stock
        .market_category
        .toLowerCase()
        .includes(searchField.toLowerCase())
      );
    }
  );

  const handleChange = e => {
    setSearchField(e.target.value);
  };

  function searchList() {
    return (
      <Scroll>
        <SearchList filteredStocks={filteredStocks} />
      </Scroll>
    );
  }

  return (
    <section className="wrap">
      <div className="search">
        <input 
          className="searchTerm"
          type = "search" 
          placeholder = "종목명을 입력하세요" 
          onChange = {handleChange}
        />
        <Button type="primary" class="searchButton"
            style={{ width: '80px', height: '80px', border: '1px solid #0058ca', textAlign: 'center',
               backgroundColor: '#0058ca', borderRadius: '0 5px 5px 0', cursor: 'pointer', fontSize: '30px'}}>
            <Icon type='search' style={{ padding: '10px 0 0 0' }}/>
        </Button> 
        {/* <Icon className="searchButton" type="search" style={{ color: 'rgba(00,B4,CC,.25)' }} /> */}
      </div>
      {searchList()}
    </section>
  );
}

export default Search;
