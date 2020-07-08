import time
import json
import requests

base_url = "https://reportedh5.17wanxiao.com/sass/api/epmpics"

text = input()
address = input()
addtext = input()
deptId = eval(input())
userId = 9022415
stuNum = 201812010301
userName = 王宇坤
phoneNum = 15538550843

area = {'address': address, 'text': addtext, 'code': "430321"}

areaStr = json.dumps(area, ensure_ascii=False)

json = {"businessType": "epmpics", "method": "submitUpInfo",}
       
response = requests.post(base_url, json=json)
print(response.text)

