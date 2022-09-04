import React, { useState } from 'react';
import Scroll from './Scroll';
import SearchList from './SearchList';

function Search({ details }) {

  const [searchField, setSearchField] = useState("");

  const filteredStocks = details.filter(
    stock => {
      return (
        stock
        .itmsNm
        .toLowerCase()
        .includes(searchField.toLowerCase()) ||
        stock
        .mrktCtg
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
        <button class="searchButton">
            <i class="fa fa-search"></i>
          </button>
      </div>
      {searchList()}
    </section>
  );
}

export default Search;