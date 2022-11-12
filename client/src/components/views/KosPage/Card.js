import React from 'react';
import { Link } from 'react-router-dom';

function Card({stock}) {
    return (
      <div className="searchedStockItem">
        <div>
         <Link to={`detail/${stock.isin_code}`}>
           <h2>[{stock.market_category}] {stock.item_name} </h2>
           <h2>({stock.short_isin_code})</h2>
         </Link>
       </div>
     </div>
    );
};

export default Card;