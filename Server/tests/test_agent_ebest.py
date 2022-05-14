import unittest
from stocklab.agent.ebest import EBest
import inspect
import time

class TestEbest(unittest.TestCase):
    def setUp(self):
        """
        하나의 테스트 케이스가 실행되기 전 호출되는 메서드
        """
        self.ebest = EBest("DEMO")
        self.ebest.login()

    def test_get_current_call_price_by_code(self):
        print(inspect.stack()[0][3])    # 실행할 메서드의 이름을 출력
        result = self.ebest.get_current_call_price_by_code("005930")
        assert result
        print(result)

    def test_get_stock_price_by_code(self):
        """
        get_stock_price_by_code() Method의 단위 테스트 함수
        """
        print(inspect.stack()[0][3])    # 실행할 메서드의 이름을 출력
        result = self.ebest.get_stock_price_by_code("005930", "30")  # 삼성전자(005930)의 최근 30일 치 데이터를 조회
        assert result is not None # result가 None이면 AssertError 발생
        print(result)

    def testLogin(self):
        print(inspect.stack()[0][3])    # 실행할 메서드의 이름을 출력
        self.ebest.login()
        assert self.ebest.xa_session_client.login_state == 1

    def test_get_code_list(self):
        """
        get_code_list() Method의 단위 테스트 함수
        """
        print(inspect.stack()[0][3])    # 실행할 메서드의 이름을 출력

        all_result = self.ebest.get_code_list("ALL") # 모든 종목 조회
        assert all_result is not None   # result가 None이면 AssertError 발생

        kospi_result = self.ebest.get_code_list("KOSPI") # 코스피 종목 조회
        assert kospi_result is not None   # result가 None이면 AssertError 발생

        kosdaq_result = self.ebest.get_code_list("KOSDAQ") # 코스닥 종목 조회
        assert kosdaq_result is not None   # result가 None이면 AssertError 발생

        print("result: # of ALL:", len(all_result), " # of KOSPI:", len(kospi_result), " # of KOSDAQ:", len(kosdaq_result))

    def test_get_stock_price_by_code(self):
        """
        get_stock_price_by_code() Method의 단위 테스트 함수
        """
        print(inspect.stack()[0][3])    # 실행할 메서드의 이름을 출력
        result = self.ebest.get_stock_price_by_code("005930", "2")  # 삼성전자(005930)의 2일전 주가 데이터를 조회
        assert result is not None # result가 None이면 AssertError 발생
        print(result)

    def test_get_credit_trend_by_code(self):
        """
        get_credit_trend_by_code() Method의 단위 테스트 함수
        """
        print(inspect.stack()[0][3])    # 실행할 메서드의 이름을 출력
        result = self.ebest.get_credit_trend_by_code("005930", "20190304")  # 삼성전자(005930)의 2019년 3월 4일 신용거래 동향을 조회
        assert result is not None # result가 None이면 AssertError 발생
        print(result)

    def test_get_short_trend_by_code(self):
        """
        get_short_trend_by_code() Method의 단위 테스트 함수
        """
        print(inspect.stack()[0][3])    # 실행할 메서드의 이름을 출력
        result = self.ebest.get_short_trend_by_code("005930", sdate="20190304", edate="20190304")  # 삼성전자(005930)의 2019년 3월 4일부터 2019년 3월 4일까지의 공매도 추이를 조회
        assert result is not None # result가 None이면 AssertError 발생
        print(result)

    def test_get_agent_trend_by_code(self):
        """
        get_agent_trend_by_code() Method의 단위 테스트 함수
        """
        print(inspect.stack()[0][3])    # 실행할 메서드의 이름을 출력
        result = self.ebest.get_agent_trend_by_code("005930", fromdt="20190304", todt="20190304")  # 삼성전자(005930)의 2019년 3월 4일부터 2019년 3월 4일까지의 외인·기관별 종목별 동향을 조회
        assert result is not None # result가 None이면 AssertError 발생
        print(result)

    def test_order_stock(self):
        print(inspect.stack()[0][3])    # 실행할 메서드의 이름을 출력
        result = self.ebest.order_stock("005930", "2", "46000", "2", "00")
        assert result
        print(result)
        #code = result[0]["ShtnIsuNo"]
        #order_no = result[0]["OrdNo"]
        #print(code, order_no)
        #time.sleep(1)
        #result1 = self.ebest.get_order_check("005930", order_no)
        #print(result1)

    def test_order_cancel(self):
        print(inspect.stack()[0][3])    # 실행할 메서드의 이름을 출력
        result = self.ebest.order_cancel("29515", "A005930", "2")
        assert result
        print(result)

    def test_get_price_n_min_by_code(self):
        print(inspect.stack()[0][3])    # 실행할 메서드의 이름을 출력
        result = self.ebest.get_price_n_min_by_code("20190412", "180640")
        assert result
        print(result)

    def test_get_price_n_min_by_code_tick(self):
        print(inspect.stack()[0][3])    # 실행할 메서드의 이름을 출력
        result = self.ebest.get_price_n_min_by_code("20190412", "005930", 0)
        assert result
        print(result)

    def test_get_account_stock_info(self):
        print(inspect.stack()[0][3])    # 실행할 메서드의 이름을 출력
        result = self.ebest.get_account_stock_info()
        assert result
        print(result)

    def test_get_account_info(self):
        print(inspect.stack()[0][3])    # 실행할 메서드의 이름을 출력
        result = self.ebest.get_account_info()
        assert result
        print(result)

    """

    def test_real_code(self):
        print(inspect.stack()[0][3])    # 실행할 메서드의 이름을 출력
        result = self.ebest._execute_real("005930")
        print(result)

    def test_order_check(self):
        print(inspect.stack()[0][3])    # 실행할 메서드의 이름을 출력
        result = self.ebest.order_check("29515")
        assert result
        print(result)

    def test_get_theme_by_code(self):
        time.sleep(1)
        print(inspect.stack()[0][3])    # 실행할 메서드의 이름을 출력
        result = self.ebest.get_theme_by_code("078020")
        assert result is not None
        print(len(result))

    def test_get_theme_list(self):
        time.sleep(1)
        print(inspect.stack()[0][3])    # 실행할 메서드의 이름을 출력
        result = self.ebest.get_theme_list()
        assert result is not None
        print(result)

    def test_get_category_list(self):
        time.sleep(1)
        print(inspect.stack()[0][3])    # 실행할 메서드의 이름을 출력
        result = self.ebest.get_category_list()
        assert result is not None
        print(len(result))

    def test_price_by_category(self):
        result = self.ebest.get_price_by_category("101")
        assert result is not None
        print(len(result))

    def test_price_by_theme(self):
        result = self.ebest.get_price_by_theme("0403")
        assert result is not None
        print(len(result))

    def test_short_trend_by_code(self):
        result = self.ebest.get_short_trend_by_code("0403", sdate="20181201", edate="20181203")
        assert result is not None
        print(len(result))

    def test_get_event_by_code(self):
        result = self.ebest.get_event_by_code("0403", date="20181201")
        assert result is not None
        print(len(result))

    def test_get_trade_history(self):
        result = self.ebest.get_trade_history("10")
        assert result is not None
        print(result)

    def test_get_account_info(self):
        result = self.ebest.get_account_info()
        assert result is not None
        print(result)

    def test_get_account_stock_info(self):
        result = self.ebest.get_account_stock_info()
        assert result is not None
        print(result)

    """
    def tearDown(self):
        """
        하나의 테스트 케이스가 실행되고난 후에 호출되는 메서드
        """
        self.ebest.logout()
