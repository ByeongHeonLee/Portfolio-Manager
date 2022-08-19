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
from server.data.dataHandler import get_financial_data_kr

# Main logic
if __name__ == "__main__":

    print("data crawler is running")

    # Set Background Scheduler 
    sched = BackgroundScheduler(timezone='Asia/Seoul')

    # Create Mongo DB Connection
    mongodb = MongoDBHandler(os.getenv("MONGODB_STOCK_INFO_URI"))

    # Run at Start of Pre-Market of Korea Market (AM 08:30)
    def sched_get_financial_data_kr():
        print("Start: get_financial_data_kr")
        mongodb.delete_items({}, "stock", "financial_info")
        items = get_financial_data_kr(serviceKey=os.getenv("KR_PUBLIC_DATA_PORTAL_KEY"))
        mongodb.insert_items(items, "stock", "financial_info")
        print("End: get_financial_data_kr")
    sched.add_job(sched_get_financial_data_kr, 'cron', day_of_week='mon-fri', hour='8', minute='30', id='financial_info')
    
    # Run
    sched.start()
    while True:
        if datetime.today().minute % 10 == 0 and datetime.today().second == 0:
            print("data crawler is running") # Print to console the message every 10 minutes

        time.sleep(1)
        