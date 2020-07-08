import time
import json
import requests

base_url = "https://reportedh5.17wanxiao.com/sass/api/epmpics"

with open('info.json', 'r') as f:
    json = json.load(f)
       
response = requests.post(base_url, json=json)
print(response.text)

