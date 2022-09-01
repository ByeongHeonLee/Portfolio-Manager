import React from 'react';
import Card from './Card';

function SearchList({ filteredStocks }) {
  const filtered = filteredStocks.map(stock =>  <Card key={stock.id} stock={stock} />); 
  return (
    <div>
      {filtered}
    </div>
  );
}

export default SearchList;