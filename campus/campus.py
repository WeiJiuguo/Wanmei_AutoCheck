import requests
import json
import hashlib
from .campus_card import des_3
from .campus_card import rsa_encrypt as rsa
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class CampusCard:
    """
    完美校园——
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

    @staticmethod
    def __create_blank_user__():
        """
        当传入的已登录设备信息不可用时，虚拟一个空的未登录设备
        :return: 空设备信息
        """
        print("开始虚拟荣耀v30设备")
        rsa_keys = rsa.create_key_pair(1024)
        return {
            'appKey': '10534101',
            'sessionId': '',
            'exchangeFlag': True,
            'login': True,
            'serverPublicKey': '',
            'deviceId': 'ffffffff-fcdd-0ad5-0000-00000033c587',
            'wanxiaoVersion': 10534101,
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
                "User-Agent": "Mozilla/5.0 (Linux; Android 10; OXF-AN00 Build/HUAWEI OXF-AN00; wv) "
                              "AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.108 Mobile "
                              "Safari/537.36 Wanxiao/5.3.4"
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
        print("交换公钥完成")

    def login(self, phone, password):
        """
        使用账号密码登录完美校园

        :param phone: 手机号码
        :param password: 完美校园密码
        :return:
        """
        password_list = []
        for i in password:
            password_list.append(des_3.des_3_encrypt(i, self.user_info["appKey"], "66666666"))
        login_args = {
            "appCode": "S06001",
            "deviceId": self.user_info["deviceId"],
            "netWork": "wifi",
            "password": password_list,
            "qudao": "guanwang",
            "requestMethod": "cam_iface46/loginnew.action",
            "shebeixinghao": "OXF-AN00",
            "systemType": "android",
            "telephoneInfo": "10",
            "telephoneModel": "HUAWEI OXF-AN00",
            "type": "1",
            "userName": phone,
            "wanxiaoVersion": 10534101,
            "yunyingshang": "07"
        }
        upload_args = {
            "session": self.user_info["sessionId"],
            "data": des_3.object_encrypt(login_args, self.user_info["appKey"])
        }
        resp = requests.post(
            "https://server.59wanmei.com/campus/cam_iface46/loginnew.action",
            headers={"campusSign": hashlib.sha256(json.dumps(upload_args).encode('utf-8')).hexdigest(),
                     'User-Agent': "Mozilla/5.0 (Linux; Android 10; OXF-AN00 Build/HUAWEI OXF-AN00; wv) "
                                   "AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.108 Mobile "
                                   "Safari/537.36 Wanxiao/5.3.4"
                     },
            json=upload_args,
            verify=False
        ).json()
        if resp["result_"]:
            print(resp["message_"])
            self.data = resp["data"]
            self.user_info["login"] = True
            self.user_info["exchangeFlag"] = False
        return resp["result_"]

    def get_main_info(self):
        resp = requests.post(
            "https://app.17wanxiao.com/YKT_Interface/xyk",
            headers={
                "Referer": "https://app.17wanxiao.com/YKT_Interface/v2/index.html"
                           "?utm_source=app"
                           "&utm_medium=card"
                           "&customerId=786"
                           "&systemType=Android"
                           "&UAinfo=wanxiao"
                           "&versioncode={args[wanxiaoVersion]}"
                           "&token={args[sessionId]}".format(args=self.user_info),
                "Origin": "https://app.17wanxiao.com",
                "User-Agent": "Mozilla/5.0 (Linux; Android 10; OXF-AN00 Build/HUAWEI OXF-AN00; wv) "
                              "AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.108 Mobile "
                              "Safari/537.36 Wanxiao/5.3.4",
            },
            data={
                "token": self.user_info["sessionId"],
                "method": "XYK_BASE_INFO",
                "param": "{}"
            },
            verify=False
        ).json()
        return json.loads(resp["body"])


def open_device(f):
    device_file = open(f, "r")
    device = json.loads(device_file.read())
    device_file.close()
    return device, f
