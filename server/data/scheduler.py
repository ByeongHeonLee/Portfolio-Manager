import os
import time
from datetime import datetime
from pytz     import timezone

# Scheduler Modules
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron         import CronTrigger

# Database Handler Modules
from mongodbHandler import MongoDBHandler   # Mongo DB Handler

# Data Crawler Modules
from dataHandler import get_krx_listed_info
from dataHandler import get_corp_outline

# # of Maximum Items in Korea Stock Exchange (KOSPI/KOSDAQ/KONEX)
# http://data.krx.co.kr/contents/MDC/MAIN/main/index.cmd
KOSPI_ITEMS  = 938
KOSDAQ_ITEMS = 1575
KONEX_ITEMS  = 125
ALL_ITEMS = str(KOSPI_ITEMS + KOSDAQ_ITEMS + KONEX_ITEMS)

# Main logic
if __name__ == "__main__":

    # Set Background Scheduler 
    sched = BackgroundScheduler(timezone='Asia/Seoul')

    # Create Mongo DB Connection
    mongodb = MongoDBHandler(os.getenv("MONGODB_STOCK_INFO_URI"))

    # Run at Start of Pre-Market of Korea Market (AM 08:30)
    def sched_get_financial_data_kr():
        mongodb.delete_items({}, "stock", "financial_info")
        items = get_krx_listed_info(serviceKey=os.getenv("KR_PUBLIC_DATA_PORTAL_KEY"))
        for item in items:
            item.append(get_corp_outline(serviceKey=os.getenv("KR_PUBLIC_DATA_PORTAL_KEY"), crno=item["crno"]))
        mongodb.insert_items(items, "stock", "financial_info")
    sched.add_job(sched_get_financial_data_kr, 'cron', day_of_week='mon-fri', hour='18', minute='43', id='financial_info')
    
    # Run
    sched.start()
    while True:
        if datetime.today().minute == 0:
            print("data crawler is running...")

        time.sleep(1)
        