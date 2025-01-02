import os
from app.module.const import Docs

HOST = "0.0.0.0"
PORT = 5000
DEBUG = True



# 儲存使用者,裝置資料的資料庫檔案
DATABASE_USER_DEVICE = "db/user_device.db"

# 儲存裝置上傳的資料的資料庫檔案
DATABASE_DEVICE_DATA = "db/device_data.db"

# session 設定
SESSION_KEY = os.urandom(24) #  session key
SESSION_EXPIRES = 60 * 60 * 24 * 30 # session 過期時間 30 天
SESSION_STORAGE = "db/session.db"

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}