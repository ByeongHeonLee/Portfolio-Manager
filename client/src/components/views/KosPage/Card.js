import React from 'react';

function Card({stock}) {
  var fltRt = String(stock.fltRt);

  if (fltRt.charAt(0) == ".") {
    fltRt = "+0" + fltRt;
  } else if (fltRt.charAt(0) != "+" && fltRt.charAt(0) != "-") {
    fltRt = "+" + fltRt;
  } else if (fltRt.charAt(0) == "-" && fltRt.charAt(1) == ".") {
    fltRt = "-0" + fltRt.slice(1, 4);
  }
  fltRt += "%";

  if(typeof stock.fltRt == "undefined")
    fltRt = "";

  return(
    <div className="searchedStockItem">
      <div>
        <a href={"http://" + stock.enpHmpgUrl}> <h2>[{stock.mrktCtg}] {stock.itmsNm} </h2></a>
        <h2>({stock.shotnIsin})</h2>
        <h2>{"￦ " + stock.clpr} ({fltRt})</h2>
      </div>
    </div>
  );
}

export default Card;