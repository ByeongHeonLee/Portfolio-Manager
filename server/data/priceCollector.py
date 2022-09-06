
# priceCollector.py
# https://www.data.go.kr (공공데이터포털)

# Author  : Byeong Heon Lee
# Contact : lww7438@gmail.com



# Required Modules
import requests
import json
import xml.etree.ElementTree as ET

from apiConfig   import *
from dataManager import *

# * * *   Functions   * * *
def get_stock_price_info(serviceKey:str, pageNo=1, numOfRows=1, resultType="json", basDt=PREVIOUS_BUSINESS_DAY, beginBasDt="", endBasDt="", likeBasDt="", likeSrtnCd="", isinCd="", likeIsinCd="", itmsNm="", likeItmsNm="", mrktCls="", beginVs="", endVs="", beginFltRt="", endFltRt="", beginTrqu="", endTrqu="", beginTrPrc="", endTrPrc="", beginLstgStCnt="", endLstgStCnt="", beginMrktTotAmt="", endMrktTotAmt=""):
    """
    금융위원회_주식시세정보: 주식시세 검색 결과를 반환한다.
    * 금융위원회_주식시세정보: 주식시세 (https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15094808)
        
    [Parameters]
    serviceKey      (str) : 공공데이터 포털에서 받은 인증키 (Mandatory) 
    pageNo          (int) : 페이지 번호 (Default: 1)
    numOfRows       (int) : 한 페이지 결과 수 (Default: ALL_CORPS (한국 전체 법인 수))
    resultType      (str) : 구분 (xml, json) (Default: json)
    basDt           (str) : 검색값과 기준일자가 일치하는 데이터를 검색 (Default: "")
    beginBasDt      (str) : 기준일자가 검색값보다 크거나 같은 데이터를 검색 (Default: "")
    endBasDt        (str) : 기준일자가 검색값보다 작은 데이터를 검색 (Default: "")
    likeBasDt       (str) : 기준일자값이 검색값을 포함하는 데이터를 검색 (Default: "")
    likeSrtnCd      (str) : 단축코드가 검색값을 포함하는 데이터를 검색 (Default: "")
    isinCd          (str) : 검색값과 ISIN코드이 일치하는 데이터를 검색 (Default: "")
    likeIsinCd      (str) : ISIN코드가 검색값을 포함하는 데이터를 검색 (Default: "")
    itmsNm          (str) : 검색값과 종목명이 일치하는 데이터를 검색 (Default: "")
    likeItmsNm      (str) : 종목명이 검색값을 포함하는 데이터를 검색 (Default: "")
    mrktCls         (str) : 검색값과 시장구분이 일치하는 데이터를 검색 (Default: "")
    beginVs         (str) : 대비가 검색값보다 크거나 같은 데이터를 검색 (Default: "")
    endVs           (str) : 대비가 검색값보다 작은 데이터를 검색 (Default: "")
    beginFltRt      (str) : 등락률이 검색값보다 크거나 같은 데이터를 검색 (Default: "")
    endFltRt        (str) : 등락률이 검색값보다 작은 데이터를 검색 (Default: "")
    beginTrqu       (str) : 거래량이 검색값보다 크거나 같은 데이터를 검색 (Default: "")
    endTrqu         (str) : 거래량이 검색값보다 작은 데이터를 검색 (Default: "")
    beginTrPrc      (str) : 거래대금이 검색값보다 크거나 같은 데이터를 검색 (Default: "")
    endTrPrc        (str) : 거래대금이 검색값보다 작은 데이터를 검색 (Default: "")
    beginLstgStCnt  (str) : 상장주식수가 검색값보다 크거나 같은 데이터를 검색 (Default: "")
    endLstgStCnt    (str) : 상장주식수가 검색값보다 작은 데이터를 검색 (Default: "")
    beginMrktTotAmt (str) : 시가총액이 검색값보다 크거나 같은 데이터를 검색 (Default: "")
    endMrktTotAmt   (str) : 시가총액이 검색값보다 작은 데이터를 검색 (Default: "")

    [Returns]
    item : 한국 주식시장에 상장된 종목들의 주식시세정보 (dict)
        basDt      (string) : 기준일자
        srtnCd     (string) : 종목 코드보다 짧으면서 유일성이 보장되는 코드(6자리)
        isinCd     (string) : 국제 채권 식별 번호. 유가증권(채권)의 국제인증 고유번호
        itmsNm     (string) : 유가증권 국제인증 고유번호 코드 이름
        mrktCtg    (string) : 주식의 시장 구분 (KOSPI/KOSDAQ/KONEX 중 1)
        clpr       (string) : 정규시장의 매매시간종료시까지 형성되는 최종가격
        vs         (number) : 전일 대비 등락
        fltRt      (number) : 전일 대비 등락에 따른 비율
        mkp        (number) : 정규시장의 매매시간개시후 형성되는 최초가격
        hipr       (number) : 하루 중 가격의 최고치
        lopr       (number) : 하루 중 가격의 최저치
        trqu       (number) : 체결수량의 누적 합계
        trPrc      (number) : 거래건 별 체결가격 * 체결수량의 누적 합계
        lstgStCnt  (number) : 종목의 상장주식수
        mrktTotAmt (number) : 종가 * 상장주식수
    """
        
    # Parameter Setting
    query_params_stock_price_info = {
        "serviceKey"      : serviceKey,      # 공공데이터 포털에서 받은 인증키
        "pageNo"          : pageNo,          # 페이지 번호
        "numOfRows"       : numOfRows,       # 한 페이지 결과 수
        "resultType"      : resultType,      # 구분 (xml, json)
        "basDt"           : basDt,           # 검색값과 기준일자가 일치하는 데이터를 검색
        "beginBasDt"      : beginBasDt,      # 기준일자가 검색값보다 크거나 같은 데이터를 검색
        "endBasDt"        : endBasDt,        # 기준일자가 검색값보다 작은 데이터를 검색
        "likeBasDt"       : likeBasDt,       # 기준일자값이 검색값을 포함하는 데이터를 검색
        "likeSrtnCd"      : likeSrtnCd,      # 단축코드가 검색값을 포함하는 데이터를 검색
        "isinCd"          : isinCd,          # 검색값과 ISIN코드이 일치하는 데이터를 검색
        "likeIsinCd"      : likeIsinCd,      # ISIN코드가 검색값을 포함하는 데이터를 검색
        "itmsNm"          : itmsNm,          # 검색값과 종목명이 일치하는 데이터를 검색
        "likeItmsNm"      : likeItmsNm,      # 종목명이 검색값을 포함하는 데이터를 검색
        "mrktCls"         : mrktCls,         # 검색값과 시장구분이 일치하는 데이터를 검색
        "beginVs"         : beginVs,         # 대비가 검색값보다 크거나 같은 데이터를 검색
        "endVs"           : endVs,           # 대비가 검색값보다 작은 데이터를 검색
        "beginFltRt"      : beginFltRt,      # 등락률이 검색값보다 크거나 같은 데이터를 검색
        "endFltRt"        : endFltRt,        # 등락률이 검색값보다 작은 데이터를 검색
        "beginTrqu"       : beginTrqu,       # 거래량이 검색값보다 크거나 같은 데이터를 검색
        "endTrqu"         : endTrqu,         # 거래량이 검색값보다 작은 데이터를 검색
        "beginTrPrc"      : beginTrPrc,      # 거래대금이 검색값보다 크거나 같은 데이터를 검색
        "endTrPrc"        : endTrPrc,        # 거래대금이 검색값보다 작은 데이터를 검색
        "beginLstgStCnt"  : beginLstgStCnt,  # 상장주식수가 검색값보다 크거나 같은 데이터를 검색
        "endLstgStCnt"    : endLstgStCnt,    # 상장주식수가 검색값보다 작은 데이터를 검색
        "beginMrktTotAmt" : beginMrktTotAmt, # 시가총액이 검색값보다 크거나 같은 데이터를 검색
        "endMrktTotAmt"   : endMrktTotAmt    # 시가총액이 검색값보다 작은 데이터를 검색
    }

    # Request
    response_stock_price_info = requests.get(set_query_url(service_url=URL_STOCK_PRICE_INFO, params=query_params_stock_price_info))

    # Parsing
    header = json.loads(response_stock_price_info.text)["response"]["header"]
    body = json.loads(response_stock_price_info.text)["response"]["body"]
    item = body["items"]["item"] # Information of each stock item

    # Assertion
    if len(item) == 0:
        return None

    # Print Result to Console (Logging)
    print("Running: Get Stock Price Info")
    print("Result Code : %s" % header["resultCode"])   # 결과코드
    print("Result Message : %s" % header["resultMsg"]) # 결과메시지 
    print("numOfRows : %d" % body["numOfRows"])        # 한 페이지 결과 수
    print("pageNo : %d" % body["pageNo"])              # 페이지번호
    print("totalCount : %d" % body["totalCount"])      # 전체 결과 수
    print() # Newline

    return item

def get_stock_market_index(serviceKey:str, pageNo=1, numOfRows=1, resultType="json", basDt="", beginBasDt="", endBasDt="", likeBasDt="", idxNm="", likeIdxNm="", beginEpyItmsCnt="", endEpyItmsCnt="", beginFltRt="", endFltRt="", beginTrqu="", endTrqu="", beginTrPrc="", endTrPrc="", beginLstgMrktTotAmt="", endLstgMrktTotAmt="", beginLsYrEdVsFltRg="", endLsYrEdVsFltRg="", beginLsYrEdVsFltRt="", endLsYrEdVsFltRt=""):
    """
    금융위원회_지수시세정보: 주가지수시세 검색 결과를 반환한다.
    * 금융위원회_지수시세정보: 주가지수시세 (https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15094807)
        
    [Parameters]
    serviceKey          (str) : 공공데이터 포털에서 받은 인증키 (Mandatory) 
    pageNo              (int) : 페이지 번호 (Default: 1)
    numOfRows           (int) : 한 페이지 결과 수 (Default: ALL_CORPS (한국 전체 법인 수))
    resultType          (str) : 구분 (xml, json) (Default: json)
    basDt               (str) : 검색값과 기준일자가 일치하는 데이터를 검색 (Default: "")
    beginBasDt          (str) : 기준일자가 검색값보다 크거나 같은 데이터를 검색 (Default: "")
    endBasDt            (str) : 기준일자가 검색값보다 작은 데이터를 검색 (Default: "")
    likeBasDt           (str) : 기준일자값이 검색값을 포함하는 데이터를 검색 (Default: "")
    idxNm               (str) : 검색값과 지수명이 일치하는 데이터를 검색
    likeIdxNm           (str) : 지수명이 검색값을 포함하는 데이터를 검색
    beginEpyItmsCnt     (str) : 채용종목수가 검색값보다 크거나 같은 데이터를 검색
    endEpyItmsCnt       (str) : 채용종목수가 검색값보다 작은 데이터를 검색
    beginFltRt          (str) : 등락률이 검색값보다 크거나 같은 데이터를 검색
    endFltRt            (str) : 등락률이 검색값보다 작은 데이터를 검색
    beginTrqu           (str) : 거래량이 검색값보다 크거나 같은 데이터를 검색
    endTrqu             (str) : 거래량이 검색값보다 작은 데이터를 검색
    beginTrPrc          (str) : 거래대금이 검색값보다 크거나 같은 데이터를 검색
    endTrPrc            (str) : 거래대금이 검색값보다 작은 데이터를 검색
    beginLstgMrktTotAmt (str) : 상장시가총액이 검색값보다 크거나 같은 데이터를 검색
    endLstgMrktTotAmt   (str) : 상장시가총액이 검색값보다 작은 데이터를 검색
    beginLsYrEdVsFltRg  (str) : 전년말대비_등락폭이 검색값보다 크거나 같은 데이터를 검색
    endLsYrEdVsFltRg    (str) : 전년말대비_등락폭이 검색값보다 작은 데이터를 검색
    beginLsYrEdVsFltRt  (str) : 전년말대비_등락률이 검색값보다 크거나 같은 데이터를 검색
    endLsYrEdVsFltRt    (str) : 전년말대비_등락률이 검색값보다 작은 데이터를 검색

    [Returns]
    item : 주가지수시세에 대한 정보 (dict)
        lsYrEdVsFltRt  (number) : 지수의 전년말대비 등락율
        basPntm        (string) : 지수를 산출하기 위한 기준시점
        basIdx         (number) : 기준시점의 지수값
        basDt          (string) : 기준일자
        idxCsf         (string) : 지수의 분류명칭
        idxNm          (string) : 지수의 명칭
        epyItmsCnt     (number) : 지수가 채용한 종목 수
        clpr           (number) : 정규시장의 매매시간종료시까지 형성되는 최종가격
        vs             (number) : 전일 대비 등락
        fltRt          (number) : 전일 대비 등락에 따른 비율
        mkp            (number) : 정규시장의 매매시간개시후 형성되는 최초가격
        hipr           (number) : 하루 중 지수의 최고치
        lopr           (number) : 하루 중 지수의 최저치
        trqu           (number) : 지수에 포함된 종목의 거래량 총합
        trPrc          (number) : 지수에 포함된 종목의 거래대금 총합
        lstgMrktTotAmt (number) : 지수에 포함된 종목의 시가총액
        lsYrEdVsFltRg  (number) : 지수의 전년말대비 등락폭
        yrWRcrdHgst    (number) : 지수의 연중최고치
        yrWRcrdHgstDt  (string) : 지수가 연중최고치를 기록한 날짜
        yrWRcrdLwst    (number) : 지수의 연중최저치
        yrWRcrdLwstDt  (string) : 지수가 연중최저치를 기록한 날짜
    """

    # Parameter Setting
    query_params_stock_market_index = {
        "serviceKey"          : serviceKey,          # 공공데이터 포털에서 받은 인증키 (Mandatory) 
        "pageNo"              : pageNo,              # 페이지 번호 (Default: 1)
        "numOfRows"           : numOfRows,           # 한 페이지 결과 수 (Default: ALL_CORPS (한국 전체 법인 수))
        "resultType"          : resultType,          # 구분 (xml, json) (Default: json)
        "basDt"               : basDt,               # 검색값과 기준일자가 일치하는 데이터를 검색 (Default: "")
        "beginBasDt"          : beginBasDt,          # 기준일자가 검색값보다 크거나 같은 데이터를 검색 (Default: "")
        "endBasDt"            : endBasDt,            # 기준일자가 검색값보다 작은 데이터를 검색 (Default: "")
        "likeBasDt"           : likeBasDt,           # 기준일자값이 검색값을 포함하는 데이터를 검색 (Default: "")
        "idxNm"               : idxNm,               # 검색값과 지수명이 일치하는 데이터를 검색
        "likeIdxNm"           : likeIdxNm,           # 지수명이 검색값을 포함하는 데이터를 검색
        "beginEpyItmsCnt"     : beginEpyItmsCnt,     # 채용종목수가 검색값보다 크거나 같은 데이터를 검색
        "endEpyItmsCnt"       : endEpyItmsCnt,       # 채용종목수가 검색값보다 작은 데이터를 검색
        "beginFltRt"          : beginFltRt,          # 등락률이 검색값보다 크거나 같은 데이터를 검색
        "endFltRt"            : endFltRt,            # 등락률이 검색값보다 작은 데이터를 검색
        "beginTrqu"           : beginTrqu,           # 거래량이 검색값보다 크거나 같은 데이터를 검색
        "endTrqu"             : endTrqu,             # 거래량이 검색값보다 작은 데이터를 검색
        "beginTrPrc"          : beginTrPrc,          # 거래대금이 검색값보다 크거나 같은 데이터를 검색
        "endTrPrc"            : endTrPrc,            # 거래대금이 검색값보다 작은 데이터를 검색
        "beginLstgMrktTotAmt" : beginLstgMrktTotAmt, # 상장시가총액이 검색값보다 크거나 같은 데이터를 검색
        "endLstgMrktTotAmt"   : endLstgMrktTotAmt,   # 상장시가총액이 검색값보다 작은 데이터를 검색
        'beginLsYrEdVsFltRg'  : beginLsYrEdVsFltRg,  # 전년말대비_등락폭이 검색값보다 크거나 같은 데이터를 검색
        "endLsYrEdVsFltRg"    : endLsYrEdVsFltRg,    # 전년말대비_등락폭이 검색값보다 작은 데이터를 검색
        "beginLsYrEdVsFltRt"  : beginLsYrEdVsFltRt,  # 전년말대비_등락률이 검색값보다 크거나 같은 데이터를 검색
        "endLsYrEdVsFltRt"    : endLsYrEdVsFltRt     # 전년말대비_등락률이 검색값보다 작은 데이터를 검색
    }

    # Request
    response_stock_market_index = requests.get(set_query_url(service_url=URL_STOCK_MARKET_INDEX, params=query_params_stock_market_index))

    # Parsing
    header = json.loads(response_stock_market_index.text)["response"]["header"]
    body = json.loads(response_stock_market_index.text)["response"]["body"]
    item = body["items"]["item"] # Information of each index item

    # Assertion
    if len(item) == 0:
        return None

    # Print Result to Console (Logging)
    print("Running: Get Stock Price Info")
    print("Result Code : %s" % header["resultCode"])   # 결과코드
    print("Result Message : %s" % header["resultMsg"]) # 결과메시지 
    print("numOfRows : %d" % body["numOfRows"])        # 한 페이지 결과 수
    print("pageNo : %d" % body["pageNo"])              # 페이지번호
    print("totalCount : %d" % body["totalCount"])      # 전체 결과 수
    print() # Newline

    return item

def test():

    # Configurations for test
    # serviceKey           ="<your api key>" # 공공데이터포털 서비스키
    serviceKey = "uZEPxYU1hcKy6To5Hex%2ByxoSPBqrjzpFi9DeHCmI3b%2FovyQR3HbAcBQQG1RtKJpp5vRJ7ChiL%2B4HqCwEsXjoJQ%3D%3D"
    samsung_crno         = "1301110006246" # 삼성전자 법인등록번호
    samsung_issucoCustno = "593"           # 삼성전자 발행회사번호
    samsung_shortIsin    = "005930"        # 삼성전자 단축 ISIN 코드

    # result = get_stock_price_info(serviceKey=serviceKey)
    result = get_stock_market_index(serviceKey=serviceKey, idxNm="코스피 200")

    with open("price_data.json", "w", encoding="utf-8") as json_file:
        json_file.write(str(result)) # Write to json file

test()