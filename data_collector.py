
# Author  : 이병헌
# Contact : lww7438@gmail.com
# Date    : 2022-11-12(토)



# Required Modules
import psycopg2    # Command to install: "pip install psycopg2-binary"
import schema
import json

from datetime    import datetime, timedelta
from pytz        import timezone



# Constants
FILE_PATH = './client/src/components/views/data/'
YESTERDAY             = datetime.strftime(datetime.now(timezone('Asia/Seoul')) - timedelta(1)  , "%Y%m%d") # Yesterday (Format:"YYYYMMDD")
PREVIOUS_BUSINESS_DAY = datetime.strftime(datetime.now(timezone('Asia/Seoul')) - timedelta(3)  , "%Y%m%d") if datetime.now(timezone('Asia/Seoul')).weekday() == 0 else YESTERDAY # Previous Business Day (Format:"YYYYMMDD")
BASE_DATE = '2022-11-13'



# Class Declaration
class PostgresCore():

    # * * *    Low-Level Methods (SQL Handlers)    * * *
    def __init__(self, user:str, password:str, host='pm330.c68tjqdjajqc.us-east-1.rds.amazonaws.com', port=5432, db_name='postgres'):

        self._client = psycopg2.connect(
            host     = host,
            port     = port,
            dbname   = db_name,
            user     = user,
            password = password            
        )

        self.conn_user = user
        self.cursor = self._client.cursor()

    def __del__(self):

        self._client.close()
        self.cursor.close()

    def __execute(self, query:str, args={}):

        self.cursor.execute(query,args)
        row = self.cursor.fetchall()
        return row

    def __commit(self):

        self.cursor.commit()

    def insert_item(self, table:str=None, columns:list=None, data:dict=None):
        """
        단일 Row를 삽입한다.
        (SQL: INSERT INTO 구문을 수행한다.)

        [Parameters]
        table   (str)  : 데이터를 조회할 테이블 이름 (default: None)
        columns (list) : 해당 테이블의 속성
        data    (dict) : 삽입할 데이터 ({<colume>:<value>}) (default: None)

        [Returns]
        True  : 데이터 삽입이 성공적으로 수행된 경우
        False : 데이터 삽입 과정에서 오류가 발생한 경우
        """

        # Processing for invalid arguments
        if (table not in schema.LIST_TABLE_NAME) or (table is None):
            print(f"[ERROR] Invalid Table Name: {table} does not exist")
            return False

        if (data is None) or (len(data) == 0):
            print(f"[ERROR] Empty Data Insertion: data is empty")
            return False

        # Setting columns and values for query
        str_values = ""

        for column in columns:
            
            if data[column] in schema.NULL_TYPES:
                str_values += "null" + ", "
            elif schema.get_type_by_column_name(table, column) in schema.STR_TYPES:
                str_values += "'" + str(data[column]) + "', "
            else:
                str_values += str(data[column]) + ", "

        # Elimination last comma
        str_values = str_values[:-2]

        # Make columns a string
        str_columns = ', '.join(columns)

        sql = f""" INSERT INTO {table} ({str_columns}) VALUES ({str_values}) ;"""

        try:
            print("Executed SQL: ", sql)
            self.cursor.execute(sql)
            self._client.commit()
            return True

        except Exception as err_msg :
            print(f"[ERROR] insert_item Error: {err_msg}")
            return False

    def insert_items(self, table:str=None, columns:list=None, data:list=None):
        """
        다수의 Row를 삽입한다.
        (SQL: INSERT INTO 구문을 수행한다.)

        [Parameters]
        table   (str)  : 데이터를 조회할 테이블 이름 (default: None)
        columns (list) : 해당 테이블의 속성
        data    (list) : 삽입할 데이터 ([{<colume>:<value>}, ...]) (default: None)

        [Returns]
        True  : 데이터 삽입이 성공적으로 수행된 경우
        False : 데이터 삽입 과정에서 오류가 발생한 경우
        """

        # Processing for invalid arguments
        if (table not in schema.LIST_TABLE_NAME) or (table is None):
            print(f"[ERROR] Invalid Table Name: {table} does not exist")
            return False

        if (data is None) or (len(data) == 0):
            print(f"[ERROR] Empty Data Insertion: data is empty")
            return False

        # Setting columns and values for query
        value_list = []
        
        for row in data:
            values = "("
            for column in columns:

                if row[column] in schema.NULL_TYPES:
                    values += "null" + ", "
                elif schema.get_type_by_column_name(table, column) in schema.STR_TYPES:
                    values += "'" + str(row[column]) + "', "
                else:
                    values += str(row[column]) + ", "
                    
            values = values[:-2]
            values += ")"
            value_list.append(values)

        # Make columns a string
        str_columns = ', '.join(columns)

        sql = f""" INSERT INTO {table} ({str_columns}) VALUES """
        for str_value in value_list:
            sql += str_value + ', '

        sql = sql[:-2]
        sql += ';'

        try:
            print("Executed SQL: ", sql)
            self.cursor.execute(sql)
            self._client.commit()
            return True

        except Exception as err_msg :
            print(f"[ERROR] insert_items Error: {err_msg}")
            return False
    
    def find_item(self, table:str=None, columns='ALL', condition:str=None, order_by:str=None, asc:bool=True):
        """
        테이블에서 조건에 부합하는 데이터를 반환한다.
        (SQL: SELECT 구문을 수행한다.)

        [Parameters]
        table     (str)        : 데이터를 조회할 테이블 이름 (default: None)
        columns   (list | str) : 반환할 데이터의 속성 (default: ALL; 모든 속성값)
        condition (list)       : 조회 조건 (WHERE Clause in SQL) (default: None)
        order_by  (str)        : 정렬의 기준이 될 속성 (default: None)
        asc       (bool)       : 오름차순 정렬 여부 (default: True)

        [Returns]
        str   : 데이터 조회가 성공적으로 수행된 경우, 조회 결과
        False : 데이터 조회 과정에서 오류가 발생한 경우
        """

        # Processing for invalid arguments
        if (table not in schema.LIST_TABLE_NAME) or (table is None):
            print(f"[ERROR] Invalid Table Name: {table} does not exist")
            return False

        # Setting SQL for query

        # SELECT Cluase in SQL
        if columns == 'ALL':
            str_columns = "DISTINCT *"
        elif type(list()) == type(columns):
            str_columns = ", ".join(columns)
            str_columns = "(" + str_columns + ")"
        elif type(str()) == type(columns):
            str_columns = columns
        
        # WHERE Cluase in SQL
        if condition is None:
            sql = f""" SELECT {str_columns} FROM {table} """
        else:
            sql = f""" SELECT {str_columns} FROM {table} WHERE {condition} """

        # ORDER BY Cluase in SQL
        if order_by is not None:
            sql += f""" ORDER BY {order_by} """

            if asc:
                sql += f""" ASC """
            else:
                sql += f""" DESC """

        sql += """ ; """

        try:
            print("Executed SQL: ", sql)
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result

        except Exception as err_msg:
            print(f"[ERROR] find_item Error: {err_msg}")
            return False

    def update_item(self, table:str=None, column:str=None, value=None, condition:str=None):
        """
        테이블에서 조건에 부합하는 데이터를 수정한다.
        (SQL: UPDATE 구문을 수행한다.)

        [Parameters]
        table     (str) : 데이터를 수정할 테이블 이름 (default: None)
        column    (str) : 수정 대상 속성 (default: None)
        value           : 수정할 값 (default: None)
        condition (str) : 수정 조건 (WHERE Clause in SQL) (default: None)

        [Returns]
        True  : 데이터 수정이 성공적으로 수행된 경우
        False : 데이터 수정 과정에서 오류가 발생한 경우
        """

        # Processing for invalid arguments
        if (table not in schema.LIST_TABLE_NAME) or (table is None):
            print(f"[ERROR] Invalid Table Name: {table} does not exist")
            return False

        # Setting SQL for query
        if schema.get_type_by_column_name(table, column) in schema.STR_TYPES:
            value = "'" + value + "'"
        
        sql = f""" UPDATE {table} SET {column}={value} WHERE {condition} ; """

        try :
            print("Executed SQL: ", sql)
            self.cursor.execute(sql)
            self._client.commit()
            return True

        except Exception as err_msg:
            print(f"[ERROR] update_item Error: {err_msg}")
            return False

    def delete_item(self, table:str=None, condition:str=None):
        """
        테이블에서 조건에 부합하는 데이터를 수정한다.
        condition의 값을 'ALL'로 지정할 경우, table의 모든 데이터를 삭제한다.
        (SQL: DELETE 구문을 수행한다.)

        [Parameters]
        table     (str) : 데이터를 수정할 테이블 이름 (default: None)
        condition (str) : 삭제 조건 (WHERE Clause in SQL) (default: None)

        [Returns]
        True  : 데이터 삭제가 성공적으로 수행된 경우
        False : 데이터 삭제 과정에서 오류가 발생한 경우
        """

        # Processing for invalid arguments
        if (table not in schema.LIST_TABLE_NAME) or (table is None):
            print(f"[ERROR] delete_item error: Invalid Table Name: {table} does not exist")
            return False
        
        if condition is None:
            print(f"[ERROR] delete_item error: Invalid condition: {condition} does not allowed")
            return False

        if condition == 'ALL':
            sql = f" DELETE FROM {table} ;"
        else:
            sql = f" DELETE FROM {table} WHERE {condition} ;"

        try :
            print("Executed SQL: ", sql)
            self.cursor.execute(sql)
            self._client.commit()
            return True

        except Exception as err_msg:
            print(f"[ERROR] delete_item Error: {err_msg}")
            return False

    def set_info_stock(self):

        response = self.find_item(table='info_stock')
        data_list = list()

        for row in response:
            data_dict = dict()
            data_dict['isin_code'] = row[0]
            data_dict['short_isin_code'] = row[1]
            data_dict['market_category'] = row[2]
            data_dict['item_name'] = row[3]
            data_dict['corp_name'] = row[4]
            data_dict['corp_number'] = row[5]

            if row[6] is not None:
                data_dict['listing_date'] = row[6].strftime("%Y%m%d")
            else:
                data_dict['listing_date'] = None

            data_dict['issue_cnt'] = row[7]
            data_dict['industry'] = row[8]
            data_dict['face_value'] = row[9]

            data_list.append(data_dict)

        with open(FILE_PATH + "info_stock.json", 'w', encoding='UTF-8') as file:
            json.dump(data_list, file, ensure_ascii=False)

    def set_info_financial(self):

        response = self.find_item(table='info_financial')
        data_list = list()

        for row in response:
            data_dict = dict()
            data_dict['isin_code'] = row[0]
            data_dict['bps'] = row[1]
            data_dict['per'] = row[2]
            data_dict['pbr'] = row[3]
            data_dict['eps'] = row[4]
            data_dict['div'] = row[5]
            data_dict['dps'] = row[6]
            data_dict['base_date'] = row[7].strftime("%Y%m%d")

            data_list.append(data_dict)

        with open(FILE_PATH + "info_financials.json", 'w', encoding='UTF-8') as file:
            json.dump(data_list, file, ensure_ascii=False)

    def set_info_news(self):

        response = self.find_item(table='info_news')
        data_list = list()

        for row in response:
            data_dict = dict()
            data_dict['isin_code'] = row[0]
            data_dict['write_date'] = row[1].strftime("%Y%m%d")
            data_dict['headline'] = row[2]
            data_dict['sentiment'] = row[3]

            data_list.append(data_dict)

        with open(FILE_PATH + "info_news.json", 'w', encoding='UTF-8') as file:
            json.dump(data_list, file, ensure_ascii=False)

    def set_info_world_index(self):

        response = self.find_item(table='info_world_index')
        data_list = list()

        for row in response:
            data_dict = dict()
            data_dict['ticker'] = row[0]
            data_dict['nation'] = row[1]
            data_dict['index_name'] = row[2]

            data_list.append(data_dict)

        with open(FILE_PATH + "info_world_index.json", 'w', encoding='UTF-8') as file:
            json.dump(data_list, file, ensure_ascii=False)

    def set_price_konex(self):

        condition = f"base_date = CAST('{BASE_DATE}' AS date)"
        response = self.find_item(table='price_konex', condition=condition)

        data_list = list()

        for row in response:
            data_dict = dict()
            data_dict['base_date'] = row[0].strftime("%Y%m%d")
            data_dict['isin_code'] = row[1]
            data_dict['market_price'] = row[2]
            data_dict['close_price'] = row[3]
            data_dict['high_price'] = row[4]
            data_dict['low_price'] = row[5]
            data_dict['fluctuation'] = row[6]
            data_dict['fluctuation_rate'] = row[7]
            data_dict['volume'] = row[8]

            data_list.append(data_dict)

        with open(FILE_PATH + "price_konex.json", 'w', encoding='UTF-8') as file:
            json.dump(data_list, file, ensure_ascii=False)
    
    def set_price_kosdaq(self):

        condition = f"base_date = CAST('{BASE_DATE}' AS date)"
        response = self.find_item(table='price_kosdaq', condition=condition)

        data_list = list()

        for row in response:
            data_dict = dict()
            data_dict['base_date'] = row[0].strftime("%Y%m%d")
            data_dict['isin_code'] = row[1]
            data_dict['market_price'] = row[2]
            data_dict['close_price'] = row[3]
            data_dict['high_price'] = row[4]
            data_dict['low_price'] = row[5]
            data_dict['fluctuation'] = row[6]
            data_dict['fluctuation_rate'] = row[7]
            data_dict['volume'] = row[8]

            data_list.append(data_dict)

        with open(FILE_PATH + "price_kosdaq.json", 'w', encoding='UTF-8') as file:
            json.dump(data_list, file, ensure_ascii=False)

    def set_prices(self):

        condition = f"base_date = CAST('{BASE_DATE}' AS date)"
        res_kospi = self.find_item(table='price_kospi', condition=condition)
        res_kosdaq = self.find_item(table='price_kosdaq', condition=condition)
        res_konex = self.find_item(table='price_konex', condition=condition)

        data_list = list()

        for row in res_kospi + res_kosdaq + res_konex:
            data_dict = dict()
            data_dict['base_date'] = row[0].strftime("%Y%m%d")
            data_dict['isin_code'] = row[1]
            data_dict['market_price'] = row[2]
            data_dict['close_price'] = row[3]
            data_dict['high_price'] = row[4]
            data_dict['low_price'] = row[5]
            data_dict['fluctuation'] = row[6]
            data_dict['fluctuation_rate'] = row[7]
            data_dict['volume'] = row[8]

            data_list.append(data_dict)

        with open(FILE_PATH + "prices.json", 'w', encoding='UTF-8') as file:
            json.dump(data_list, file, ensure_ascii=False)

    def set_price_world_index(self):

        response = self.find_item(table='price_world_index')
        data_list = list()

        for row in response:
            data_dict = dict()
            data_dict['ticker'] = row[0]
            data_dict['base_date'] = row[1].strftime("%Y%m%d")
            data_dict['market_price'] = row[2]
            data_dict['close_price'] = row[3]
            data_dict['adj_close_price'] = row[4]
            data_dict['high_price'] = row[5]
            data_dict['low_price'] = row[6]
            data_dict['fluctuation'] = row[7]
            data_dict['fluctuation_rate'] = row[8]
            data_dict['volume'] = row[9]

            data_list.append(data_dict)

        with open(FILE_PATH + "price_world_index.json", 'w', encoding='UTF-8') as file:
            json.dump(data_list, file, ensure_ascii=False)

    def set_world_index(self):

        condition = f"base_date = CAST('{'2022-11-11'}' AS date)"
        res_info_world_index = self.find_item(table='info_world_index')
        res_price_world_index = self.find_item(table='price_world_index', condition=condition)

        data_list = list()

        for row_info in res_info_world_index:
            for row_price in res_price_world_index:

                if row_info[0] == row_price[0]:

                    data_dict = dict()
                    data_dict['ticker'] = row_info[0]
                    data_dict['index_name'] = row_info[2]
                    data_dict['close_price'] = str(round(row_price[3],2))
                    data_dict['lat'] = row_info[3]
                    data_dict['lon'] = row_info[4]

                    data_list.append(data_dict)

        with open(FILE_PATH + "world_index.json", 'w', encoding='UTF-8') as file:
            json.dump(data_list, file, ensure_ascii=False)

pgdb = PostgresCore(user='byeong_heon', password='7760lorngn!')

# pgdb.set_info_stock()
# pgdb.set_info_financial()
# pgdb.set_info_news()
# pgdb.set_info_world_index()
# pgdb.set_prices()
pgdb.set_world_index()
# pgdb.set_price_world_index()
