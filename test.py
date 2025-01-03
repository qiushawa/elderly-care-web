# 註冊設備

import requests
import json

def test_register_device():
    url = "http://localhost:3000/device/register"
    data = {
        "id": "0987654321",
        "name": "Max30102",
        "type": "Max30102"
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)
    print(response.json())
    
test_register_device()