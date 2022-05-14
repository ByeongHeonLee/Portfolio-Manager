import requests
import configparser
import xml.etree.ElementTree as ET

class Data():
    # 기업코드
    CORP_CODE_URL = "http://api.seibro.or.kr/openapi/service/CorpSvc/getIssucoCustnoByNm"

    # 기업 개요
    CORP_INFO_URL = "http://api.seibro.or.kr/openapi/service/CorpSvc/getIssucoBasicInfo"

    # 주식분포 주주별현황
    STOCK_DISTRIBUTION_URL = "http://api.seibro.or.kr/openapi/service/CorpSvc/getStkDistributionStatus"

    def __init__(self):
        config = configparser.RawConfigParser() # api_key에 포함된 특수문자 처리를 위해 ConfigParser 대신 RawConfigParser 사용
        config.read('conf/config.ini', encoding='UTF8')
        self.api_key = config["DATA"]["api_key"]
        if self.api_key is None:
            raise Exception("Need to api key")

    def get_corp_code(self, name=None):
        """
        한국예탁결제원(KSD)에서 제공하는 기업코드를 회사명칭으로 검색한다.
        이때, 기업코드는 KSD에서 자체적으로 관리하는 코드로
        주식시장에서의 종목코드와 다르다.

        [Parameters]
        name : 회사명칭 (삼성전자, 삼성 등) (str) (default=None)

        [Returns]
        result : 회사코드와 명칭이 저장된 딕셔너리 (dict)



        * KSD - SEIBro API - getIssucoCustnoByNm

        [Inputs]
        issucoNm   : 발행회사명 (Optional)
        pageNo     : 페이지 번호 (한 페이지 결과 수) (Optional)
        numOfRows  : 한 페이지 결과 수 (페이지 번호) (Optional)
        ServiceKey : 부여받은 서비스 키

        [Outputs]
        issucoCustno : 발행회사번호
        issucoNm     : 발행회사명
        listNm       : 상장시장명
        numofRows    : 한페이지 결과 수
        pageNo       : 페이지 번호
        """

        # Request to KSD
        query_params = {"serviceKey":self.api_key,
                        "issucoNm": name,
                        "numOfRows": str(5000)}
        request_url =self.CORP_CODE_URL+"?"
        for k, v in query_params.items(): # <Key, Value> Pairs
            request_url = request_url + k + "=" + v +"&" # 매개변수들 사이는 "&"로 구분, 매개변수명과 값은 "="로 구분
        print(request_url)
        res = requests.get(request_url[:-1]) # URL의 마지막 &는 제외하고 전송, 변수 res에는 XML 파일이 반환됨

        # XML Parsing
        root = ET.fromstring(res.text) # 본문 로딩
        from_tags = root.iter("items") # "items" 노드들의 iterator 저장
        result = {}
        for items in from_tags:
            for item in items.iter('item'): # 해당 XML 파일에는 "items"의 하위에 "item"들이 저장되어 있음 (기업 검색 결과는 0개 이상이므로 "items" 노드에 다수의 하위 "item" 노드가 존재)
                if name in item.find('issucoNm').text.split(): # 해당 회사명칭이 issucoNm 속성에 포함되어 있는 경우
                    result["issucoCustno"] = item.find('issucoCustno').text # 결과에 KSD 기업코드를 저장함
                    result["issucoNm"] = item.find('issucoNm').text # 결과에 기업명을 저장함
        return result

    def get_corp_info(self, code=None):
        """
        기업 기본정보 기업개요를 조회한다.

        [Parameters]
        code : KSD 기업코드 (숫자, 발행회사번호 조회로 확인, 주식 종목코드와 다름) (str) (default=None)

        [Returns]
        result : 기업개요 정보가 저장된 딕셔너리 (dict)



        * KSD - SEIBro API - getIssucoBasicInfo

        [Inputs]
        issucoCustno : 발행회사번호

        [Outputs]     
        agOrgTpcd           : 대행기관구분코드
        agOrgTpcdNm         : 대행기관명
        apliDt              : 상장일
        apliDtY             : 예탁지정일
        bizno               : 사업자번호
        caltotMartTpcd      : 시장구분코드
        caltotMartTpcdNm    : 시장구분명
        ceoNm               : CEO명
        custXtinDt          : 회사소멸일
        engCustNm           : 영문회사명
        engLegFormNm        : 법인형태구분영문명
        founDt              : 설립일
        homepAddr           : 홈페이지주소
        issucoCustno        : 발행회사번호
        pval                : 액면가
        pvalStkqty          : 수권자본금
        repSecnNm           : 발행회사명
        rostCloseTerm       : 명부폐쇄기간
        rostCloseTermTpcd   : 명부폐쇄기간구분코드
        rostCloseTermUnitCd : 명부폐쇄기간단위구분코드
        rostCloseTermUnitNm : 명부폐쇄기간단위구분명
        rostCloseTerms      : 명부폐쇄기간수
        setaccMmdd          : 결산월
        shotnIsin           : 단축코드
        totalStkCnt         : 총발행주식수
        """

        # Request to KSD
        query_params = {"ServiceKey":self.api_key,
                        "issucoCustno": code}
        request_url =self.CORP_INFO_URL+"?"
        for k, v in query_params.items():
            request_url = request_url + k + "=" + v +"&"
        print(request_url)
        res = requests.get(request_url[:-1])

        # XML Parsing
        root = ET.fromstring(res.text)
        from_tags = root.iter("item")
        result = {} 
        for item in from_tags: # 단일 기업의 기업개요를 조회하므로, "items" 노드가 아닌 "item" 노드를 바로 Parsing
            result["apliDt"] = item.find('apliDt').text
            result["bizno"] = item.find('bizno').text
            result["ceoNm"] = item.find('ceoNm').text
            result["engCustNm"] = item.find('engCustNm').text
            result["foundDt"] = item.find('founDt').text
            result["homepAddr"] = item.find('homepAddr').text
            result["pval"] = item.find('pval').text
            result["totalStkcnt"] = item.find('totalStkCnt').text
        return result     

    def get_stk_distribution_info(self, code=None, date=None):
        """
        주식분포내역 주주별 현황을 조회한다.

        [Parameters]
        code : KSD 기업코드 (숫자, 발행회사번호 조회로 확인, 주식 종목코드와 다름) (str) (default=None)
        data : 조회할 기준일 8자리 (yyyymmdd) (str) (default=None)

        [Returns]
        result : 주주별 주식보유 현황 정보가 저장된 리스트 (list)



        * KSD - SEIBro API - getStkDistributionStatus

        [Inputs]
        issucoCustno : 발행회사번호
        rgtStdDt     : 기준일 (yyyymmdd)


        [Outputs]     
        shrs           : 기준일 시점에 회사의 주식을 보유하고 있는 주주수 (명)
        shrsRatio      : 기준일 시점에 주식 보유 주주비율 (%)
        stkDistbutTpnm : 주주 유형별 분류
        stkqty         : 기준일 시점에 회사가 보유하고 있는 발행주식수 (주수)
        stkqtyRatio    : 기준일 시점에 회사가 보유하고 있는 발행주식수의 비율 (%)
        """

        query_params = {"ServiceKey": self.api_key,
                        "issucoCustno": code,
                        "rgtStdDt": date}

        request_url =self.STOCK_DISTRIBUTION_URL+"?"
        for k, v in query_params.items():
            request_url = request_url + k + "=" + v +"&"
        print(request_url)
        res = requests.get(request_url[:-1])
        root = ET.fromstring(res.text)
        from_tags = root.iter("items")
        result_list = []
        for items in from_tags:
            for item in items.iter('item'):
                result = {}
                result["shrs"] = item.find('shrs').text
                result["shrs_ratio"] = item.find('shrsRatio').text
                result["stk_dist_name"] = item.find('stkDistbutTpnm').text
                result["stk_qty"] = item.find('stkqty').text
                result["stk_qty_ratio"] = item.find('stkqtyRatio').text
                result_list.append(result)
        return result_list
