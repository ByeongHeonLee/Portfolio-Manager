import apshceduler # Scheduler module

from mongodbHandler import MongoDBHandler   # Mongo DB Handler
from krxListedInfo  import getKrxListedInfo # 금융위원회_KRX상장종목정보

# Main logic
if __name__ == "__main__":

    # Create Mongo DB Connection    
    mongodb = MongoDBHandler()

    # Insert into Mongo DB
    mongodb.delete_items({}, "stock", "financial_statement")
    mongodb.insert_items(getKrxListedInfo(), "stock", "financial_statement")