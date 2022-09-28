import React from 'react';
import Card from './Card';

function SearchList({ filteredStocks }) {
  const filtered = filteredStocks.map(stock =>  <Card stock={stock} />); 
  return (
    <div>
      {filtered}
    </div>
  );
}

export default SearchList;