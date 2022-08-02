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

import requests
import pprint
import json
import configparser

URL = "http://apis.data.go.kr/1160100/service/GetKrxListedInfoService/getItemInfo?serviceKey={0}&pageNo={1}&numOfRows={2}&resultType={3}&basDt={4}&beginBasDt={5}&endBasDt={6}&likeBasDt={7}&likeSrtnCd={8}&isinCd={9}&likeIsinCd={10}&itmsNm={11}&likeItmsNm={12}&crno={13}&corpNm={14}&likeCorpNm={15}"

# Authentication Key Parsing from config.ini
config = configparser.ConfigParser()
config.read('config/config.ini', encoding='utf-8-sig')
SERVICE_KEY = config['KEY']['OPEN_API_KEY']

# The number of stock items on Korea Stock Exchange Market
KOSPI_ITEMS  = 941
KOSDAQ_ITEMS = 1569
KONEX_ITEMS  = 123

# Setting Input Parameters
serviceKey = SERVICE_KEY
pageNo     = ""
numOfRows  = KOSPI_ITEMS + KOSDAQ_ITEMS + KONEX_ITEMS
resultType = "json"
basDt      = ""
beginBasDt = ""
endBasDt   = ""
likeBasDt  = ""
likeSrtnCd = ""
isinCd     = ""
likeIsinCd = ""
itmsNm     = ""
likeItmsNm = ""
crno       = ""
corpNm     = ""
likeCorpNm = ""

# Request Query
response = requests.get(URL.format(serviceKey, pageNo, numOfRows, resultType, basDt, beginBasDt, endBasDt, likeBasDt, likeSrtnCd, isinCd, likeIsinCd, itmsNm, likeItmsNm, crno, corpNm, likeCorpNm))

# Parsing query output
header = json.loads(response.text)["response"]["header"]
body = json.loads(response.text)["response"]["body"]

resultCode = header["resultCode"]
resultMsg = header["resultMsg"]
numOfRows = body["numOfRows"]
pageNo = body["pageNo"]
totalCount = body["totalCount"]

item = body["items"]["item"]

# Output processing (to console for debugging)
print("resultCode : {}", resultCode)
print("numOfRows : {}", numOfRows)
print("pageNo : {}", pageNo)
print("totalCount : {}", totalCount)

# Output processing (to .json file)
with open("krx_stock_info.json", "w", encoding="utf-8") as json_file:
    json_file.write("[") # Start of .json file

    for i in range(0, numOfRows): # Iteration for each item
        json_file.write("{")
        json_file.write('"id":{},'.format(i+1))
        json_file.write('"srtnCd":"'  + item[i]["srtnCd"]  + '",')
        json_file.write('"isinCd":"'  + item[i]["isinCd"]  + '",')
        json_file.write('"itmsNm":"'  + item[i]["itmsNm"]  + '",')
        json_file.write('"corpNm":"'  + item[i]["corpNm"]  + '",')
        json_file.write('"crno":"'    + item[i]["crno"]    + '",')
        json_file.write('"mrktCtg":"' + item[i]["mrktCtg"] + '",')
        json_file.write('"basDt":"'   + item[i]["basDt"]   + '"' )
        json_file.write("}")

        if(i != numOfRows - 1):
            json_file.write(",")

    json_file.write("]") # End of .json file
        