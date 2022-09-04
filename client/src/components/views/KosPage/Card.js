import React from 'react';

function Card({stock}) {
  return(
    <div className="searchedStockItem">
      <div>
        <h2>[{stock.mrktCtg}]   {stock.itmsNm}</h2>
        <h2>({stock.shotnIsin})</h2>
      </div>
    </div>
  );
}

export default Card;