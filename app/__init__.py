"""
主應用程式模組

此模組設定 Flask 應用程式，並初始化相關擴展（CORS、SQLAlchemy、Migrate）。
此外，定義了全局錯誤處理器，並載入應用程式所需的其他模組。

模組功能概述：
1. 初始化 Flask 應用程式及相關配置。
2. 啟用 CORS（跨來源資源共享）。
3. 使用 SQLAlchemy 作為 ORM 工具進行資料庫交互。
4. 提供全局的 404（頁面未找到）和 500（伺服器內部錯誤）錯誤處理。
5. 動態載入模型與控制器模組。

模組：
- `flask`：核心 Flask 框架，用於構建網頁應用程式。
- `flask_cors`：提供 CORS 支援，允許跨來源的 HTTP 請求。
- `flask_sqlalchemy`：ORM 工具，簡化資料庫操作。
- `flask_migrate`：提供資料庫遷移功能。
- `app.setting`：自定義應用程式設定模組。

屬性：
- app (Flask): Flask 應用程式實例。
- db (SQLAlchemy): ORM 資料庫實例。
- migrate (Migrate): 資料庫遷移管理工具。

全局錯誤處理：
- 404 錯誤：頁面未找到。
- 500 錯誤：伺服器內部錯誤。

模組加載：
- `app.module.models`：載入資料庫模型。
- `app.module.controller`：載入應用程式控制器。
"""


from flask import Flask, render_template, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.module.util.stream_manager import StreamManager, StreamState
from app.setting import AppSetting

# 初始化 Flask 應用程式，並設定靜態檔案資料夾
app = Flask(__name__, static_folder="static")

# 啟用 CORS，允許跨來源請求
CORS(app, supports_credentials=True)


for key in dir(AppSetting):
    if not key.startswith("__") and key.isupper():  # 過濾非公有屬性與大寫屬性
        app.config[key] = getattr(AppSetting, key)
# 設定會話密鑰及有效時間
app.secret_key = app.config["SESSION_KEY"]  # 設定會話密鑰
app.permanent_session_lifetime = app.config["SESSION_EXPIRES"]  # 設定會話有效時間

# 初始化資料庫及遷移工具
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# 初始化串流管理器
state:StreamState= StreamState()
manager:StreamManager = StreamManager(state)

# 全局錯誤處理：404 錯誤（頁面未找到）
@app.errorhandler(404)
def not_found_error(e):
    """
    處理 404 錯誤的回呼函式

    Args:
        e (Exception): 捕獲的例外物件

    Returns:
        Tuple[Response, int]: 錯誤頁面及 HTTP 狀態碼
    """
    return (
        render_template(
            "error.html",
            error_code=404,
            error_message="頁面未找到",
            previous_page=request.referrer,
        ),
        404,
    )

# 全局錯誤處理：500 錯誤（伺服器內部錯誤）
@app.errorhandler(500)
def internal_error(e):
    """
    處理 500 錯誤的回呼函式

    Args:
        e (Exception): 捕獲的例外物件

    Returns:
        Tuple[Response, int]: 錯誤頁面及 HTTP 狀態碼
    """
    return (
        render_template(
            "error.html",
            error_code=500,
            error_message="伺服器內部錯誤",
            previous_page=request.referrer,
        ),
        500,
    )

# 引入應用程式的模組
from app.module.models import *  # 資料模型
from app.module.controller import *  # 控制器
