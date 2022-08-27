//코스피 코스닥 주가정보 페이지
//ex)시총순위 나열

import React from 'react';
import Search from './Search';
const mongoose = require('mongoose')
import krx_stock_info from './data/krx_stock_info.json';

mongoose.connect(config.mongoURI_stock_info, {
  useNewUrlParser: true,
  useUnifiedTopology: true,
  useCreateIndex: true,
  useFindAndModify:false}
).then(() => console.log('MongoDB Connected..')
).catch(err => console.log(err))

function KosPage() {
  return (
    <div className="tc bg-green ma0 pa4 min-vh-100">
      <Search details={krx_stock_info}/>
    </div>
  );
}

export default KosPage
