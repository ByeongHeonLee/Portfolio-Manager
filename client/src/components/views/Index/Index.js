// 세계 증시 현황

import React from 'react';
import { Table } from 'antd';
import Plot from 'react-plotly.js';

import info_world_indexes from '../data/info_world_index.json';
import prices_world_index from '../data/price_world_index.json';

function Index() {
  // const dataSource = indexes_kr;
  
  const columns = [
    {
      title: '지수명',
      dataIndex: 'index_name',
      key: 'index_name',
    },
    {
      title: '국가',
      dataIndex: 'nation',
      key: 'nation',
    },
    {
      title: '고가',
      dataIndex: 'high_price',
      key: 'high_price',
    },
    {
      title: '저가',
      dataIndex: 'low_price',
      key: 'low_price',
    },
    {
      title: '종가',
      dataIndex: 'close_price',
      key: 'close_price',
    },
    {
      title: '전일대비 등락률',
      dataIndex: 'fluctuation_rate',
      key: 'fluctuation_rate',
    },
  ];

  var data = [{
    type: 'scattergeo',
    mode: 'markers+text',
    text: ["KOSPI", "NIKKEI",  "SHENZHEN", "SSE", "HANGSENG", "TSEC", "S&P500", "DOW JONES", "NASDAQ", "VIX","FTSE 100", "ESTX 50", "EURONEXT", "DAX", "CAC 40"],
    lon: [128.00, 138.24,116.5, 119.2, 120.1, 121.3, -118.3, -94.2, -74.1, -84.2,-2.1, 13.5, 2.1, 10.45, 4.3],
    lat: [37.5, 36.4, 37.1, 29.1, 22.1, 24.4, 39.1, 38.7,  42.5, 44.1,53.5, 41.9, 46.4, 52.8, 48.2],
    marker: {
        size: 10,
        color: ["#810023", "#0D0863", "#1C7600", "#3BF400", "#E9C200", "#E2E200", "#B9005E", "#630497", "#920092", "#B88CDB", "#431F01","#ff0000","#B3A000", "#006B6B","#B4D900"],
        line: {
            width: 1
        }
    },
    name: 'Canadian cities',
    textposition: ["top center", "bottom center", "middle left", "middle left", "bottom center", "middle right", "top right", "bottom center", "bottom right", 
    "top center","top left", "bottom center", "middle left", "middle right", "middle right"],
}];

var layout = {
    title: '',
    font: {
        family: 'Arial, sans-serif',
        size: 20
    },
    titlefont: {
        size: 16
    },
    width:1920,
    height:1500,
    margin: {"r":10,"t":0,"l":10,"b":0},
    geo: {
        // scope: 'north america',
        resolution: 100,
        lonaxis: {
            'range': [-125, 155]
        },
        lataxis: {
            'range': [-10, 70]
        },
        showrivers: true,
        rivercolor: '#fff',
        showlakes: true,
        lakecolor: '#fff',
        showland: true,
        landcolor: '#EAEAAE',
        countrycolor: '#d3d3d3',
        countrywidth: 1.5,
        subunitcolor: '#d3d3d3'
    }
};

  return (
    <div>
      
      <Plot data={data} layout={layout}/>

      {/* {<Table dataSource={indexes_kr} columns={columns} />} */}
    </div>
  )
}

export default Index