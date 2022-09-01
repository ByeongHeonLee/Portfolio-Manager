import React from 'react';

function Card({stock}) {
  return(
    <div className="searched stock list">
      <div>
        <h2>{stock.itmsNm}</h2>
        <p>{stock.mrktCtg}</p>
      </div>
    </div>
  );
}

export default Card;