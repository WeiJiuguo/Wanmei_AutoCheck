import time
import json
import requests
import random
import datetime

# sectets字段录入
deptId = input()
deptText = input()
areaStr = input()
stuNo = input()
username = input()
userid = input()
sckey = input()

# 时间判断
now = time.localtime().tm_hour + 8
if (now >= 6) & (now < 8):
    templateid = "clockSign1"
    customerAppTypeRuleId = 146
elif (now >= 12) & (now < 18):
    templateid = "clockSign2"
    customerAppTypeRuleId = 147
elif (now >= 21) & (now< 22):
    templateid = "clockSign3"
    customerAppTypeRuleId = 148
else:
    print("现在是%d点%d分，打卡时间将自动打卡" %(now,time.localtime().tm_min))
    exit(0)

# 随机温度(36.2~36.4)
a = random.uniform(36.2, 36.4)
temperature = round(a, 1)

sign_url = "https://reportedh5.17wanxiao.com/sass/api/epmpics"

jsons = {
    "businessType": "epmpics",
    "method": "submitUpInfoSchool",
    "jsonData": {
        "deptStr": {
            "deptid": deptId,
            "text": deptText
        },
        "areaStr": areaStr,
        "reportdate": round(time.time() * 1000),
        "customerid": 43,
        "deptid": deptId,
        "source": "app",
        "templateid": templateid,
        "stuNo": stuNo,
        "username": username,
        "userid": userid,
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
        "customerAppTypeRuleId": customerAppTypeRuleId,
        "clockState": 0
    },
}
# 提交打卡
response = requests.post(sign_url, json=jsons)
utcTime = (datetime.datetime.utcnow() + datetime.timedelta(hours=8))
cstTime = utcTime.strftime("%H时%M分%S秒")
print(response.text)
# 结果判定
if response.json()["msg"] == '成功':
    msg = cstTime + "打卡成功"
else:
    msg = cstTime + "打卡异常"
print(msg)
# 微信通知

title = msg
result = json.dumps(response.json(), sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)
content = f"""
```
{result}
```
"""
data = {
    "text": title,
    "desp": content
}
req = requests.post(sckey, data=data)