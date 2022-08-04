import time

# Scheduler Modules
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron         import CronTrigger

# Database Handler Modules
from mongodbHandler                    import MongoDBHandler   # Mongo DB Handler

# Data Crawler Modules
from krxListedInfo                     import getKrxListedInfo # 금융위원회_KRX상장종목정보

# Main logic
if __name__ == "__main__":

    # Set Background Scheduler 
    sched = BackgroundScheduler(timezone='Asia/Seoul')

    # Create Mongo DB Connection    
    mongodb = MongoDBHandler()

    # 금융위원회_KRX상장종목정보
    # Run at Start of Pre-Market (AM 08:30)
    def schedGetKrxListedInfo():
        mongodb.delete_items({}, "stock", "financial_statement")
        mongodb.insert_items(getKrxListedInfo(), "stock", "financial_statement")
    sched.add_job(schedGetKrxListedInfo, 'cron', day_of_week='mon-fri', hour='8', minute='30', id='krxListedInfo')
    
    # Run
    sched.start()
    while True:
        time.sleep(1)
        