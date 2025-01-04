from functools import wraps
from flask import redirect, request, session
from app.module.const import ErrResponse, HttpStatus
from app.module.models.device import Device
from sqlalchemy.exc import SQLAlchemyError

from app.setting import AppSetting


# 當不可名狀的例外事件發生時，這個函數會試圖將混亂歸於秩序
def handle_exception(e, default_message="未知錯誤"):
    # 若這是一場來自資料庫的災厄
    if isinstance(e, SQLAlchemyError):
        return ErrResponse(
            f"資料庫錯誤: {str(e)}", HttpStatus.INTERNAL_SERVER_ERROR
        ).response
    # 若命運對你隱藏了必要的資料
    elif isinstance(e, KeyError):
        return ErrResponse(f"缺少必要的資料: {str(e)}", HttpStatus.BAD_REQUEST).response
    # 當其他未知的恐怖來襲時
    else:
        return ErrResponse(
            f"{default_message}: {str(e)}", HttpStatus.INTERNAL_SERVER_ERROR
        ).response


# 黑暗之門的守護者——檢查使用者是否已登入
def check_login(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        # 嘗試從遺忘的空間中尋找使用者的靈魂
        user = session.get("user")
        return f(user) if user else redirect(f"/login?next={request.url}")
    return wrapper


# 驗證設備的存在性，確保不與虛無打交道
def check_device(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            # 試圖從深淵中提取設備編號
            id = request.args.get("id")
            if not id:
                return ErrResponse("請提供設備編號", HttpStatus.BAD_REQUEST).response
            # 尋找存在於資料庫中的設備，卻不知這是否會喚醒沉睡的古老力量
            device = Device.query.filter_by(id=id).first()
            if not device:
                return ErrResponse("設備不存在", HttpStatus.NOT_FOUND).response
        except Exception as e:
            # 若在探索過程中觸及禁忌，處理這場災禍
            return handle_exception(e)
        # 若一切看似安然無恙，放行
        return f(*args, **kwargs)

    return wrapper


# 檢查提供的檔案是否為被允許的類型
def allowed_file(filename):
    # 只接受那些符合條件的檔案，其他的則會被拒之門外，仿若亡靈無法穿越聖域
    return "." in filename and filename.rsplit(".", 1)[1].lower() in AppSetting.ALLOWED_EXTENSIONS

