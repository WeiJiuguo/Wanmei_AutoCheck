import time,json,requests,random,datetime
import campus

def main():
    phone, password, sckey = [], [], []
    #多人循环录入
    while True:  
        try:
            users = input()
            info = users.split(',')
            phone.append(info[0])
            password.append(info[1])
            sckey.append(info[2])
        except:
            break

    #提交打卡
    for index,value in enumerate(phone):
        print("开始尝试为用户%s打卡"%(value[-4:]))
        count = 0
        while (count <= 3):
            try:
                token = campus.campus_start(phone[index],password[index])
                print(token)
            except Exception as e:
                print(e.__class__)


if __name__ == '__main__':
    mark = 1
    main()
