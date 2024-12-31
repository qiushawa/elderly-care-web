# app/module/docs.py
import os
from app.module.const import Docs
from app.module.util.doc_generator import generate_route_metadata

HOST = "0.0.0.0"
PORT = 5000
DEBUG = True

# 路由文件
ROUTES = [
    "app.module.controller.users",
    "app.module.controller.devices",
    "app.module.controller.docs",
]


# 資料庫設定

# 儲存使用者,裝置資料的資料庫檔案
DATABASE_USER_DEVICE = "db/user_device.db"

# 儲存裝置上傳的資料的資料庫檔案
DATABASE_DEVICE_DATA = "db/device_data.db"


user_register = Docs(
    title="註冊使用者",
    description="註冊使用者",
    example_response={
        "success": True,
        "message": "User has been registered.",
        "data": {
            "user_id": "1234567890",
        },
    },
)
userData = Docs(
    title="取得使用者資料",
    description="回傳使用者的基礎資訊，包含名稱、電子郵件，以及註冊的設備資訊",
    example_response={
        "data": {
            "devices": [],
            "email": "qiushawa@gmail.com",
            "health": {
                "blood_oxygen": [],
                "heartrate": [],
                "temperature": [],
            },
            "id": "1733640721",
            "username": "qiushawa",
        },
        "success": True,
    },
)
device_register = Docs(
    title="註冊裝置",
    description="設備可以在第一次啟動時，向api註冊，註冊後即可綁定使用者",
    example_response={
        "success": True,
        "message": "Device has been registered.",
    },
)

device_bind = Docs(
    title="綁定裝置",
    description="綁定使用者與設備，允許使用者新增設備",
    example_response={
        "success": True,
        "message": "Device has been binded.",
    },
)
update_max30102 = Docs(
    title="上傳設備數據",
    description="透過device_id識別設備型號，將裝置獲取的數據上傳至伺服器，數據是可選參數，請參考參數說明",
    example_response={
        "success": True,
        "message": "Data has been uploaded.",
    },
)

userHealth = Docs(
    title="取得使用者健康資訊",
    description="回傳使用者的健康資訊，包含心率、血氧、血壓等資訊",
    example_response={
        "success": True,
        "data": {
            "heart_rate": 80,
            "blood_oxygen": 98,
            "blood_pressure": "120/80",
        },
    },
)

device_status_get = Docs(
    title="取得裝置狀態",
    description="回傳裝置的狀態，包含是否被穿戴",
    example_response={
        "success": True,
        "data": {
            "status": True,
        },
    },
)

device_status_post = Docs(
    title="更新裝置狀態",
    description="更新裝置的狀態，包含是否被穿戴",
    example_response={
        "success": True,
        "data": {
            "status": True,
        },
    },
)
