import React from 'react';

function Card({person}) {
  return(
    <div className="tc bg-light-green dib br3 pa3 ma2 grow bw2 shadow-5">
      <div>
        <h2>{person.itmsNm}</h2>
        <p>{person.mrktCtg}</p>
      </div>
    </div>
  );
}

export default Card;