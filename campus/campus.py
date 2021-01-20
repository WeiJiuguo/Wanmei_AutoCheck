import requests, random, json, hashlib
from .campus_card import des_3
from .campus_card import rsa_encrypt as rsa
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class CampusCard:
    """
    完美校园APP
    初始化时需要传入手机号码、密码、用户信息（如果有）
    """
    data = None

    def __init__(self, phone, password, user_info=(None, '{}.info')):
        """
        初始化一卡通类
        :param phone: 完美校园账号
        :param password: 完美校园密码
        :param user_info: 已登录的虚拟设备
        """
        self.user_info = user_info[0] if user_info[0] else self.__create_blank_user__()
        if self.user_info['exchangeFlag']:
            self.exchange_secret()
            self.login(phone, password)
        
        """
        with open(user_info[1].format(phone), 'w') as f:
            f.write(self.save_user_info())
        """
    @staticmethod
    def __create_blank_user__():
        """
        当传入的已登录设备信息不可用时，虚拟一个空的未登录设备
        :return: 空设备信息
        """
        rsa_keys = rsa.create_key_pair(1024)
        return {
            'appKey': '',
            'sessionId': '',
            'exchangeFlag': True,
            'login': False,
            'serverPublicKey': '',
            'deviceId': str(random.randint(999999999999999, 9999999999999999)),
            'wanxiaoVersion': 10531102,
            'rsaKey': {
                'private': rsa_keys[1],
                'public': rsa_keys[0]
            }
        }

    def exchange_secret(self):
        """
        与完美校园服务器交换RSA加密的公钥，并取得sessionId
        :return:
        """
        resp = requests.post(
            "https://app.17wanxiao.com:443/campus/cam_iface46/exchangeSecretkey.action",
            headers={
                "User-Agent": "NCP/5.3.1 (iPhone; iOS 13.5; Scale/2.00)",
            },
            json={
                "key": self.user_info["rsaKey"]["public"]
            },
            verify=False
        )
        session_info = json.loads(
            rsa.rsa_decrypt(resp.text.encode(resp.apparent_encoding), self.user_info["rsaKey"]["private"])
        )
        self.user_info["sessionId"] = session_info["session"]
        self.user_info["appKey"] = session_info["key"][:24]

    def login(self, phone, password):
        """
        使用账号密码登录完美校园APP
        :param phone: 完美校园APP绑定的手机号码
        :param password: 完美校园密码
        :return:
        """
        password_list = []
        for i in password:
            password_list.append(des_3.des_3_encrypt(i, self.user_info["appKey"], "66666666"))
        login_args = {
            "appCode": "M002",
            "deviceId": self.user_info["deviceId"],
            "netWork": "wifi",
            "password": password_list,
            "qudao": "guanwang",
            "requestMethod": "cam_iface46/loginnew.action",
            "shebeixinghao": "iPhone12",
            "systemType": "iOS",
            "telephoneInfo": "13.5",
            "telephoneModel": "iPhone",
            "type": "1",
            "userName": phone,
            "wanxiaoVersion": 10531102,
            "yunyingshang": "07"
        }
        upload_args = {
            "session": self.user_info["sessionId"],
            "data": des_3.object_encrypt(login_args, self.user_info["appKey"])
        }
        resp = requests.post(
            "https://app.17wanxiao.com/campus/cam_iface46/loginnew.action",
            headers={"campusSign": hashlib.sha256(json.dumps(upload_args).encode('utf-8')).hexdigest()},
            json=upload_args,
            verify=False
        ).json()
        if resp["result_"]:
            self.data = resp["data"]
            self.user_info["login"] = True
            self.user_info["exchangeFlag"] = False
        return resp["result_"]

    #如果不请求一下token会失效
    def get_main_info(self):
        resp = requests.post(
            "https://reportedh5.17wanxiao.com/api/clock/school/getUserInfo",
            headers={
                "Referer": "https://reportedh5.17wanxiao.com/health/index.html?templateid=pneumonia&businessType=epmpics&versioncode=10531102&systemType=IOS&UAinfo=wanxiao&token="+self.user_info["sessionId"],   
                "Origin": "https://reportedh5.17wanxiao.com",
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E149 Wanxiao/5.3.1"
                   
            },
            data={
                "appClassify": "DK",
                "token": self.user_info["sessionId"],
            },
            verify=False
        ).json()
        if resp["msg"] == '成功':
            return resp["userInfo"]
        print(resp)
        return resp

    def save_user_info(self):
        """
        保存当前的设备信息
        :return: 当前设备信息的json字符串
        """
        return json.dumps(self.user_info)


def open_device(f):
    try:
        device_file = open(f, "r")
        device = json.loads(device_file.read())
        device_file.close()
    except:
        device = None
    return device, f



