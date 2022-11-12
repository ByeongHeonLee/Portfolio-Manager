import React from 'react';
import Search from './Search';
// const mongoose = require('mongoose')
import info_stock from '../data/info_stock.json';

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
      <Search details={info_stock}/>
    </div>
        
  );
}

export default KosPage
