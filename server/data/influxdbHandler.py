
# influxdbHandler.py
# https://influxdb-python.readthedocs.io/en/latest/api-documentation.html#influxdbclient (API Documentation of InfluxDB)

# Author  : Byeong Heon Lee
# Contact : lww7438@gmail.com
 
import influxdb_client, os, time

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client.client.write_api import ASYNCHRONOUS

class InfluxDBHandler:

  def __init__(self, connection_url, token, org):
    self._client = InfluxDBClient(url=connection_url, token=token, org=org)

  def insert_item(self, data, params:dict=None, expected_response_code:int=204, protocol:str=u'json' ):
    """
    Write data to InfluxDB.

    Parameters:	
    data : the data to be written
    params (dict) : additional parameters for the request, defaults to None
    expected_response_code (int) : the expected response code of the write operation, defaults to 204
    protocol (str) : protocol of input data, either ‘json’ or ‘line’

    Returns:	
    True, if the write operation is successful

    Return type:	
    bool
    """

    return self._client.write(data, params, expected_response_code, protocol)

  def insert_items(self, points, database,  retention_policy, protocol, consistency, time_precision=None, tags=None, batch_size=None):
    """
    1개 이상의 Time Series Names를 저장한다.
    
    [Parameters]	
    points           : Database에 저장할 Points들의 List (list of dictionaries, each dictionary represents a point)
    database         : Point를 저장할 Database의 이름 (str) (default=<client's current database>)
    retention_policy : Point들에 대한 저장정책 (str) (default=<client's current using retention policy>)
    protocol         : 데이터를 저장할 때 사용할 프로토콜 ('line' | 'json) (str)
    consistency      : Point들에 대한 Consistency ('any' | 'one' | 'quorum' | 'all') (str)
    time_precision   : 시간 단위 (‘s’ | ‘m’ | ‘ms’ | ‘u’) (str) (default=None)
    tags             : Key-Value Pairs로 구성된 각각의 Point들. Key와 Value의 타입은 반드시 string. 이들은 Tag들과 공유되며 Point-Specific Tag들과 합쳐질 수 있음. (dict) (default=None)
    batch_size       : 한꺼번에 저장할 Point의 개수. 대량의 Point들을 저장하거나 한 Database에서 다른 Database로 Data들을 Dump시키기에 용이함. (int) (default=None)
    
    [Returns]
    result : write_points()가 성공적으로 수행되었는지에 대한 여부 (bool)
    """

    write_api = self._client.write_api(write_options=SYNCHRONOUS)

    return write_api.write_points(points, time_precision, database, retention_policy, tags, batch_size, protocol, consistency)
  

  def find_item():
    pass

  def find_items():
    pass

  def delete_items():
    pass

  def update_item():
    pass

  def update_items():
    pass

  def aggregate():
    pass

  def get_databases(self):
    return self._client.get_list_database()

  def get_measurements(self):
    return self._client.get_list_measurements()

  def get_continuous_queries(self):
    return self._client.get_list_continuous_queries()

  def get_retention_policies(self, databaseName=None):
    return self._client.get_list_retention_policies(database=databaseName)

  def get_series(self, databaseName=None, measurementName=None, tagsName=None):
    return self._client.get_list_series(database=databaseName, measurement=measurementName, tags=tagsName)
