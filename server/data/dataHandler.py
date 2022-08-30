
# dataHandler.py
# https://www.data.go.kr (공공데이터포털)

# Author  : Byeong Heon Lee
# Contact : lww7438@gmail.com



# Required Modules
import os
from tkinter import CURRENT
import requests
import json
import configparser

from pytz import timezone
from datetime   import datetime, timedelta



# * * *   Date Strings   * * *
YESTERDAY    = datetime.strftime(datetime.now(timezone('Asia/Seoul')) - timedelta(1), "%Y%m%d") # Yesterday (Format:"YYYYMMDD")
TODAY        = datetime.strftime(datetime.now(timezone('Asia/Seoul'))               , "%Y%m%d") # Yesterday (Format:"YYYYMMDD")
TOMORROW     = datetime.strftime(datetime.now(timezone('Asia/Seoul')) + timedelta(1), "%Y%m%d") # Yesterday (Format:"YYYYMMDD")
CURRENT_YEAR = datetime.strftime(datetime.now(timezone('Asia/Seoul'))               , "%Y")     # This year (Format:"YYYY")



# * * *   API URLs   * * *
URL_CORP_OUTLINE      = "http://apis.data.go.kr/1160100/service/GetCorpBasicInfoService/getCorpOutline"          # 금융위원회_기업기본정보: 기업개요조회
URL_STOC_ISSU_STAT    = "http://apis.data.go.kr/1160100/service/GetStocIssuInfoService/getStocIssuStat"          # 금융위원회_주식발행정보: 주식발행현황조회
URL_KRX_LISTED_INFO   = "http://apis.data.go.kr/1160100/service/GetKrxListedInfoService/getItemInfo"             # 금융위원회_KRX상장종목정보
URL_ITEM_BASI_INFO    = "http://apis.data.go.kr/1160100/service/GetStocIssuInfoService/getItemBasiInfo"          # 금융위원회_주식발행정보: 종목기본정보조회
URL_SUMM_FINA_STAT    = "http://apis.data.go.kr/1160100/service/GetFinaStatInfoService/getSummFinaStat"          # 금융위원회_기업 재무정보: 요약재무제표조회
URL_STOCK_PRICE_INFO  = "http://apis.data.go.kr/1160100/service/GetStockSecuritiesInfoService/getStockPriceInfo" # 금융위원회_주식시세정보: 주식시세


# * * *   Contants   * * *
# The number of Maximum Items in Korea Stock Exchange (KOSPI/KOSDAQ/KONEX)
# http://data.krx.co.kr/contents/MDC/MAIN/main/index.cmd
KOSPI_ITEMS  = 939
KOSDAQ_ITEMS = 1579
KONEX_ITEMS  = 125
ALL_ITEMS = KOSPI_ITEMS + KOSDAQ_ITEMS + KONEX_ITEMS

# The number of Maximum Corporations in Korea
ALL_CORPS = 999999999



# * * *   Functions   * * *

def set_query_url(service_url : str, params : dict):

    # Set URL with Parameters
    request_url = service_url + '?'    
    for k, v in params.items():
        request_url += str(k) + '=' + str(v) + '&'

    return request_url[:-1] # Eliminate last '&' character 

def filter_params(data_list:list, params:list):
    filtered_list=[]

    for data in data_list:
        new_dict = dict()

        for k, v in data.items():
            if k in params:
                new_dict[k] = v
            else:
                continue
        
        filtered_list.append(new_dict)

    return filtered_list

def left_join_by_key(ldata:list, rdata:list, key:str):
    merged_list = []

    for data in ldata:
        merged_list.append(data)

    for item in merged_list:
        for data in rdata:
            if item[key] == data[key]:
                for k, v in data.items():
                    item[k] = v

    return merged_list

def get_corp_outline(serviceKey:str, pageNo=1, numOfRows=ALL_CORPS, resultType="json", basDt=YESTERDAY, crno="", corpNm=""):
    """
    금융위원회_기업기본정보_기업개요조회 검색 결과를 반환한다.
    * 금융위원회_기업기본정보_기업개요조회 (https://www.data.go.kr/data/15043184/openapi.do)
        
    [Parameters]
    serviceKey (str) : 공공데이터 포털에서 받은 인증키 (Mandatory) 
    pageNo     (int) : 페이지 번호 (Default: 1)
    numOfRows  (int) : 한 페이지 결과 수 (Default: ALL_CORPS (한국 전체 법인 수))
    resultType (str) : 구분 (xml, json) (Default: json)
    basDt      (str) : 검색값과 기준일자가 일치하는 데이터를 검색 (Default: "")
    crno       (str) : 법인등록번호 (Default: "")
    corpNm     (str) : 법인의 명칭 (Default: "")

    [Returns]
    item : 한국 주식시장에 상장된 종목들의 기업개요정보 (dict)
         0. resultCode          (str) : 결과코드
         1. resultMsg           (str) : 결과메시지
         2. numOfRows           (int) : 한 페이지 결과 수
         3. pageNo              (int) : 페이지 번호
         4. totalCount          (int) : 전체 결과 수
         5. basDt               (str) : 기준일자 (YYYYMMDD)
         6. crno                (str) : 법인등록번호
         7. corpNm              (str) : 법인명
         8. corpEnsnNm          (str) : 법인영문명
         9. enpPbanCmpyNm       (str) : 기업공시회사명
        10. enpRprFnm           (str) : 기업대표자성명
        11. corpRegMrktDcd      (str) : 법인등록시장구분코드
        12. corpRegMrktDcdNm    (str) : 법인등록시장구분코드명
        13. corpDcd             (str) : 법인구분코드
        14. corpDcdNm           (str) : 법인구분코드명
        15. bzno                (str) : 사업자등록번호
        16. enpOzpno            (str) : 기업구우편번호
        17. enpBsadr            (str) : 기업기본주소
        18. enpDtadr            (str) : 기업상세주소
        19. enpHmpgUrl          (str) : 기업홈페이지URL
        20. enpTlno             (str) : 기업전화번호
        21. enpFxno             (str) : 기업팩스번호
        22. sicNm               (str) : 표준산업분류명
        23. enpEstbDt           (str) : 기업설립일자
        24. enpStacMm           (str) : 기업결산월
        25. enpXchgLstgDt       (str) : 기업거래소상장일자
        26. enpXchgLstgAbolDt   (str) : 기업거래소상장폐지일자
        27. enpKosdaqLstgDt     (str) : 기업코스닥상장일자
        28. enpKosdaqLstgAbolDt (str) : 기업코스닥상장폐지일자
        29. enpKrxLstgDt        (str) : 기업KONEX상장일자
        30. enpKrxLstgAbolDt    (str) : 기업KONEX상장폐지일자
        31. smenpYn             (str) : 중소기업여부
        32. enpMntrBnkNm        (str) : 기업주거래은행명
        33. enpEmpeCnt          (str) : 기업종업원수
        34. empeAvgCnwkTermCtt  (str) : 종업원평균근속기간내용
        35. enpPn1AvgSlryAmt    (str) : 기업1인평균급여금액
        36. actnAudpnNm         (str) : 회계감사인명
        37. audtRptOpnnCtt      (str) : 감사보고서의견내용
        38. enpMainBizNm        (str) : 기업주요사업명
        39. fssCorpUnqNo        (str) : 금융감독원법인고유번호
        40. fssCorpChgDtm       (str) : 금융감독원법인변경일시     
    """
    
    # Parameter Setting
    query_params_corp_outline = {
        "serviceKey" : serviceKey, # 공공데이터 포털에서 받은 인증키
        "pageNo"     : pageNo,     # 페이지 번호
        "numOfRows"  : numOfRows,  # 한 페이지 결과 수
        "resultType" : resultType, # 구분 (xml, json) (Default: json)
        "basDt"      : basDt,      # 검색값과 기준일자가 일치하는 데이터를 검색
        "crno"       : crno,       # 법인등록번호
        "corpNm"     : corpNm      # 법인의 명칭
    }

    # Request
    response_corp_outline = requests.get(set_query_url(service_url=URL_CORP_OUTLINE, params=query_params_corp_outline))

    # Parsing
    header = json.loads(response_corp_outline.text)["response"]["header"]
    body = json.loads(response_corp_outline.text)["response"]["body"]
    item = body["items"]["item"] # Information of each corporation
    
    # Print Result to Console
    print("Running: Get Corp Outline")
    print("Result Code : %s" % header["resultCode"])   # 결과코드
    print("Result Message : %s" % header["resultMsg"]) # 결과메시지 
    print("numOfRows : %d" % body["numOfRows"])        # 한 페이지 결과 수
    print("pageNo : %d" % body["pageNo"])              # 페이지번호
    print("totalCount : %d" % body["totalCount"])      # 전체 결과 수
    print() # Newline

    return item

def get_stoc_issu_stat(serviceKey:str, pageNo=1, numOfRows=ALL_ITEMS, resultType="json", basDt=YESTERDAY, crno="", stckIssuCmpyNm=""):
    """
    금융위원회_주식발행정보: 주식발행현황조회 검색 결과를 반환한다.
    * 금융위원회_주식발행정보: 주식발행현황조회 (https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15043423)
        
    [Parameters]
    serviceKey     (str) : 공공데이터 포털에서 받은 인증키 (Mandatory)
    pageNo         (int) : 페이지 번호 (Default: 1)
    numOfRows      (int) : 한 페이지 결과 수 (Default: ALL_ITEMS (한국시장 전체 종목 수))
    resultType     (str) : 구분 (xml, json) (Default: json)
    basDt          (str) : 검색값과 기준일자가 일치하는 데이터를 검색 (Default: "")
    crno           (str) : 검색값과 법인등록번호가 일치하는 데이터를 검색 (Default: "")
    stckIssuCmpyNm (str) : 주식발행회사명이 일치하는 데이터를 검색 (Default: "")

    [Returns]
    item : 한국 주식시장에 상장된 종목들의 기본정보 (dict)
        0. resultCode     (str) : 결과코드
        1. resultMsg      (str) : 결과메시지
        2. numOfRows      (int) : 한 페이지 결과 수
        3. pageNo         (int) : 페이지번호
        4. totalCount     (int) : 전체 결과 수
        5. basDt          (str) : YYYYMMDD, 조회의 기준일, 통상 거래일
        6. crno           (str) : 종목의 법인등록번호
        7. stckIssuCmpyNm (str) : 주식 발행 회사명
        8. onskTisuCnt    (str) : 보통주 총 발행수
        9. pfstTisuCnt    (str) : 우선주 총 발행수
    """
    
    # Parameter Setting
    query_params_stoc_issu_stat = {
        "serviceKey"     : serviceKey,      # 공공데이터 포털에서 받은 인증키
        "pageNo"         : pageNo,          # 페이지 번호
        "numOfRows"      : numOfRows,       # 한 페이지 결과 수
        "resultType"     : resultType,      # 구분 (xml, json) (Default: xml)
        "basDt"          : basDt,           # 검색값과 기준일자가 일치하는 데이터를 검색
        "crno"           : crno,            # 검색값과 법인등록번호가 일치하는 데이터를 검색 
        "stckIssuCmpyNm" : stckIssuCmpyNm   # 주식발행회사명이 일치하는 데이터를 검색
    }

    # Request
    response_stoc_issu_stat = requests.get(set_query_url(service_url=URL_STOC_ISSU_STAT, params=query_params_stoc_issu_stat))

    # Parsing
    header = json.loads(response_stoc_issu_stat.text)["response"]["header"]
    body = json.loads(response_stoc_issu_stat.text)["response"]["body"]
    item = body["items"]["item"] # Information of each stock items
    
    # Print Result to Console
    print("Running: Get Stoc Issu Stat")
    print("Result Code : %s" % header["resultCode"])   # 결과코드
    print("Result Message : %s" % header["resultMsg"]) # 결과메시지 
    print("numOfRows : %d" % body["numOfRows"])        # 한 페이지 결과 수
    print("pageNo : %d" % body["pageNo"])              # 페이지번호
    print("totalCount : %d" % body["totalCount"])      # 전체 결과 수
    print() # Newline

    return item

def get_krx_listed_info(serviceKey:str, pageNo=1, numOfRows=ALL_ITEMS, resultType="json", basDt=YESTERDAY, beginBasDt="", endBasDt="", likeBasDt="", likeSrtnCd="", isinCd="", likeIsinCd="", itmsNm="", likeItmsNm="", crno="", corpNm="", likeCorpNm=""):
    """
    금융위원회_KRX상장종목정보 검색 결과를 반환한다.
    * 금융위원회_KRX상장종목정보 (https://www.data.go.kr/data/15094775/openapi.do)
        
    [Parameters]
    serviceKey (str) : 공공데이터 포털에서 받은 인증키 (Mandatory)
    pageNo     (int) : 페이지 번호 (Default: 1)
    numOfRows  (int) : 한 페이지 결과 수 (Default: ALL_ITEMS (한국시장 전체 종목 수))
    resultType (str) : 구분 (xml, json) (Default: json)
    basDt      (str) : 검색값과 기준일자가 일치하는 데이터를 검색 (Default: "")
    beginBasDt (str) : 기준일자가 검색값보다 크거나 같은 데이터를 검색 (Default: "")
    endBasDt   (str) : 기준일자가 검색값보다 작은 데이터를 검색 (Default: "")
    likeBasDt  (str) : 기준일자값이 검색값을 포함하는 데이터를 검색 (Default: "")
    likeSrtnCd (str) : 단축코드가 검색값을 포함하는 데이터를 검색 (Default: "")
    isinCd     (str) : 검색값과 ISIN코드이 일치하는 데이터를 검색 (Default: "")
    likeIsinCd (str) : ISIN코드가 검색값을 포함하는 데이터를 검색 (Default: "")
    itmsNm     (str) : 검색값과 종목명이 일치하는 데이터를 검색 (Default: "")
    likeItmsNm (str) : 종목명이 검색값을 포함하는 데이터를 검색 (Default: "")
    crno       (str) : 검색값과 법인등록번호가 일치하는 데이터를 검색 (Default: "")
    corpNm     (str) : 검색값과 법인명이 일치하는 데이터를 검색 (Default: "")
    likeCorpNm (str) : 법인명이 검색값을 포함하는 데이터를 검색 (Default: "")

    [Returns]
    item : 한국 주식시장에 상장된 종목들의 기본정보 (dict)
        0. resultCode (str) : 결과코드
        1. resultMsg  (str) : 결과메시지
        2. numOfRows  (int) : 한 페이지 결과 수
        3. pageNo     (int) : 페이지번호
        4. totalCount (int) : 전체 결과 수
        5. basDt      (str) : YYYYMMDD, 조회의 기준일, 통상 거래일
        6. srtnCd     (str) : 종목 코드보다 짧으면서 유일성이 보장되는 코드
        7. isinCd     (str) : 현선물 통합상품의 종목 코드(12자리)
        8. mrktCtg    (str) : 시장 구분 (KOSPI/KOSDAQ/KONEX 등)
        9. itmsNm     (str) : 종목의 명칭
        10. crno      (str) : 종목의 법인등록번호
        11. corpNm    (str) : 종목의 법인 명칭
    """
    
    # Parameter Setting
    query_params_krx_listed_info = {
        "serviceKey" : serviceKey,  # 공공데이터 포털에서 받은 인증키
        "pageNo"     : pageNo,      # 페이지 번호
        "numOfRows"  : numOfRows,   # 한 페이지 결과 수
        "resultType" : resultType,  # 구분 (xml, json) (Default: xml)
        "basDt"      : basDt,       # 검색값과 기준일자가 일치하는 데이터를 검색
        "beginBasDt" : beginBasDt,  # 기준일자가 검색값보다 크거나 같은 데이터를 검색
        "endBasDt"   : endBasDt,    # 기준일자가 검색값보다 작은 데이터를 검색
        "likeBasDt"  : likeBasDt,   # 기준일자값이 검색값을 포함하는 데이터를 검색
        "likeSrtnCd" : likeSrtnCd,  # 단축코드가 검색값을 포함하는 데이터를 검색
        "isinCd"     : isinCd,      # 검색값과 ISIN코드이 일치하는 데이터를 검색
        "likeIsinCd" : likeIsinCd,  # ISIN코드가 검색값을 포함하는 데이터를 검색
        "itmsNm"     : itmsNm,      # 검색값과 종목명이 일치하는 데이터를 검색
        "likeItmsNm" : likeItmsNm,  # 종목명이 검색값을 포함하는 데이터를 검색
        "crno"       : crno,        # 검색값과 법인등록번호가 일치하는 데이터를 검색 
        "corpNm"     : corpNm,      # 검색값과 법인명이 일치하는 데이터를 검색
        "likeCorpNm" : likeCorpNm,  # 법인명이 검색값을 포함하는 데이터를 검색
    }

    # Request
    response_krx_listed_info = requests.get(set_query_url(service_url=URL_KRX_LISTED_INFO, params=query_params_krx_listed_info))

    # Parsing
    header = json.loads(response_krx_listed_info.text)["response"]["header"]
    body = json.loads(response_krx_listed_info.text)["response"]["body"]
    item = body["items"]["item"] # Information of each stock items
    
    # Print Result to Console
    print("Running: Get KRX Listed Info")
    print("Result Code : %s" % header["resultCode"])   # 결과코드
    print("Result Message : %s" % header["resultMsg"]) # 결과메시지 
    print("numOfRows : %d" % body["numOfRows"])        # 한 페이지 결과 수
    print("pageNo : %d" % body["pageNo"])              # 페이지번호
    print("totalCount : %d" % body["totalCount"])      # 전체 결과 수
    print() # Newline

    # Print Result to JSON File
    # with open("krx_listed_info.json", "w", encoding="utf-8") as json_file:
    #     json_file.write("[") # Start of .json file
    #     totalCount = body["totalCount"]
    #     for i in range(0, totalCount): # Iteration for each item
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

    return item

def get_item_basi_info(serviceKey:str, pageNo=1, numOfRows=ALL_ITEMS, resultType="json", basDt=YESTERDAY, crno="", corpNm="", stckIssuCmpyNm=""):
    """
    금융위원회_주식발행정보: 종목기본정보조회 검색 결과를 반환한다.
    * 금융위원회_KRX상장종목정보 (https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15043423)
        
    [Parameters]
    serviceKey     (str) : 공공데이터 포털에서 받은 인증키 (Mandatory)
    pageNo         (int) : 페이지 번호 (Default: 1)
    numOfRows      (int) : 한 페이지 결과 수 (Default: ALL_ITEMS (한국시장 전체 종목 수))
    resultType     (str) : 구분 (xml, json) (Default: json)
    basDt          (str) : 검색값과 기준일자가 일치하는 데이터를 검색 (Default: YESTERDAY)
    crno           (str) : 검색값과 법인등록번호가 일치하는 데이터를 검색 (Default: "")
    corpNm         (str) : 검색값과 법인명이 일치하는 데이터를 검색 (Default: "")
    stckIssuCmpyNm (str) : 주식발행회사명이 검색값을 포함하는 데이터를 검색 (Default: "")

    [Returns]
    item : 한국 주식시장에 상장된 종목들의 기본정보 (dict)
        0. resultCode      (str) : 결과코드
        1. resultMsg       (str) : 결과메시지
        2. numOfRows       (int) : 한 페이지 결과 수
        3. pageNo          (int) : 페이지번호
        4. totalCount      (int) : 전체 결과 수
        5. basDt           (str) : YYYYMMDD, 조회의 기준일, 통상 거래일
        6. crno            (str) : 종목의 법인등록번호
        7. isinCd          (str) : ISIN코드
        8. stckIssuCmpyNm  (str) : 주식발행회사명
        9. isinCdNm        (str) : ISIN코드명
        10. scrsItmsKcd    (str) : 유가증권종목종류코드
        11. scrsItmsKcdNm  (str) : 유가증권종목종류코드명
        12. stckParPrc     (str) : 주식액면가
        13. issuStckCnt    (str) : 발행주식수
        14. lstgDt         (str) : 상장일자
        15. lstgAbolDt     (str) : 상장폐지일자
        16. dpsgRegDt      (str) : 예탁등록일자
        17. dpsgCanDt      (str) : 예탁취소일자
        18. issuFrmtClsfNm (str) : 발행형태구분명
    """

    # Parameter Setting
    query_params_item_basi_info = {
        "serviceKey"     : serviceKey,    # 공공데이터 포털에서 받은 인증키
        "pageNo"         : pageNo,        # 페이지 번호
        "numOfRows"      : numOfRows,     # 한 페이지 결과 수
        "resultType"     : resultType,    # 구분 (xml, json) (Default: xml)
        "basDt"          : basDt,         # 검색값과 기준일자가 일치하는 데이터를 검색
        "crno"           : crno,          # 법인등록번호
        "corpNm"         : corpNm,        # 법인의 명칭
        "stckIssuCmpyNm" : stckIssuCmpyNm # 주식발행회사명
    }

    # Request
    response_item_basi_info = requests.get(set_query_url(service_url=URL_ITEM_BASI_INFO, params=query_params_item_basi_info))

    # Parsing
    header = json.loads(response_item_basi_info.text)["response"]["header"]
    body = json.loads(response_item_basi_info.text)["response"]["body"]
    item = body["items"]["item"] # Information of each corporation
    
    # Print Result to Console
    print("Running: Get Item Basi Info")
    print("Result Code : %s" % header["resultCode"])   # 결과코드
    print("Result Message : %s" % header["resultMsg"]) # 결과메시지 
    print("numOfRows : %d" % body["numOfRows"])        # 한 페이지 결과 수
    print("pageNo : %d" % body["pageNo"])              # 페이지번호
    print("totalCount : %d" % body["totalCount"])      # 전체 결과 수
    print() # Newline

    return item

def get_summ_fina_stat(serviceKey:str, pageNo=1, numOfRows=ALL_CORPS, resultType="json", crno="", bizYear="2021", type="ALL"):
    """
    금융위원회_기업 재무정보: 요약재무제표조회 검색 결과를 반환한다.
    * 금융위원회_기업 재무정보: 요약재무제표조회 (https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15043459)
        
    [Parameters]
    0. serviceKey (str) : 공공데이터 포털에서 받은 인증키 (Mandatory) 
    1. pageNo     (int) : 페이지 번호 (Default: 1)
    2. numOfRows  (int) : 한 페이지 결과 수 (Default: ALL_CORPS (한국 전체 법인 수))
    3. resultType (str) : 구분 (xml, json) (Default: json)
    4. crno       (str) : 법인등록번호 (Default: "")
    5. bizYear    (str) : 사업연도 (Default: "")
    6. type       (str) : 재무제표 유형 (전체: "ALL", 연결: "CONSOLIDATED", 요약: "SEPARATE") (Default: ALL)

    [Returns]
    item : 한국 주식시장에 상장된 종목들의 기업개요정보 (dict)
         0. resultCode    (str) : 결과코드
         1. resultMsg     (str) : 결과메시지
         2. numOfRows     (int) : 한 페이지 결과 수
         3. pageNo        (int) : 페이지 번호
         4. totalCount    (int) : 전체 결과 수
         5. basDt         (str) : 기준일자 (YYYYMMDD)
         6. crno          (str) : 법인등록번호
         7. bizYear       (str) : 사업연도
         8. fnclDcd       (str) : 재무제표구분코드
         9. fnclDcdNm     (str) : 재무제표구분코드명
        10. enpSaleAmt    (str) : 기업매출금액
        11. enpBzopPft    (str) : 기업영업이익
        12. iclsPalClcAmt (str) : 포괄손익계산금액
        13. enpCrtmNpf    (str) : 기업당기순이익
        14. enpTastAmt    (str) : 기업총자산금액
        15. enpTdbtAmt    (str) : 기업총부채금액
        16. enpTcptAmt    (str) : 기업총자본금액
        17. enpCptlAmt    (str) : 기업자본금액
        18. fnclDebtRto   (str) : 재무제표부채비율  
    """
        
    # Parameter Setting
    query_params_summ_fina_stat = {
        "serviceKey" : serviceKey, # 공공데이터 포털에서 받은 인증키
        "pageNo"     : pageNo,     # 페이지 번호
        "numOfRows"  : numOfRows,  # 한 페이지 결과 수
        "resultType" : resultType, # 구분 (xml, json) (Default: xml)
        "crno"       : crno,       # 법인등록번호
        "bizYear"    : bizYear     # 사업연도
    }
    
    # Request
    response_summ_fina_stat = requests.get(set_query_url(service_url=URL_SUMM_FINA_STAT, params=query_params_summ_fina_stat))

    # Parsing
    header = json.loads(response_summ_fina_stat.text)["response"]["header"]
    body = json.loads(response_summ_fina_stat.text)["response"]["body"]
    item = body["items"]["item"] # Information of each corporation
    
    # Print Result to Console (Logging)
    print("Running: Get Summ Fina Stat")
    print("Result Code : %s" % header["resultCode"])   # 결과코드
    print("Result Message : %s" % header["resultMsg"]) # 결과메시지 
    print("numOfRows : %d" % body["numOfRows"])        # 한 페이지 결과 수
    print("pageNo : %d" % body["pageNo"])              # 페이지번호
    print("totalCount : %d" % body["totalCount"])      # 전체 결과 수
    print() # Newline

    
    # To Distinguish between Types of Financial Statements (ALL, CONSOLIDATED, SEPARATE)
    result = []

    if type == "CONSOLIDATED":
        for data in item:
            if data["fnclDcd"] in ["110", "ifrs_ConsolidatedMember", "999"]:
                result.append(data)
                
    elif type == "SEPARATE":
        for data in item:
            if data["fnclDcd"] in ["120", "ifrs_SeparateMember", "999"]:
                result.append(data)

    else: # Default is "ALL"
        return item
    
    return result

def get_stock_price_info(serviceKey:str, pageNo=1, numOfRows=ALL_ITEMS, resultType="json", basDt="20220826", beginBasDt="", endBasDt="", likeBasDt="", likeSrtnCd="", isinCd="", likeIsinCd="", itmsNm="", likeItmsNm="", mrktCls="", beginVs="", endVs="", beginFltRt="", endFltRt="", beginTrqu="", endTrqu="", beginTrPrc="", endTrPrc="", beginLstgStCnt="", endLstgStCnt="", beginMrktTotAmt="", endMrktTotAmt=""):
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

    # Print Result to Console (Logging)
    print("Running: Get Stock Price Info")
    print("Result Code : %s" % header["resultCode"])   # 결과코드
    print("Result Message : %s" % header["resultMsg"]) # 결과메시지 
    print("numOfRows : %d" % body["numOfRows"])        # 한 페이지 결과 수
    print("pageNo : %d" % body["pageNo"])              # 페이지번호
    print("totalCount : %d" % body["totalCount"])      # 전체 결과 수
    print() # Newline

    return item

def get_stock_index_kr():
    pass

def get_financial_data_kr(serviceKey:str):
    financial_data = []
    key = "crno"

    # 금융위원회_KRX상장종목정보
    list_krx_listed_info = get_krx_listed_info(serviceKey=serviceKey)
    list_krx_listed_info = filter_params(list_krx_listed_info, ["srtnCd", "isinCd", "mrktCtg", "itmsNm", "crno", "corpNm"])

    # 금융위원회_기업기본정보: 기업개요조회
    list_corp_outline = get_corp_outline(serviceKey=serviceKey)
    list_corp_outline = filter_params(list_corp_outline, ["crno", "corpNm", "corpEnsnNm", "corpRegMrktDcd", "corpRegMrktDcdNm", "corpDcd", "corpDcdNm", "bzno", "enpHmpgUrl", "sicNm", "enpEstbDt", "smenpYn", "enpEmpeCnt", "empeAvgCnwkTermCtt", "enpPn1AvgSlryAmt"])
    financial_data.append(left_join_by_key(list_krx_listed_info, list_corp_outline, "crno"))

    # 금융위원회_주식발행정보: 주식발행현황조회
    list_stoc_issu_stat = get_stoc_issu_stat(serviceKey=serviceKey)
    list_stoc_issu_stat = filter_params(list_stoc_issu_stat, ["crno", "stckIssuCmpyNm", "onskTisuCnt", "pfstTisuCnt"])
    financial_data = left_join_by_key(list_krx_listed_info, list_stoc_issu_stat, "crno")

    # 금융위원회_주식발행정보: 종목기본정보조회
    list_item_basi_info = get_item_basi_info(serviceKey=serviceKey)
    list_item_basi_info = filter_params(list_item_basi_info, ["crno", "isinCd", "stckIssuCmpyNm", "isinCdNm", "scrsItmsKcd", "scrsItmsKcdNm", "stckParPrc", "issuStckCnt", "lstgDt"])
    financial_data = left_join_by_key(list_krx_listed_info, list_item_basi_info, "crno")

    # 금융위윈회_기업 재무정보: 요약재무제표조회
    list_summ_fina_stat = get_summ_fina_stat(serviceKey=serviceKey, type="SEPARATE")
    list_summ_fina_stat = filter_params(list_summ_fina_stat, ["crno", "bizYear", "fnclDcd", "fnclDcdNm", "enpSaleAmt", "enpBzopPft", "iclsPalClcAmt", "enpCrtmNpf", "enpTastAmt", "enpTdbtAmt", "enpTcptAmt", "enpCptlAmt", "fnclDebtRto"])
    financial_data = left_join_by_key(list_krx_listed_info, list_summ_fina_stat, "crno")

    return financial_data

def get_financial_data_us():
    pass

def test():
    serviceKey="<your service key>"

    # result = get_krx_listed_info(serviceKey)
    # result = get_corp_outline(serviceKey)
    # result = get_stoc_issu_stat(serviceKey)
    # result = get_item_basi_info(serviceKey)
    # result = get_summ_fina_stat(serviceKey=serviceKey, type="CONSOLIDATED")
    # result = get_financial_data_kr(serviceKey)

    result = get_stock_price_info(serviceKey=serviceKey)

    with open("test.json", "w", encoding="utf-8") as json_file:
        json_file.write(str(result)) # Start of .json file
