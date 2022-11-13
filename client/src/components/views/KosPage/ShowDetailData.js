import React from "react"
import {useParams} from "react-router-dom"

import info_stocks from "../data/info_stock.json"
import info_financials from "../data/info_financials.json"
import prices from "../data/prices.json"
import newses from "../data/info_news.json"

function ShowDetailData() {
    const {isin_code} = useParams()
    const info_stock = info_stocks.find(prod => prod.isin_code == isin_code)
    const info_financial = info_financials.find(prod => prod.isin_code == isin_code)
    const price = prices.find(prod => prod.isin_code == isin_code)
    
    const newsList = newses.filter(news => ( 
        news.isin_code === isin_code				
    ))
    
    return (
        <div>
          <br/>
          <br/>
          <br/>
          <br/>
            <h2>[기본정보]</h2>
            <p>시장 구분 : {info_stock.market_category}</p>
            <p>종목명 : {info_stock.item_name}</p>
            <p>ISIN : {info_stock.isin_code}</p>
            <p>상장일 : {info_stock.listing_date}</p>
            <br/>
            <h2>[재무정보]</h2>
            <p>BPS : {info_financial.bps}</p>
            <p>PER : {info_financial.per}</p>
            <p>PBR : {info_financial.pbr}</p>
            <p>EPS : {info_financial.eps}</p>
            <p>DIV : {info_financial.div}</p>
            <p>DPS : {info_financial.dps}</p>
            <br/>
            <h2>[전일 주가정보]</h2>
            <p>시가 : {price.market_price}</p>
            <p>종가 : {price.close_price}</p>
            <p>고가 : {price.high_price}</p>
            <p>저가 : {price.low_price}</p>
            <p>등락 : {price.fluctuation}</p>
            <p>등락률 : {price.fluctuation_rate}</p>
            <p>거래량 : {price.volume}</p>
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