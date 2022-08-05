# 금융위원회_KRX상장종목정보
# https://www.data.go.kr/data/15094775/openapi.do

# Author  : Byeong Heon Lee
# Contact : lww7438@gmail.com

# [Query Inputs]
#  0. serviceKey : 공공데이터 포털에서 받은 인증키
#  1. pageNo     : 페이지 번호
#  2. numOfRows  : 한 페이지 결과 수
#  3. resultType : 구분 (xml, json) (Default: xml)
#  4. basDt      : 검색값과 기준일자가 일치하는 데이터를 검색
#  5. beginBasDt : 기준일자가 검색값보다 크거나 같은 데이터를 검색
#  6. endBasDt   : 기준일자가 검색값보다 작은 데이터를 검색
#  7. likeBasDt  : 기준일자값이 검색값을 포함하는 데이터를 검색
#  8. likeSrtnCd : 단축코드가 검색값을 포함하는 데이터를 검색
#  9. isinCd     : 검색값과 ISIN코드이 일치하는 데이터를 검색
# 10. likeIsinCd : ISIN코드가 검색값을 포함하는 데이터를 검색
# 11. itmsNm     : 검색값과 종목명이 일치하는 데이터를 검색
# 12. likeItmsNm : 종목명이 검색값을 포함하는 데이터를 검색
# 13. crno       : 검색값과 법인등록번호가 일치하는 데이터를 검색
# 14. corpNm     : 검색값과 법인명이 일치하는 데이터를 검색
# 15. likeCorpNm : 법인명이 검색값을 포함하는 데이터를 검색

# [Query Outputs]
#  0. resultCode (str) : 결과코드
#  1. resultMsg  (str) : 결과메시지
#  2. numOfRows  (int) : 한 페이지 결과 수
#  3. pageNo     (int) : 페이지번호
#  4. totalCount (int) : 전체 결과 수
#  5. basDt      (str) : YYYYMMDD, 조회의 기준일, 통상 거래일
#  6. srtnCd     (str) : 종목 코드보다 짧으면서 유일성이 보장되는 코드
#  7. isinCd     (str) : 현선물 통합상품의 종목 코드(12자리)
#  8. mrktCtg    (str) : 시장 구분 (KOSPI/KOSDAQ/KONEX 등)
#  9. itmsNm     (str) : 종목의 명칭
# 10. crno       (str) : 종목의 법인등록번호
# 11. corpNm     (str) : 종목의 법인 명칭

import json
import configparser

from dataHandler    import get_data
from datetime       import datetime, timedelta

# # of Maximum Items in Korea Stock Exchange (KOSPI/KOSDAQ/KONEX)
# http://data.krx.co.kr/contents/MDC/MAIN/main/index.cmd
KOSPI_ITEMS  = 938
KOSDAQ_ITEMS = 1575
KONEX_ITEMS  = 125
ALL_ITEMS = str(KOSPI_ITEMS + KOSDAQ_ITEMS + KONEX_ITEMS) 

YESTERDAY = datetime.strftime(datetime.now() - timedelta(1), "%Y%m%d") # Yesterday (Format:"YYYYMMDD")

def getKrxListedInfo():
    
    # Credential Parsing from config.ini
    config = configparser.RawConfigParser()
    config.read("./config.ini", encoding='UTF8')

    # Service URL
    SERVICE_URL = config["URL"]["KRX_LISTED_INFO_SERVICE"] 
    if SERVICE_URL is None:
        raise Exception("[ERROR] Fail to load API URL")

    # Service Key
    SERVICE_KEY = config["KEY"]["KEY_OPENAPI"]     
    if SERVICE_KEY is None:
        raise Exception("[ERROR] Fail to load API Key")

    # Setting Input Parameters
    query_params = {
        "serviceKey" : SERVICE_KEY,
        "pageNo"     : "",
        "numOfRows"  : ALL_ITEMS,
        "resultType" : "json",
        "basDt"      : YESTERDAY,
        "beginBasDt" : "",
        "endBasDt"   : "",
        "likeBasDt"  : "",
        "likeSrtnCd" : "",
        "isinCd"     : "",
        "likeIsinCd" : "",
        "itmsNm"     : "",
        "likeItmsNm" : "",
        "crno"       : "",
        "corpNm"     : "",
        "likeCorpNm" : "",
    }

    # Get data from SERVICE_URL
    response = get_data(service_url = SERVICE_URL, params = query_params)

    # Parsing query output
    header = json.loads(response.text)["response"]["header"]
    resultCode = header["resultCode"]
    resultMsg = header["resultMsg"]

    body = json.loads(response.text)["response"]["body"]
    numOfRows = body["numOfRows"]
    pageNo = body["pageNo"]
    totalCount = body["totalCount"]
    items = body["items"]["item"] # Information of each stock items

    # Logging to Console
    print("Running : krxListedInfo.py")
    print(f"Result Code : {resultCode}")
    print(f"Result Message : {resultMsg}")
    
    print(f"basDt : {YESTERDAY}")
    print(f"numOfRows : {numOfRows}")
    print(f"pageNo : {pageNo}")
    print(f"totalCount : {totalCount}")
    print() # Newline

    # Output processing (to json file)
    # with open("krx_stock_info.json", "w", encoding="utf-8") as json_file:
    #     json_file.write("[") # Start of .json file

    #     for i in range(0, numOfRows): # Iteration for each item
    #         json_file.write("{")
    #         json_file.write('"id":{},'.format(i+1))
    #         json_file.write('"srtnCd":"'  + item[i]["srtnCd"]  + '",')
    #         json_file.write('"isinCd":"'  + item[i]["isinCd"]  + '",')
    #         json_file.write('"itmsNm":"'  + item[i]["itmsNm"]  + '",')
    #         json_file.write('"corpNm":"'  + item[i]["corpNm"]  + '",')
    #         json_file.write('"crno":"'    + item[i]["crno"]    + '",')
    #         json_file.write('"mrktCtg":"' + item[i]["mrktCtg"] + '",')
    #         json_file.write('"basDt":"'   + item[i]["basDt"]   + '"' )
    #         json_file.write("}")

    #         if(i != numOfRows - 1):
    #             json_file.write(",")

    #     json_file.write("]") # End of .json file

    return items
