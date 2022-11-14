import React from 'react';
import Plot from 'react-plotly.js';

import world_indices from '../data/world_index.json';

function Index() {

  const json = world_indices
  var texts = new Array();
  var lons = new Array();
  var lats = new Array();

  for(var i=0; i<json.length; i++)
  {
    texts[i] = json[i]['index_name'] + '<br />' + String(json[i]['close_price']);
    lons[i] = json[i]['lon'];
    lats[i] = json[i]['lat'];
  }

  var data = [{
    type: 'scattergeo',
    mode: 'markers+text',
    // text: ["KOSPI", "NIKKEI",  "SHENZHEN", "SSE", "HANGSENG", "TSEC", "S&P500", "DOW JONES", "NASDAQ", "VIX","FTSE 100", "ESTX 50", "EURONEXT", "DAX", "CAC 40"],
    // lon: [128.00, 138.24,116.5, 119.2, 120.1, 121.3, -118.3, -94.2, -74.1, -84.2,-2.1, 13.5, 2.1, 10.45, 4.3],
    // lat: [37.5, 36.4, 37.1, 29.1, 22.1, 24.4, 39.1, 38.7,  42.5, 44.1,53.5, 41.9, 46.4, 52.8, 48.2],
    text: texts,
    lon: lons,
    lat: lats,
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
        size: 15
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
    </div>
  )
}

export default Index