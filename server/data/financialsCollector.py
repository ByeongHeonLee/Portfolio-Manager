
# financialsCollector.py
# https://www.data.go.kr (공공데이터포털)

# Author  : Byeong Heon Lee
# Contact : lww7438@gmail.com

# Required Modules
import requests
import xml.etree.ElementTree as ET # XML Parser
import json                        # JSON Parser
import time

from apiConfig      import *
from dataManager    import *
from priceCollector import *

# * * *   Functions   * * *
def get_corp_outline(serviceKey:str, pageNo=1, numOfRows=1, resultType="json", basDt="", crno="", corpNm=""):
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
    item : 한국 주식시장에 상장된 종목들의 기업개요정보 (list of dict)
        basDt               (str) : 기준일자 (YYYYMMDD)
        crno                (str) : 법인등록번호
        corpNm              (str) : 법인명
        corpEnsnNm          (str) : 법인영문명
        enpPbanCmpyNm       (str) : 기업공시회사명
        enpRprFnm           (str) : 기업대표자성명
        corpRegMrktDcd      (str) : 법인등록시장구분코드
        corpRegMrktDcdNm    (str) : 법인등록시장구분코드명
        corpDcd             (str) : 법인구분코드
        corpDcdNm           (str) : 법인구분코드명
        bzno                (str) : 사업자등록번호
        enpOzpno            (str) : 기업구우편번호
        enpBsadr            (str) : 기업기본주소
        enpDtadr            (str) : 기업상세주소
        enpHmpgUrl          (str) : 기업홈페이지URL
        enpTlno             (str) : 기업전화번호
        enpFxno             (str) : 기업팩스번호
        sicNm               (str) : 표준산업분류명
        enpEstbDt           (str) : 기업설립일자
        enpStacMm           (str) : 기업결산월
        enpXchgLstgDt       (str) : 기업거래소상장일자
        enpXchgLstgAbolDt   (str) : 기업거래소상장폐지일자
        enpKosdaqLstgDt     (str) : 기업코스닥상장일자
        enpKosdaqLstgAbolDt (str) : 기업코스닥상장폐지일자
        enpKrxLstgDt        (str) : 기업KONEX상장일자
        enpKrxLstgAbolDt    (str) : 기업KONEX상장폐지일자
        smenpYn             (str) : 중소기업여부
        enpMntrBnkNm        (str) : 기업주거래은행명
        enpEmpeCnt          (str) : 기업종업원수
        empeAvgCnwkTermCtt  (str) : 종업원평균근속기간내용
        enpPn1AvgSlryAmt    (str) : 기업1인평균급여금액
        actnAudpnNm         (str) : 회계감사인명
        audtRptOpnnCtt      (str) : 감사보고서의견내용
        enpMainBizNm        (str) : 기업주요사업명
        fssCorpUnqNo        (str) : 금융감독원법인고유번호
        fssCorpChgDtm       (str) : 금융감독원법인변경일시     
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
    try:
        header = json.loads(response_corp_outline.text)["response"]["header"]
        body = json.loads(response_corp_outline.text)["response"]["body"]
        item = body["items"]["item"] # Information of each corporation
    except:
        return None

    # Assertion
    if len(item) == 0:
        return None
    
    # Print Result to Console
    print("Running: Get Corp Outline")
    print("Result Code : %s" % header["resultCode"])   # 결과코드
    print("Result Message : %s" % header["resultMsg"]) # 결과메시지 
    print("numOfRows : %d" % body["numOfRows"])        # 한 페이지 결과 수
    print("pageNo : %d" % body["pageNo"])              # 페이지번호
    print("totalCount : %d" % body["totalCount"])      # 전체 결과 수
    print() # Newline

    return item

def get_stoc_issu_stat(serviceKey:str, pageNo=1, numOfRows=1, resultType="json", basDt="", crno="", stckIssuCmpyNm=""):
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
    item : 한국 주식시장에 상장된 종목들의 기본정보 (list of dict)
        basDt          (str) : YYYYMMDD, 조회의 기준일, 통상 거래일
        crno           (str) : 종목의 법인등록번호
        stckIssuCmpyNm (str) : 주식 발행 회사명
        onskTisuCnt    (str) : 보통주 총 발행수
        pfstTisuCnt    (str) : 우선주 총 발행수
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
    try:
        header = json.loads(response_stoc_issu_stat.text)["response"]["header"]
        body = json.loads(response_stoc_issu_stat.text)["response"]["body"]
        item = body["items"]["item"] # Information of each stock items
    except:
        return None

    # Assertion
    if len(item) == 0:
        return None
    
    # Print Result to Console
    print("Running: Get Stoc Issu Stat")
    print("Result Code : %s" % header["resultCode"])   # 결과코드
    print("Result Message : %s" % header["resultMsg"]) # 결과메시지 
    print("numOfRows : %d" % body["numOfRows"])        # 한 페이지 결과 수
    print("pageNo : %d" % body["pageNo"])              # 페이지번호
    print("totalCount : %d" % body["totalCount"])      # 전체 결과 수
    print() # Newline

    return item

def get_krx_listed_info(serviceKey:str, pageNo=1, numOfRows=1, resultType="json", basDt="", beginBasDt="", endBasDt="", likeBasDt="", likeSrtnCd="", isinCd="", likeIsinCd="", itmsNm="", likeItmsNm="", crno="", corpNm="", likeCorpNm=""):
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
        basDt     (str) : YYYYMMDD, 조회의 기준일, 통상 거래일
        shortIsin (str) : 종목 코드보다 짧으면서 유일성이 보장되는 코드
        srtnCd    (str) : 현선물 통합상품의 종목 코드(12자리)
        mrktCtg   (str) : 시장 구분 (KOSPI/KOSDAQ/KONEX 등)
        itmsNm    (str) : 종목의 명칭
        crno      (str) : 종목의 법인등록번호
        corpNm    (str) : 종목의 법인 명칭
        shotnIsin (str) : 단축 ISIN 코드 (6자리)
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
    try:
        header = json.loads(response_krx_listed_info.text)["response"]["header"]
        body = json.loads(response_krx_listed_info.text)["response"]["body"]
        item = body["items"]["item"] # Information of each stock items
    except:
        return None

    # Assertion
    if len(item) == 0:
        return None

    # Make new pair (Short ISIN Code made by srtnCd)
    for data in item:
        data["shotnIsin"] = data["srtnCd"][1:] 
    
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

def get_item_basi_info(serviceKey:str, pageNo=1, numOfRows=1, resultType="json", basDt="", crno="", corpNm="", stckIssuCmpyNm=""):
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
        basDt          (str) : YYYYMMDD, 조회의 기준일, 통상 거래일
        crno           (str) : 종목의 법인등록번호
        isinCd         (str) : ISIN코드
        stckIssuCmpyNm (str) : 주식발행회사명
        isinCdNm       (str) : ISIN코드명
        scrsItmsKcd    (str) : 유가증권종목종류코드
        scrsItmsKcdNm  (str) : 유가증권종목종류코드명
        stckParPrc     (str) : 주식액면가
        issuStckCnt    (str) : 발행주식수
        lstgDt         (str) : 상장일자
        lstgAbolDt     (str) : 상장폐지일자
        dpsgRegDt      (str) : 예탁등록일자
        dpsgCanDt      (str) : 예탁취소일자
        issuFrmtClsfNm (str) : 발행형태구분명
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
    try:
        header = json.loads(response_item_basi_info.text)["response"]["header"]
        body = json.loads(response_item_basi_info.text)["response"]["body"]
        item = body["items"]["item"] # Information of each corporation
    except:
        return None

    # Assertion
    if len(item) == 0:
        return None

    # Print Result to Console
    print("Running: Get Item Basi Info")
    print("Result Code : %s" % header["resultCode"])   # 결과코드
    print("Result Message : %s" % header["resultMsg"]) # 결과메시지 
    print("numOfRows : %d" % body["numOfRows"])        # 한 페이지 결과 수
    print("pageNo : %d" % body["pageNo"])              # 페이지번호
    print("totalCount : %d" % body["totalCount"])      # 전체 결과 수
    print() # Newline

    return item

def get_summ_fina_stat(serviceKey:str, pageNo=1, numOfRows=2, resultType="json", crno="", bizYear=LAST_YEAR, type="ALL"):
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
    item : 한국 주식시장에 상장된 종목들의 기업개요정보 (list of dict)
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
    try:
        header = json.loads(response_summ_fina_stat.text)["response"]["header"]
        body = json.loads(response_summ_fina_stat.text)["response"]["body"]
        item = body["items"]["item"] # Information of each corporation
    except:
        return None

    # Assertion
    if len(item) == 0:
        return None
    
    # Print Result to Console (Logging)
    print("Running: Get Summ Fina Stat")
    print("Result Code : %s" % header["resultCode"])   # 결과코드
    print("Result Message : %s" % header["resultMsg"]) # 결과메시지 
    print("numOfRows : %d" % body["numOfRows"])        # 한 페이지 결과 수
    print("pageNo : %d" % body["pageNo"])              # 페이지번호
    print("totalCount : %d" % body["totalCount"])      # 전체 결과 수
    print() # Newline

    # Return depends on Option 'type'
    if type == "CONSOLIDATED":
        if item[0]["fnclDcd"] in ["110", "ifrs_ConsolidatedMember", "999"]:
            return item
                
    elif type == "SEPARATE":
        if item[0]["fnclDcd"] in ["120", "ifrs_SeparateMember", "999"]:
            return item

    else: # Default is "ALL"
        return item
    
def get_issuco_basic_info(serviceKey:str, issucoCustno=""):
    """
    한국예탁결제원_기업정보서비스: 기업기본정보 기업개요 조회 검색 결과를 반환한다.
    * 한국예탁결제원_기업정보서비스: 기업기본정보 기업개요 조회 (https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15001153)
        
    [Parameters]
    serviceKey   (str) : 공공데이터 포털에서 받은 인증키 (Mandatory)
    issucoCustno (str) : 발행회사번호 (Mandatory)

    [Returns]
    item : 한국 주식시장에 상장된 종목들의 기본정보 (dict)
        agOrgTpcd           (str) : 대행기관구분코드
        agOrgTpcdNm         (str) : 대행기관명
        apliDt              (str) : 상장일
        apliDtY             (str) : 예탁지정일
        bizno               (str) : 사업자번호
        caltotMartTpcd      (str) : 시장구분코드
        caltotMartTpcdNm    (str) : 시장구분명
        ceoNm               (str) : CEO명
        custXtinDt          (str) : 회사소멸일
        engCustNm           (str) : 영문회사명
        engLegFormNm        (str) : 법인형태구분영문명
        founDt              (str) : 설립일
        homepAddr           (str) : 홈페이지주소
        issucoCustno        (str) : 발행회사번호
        pval                (str) : 액면가
        pvalStkqty          (str) : 수권자본금
        repSecnNm           (str) : 발행회사명
        rostCloseTerm       (str) : 명부폐쇄기간
        rostCloseTermTpcd   (str) : 명부폐쇄기간구분코드
        rostCloseTermUnitCd (str) : 명부폐쇄기간단위구분코드
        rostCloseTermUnitNm (str) : 명부폐쇄기간단위구분명
        rostCloseTerms      (str) : 명부폐쇄기간수
        setaccMmdd          (str) : 결산월
        shotnIsin           (str) : 단축코드
        totalStkCnt         (str) : 총발행주식수

    """

    # Parameter Setting
    query_params_issuco_basic_info = {
        "serviceKey"   : serviceKey,  # 공공데이터 포털에서 받은 인증키 (Mandatory) 
        "issucoCustno" : issucoCustno # 발행 번호 (Default: "")
    }

    # Request
    response_issuco_basic_info = requests.get(set_query_url(service_url=URL_ISSUCO_BASIC_INFO, params=query_params_issuco_basic_info))

    # Parsing
    try:
        root = ET.fromstring(response_issuco_basic_info.text)
        header = root.find("header")
        body = root.find("body")
    except:
        return None
    
    items = body.find("item") # Information of each index item

    # Assertion
    if items is None:
        return None

    item = dict()
    for data in items:
        item[data.tag] = data.text

    # Print Result to Console (Logging)
    print("Running: Get ISSUCO BASIC INFO")
    print("Result Code : %s" % header.find("resultCode").text)   # 결과코드
    print("Result Message : %s" % header.find("resultMsg").text) # 결과메시지 
    print() # Newline

    return item

def get_issuco_custno_by_short_isin(serviceKey:str, shortIsin:str):
    """
    한국예탁결제원_기업정보서비스: 단축번호로 발행회사번호 조회 검색 결과를 반환한다.
    * 한국예탁결제원_기업정보서비스: 단축번호로 발행회사번호 조회 (https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15001153)
        
    [Parameters]
    serviceKey (str) : 공공데이터 포털에서 받은 인증키 (Mandatory) 
    shortIsin  (str) : 종목 코드보다 짧으면서 유일성이 보장되는 코드 (Mandatory) 

    [Returns]
    item : 단축번호에 해당되는 발행회사정보 (dict)
        issucoCustno  (str) : 발행회사번호
        issucoNm      (str) : 발행회사명
        listNm        (str) : 상장시장명
    """
    
    # Parameter Setting
    query_params_issuco_custno_by_short_isin = {
        "serviceKey" : serviceKey, # 공공데이터 포털에서 받은 인증키 (Mandatory) 
        "shortIsin"  : shortIsin   # 종목 코드보다 짧으면서 유일성이 보장되는 코드 (Mandatory) 
    }

    # Request
    response_issuco_custno_by_short_isin = requests.get(set_query_url(service_url=URL_ISSUCO_CUSTNO_BY_SHORT_ISIN, params=query_params_issuco_custno_by_short_isin))

    # Parsing
    try:
        root = ET.fromstring(response_issuco_custno_by_short_isin.text)
        header = root.find("header")
        body = root.find("body")
        items = body.find("item") # Information of each index item
    except:
        return None

    # Assertion
    if items is None: 
        return None

    item = dict()
    for data in items:
        item[data.tag] = data.text

    # Print Result to Console (Logging)
    print("Running: Get ISSUCO CUSTNO BY SHORT ISIN")
    print("Result Code : %s" % header.find("resultCode").text)   # 결과코드
    print("Result Message : %s" % header.find("resultMsg").text) # 결과메시지 
    print() # Newline

    return item

def get_financials_kr(serviceKey:str):
    list_financial_data = []

    # 금융위원회_KRX상장종목정보
    list_financial_data = get_krx_listed_info(serviceKey=serviceKey, numOfRows=ALL_STOCKS_KR)
    list_financial_data = filter_params(list_financial_data, ["srtnCd", "isinCd", "mrktCtg", "itmsNm", "crno", "corpNm", "shotnIsin"])

    item_id = 1
    for financial_data in list_financial_data:
        # Logging
        print("Collecting data for %s" % financial_data["corpNm"])

        # Give Index
        financial_data['id'] = item_id
        item_id += 1
        
        try:
            # 금융위원회_기업기본정보: 기업개요조회
            if financial_data.get("crno", None) is not None:
                corp_outline = get_corp_outline(serviceKey=serviceKey, crno=financial_data["crno"])
                if corp_outline is not None:
                    financial_data.update(corp_outline[0])
            time.sleep(INTERVAL_API_CALL)

            # 한국예탁결제원_기업정보서비스: 기업기본정보 기업개요 조회
            if financial_data.get("shotnIsin", None) is not None:
                issucoCustno = get_issuco_custno_by_short_isin(serviceKey=serviceKey, shortIsin=financial_data["shotnIsin"])
                if getattr(issucoCustno, "issucoCustno", None) is not None:
                    issuco_basic_info = get_issuco_basic_info(serviceKey=serviceKey, issucoCustno=issucoCustno["issucoCustno"])
                    if issuco_basic_info is not None:
                        financial_data.update(issuco_basic_info)
            time.sleep(INTERVAL_API_CALL)

            # 금융위원회_주식발행정보: 주식발행현황조회
            if financial_data.get("crno", None) is not None:
                stoc_issu_stat = get_stoc_issu_stat(serviceKey=serviceKey, crno=financial_data["crno"])
                if stoc_issu_stat is not None:
                    financial_data.update(stoc_issu_stat[0])
            time.sleep(INTERVAL_API_CALL)

            # 금융위원회_주식발행정보: 종목기본정보조회
            if financial_data.get("crno", None) is not None:
                item_basi_info = get_item_basi_info(serviceKey=serviceKey, crno=financial_data["crno"])
                if item_basi_info is not None:
                    financial_data.update(item_basi_info[0])
            time.sleep(INTERVAL_API_CALL)

            # 금융위윈회_기업 재무정보: 요약재무제표조회
            if financial_data.get("crno", None) is not None:
                summ_fina_stat = get_summ_fina_stat(serviceKey=serviceKey, numOfRows="", crno=financial_data["crno"], type="ALL")
                if summ_fina_stat is not None:
                    financial_data.update(summ_fina_stat[0])
            time.sleep(INTERVAL_API_CALL)

            # 금융위원회_주식시세정보: 주식시세
            if financial_data.get("isinCd", None) is not None:
                stock_price_info = get_stock_price_info(serviceKey=serviceKey, isinCd=financial_data["isinCd"])
                if stock_price_info is not None:
                    financial_data.update(stock_price_info)
            time.sleep(INTERVAL_API_CALL)
        except Exception as err_msg:
            print("Error Detected:", err_msg)
            continue

    return list_financial_data

def test():

    # Configurations for test
    serviceKey           = "<your api key>" # 공공데이터포털 서비스키
    samsung_crno         = "1301110006246"  # 삼성전자 법인등록번호
    samsung_issucoCustno = "593"            # 삼성전자 발행회사번호
    samsung_shortIsin    = "005930"         # 삼성전자 단축 ISIN 코드

    # result = get_krx_listed_info(serviceKey=serviceKey)
    # result = get_corp_outline(serviceKey=serviceKey, crno=samsung_crno)
    # result = get_issuco_basic_info(serviceKey=serviceKey, issucoCustno=samsung_issucoCustno)
    # result = get_issuco_custno_by_short_isin(serviceKey=serviceKey, shortIsin=samsung_shortIsin)
    # result = get_stoc_issu_stat(serviceKey=serviceKey, crno=samsung_crno)
    # result = get_item_basi_info(serviceKey=serviceKey, crno=samsung_crno)    
    # result = get_summ_fina_stat(serviceKey=serviceKey, type="ALL", crno=samsung_crno)

    result = get_financials_kr(serviceKey=serviceKey)

    with open("financials_kr.json", "w", encoding="utf-8") as json_file:
        json_file.write(str(result)) # Write to json file
        