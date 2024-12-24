import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# 獲取專案目錄
project_dir = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
CORS(app)

# 設定資料庫連接配置
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///{}".format(os.path.join(project_dir, 'db/app.db'))
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# 初始化 db 和 migrate
from app.module.models import db
db.init_app(app)
migrate = Migrate(app, db)

from app.module.models import *
from app.module.controller import *