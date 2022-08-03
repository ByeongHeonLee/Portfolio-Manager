import time

from apscheduler.schedulers.background import BackgroundScheduler # Scheduler module
from mongodbHandler import MongoDBHandler   # Mongo DB Handler
from krxListedInfo  import getKrxListedInfo # 금융위원회_KRX상장종목정보

# Main logic
if __name__ == "__main__":

    # Set Background Scheduler 
    sched = BackgroundScheduler()

    # Create Mongo DB Connection    
    mongodb = MongoDBHandler()

    # Insert into Mongo DB
    mongodb.delete_items({}, "stock", "financial_statement")
    mongodb.insert_items(getKrxListedInfo(), "stock", "financial_statement")

    # 5초마다 실행
    @sched.scheduled_job('interval', seconds=5, id='test_1')
    def job1():
        print(f'job1 : {time.strftime("%H:%M:%S")}')

    # 매일 12시 30분에 실행
    @sched.scheduled_job('cron', hour='12', minute='30', id='test_2')
    def job2():
        print(f'job2 : {time.strftime("%H:%M:%S")}')

    # 이런식으로 추가도 가능. 매분에 실행
    sched.add_job(job2, 'cron', second='0', id="test_3")


    print('sched before~')
    sched.start()
    print('sched after~')

    while True:
        time.sleep(1)