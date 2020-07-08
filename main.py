import time
import json
import requests

deptId = eval(input())
text = input()
emergencyNum = input()

area = {'address': address, 'text': addtext, 'code': "430321"}
areaStr = json.dumps(area, ensure_ascii=False)

sign_url = "https://reportedh5.17wanxiao.com/sass/api/epmpics"

with open('info.json', 'r') as f:
    json = json.load(f)
       
response = requests.post(sign_url, json=json)
print(response.text)

