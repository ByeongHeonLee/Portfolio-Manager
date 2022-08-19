
# dataHandler.py
# https://www.data.go.kr (공공데이터포털)

# Author  : Byeong Heon Lee
# Contact : lww7438@gmail.com

import os
import requests
import json
import configparser

from datetime   import datetime, timedelta

# * * *   Date String   * * *
YESTERDAY = datetime.strftime(datetime.now() - timedelta(1), "%Y%m%d") # Yesterday (Format:"YYYYMMDD")

# * * *   API URL   * * *
URL_KRX_LISTED_INFO = "http://apis.data.go.kr/1160100/service/GetKrxListedInfoService/getItemInfo"
URL_CORP_OUTLINE    = "http://apis.data.go.kr/1160100/service/GetCorpBasicInfoService/getCorpOutline"

# * * *   Contants   * * *
# The number of Maximum Items in Korea Stock Exchange (KOSPI/KOSDAQ/KONEX)
# http://data.krx.co.kr/contents/MDC/MAIN/main/index.cmd
KOSPI_ITEMS  = 938
KOSDAQ_ITEMS = 1575
KONEX_ITEMS  = 125
ALL_ITEMS = str(KOSPI_ITEMS + KOSDAQ_ITEMS + KONEX_ITEMS)

def set_query_url(service_url : str, params : dict):

    # Set URL with Parameters
    request_url = service_url + '?'
    for k, v in params.items():
        request_url += str(k) + '=' + str(v) + '&'

    return request_url[:-1] # Eliminate last '&' character 

    # Request Query
    # response = requests.get(request_url[:-1])
    # return response

def merge_by_key(ldata:list, rdata:list, key=None):
    merged_list = []

    for data in ldata:
        merged_list.append(data)

    for item in merged_list:
        for data in rdata:
            if item[key] == data[key]:
                for k, v in data.items():
                    item[k] = v

    return merged_list

def get_krx_listed_info(serviceKey:str, pageNo=1, numOfRows:str="", resultType="json", basDt=YESTERDAY, beginBasDt="", endBasDt="", likeBasDt="", likeSrtnCd="", isinCd="", likeIsinCd="", itmsNm="", likeItmsNm="", crno="", corpNm="", likeCorpNm=""):
    """
    금융위원회_KRX상장종목정보 검색 결과를 반환한다.
    * 금융위원회_KRX상장종목정보 (https://www.data.go.kr/data/15094775/openapi.do)
        
    [Parameters]
    serviceKey (str) : 공공데이터 포털에서 받은 인증키 (Mandatory)
    pageNo     (int) : 페이지 번호 (Default: 1)
    numOfRows  (str) : 한 페이지 결과 수 (Default: "")
    resultType (str) : 구분 (xml, json) (Default: xml)
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

def get_corp_outline(serviceKey:str, pageNo=1, numOfRows="", resultType="json", basDt=YESTERDAY, crno:str="", corpNm:str=""):
    """
    금융위원회_기업기본정보_기업개요조회 검색 결과를 반환한다.
    * 금융위원회_기업기본정보_기업개요조회 (https://www.data.go.kr/data/15043184/openapi.do)
        
    [Parameters]
    0. serviceKey (str) : 공공데이터 포털에서 받은 인증키 (Mandatory) 
    1. pageNo     (int) : 페이지 번호 (Default: 1)
    2. numOfRows  (str) : 한 페이지 결과 수 (Default: "")
    3. resultType (str) : 구분 (xml, json) (Default: xml)
    4. basDt      (str) : 검색값과 기준일자가 일치하는 데이터를 검색 (Default: "")
    5. crno       (str) : 법인등록번호 (Default: "")
    6. corpNm     (str) : 법인의 명칭 (Default: "")

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
        "resultType" : resultType, # 구분 (xml, json) (Default: xml)
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

def get_stock_index_kr():
    pass

def get_financial_data_kr(serviceKey:str):
    list_krx_listed_info = get_krx_listed_info(serviceKey=serviceKey, numOfRows=ALL_ITEMS)
    list_corp_outline    = get_corp_outline(serviceKey=serviceKey, numOfRows=ALL_ITEMS)
    return merge_by_key(ldata=list_krx_listed_info, rdata=list_corp_outline, key="crno")

def get_financial_data_us():
    pass
