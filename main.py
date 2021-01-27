import datetime
import json
import random
import time
import pretty_errors
import requests

from campus import CampusCard


def main():
    phone, password, sckey = [], [], []  # sectets字段多人循环录入
    while True:
        try:
            users = input()
            info = users.split(',')
            phone.append(info[0])
            password.append(info[1])
            sckey.append(info[2])
        except:
            print("sectets字段录入信息完成")
            break
    success, failure = [], []
    for index, value in enumerate(phone):  # 循环提交提交打卡
        print("开始尝试为用户%s打卡" % (value[-4:]))
        count = 0
        while count <= 2:
            str_time = getnowtime()
            try:
                campus = CampusCard(phone[index], password[index])
                token = campus.user_info["sessionId"]
                # base=campus.get_main_info()
                # print(base['name']+"的学生卡硬件ID号为"+base['scardsnr'])
                userInfo = get_user_info(token)
                response = check_in(userInfo, token)
                if response["msg"] == '成功':
                    success.append(userInfo["username"])
                    print(response)
                    msg = str_time + userInfo["username"] + "打卡成功"
                    if index == 0:
                        result = response
                    break
                else:
                    failure.append(value[-4:])
                    print(response)
                    msg = str_time + value[-4:] + "打卡异常"
                    count = count + 1
                    if index == 0:
                        result = response

                    if count <= 2:
                        print('%s打卡失败，开始第%d次重试...' % (value[-4:], count))
                    time.sleep(5)
            except Exception as e:
                print(e.__class__)
                failure.append(value[-4:])
                msg = "打卡出错"
                break
        print(msg)
        print("-----------------------")
    fail = sorted(set(failure), key=failure.index)
    title = "成功: %s 人,失败: %s 人" % (len(success), len(fail))

    try:
        print('主用户开始微信推送...')
        wechatpush(title, sckey[0], success, fail, result)
    except:
        print("微信推送出错！")


def getnowtime():  # 获取现在时间
    csttime = (datetime.datetime.utcnow() + datetime.timedelta(hours=8))
    strTime = csttime.strftime("%H:%M:%S ")
    return strTime


def get_user_json(userInfo, token):  # 打卡参数配置函数
    # 随机温度(36.0~36.6)
    a = random.uniform(36.0, 36.6)
    temperature = round(a, 1)
    return {
        "businessType": "epmpics",
        "method": "submitUpInfo",
        "jsonData": {
            "deptStr": {
                "deptid": userInfo['classId'],
                "text": userInfo['classDescription']
            },
            # 如果你来自其他学校，请自行打卡抓包修改地址字段
            "areaStr": {"streetNumber": "", "street": "崇德路", "district": "天元区", "city": "株洲市", "province": "湖南省",
                        "town": "", "pois": "湖南工业大学新校区", "lng": 113.11425800000013 + random.random() / 1000,
                        "lat": 27.82441698950754 + random.random() / 1000, "address": "天元区崇德路湖南工业大学新校区",
                        "text": "湖南省-株洲市", "code": ""},
            "reportdate": round(time.time() * 1000),
            "customerid": userInfo['customerId'],
            "deptid": userInfo['classId'],
            "source": "app",
            "templateid": "pneumonia",
            "stuNo": userInfo['stuNo'],
            "username": userInfo['username'],
            "phonenum": "13293261470",
            "userid": round(time.time()),
            "updatainfo": [
                {
                    "propertyname": "temperature",
                    "value": temperature
                },
                {
                    "propertyname": "symptom",
                    "value": "无症状"
                },
                {
                    "propertyname": "isConfirmed",
                    "value": "否"
                },
                {
                    "propertyname": "isdefinde",
                    "value": "否.未隔离"
                },
                {
                    "propertyname": "isGoWarningAdress",
                    "value": "否"
                },
                {
                    "propertyname": "isTouch",
                    "value": "否"
                },
                {
                    "propertyname": "isFFHasSymptom",
                    "value": "没有"
                },
                {
                    "propertyname": "isContactFriendIn14",
                    "value": "没有"
                },
                {
                    "propertyname": "xinqing",
                    "value": "健康"
                },
                {
                    "propertyname": "bodyzk",
                    "value": "否"
                },
                {
                    "propertyname": "cxjh",
                    "value": "否"
                },
                {
                    "propertyname": "isleaveaddress",
                    "value": "否"
                },
                {
                    "propertyname": "gtjz0511",
                    "value": "否"
                },
                {
                    "propertyname": "medicalObservation",
                    "value": "绿色"
                },
                {
                    "propertyname": "ownPhone",
                    "value": "13293261470"
                },
                {
                    "propertyname": "emergencyContact",
                    "value": "13293261470"
                },
                {
                    "propertyname": "mergencyPeoplePhone",
                    "value": "13272222656"
                },
                {
                    "propertyname": "assistRemark",
                    "value": ""
                }

            ],
            "gpsType": 1,

            "token": token
        },

    }


def get_user_info(token):  # 打卡信息获取函数
    head = {
        'User-Agent': "Mozilla/5.0 (Linux; Android 10; OXF-AN00 Build/HUAWEIOXF-AN00; wv) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.108 Mobile "
                      "Safari/537.36 Wanxiao/5.3.4"
    }
    info = {'token': token}
    sign_url = "https://reportedh5.17wanxiao.com/api/clock/school/getUserInfo"

    response = requests.post(sign_url, headers=head, data=info).json()
    userInfo=response['userInfo']
    print('正在获取上次打卡JSON信息:')
    return userInfo


def check_in(user_info, token):  # 打卡提交函数
    sign_url = "https://reportedh5.17wanxiao.com/sass/api/epmpics"
    jsons = get_user_json(user_info, token)
    # 提交打卡
    response = requests.post(sign_url, json=jsons).json()
    print("打卡提交状态:" + response['msg'])
    if response['code']=='10006':
        print(response['data'])
    return response


def wechatpush(title, sckey, success, fail, result):  # 微信通知
    str_time = getnowtime()
    page = json.dumps(result.json(), sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)
    content = f"""
`{str_time}` 
#### 打卡成功用户：
`{success}` 
#### 打卡失败用户:
`{fail}`
#### 主用户打卡信息:
```
{page}
```


        """

    data0 = {
        "text": title,
        "desp": content
    }
    scurl = 'https://sc.ftqq.com/' + sckey + '.send'
    try:
        req = requests.post(scurl, data=data0)
        if req.json()["errmsg"] == 'success':
            print("Server酱推送服务成功")
        else:
            print("Server酱推送服务失败")
    except Exception:
        print("微信推送参数错误")


'''
    data1 = {
        "token": "10f179ec7405a6426d87b0e42b3aca51",
        "group_id": "698639533",
        "message": "大家早上好呀，今早已经打卡成功的用户如下:\n" + str(success) + "\n打卡失败用户手机的后4位尾号如下:\n" + str(
            fail) + "\n请打卡出问题的小伙伴联系下小高同学，没打卡的小伙伴尽快打卡。"

    }
    qq_url = 'http://api.qqpusher.yanxianjun.com/send_group_msg'
    try:
        req = requests.post(qq_url, data1)
        print(req.json())
        if req.json()['status'] == True:
            print("QQ推送成功")
        else:
            print("QQ推送失败")
    except:
        print("QQ推送参数错误")

'''
if __name__ == '__main__':
    main()
