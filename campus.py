import urllib3
import base64
import hashlib
import json
import random
import requests
from Crypto import Random  # pycryptodome
from Crypto.Cipher import DES3
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Util.Padding import pad

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def des_3_encrypt(string, key,iv):
    cipher = DES3.new(key, DES3.MODE_CBC,iv.encode("utf-8"))
    ct_bytes = cipher.encrypt(pad(string.encode('utf8'), DES3.block_size))
    ct = base64.b64encode(ct_bytes).decode('utf8')
    return ct

def object_encrypt(object_to_encrypt,key,iv="66666666"):
    return des_3_encrypt(json.dumps(object_to_encrypt),key,iv)

def rsa_decrypt(input_string, private_key):
    input_bytes = base64.b64decode(input_string)
    rsa_key = RSA.importKey("-----BEGIN RSA PRIVATE KEY-----\n" + private_key + "\n-----END RSA PRIVATE KEY-----")
    cipher = PKCS1_v1_5.new(rsa_key)
    # noinspection PyArgumentList
    return str(cipher.decrypt(input_bytes, Random.new().read), 'utf-8')

def create_key_pair(size):
    rsa = RSA.generate(size, Random.new().read)
    private_key = str(rsa.export_key(), 'utf8')
    private_key = private_key.split('-\n')[1].split('\n-')[0]
    public_key = str(rsa.publickey().export_key(), 'utf8')
    public_key = public_key.split('-\n')[1].split('\n-')[0]
    return public_key, private_key

def create_info(deviceId):
    rsa_keys = create_key_pair(1024)
    deviceId = deviceId
    public_key = rsa_keys[0]
    private_key = rsa_keys[1]
    return deviceId, public_key, private_key

def exchange_secret(public_key, private_key):
    resp_exch = requests.post(
        "https://app.17wanxiao.com:443/campus/cam_iface46/exchangeSecretkey.action",
        headers={"User-Agent": "Dalvik/2.1.0 (Linux; U; Android 5.1.1; HUAWEI MLA-AL10 Build/HUAWEIMLA-AL10)"},
        json={"key": public_key}
    )
    session_info = json.loads(
        rsa_decrypt(resp_exch.text.encode(resp_exch.apparent_encoding), private_key)
    )
    sessionId = session_info["session"]
    appKey = session_info["key"][:24]
    return sessionId, appKey

def login(phone, password, deviceId, sessionId, appKey):
    password_list = []
    for i in password:
        password_list.append(des_3_encrypt(i, appKey, "66666666"))
    login_args = {
        "appCode": "M002",
        "deviceId": deviceId,
        "netWork": "wifi",
        "password": password_list,
        "qudao": "guanwang",
        "requestMethod": "cam_iface46/loginnew.action",
        "shebeixinghao": "MLA-AL10",
        "systemType": "android",
        "telephoneInfo": "5.1.1",
        "telephoneModel": "HUAWEI MLA-AL10",
        "type": "1",
        "userName": phone,
        "wanxiaoVersion": 10462101,
        "yunyingshang": "07"
    }
    upload_args = {
        "session": sessionId,
        "data": object_encrypt(login_args, appKey)
    }
    resp_login = requests.post(
        "https://app.17wanxiao.com/campus/cam_iface46/loginnew.action",
        headers={"campusSign": hashlib.sha256(json.dumps(upload_args).encode('utf-8')).hexdigest()},
        json=upload_args,
        verify=False
    ).json()
    return resp_login

def campus_start(phone,password,deviceId):
    # 第一步
    create_info_result = create_info(deviceId)
    deviceId = create_info_result[0]
    public_key = create_info_result[1]   
    private_key = create_info_result[2]
    # 第二步
    exchange_secret_result = exchange_secret(public_key, private_key)
    sessionId = exchange_secret_result[0]
    appKey = exchange_secret_result[1]
    try:
        resp_login=login(phone, password, deviceId, sessionId, appKey)
        if '登录成功' in resp_login['message_']:
            print('登录成功')
        else:
            print('登录失败')    
    except Exception as e:
        print('登录出错：')
        print(e.__class__)
    return sessionId
