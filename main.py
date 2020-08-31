import time
import json
import requests
import random
import os

#sectets字段录入
deptId = eval(input())
text = input()
emergencyNum = input()
phoneNum = input()
userName = input()
stuNum = input()
userId = input()
dormNum = input()
homeTown = input()
personNum = input()
homeAddress = input()
local = input()
sex = "男"
area = {'address':homeAddress,'text':local,'code':""}
areaStr = json.dumps(area, ensure_ascii=False)

#随机温度(36.2~36.8)
a=random.uniform(36.2,36.8)
temperature = round(a, 1)

sign_url = "https://reportedh5.17wanxiao.com/sass/api/epmpics"

jsons =  {
    "businessType": "epmpics",
    "method": "submitUpInfo",
    "jsonData": {
        "deptStr": {
            "deptid": deptId,
            "text": text
        },
        "areaStr": areaStr,
        "reportdate": round(time.time()*1000),
        "customerid": "43",
        "deptid": deptId,
        "source": "app",
        "templateid": "pneumonia",
        "stuNo": stuNum,
        "username": userName,
        "phonenum": phoneNum,
        "userid": userId,
        "updatainfo": [
            {
                "propertyname": "isGoWarningAdress",
                "value": sex
            },
            {
                "propertyname": "jtdz",
                "value": homeTown
            },
            {
                "propertyname": "personNO",
                "value": personNum
            },
            {
                "propertyname": "langtineadress",
                "value": homeAddress
            },
            {
                "propertyname": "ownPhone",
                "value": phoneNum
            },
            {
                "propertyname": "emergencyContact",
                "value": emergencyNum
            },
            {
                "propertyname": "tradeNum",
                "value": dormNum
            },
            {
                "propertyname": "temperature",
                "value": temperature
            },
            {
                "propertyname": "symptom",
                "value": "均无"
            },
            {
                "propertyname": "isContactpatient",
                "value": "均无"
            },
            {
                "propertyname": "istouchcb",
                "value": "否"
            },
            {
                "propertyname": "isTransitProvince",
                "value": "否"
            },
            {
                "propertyname": "isTouch",
                "value": "否"
            },
            {
                "propertyname": "backadress",
                "value": ""
            },
            {
                "propertyname": "isContactFriendIn14",
                "value": "否"
            },
            {
                "propertyname": "sxaddress",
                "value": ""
            },
            {
                "propertyname": "medicalObservation",
                "value": "否"
            },
            {
                "propertyname": "sxss",
                "value": ""
            },
            {
                "propertyname": "isConfirmed",
                "value": "否"
            },
            {
                "propertyname": "assistRemark",
                "value": ""
            },
            {
                "propertyname": "gyfh",
                "value": "否"
            },
            {
                "propertyname": "FamilyIsolate",
                "value": ""
            },
            {
                "propertyname": "ishborwh",
                "value": "否"
            },
            {
                "propertyname": "IsHospitaltxt",
                "value": ""
            },
            {
                "propertyname": "fhhb",
                "value": "否"
            },
            {
                "propertyname": "isname",
                "value": ""
            },
            {
                "propertyname": "other1",
                "value": ""
            },
            {
                "propertyname": "isFFHasSymptom",
                "value": "是"
            }
        ],
        "gpsType": 1
    }
}                       
response = requests.post(sign_url, json=jsons)
print(response.text)
result = json.dumps(response.json(), sort_keys=True, indent=4, separators=(',', ': '),ensure_ascii=False)
if response.json()["msg"] == '成功':
        msg = "检测到打卡成功！"
else:
        msg = "出现异常！"
sckey = input()
title = "打卡结果通知"
content = f"""
```
{result}

```
{msg}
[收藏](https://github.com/YooKing/HAUT_autoCheck)此项目
"""
data = {
"text":title,
"desp":content
}
req = requests.post(sckey,data = data)
