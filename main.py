import time
import json
import requests
import random
import datetime

#sectets字段录入
deptId = eval(input())
text = input()
userName = input()
stuNum = input()
userId = input()

#随机温度(36.2~36.8)
a=random.uniform(36.2,36.8)
temperature = round(a, 1)

#时间获取
cstTime = (datetime.datetime.utcnow() + datetime.timedelta(hours=8))
strTime = cstTime.strftime("%H:%M:%S")

#reqURl
sign_url = "https://reportedh5.17wanxiao.com/sass/api/epmpics"

#早中午判断
nowTime = time.localtime().tm_hour + 8
if (nowTime >= 30) & (nowTime < 32):
    templateid = "clockSign1"
    RuleId = 146
elif (nowTime >= 12) & (nowTime < 14):
    templateid = "clockSign2"
    RuleId = 147
elif (nowTime >= 21) & (nowTime< 22):
    templateid = "clockSign3"
    RuleId = 148
else:
    print("现在时间%d点%d分，打卡时间未到！" %(nowTime,time.localtime().tm_min))
    exit(0)

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
        "templateid": templateid,
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
        "customerAppTypeRuleId": RuleId,
        "clockState": 0
    },
}    

#提交打卡
response = requests.post(sign_url, json=jsons)
print(response.text)

#结果判定
if response.json()["msg"] == '成功':
        msg = "打卡成功-" + strTime
else:
        msg = "打卡异常-" + strTime
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
