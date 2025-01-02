from flask import Flask, render_template, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from flask_session import Session  # Flask-Session 用於儲存 session
from . import setting

# 獲取專案目錄
project_dir = os.path.dirname(os.path.abspath(__file__))

# 創建 Flask 應用
app = Flask(__name__)
CORS(app)

# 設定 session key
app.secret_key = os.urandom(24)

# 設定 session 過期時間
app.permanent_session_lifetime = setting.SESSION_EXPIRES

# 設定資料庫連接配置
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(project_dir, 'db/app.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# 初始化 SQLAlchemy 和 Migrate
db = SQLAlchemy(app)  # 在這裡初始化 SQLAlchemy
migrate = Migrate(app, db)
if not os.path.exists(os.path.join(project_dir, 'db/app.db')):
    db.create_all()
# 配置 Flask-Session
app.config["SESSION_TYPE"] = "sqlalchemy"
app.config["SESSION_SQLALCHEMY"] = db
app.config["SESSION_SQLALCHEMY_TABLE"] = "session"
Session(app)

@app.errorhandler(404)
def not_found_error(e):
    return render_template(
        "error.html", 
        error_code=404, 
        error_message="頁面未找到", 
        previous_page=request.referrer
    ), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template(
        "error.html", 
        error_code=500, 
        error_message="伺服器內部錯誤", 
        previous_page=request.referrer
    ), 500

# 導入模型
from app.module.models import *

# 導入路由
from app.module.controller import *