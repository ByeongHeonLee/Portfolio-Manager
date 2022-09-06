import React from 'react';
import Search from './Search';
// const mongoose = require('mongoose')
import financials_kr from './data/financials_kr.json';

// mongoose.connect(config.mongoURI_stock_info, {
//   useNewUrlParser: true,
//   useUnifiedTopology: true,
//   useCreateIndex: true,
//   useFindAndModify:false}
// ).then(() => console.log('MongoDB Connected..')
// ).catch(err => console.log(err))

function KosPage() {
  return (
    <div className="stock search bar">
      <Search details={financials_kr}/>
    </div>
        
  );
}

export default KosPage
