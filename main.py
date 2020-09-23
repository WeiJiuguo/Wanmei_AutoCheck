import time
import json
import requests
import random
import datetime
import os

#json读取函数
def GetFromJSON(filename): 
    flag = False
    idStr={} 
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
    #sectets字段录入
    userName = []
    stuNum = []
    text = []
    sckey = []
    success = []
    failure = []
    result = {"msg":"主用户打卡出错"}
    #多人循环录入
    while True:  
        try:
            users = input()
            info = users.split(',')
            userName.append(info[0])
            stuNum.append(info[1])
            text.append(info[2])
            sckey.append(info[3])
        except:
            break
    #早中午判断
    nowTime = (time.localtime().tm_hour + 8 ) % 24
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

    #提交打卡
    for index,value in enumerate(stuNum):
        cstTime = (datetime.datetime.utcnow() + datetime.timedelta(hours=8))
        strTime = cstTime.strftime("%H:%M:%S")
        print("开始获取用户%sDeptId"%(value[-6:]))
        count = 0
        while (count < 3):
            try:
                response = check_in(text[index],stuNum[index],userName[index],RuleId,templateid)
                if  response.json()["msg"] == '成功':
                    success.append(value[-6:])
                    print(response.text)
                    msg = value[-6:]+"打卡成功-" + strTime
                    result=response
                    break
                else:
                    failure.append(value[-6:])
                    print(response.text)
                    msg = value[-6:] + "打卡异常-" + strTime
                    count = count + 1
                    print('%s打卡失败，开始第%d次重试...'%(value[-6:],count))
                    time.sleep(15)
                
            except:
                print("服务器错误！")
                failure.append(value[-6:])
        print(msg)
        print("-----------------------")
    fail = sorted(set(failure),key=failure.index)
    title = strTime + "%s人打卡成功,%s人打卡失败!"%(len(success),len(fail)) 
    if  len(sckey[0])>2:
        print('主用户开始微信推送...')
        WechatPush(title,sckey[0],success,fail,result)

#班级获取函数
def GetDeptId(text):
    try:
        TextStr = text.split('-', 3)
        ClassName = TextStr[2] 
    # 获取deptId
    except:
        print("获取失败，请检查格式")
    try:
        for Class in AllClass:
            if (Class['name'] == ClassName):
                deptId = Class['deptId']
        if deptId:
            print('获取deptId成功!')
    except:
        print("获取deptId失败！")
        exit(1)
    return deptId
#打卡参数配置函数
def GetUserJson(deptId,text,stuNum,userName,RuleId,templateid):
    #随机温度(36.2~36.8)
    a=random.uniform(36.2,36.8)
    temperature = round(a, 1)
    return  {
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
#打卡提交函数
def check_in(text,stuNum,userName,RuleId,templateid):
    deptId = GetDeptId(text)
    sign_url = "https://reportedh5.17wanxiao.com/sass/api/epmpics"
    jsons=GetUserJson(deptId,text,stuNum,userName,RuleId,templateid)
    #提交打卡
    response = requests.post(sign_url, json=jsons)
    return response

#微信通知
def WechatPush(title,sckey,success,fail,result):    
    page = json.dumps(result.json(), sort_keys=True, indent=4, separators=(',', ': '),ensure_ascii=False)
    content = f"""
### 打卡成功用户：
```
{success}
```    
### 打卡失败用户:
```
{fail}
```
### 主用户打卡信息:
```
{page}
```
### 😀[收藏](https://github.com/YooKing/HAUT_autoCheck)此项目

        """
    data = {
            "text":title,
            "desp":content
    }
    try:
        req = requests.post(sckey,data = data)
        if req.json()["errmsg"] == 'success':
            print("Server酱推送服务成功")
        else:
            print("Server酱推送服务失败")
    except:
        print("微信推送参数错误")
if __name__ == '__main__':
    main()
