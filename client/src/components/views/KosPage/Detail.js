import React from "react"
import {useParams} from "react-router-dom"
import stockData from "./data/financials_kr.json"

function DetailPage() {
    const stockId = useParams();

    const thisStock = stockData.find(prod => prod.id == stockId.id)
    
    return (
        <div>
            <h1>{thisStock.itmsNm}</h1>
            <p>{thisStock.corpEnsnNm}</p>
            <p>{thisStock.mrktCtg}</p>
        </div>
    )
}

export default DetailPage;