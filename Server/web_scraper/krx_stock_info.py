# 금융위원회_KRX상장종목정보
# https://www.data.go.kr/data/15094775/openapi.do

import requests
import pprint
import json

OPEN_DATA_URL = "http://apis.data.go.kr/1160100/service/GetKrxListedInfoService/getItemInfo"
serviceKey = "uZEPxYU1hcKy6To5Hex%2ByxoSPBqrjzpFi9DeHCmI3b%2FovyQR3HbAcBQQG1RtKJpp5vRJ7ChiL%2B4HqCwEsXjoJQ%3D%3D"

OPEN_DATA_URL += "?serviceKey="
OPEN_DATA_URL += serviceKey
response = requests.get(OPEN_DATA_URL)

contents = response.text
pp = pprint.PrettyPrinter(indent=4)
print(pp.pprint(contents))