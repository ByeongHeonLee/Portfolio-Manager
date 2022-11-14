import React from "react"
import {useParams} from "react-router-dom"

import info_stocks from "../data/info_stock.json"
import info_financials from "../data/info_financials.json"
import prices from "../data/prices.json"
import newses from "../data/info_news.json"
import './ShowDetailData.css'
import {
    BarChart,
    Bar,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend,
    LineChart,
    Line
  } from "recharts";

function ShowDetailData() {
    const {isin_code} = useParams()
    const info_stock = info_stocks.find(prod => prod.isin_code == isin_code)
    const info_financial = info_financials.find(prod => prod.isin_code == isin_code)
    const price = prices.find(prod => prod.isin_code == isin_code)
    
    const newsList = newses.filter(news => ( 
        news.isin_code === isin_code				
    ))
    
    const price_data = [
        {
          name: "전일주가정보",
          시가: price.market_price,
          저가: price.low_price,
          고가: price.high_price,
          종가: price.close_price
        },
    ];
    
    const per_data = [
        {
          name: "어제",
          등락률: 0,
        },
        {
          name: "오늘",
          등락률: price.fluctuation_rate,
        },
      ];
    
    return (
        <div class="container">
            <table class="rwd-table" style={{marginTop:'35px', marginLeft: '100px'}}>
                <tbody class="table1">
                    <tr> <th>기본정보</th> <th></th> </tr>
                    <tr> <td>시장구분</td> <td>{info_stock.market_category}</td> </tr>
                    <tr> <td>종목명</td> <td>{info_stock.item_name}</td> </tr>
                    <tr> <td>ISIN</td> <td>{info_stock.isin_code}</td> </tr>
                    <tr> <td>상장일</td> <td>{info_stock.listing_date}</td> </tr>
                </tbody>
            </table>
            <table class="rwd-table" style={{marginTop:'15px', marginLeft: '100px'}}>
                <tbody class="table2">
                    <tr> <th>재무정보</th> <th></th> </tr>
                    <tr> <td>BPS</td> <td>{info_financial.bps}</td> </tr>
                    <tr> <td>PER</td> <td>{info_financial.per}</td> </tr>
                    <tr> <td>PBR</td> <td>{info_financial.pbr}</td> </tr>
                    <tr> <td>EPS</td> <td>{info_financial.eps}</td> </tr>
                    <tr> <td>DIV</td> <td>{info_financial.div}</td> </tr>
                    <tr> <td>DPS</td> <td>{info_financial.dps}</td> </tr>
                </tbody>
            </table>
            <table class="rwd-table" style={{marginTop:'-680px', marginLeft: '500px'}}>
                <tbody class="table3">
                    <tr> <th>전일 주가정보</th> <th></th> </tr>
                    <tr> <td>시가</td> <td>{price.market_price}</td> </tr>
                    <tr> <td>종가</td> <td>{price.close_price}</td> </tr>
                    <tr> <td>고가</td> <td>{price.high_price}</td> </tr>
                    <tr> <td>저가</td> <td>{price.low_price}</td> </tr>
                    <tr> <td>등락</td> <td>{price.fluctuation}</td> </tr>
                    <tr> <td>등락률</td> <td>{price.fluctuation_rate}</td> </tr>
                    <tr> <td>거래량</td> <td>{price.volume}</td> </tr>
                </tbody>
            </table>
            <BarChart
                style={{marginTop:'-445px', marginLeft: '1105px'}}
                width={300}
                height={500}
                data={price_data}
                margin={{
                    top: 0,
                    right: 20,
                    left: 40,
                    bottom: 0
                }}
                >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="시가" fill="#19a86c" />
                <Bar dataKey="저가" fill="#286dd5" />
                <Bar dataKey="고가" fill="#d52828" />
                <Bar dataKey="종가" fill="#231f1d" />
            </BarChart>
            <LineChart 
                style={{marginTop:'-230px', marginLeft: '830px'}}
                width={300}
                height={200}
                data={per_data}>

                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="등락률" stroke="#8884d8" strokeWidth={3} />
            </LineChart>
          
            <br/>
            <h2>[관련뉴스]</h2>
            <table>
                <tbody>
                    {newsList.map((news) => (
                    <tr key={news.isin_code}>	  		
                        <td>헤드라인: {news.headline}</td>	  		
                        <td>감성도: {news.sentiment}</td>	  		
                    </tr>
                    ))}
                </tbody>
                </table>
        </div>
    )
}

export default ShowDetailData
