import React from "react"
import {useParams} from "react-router-dom"
import stockData from "./data/financials_kr.json"

function ShowDetailData() {
    const {id} = useParams()
    const stock = stockData.find(prod => prod.id == id)
    
    return (
        <div>
          <br/>
          <br/>
          <br/>
          <br/>
            <h2>[기본정보]</h2>
            <p>시장 구분 : {stock.mrktCtg}</p>
            <p>종목명 : {stock.itmsNm}</p>
            <p>ISIN : {stock.isinCd}</p>
            <p>기업 홈페이지 : {stock.enpHmpgUrl}</p>
            <br/>
            <h2>[재무정보]</h2>
            <p>재무제표부채비율 : {stock.fnclDebtRto}</p>
            <p>기업자본금액 : {stock.enpCptlAmt}</p>
            <p>당기순이익 : {stock.enpCrtmNpf}</p>
            <p>영업이익 : {stock.enpBzopPft}</p>
            <p>매출금액 : {stock.enpSaleAmt}</p>
            <p>주식 액면가 : {stock.stckParPrc}</p>
            <p>발행 주식수 : {stock.issuStckCnt}</p>
            <p>상장일자 : {stock.lstgDt}</p>
            <br/>
            <h2>[전일 주가정보]</h2>
            <p>시가 : {stock.mkp}</p>
            <p>종가 : {stock.clpr}</p>
            <p>고가 : {stock.hipr}</p>
            <p>저가 : {stock.lopr}</p>
        </div>
    )
}

export default ShowDetailData