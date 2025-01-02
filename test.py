# 註冊設備

import requests
import json

def test_register_device():
    url = "https://eldercare.qiushawa.me/device/register"
    data = {
        "id": "1234567890",
        "name": "ESP32",
        "type": "ESP32"
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)
    print(response.json())
    
test_register_device()