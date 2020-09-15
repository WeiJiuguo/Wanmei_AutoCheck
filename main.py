import time
import json
import requests
import random
import datetime
import os

#sectets字段录入
text = input()
userName = input()
stuNum = input()
sckey = input()

#json读取函数
def GetFromJSON(filename): 
    flag = False
    idStr={} 
    path = os.getcwd()
    try:
        j_file=open(filename,'r', encoding='utf8')
        idStr=json.load(j_file)
        flag=True
    except:
        print('从%s读取JSON数据出错！'%filename)
    finally:
        if flag:
            j_file.close()
    return idStr

#读取text.json文件
filename = r'text.json'
jsonDic = GetFromJSON(filename)
AllClass = jsonDic['data']['classAll']

def main():
    #获取班级
    try:
        TextStr = text.split('-', 3)
        ClassName = TextStr[2] 
    # 获取deptId
    except:
        print("获取失败")
    try:
        for Class in AllClass:
            if (Class['name'] == ClassName):
                deptId = Class['deptId']
        if deptId:
            print('获取deptId成功!')
    except:
        print("获取deptId失败！")
        exit(1)
    
    #随机温度(36.2~36.8)
    a=random.uniform(36.2,36.8)
    temperature = round(a, 1)

    #早中午判断
    nowTime = (time.localtime().tm_hour + 8) % 24
    if (nowTime >= 6) & (nowTime < 8):
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

    sign_url = "https://reportedh5.17wanxiao.com/sass/api/epmpics"

    jsons =  {
    "businessType": "epmpics",
    "method": "submitUpInfoSchool",
    "jsonData": {
        "deptStr": {
            "deptid": deptId,
            "text": text
        },
        "areaStr": {"streetNumber":"","street":"长椿路辅路","district":"中原区","city":"郑州市","province":"河南省","town":"","pois":"河南工业大学(莲花街校区)","lng":113.55064699999795 + random.random()/1000,"lat":34.83870696238093 + random.random()/1000,"address":"中原区长椿路辅路河南工业大学(莲花街校区)","text":"河南省-郑州市","code":""},
        "reportdate": round(time.time()*1000),
        "customerid": "43",
        "deptid": deptId,
        "source": "app",
        "templateid": templateid,
        "stuNo": stuNum,
        "username": userName,
        "userid": round(time.time()),
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

    #时间获取
    cstTime = (datetime.datetime.utcnow() + datetime.timedelta(hours=8))
    strTime = cstTime.strftime("%H:%M:%S")

    #提交打卡
    count = 0
    while (count < 3):
        response = requests.post(sign_url, json=jsons)
        if response.json()["msg"] == '成功':
            print(response.text)
            msg = "打卡成功-" + strTime
            break
        else:
            print(response.text)
            msg = "打卡异常-" + strTime
            count = count + 1
            print('打卡失败，开始第%d次重试...'%(count))
            time.sleep(15)
    print(msg)

    #微信通知
    def WechatPush(msg):    
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
        if req.json()["errmsg"] == 'success':
            print("Server酱推送服务成功")
        else:
            print("Server酱推送服务失败")

    if  msg:
        WechatPush(msg)

if __name__ == '__main__':
    main()
