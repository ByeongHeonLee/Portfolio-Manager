import React from 'react';
import { Link } from 'react-router-dom';

function Card({stock}) {
    return (
      <div className="searchedStockItem">
        <div>
         <Link to={`detail/${stock.id}`}>
           <h2>[{stock.mrktCtg}] {stock.itmsNm} </h2>
           <h2>({stock.shotnIsin})</h2>
           <h2>{"￦ " + stock.clpr} ({stock.fltRt})</h2>
         </Link>
       </div>
     </div>
    );
};

export default Card;