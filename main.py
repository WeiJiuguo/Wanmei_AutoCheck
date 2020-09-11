import time
import json
import requests
import random
import datetime

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

#随机温度(36.2~36.8)
a=random.uniform(36.2,36.8)
temperature = round(a, 1)

sign_url = "https://reportedh5.17wanxiao.com/sass/api/epmpics"

jsons =  {
    "businessType": "epmpics",
    "method": "submitUpInfoSchool",
    "jsonData": {
        "deptStr": {
            "deptid": deptId,
            "text": text
        },
        "areaStr": "{\"streetNumber\":\"\",\"street\":\"长椿路辅路\",\"district\":\"中原区\",\"city\":\"郑州市\",\"province\":\"河南省\",\"town\":\"\",\"pois\":\"河南工业大学(莲花街校区)\",\"lng\":113.55064699999795,\"lat\":34.83870696238093,\"address\":\"中原区长椿路辅路河南工业大学(莲花街校区)\",\"text\":\"河南省-郑州市\",\"code\":\"\"}",
        "reportdate": round(time.time()*1000),
        "customerid": "43",
        "deptid": deptId,
        "source": "app",
        "templateid": "clockSign2",
        "stuNo": stuNum,
        "username": userName,
        "userid": userId,
        "updatainfo": [  
            {
                "propertyname": "temperature",
                "value": temperature
            },
            {
                "propertyname": "symptom",
                "value": "无症状"
            }
        ],
        "customerAppTypeRuleId": 147,
        "clockState": 0
    },
}                       
#提交打卡
response = requests.post(sign_url, json=jsons)
utcTime = (datetime.datetime.utcnow() + dateti/me.timedelta(hours=8))
cstTime = utcTime.strftime("%H:%M:%S")
print(response.text)
#结果判定
if response.json()["msg"] == '成功':
        msg = "打卡成功-" + cstTime
else:
        msg = "打卡异常-" + cstTime
print(msg)
#微信通知
sckey = input()
title = msg
result = json.dumps(response.json(), sort_keys=True, indent=4, separators=(',', ': '),ensure_ascii=False)
content = f"""
```
{result}
```
### 😀[收藏](https://github.com/YooKing/HAUT_autoCheck)此项目
"""
data = {
"text":title,
"desp":content
}
req = requests.post(sckey,data = data)
