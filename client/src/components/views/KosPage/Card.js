import React from 'react';
import { Link } from 'react-router-dom';
import ShowDetailData from './ShowDetailDataShow';

function Card({stock}) {

  return(
    <div className="searchedStockItem">
      <div>
        <Link to={`detail/${stock.id}`}>
        {/* <a href={"http://" + stock.enpHmpgUrl> <h2>[{stock.mrktCtg}] {stock.itmsNm} </h2>}> </a> */}
        <h2>[{stock.mrktCtg}] {stock.itmsNm} </h2>
        <h2>({stock.shotnIsin})</h2>
        <h2>{"￦ " + stock.clpr} ({stock.fltRt})</h2>
      </div>
    </div>
  );
};

export default Card;