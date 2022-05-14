import time
import inspect
from datetime import datetime

# 멀티 프로세싱
from multiprocessing import Process

# 스케줄링
from apscheduler.schedulers.background import BackgroundScheduler 

from stocklab.agent.ebest import EBest
from stocklab.agent.data import Data
from stocklab.db_handler.mongodb_handler import MongoDBHandler

def run_process_collect_code_list():
    print(inspect.stack()[0][3])
    p = Process(target=collect_code_list)
    
    # 멀티 프로세싱
    p.start()
    p.join()

def run_process_collect_stock_info():
    print(inspect.stack()[0][3])
    p = Process(target=collect_stock_info)
    
    # 멀티 프로세싱
    p.start()
    p.join()

def collect_code_list():
    """
    종목 코드를 수집한다.

    [수집 대상]
    KOSPI
    KOSDAQ
    """

    ebest = EBest("DEMO")
    mongodb = MongoDBHandler()
    ebest.login()

    # 종목 코드 리스트를 불러온다.
    result = ebest.get_code_list("ALL")
    
    # "code_info" Collection의 모든 Document들을 삭제한다.
    mongodb.delete_items({}, "stocklab", "code_info")

    # result를 "code_info"에 삽입한다.
    mongodb.insert_items(result, "stocklab", "code_info")

def collect_stock_info():
    """
    주식 가격 정보를 수집한다.
    
    [수집 대상]
    KOSPI
    KOSDAQ
    """

    ebest = EBest("DEMO")
    mongodb = MongoDBHandler()
    ebest.login()


    code_list = mongodb.find_items({}, "stocklab", "code_info")
    target_code = set([item["단축코드"] for item in code_list])
    today = datetime.today().strftime("%Y%m%d")
    print(today)
    collect_list = mongodb.find_items({"날짜":today}, "stocklab", "price_info").distinct("code")

    for col in collect_list:
        target_code.remove(col)
        
    for code in target_code:
        time.sleep(1)
        print("code:", code)
        result_price = ebest.get_stock_price_by_code(code, "1")
        if len(result_price) > 0:
            print(result_price)
            mongodb.insert_items(result_price, "stocklab", "price_info")

        result_credit = ebest.get_credit_trend_by_code(code, today)
        if len(result_credit) > 0:
            mongodb.insert_items(result_credit, "stocklab", "credit_info")

        result_short = ebest.get_short_trend_by_code(code, sdate=today, edate=today)
        
        if len(result_short) > 0:
            mongodb.insert_items(result_short, "stocklab", "short_info")

        result_agent = ebest.get_agent_trend_by_code(code, fromdt=today, todt=today)

        if len(result_agent) > 0:
            mongodb.insert_items(result_agent, "stocklab", "agent_info")
    
if __name__ == '__main__':
    
    scheduler = BackgroundScheduler()
    
    # Shcedule: id="1"
    # run_process_collect_code_list (종목코드 수집)
    # 매 주 평일(월요일-금요일) 19시 정각에 수행
    scheduler.add_job(func=run_process_collect_code_list, trigger="cron", day_of_week="mon-fri", hour="14", minute="08", id="1")

    # Shcedule: id="2"
    # run_process_collect_stock_info (종목별 가격 정보 수집)
    # 매 주 평일(월요일-금요일) 19시 5분에 수행
    scheduler.add_job(func=run_process_collect_stock_info, trigger="cron", day_of_week="mon-fri", hour="14", minute="08", id="2")

    # Scheduling
    scheduler.start()

    while True:
        print("running", datetime.now())
        time.sleep(1)