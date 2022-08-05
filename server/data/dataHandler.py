# Open API 데이터 로드 모듈
# https://www.data.go.kr (공공데이터포털)

# Author  : Byeong Heon Lee
# Contact : lww7438@gmail.com

import requests

def get_data(service_url : str, params : dict):

    # Set URL with Parameters
    request_url = service_url + '?'
    for k, v in params.items():
        request_url += k + '=' + v + '&'

    # Request Query
    response = requests.get(request_url[:-1]) # Eliminate last '&' character 

    return response

def merge(df1 : dict, df2: dict, key : str):
    pass