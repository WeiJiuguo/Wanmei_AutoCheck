import time,json,requests,random,datetime
from campus import CampusCard

def main():
    #sectets字段录入
    phone, password = [], []
    #多人循环录入
    while True:  
        try:
            users = input()
            info = users.split(',')
            phone.append(info[0])
            password.append(info[1])
            #text.append(info[2])
            #sckey.append(info[3])
        except:
            break

    #提交打卡
    for index,value in enumerate(phone):
        print("开始获取用户%sDeptId"%(value[-4:]))
        count = 0
        while (count < 3):
            try:
                campus = CampusCard(phone[index], password[index])
                loginJson = campus.get_main_info()
                token = campus.user_info["sessionId"]
                userInfo=getUserInfo(token) 
                #time.sleep(10)
                response = check_in(userInfo)
                if  response.json()["msg"] == '成功'and index == 0:
                    strTime = GetNowTime()
                    #success.append(value[-4:])
                    print(response.text)
                    msg = value[-4:]+"打卡成功-" + strTime
                    result=response
                    break
                elif response.json()["msg"] == '业务异常'and index == 0:
                    strTime = GetNowTime()
                    #failure.append(value[-4:])
                    print(response.text)
                    msg = value[-4:]+"打卡失败-" + strTime
                    result=response
                    count = count + 1
                elif response.json()["msg"] == '成功':
                    strTime = GetNowTime()
                    #success.append(value[-4:])
                    print(response.text)
                    msg = value[-4:]+"打卡成功-" + strTime
                    break
                else:
                    strTime = GetNowTime()
                    #failure.append(value[-4:])
                    print(response.text)
                    msg = value[-4:] + "打卡异常-" + strTime
                    count = count + 1
                    print('%s打卡失败，开始第%d次重试...'%(value[-6:],count))
                    time.sleep(15)
        
            except:
                msg = "出现错误"
                #failure.append(value[-4:])
                break
        print(msg)
        print("-----------------------")
    #fail = sorted(set(failure),key=failure.index)
    strTime = GetNowTime()
    title = "成功: %s 人,失败: %s 人"%(len(success),len(fail))
    # try:
    #     if  len(sckey[0])>2:
    #         print('主用户开始微信推送...')
    #         WechatPush(title,sckey[0],success,fail,result)
    # except:
    #     print("微信推送出错！")
#时间函数
def GetNowTime():
    cstTime = (datetime.datetime.utcnow() + datetime.timedelta(hours=8))
    strTime = cstTime.strftime("%H:%M:%S")
    return strTime

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
def GetUserJson(userInfo,token):
    #随机温度(36.2~36.8)
    a=random.uniform(36.2,36.8)
    temperature = round(a, 1)
    return  {
        "businessType": "epmpics",
        "method": "submitUpInfoSchool",
        "jsonData": {
        "deptStr": {
            "deptid": userInfo.classId,
            "text": userInfo.classDescription
        },
        #如果你来自其他学校，请自行打卡抓包修改地址字段
        "areaStr": {"streetNumber":"","street":"长椿路辅路","district":"中原区","city":"郑州市","province":"河南省","town":"","pois":"河南工业大学(莲花街校区)","lng":113.55064699999795 + random.random()/1000,"lat":34.83870696238093 + random.random()/1000,"address":"中原区长椿路辅路河南工业大学(莲花街校区)","text":"河南省-郑州市","code":""},
        "reportdate": round(time.time()*1000),
        "customerid": userInfo.customerId,
        "deptid": userInfo.classId,
        "source": "app",
        "templateid": "clockSign2",
        "stuNo": userInfo.stuNo,
        "username": userInfo.username,
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
        "customerAppTypeRuleId": 147,
        "clockState": 0,
        "token": token
        },
        "token": token
    }    

#信息获取函数
def getUserInfo(token):
    token={'token':token}
    sign_url = "https://reportedh5.17wanxiao.com/api/clock/school/getUserInfo"
    #提交打卡
    response = requests.post(sign_url, data=token)
    return response

#打卡提交函数
def check_in(text,stuNum,userName,RuleId,templateid,token):
    deptId = GetDeptId(text)
    sign_url = "https://reportedh5.17wanxiao.com/sass/api/epmpics"
    jsons=GetUserJson(deptId,text,stuNum,userName,RuleId,templateid,token)
    #提交打卡
    response = requests.post(sign_url, json=jsons,)
    return response

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

#微信通知
def WechatPush(title,sckey,success,fail,result):    
    strTime = GetNowTime()
    page = json.dumps(result.json(), sort_keys=True, indent=4, separators=(',', ': '),ensure_ascii=False)
    content = f"""
`{strTime}` 
#### 打卡成功用户：
`{success}` 
#### 打卡失败用户:
`{fail}`
#### 主用户打卡信息:
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
    filename = r'text.json'
    AllClass = GetFromJSON(filename)['data']['classAll']
    main()
