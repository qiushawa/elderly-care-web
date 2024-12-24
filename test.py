

import requests,time, random
import json
base_url = 'https://api.qiushawa.me/api/v1/'


# 模擬註冊使用者
def register(username, password, email):
    url = base_url + 'users/register'
    headers = {'Content-Type': 'application/json'}
    data = {
        "body": {
        "username": username,
        "password": password,
        "email": email
        }
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()["data"]["user_id"]

# 模擬註冊裝置
def register_device(device_id, device_name):
    url = base_url + 'devices/register'
    headers = {'Content-Type': 'application/json'}
    data = {
        "body": {
        "device_id": device_id,
        "device_name": device_name
        }
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.text)

# 模擬綁定裝置
def bind_device(device_id, user_id):
    url = base_url + 'devices/bind'
    headers = {'Content-Type': 'application/json'}
    data = {
        "body": {
        "device_id": device_id,
        "user_id": user_id
        }
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.text)
    
# 模擬MAX30102定時上傳數據




def upload_data(device_id, data):
    url = base_url + 'update/' + str(device_id)
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=data, headers=headers)
    print(response.text)
    
    
# # 註冊使用者
# user_id = register("qiushawa", "dewef", "qiushawa@gmail.com")
# print(user_id)

# # 註冊裝置
# register_device("1234567890", "MAX30102")

# # 綁定裝置
# bind_device("1234567890", user_id)

# 上傳數據
while True:
    data = {
        "body": {
            "heartrate": random.randint(60, 100),
            "spo2": random.randint(95, 100)
        }
    }
    upload_data("1234567890", data)