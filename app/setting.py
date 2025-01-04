# The `AppSetting` class centralizes and manages various configuration parameters for an application,
# including project directory, server settings, file upload configurations, database settings, session
# management, and file upload directory.
import os
from datetime import timedelta

class AppSetting:
    """
    AppSetting 是一個應用程式的設定類別，負責集中管理各項設定參數。
    
    屬性:
        PROJECT_DIR (str): 專案目錄的絕對路徑。
        HOST (str): 伺服器綁定的主機地址，預設為 "0.0.0.0"。
        PORT (int): 伺服器埠號，預設為 3000。
        DEBUG (bool): 是否啟用調試模式，預設為 True。
        # The `ALLOWED_EXTENSIONS` attribute in the `AppSetting` class is defining a set that contains
        # the file extensions that are allowed for file uploads in the application. In this case, the
        # allowed file extensions are 'png', 'jpg', 'jpeg', and 'gif'. This set restricts the types of
        # files that can be uploaded to only those with these specified extensions.
        ALLOWED_EXTENSIONS (set): 允許上傳的檔案副檔名集合。
        SQLALCHEMY_DATABASE_URI (str): SQLite 資料庫的連接 URI。
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): 是否啟用資料庫的變更追蹤，預設為 False。
        SESSION_TYPE (str): Session 儲存方式，預設為 "sqlalchemy"。
        SESSION_SQLALCHEMY_TABLE (str): 儲存 Session 的資料表名稱，預設為 "session"。
        SESSION_EXPIRES (timedelta): Session 過期時間，預設為 30 天。
        SESSION_KEY (str): Session 的密鑰，從環境變數讀取，若無則使用 "default-secret-key"。
        UPLOAD_FOLDER (str): 上傳檔案的目錄路徑，預設為 "static/images/avatars"。
    """

    # 獲取專案目錄
    PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

    # 伺服器設定
    HOST = "0.0.0.0"  # 預設綁定至所有網絡介面
    PORT = 3000  # 預設伺服器埠號
    DEBUG = True  # 啟用調試模式

    # 檔案上傳設定
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # 設定允許的檔案副檔名

    # 資料庫設定
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(PROJECT_DIR, 'db/app.db')}"  # SQLite 資料庫路徑
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 關閉資料庫追蹤，提升效能

    # Session 設定
    SESSION_TYPE = "sqlalchemy"  # 使用 SQLAlchemy 儲存 Session
    SESSION_SQLALCHEMY_TABLE = "session"  # 儲存 Session 的資料表名稱
    SESSION_EXPIRES = timedelta(days=30)  # Session 過期時間設定為 30 天
    SESSION_KEY = os.environ.get("SESSION_KEY", "default-secret-key")  # 從環境變數讀取 Session Key，無設定則使用預設值

    # 上傳檔案設定
    UPLOAD_FOLDER = os.path.join(PROJECT_DIR, 'static/images/avatars')  # 設定檔案上傳的目錄

# 定義模組導出內容
__all__ = [
    'AppSetting'
]
