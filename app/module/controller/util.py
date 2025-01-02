from functools import wraps
from flask import redirect, request, session
from app.module.const import ErrResponse, HttpStatus
from app.module.models.device import Device
from sqlalchemy.exc import SQLAlchemyError

def handle_exception(e, default_message="未知錯誤"):
    if isinstance(e, SQLAlchemyError):
        return ErrResponse(
            f"資料庫錯誤: {str(e)}", HttpStatus.INTERNAL_SERVER_ERROR
        ).response
    elif isinstance(e, KeyError):
        return ErrResponse(f"缺少必要的資料: {str(e)}", HttpStatus.BAD_REQUEST).response
    else:
        return ErrResponse(
            f"{default_message}: {str(e)}", HttpStatus.INTERNAL_SERVER_ERROR
        ).response

# 重新定向 next page 裝飾器
def check_login(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        user = session.get("user")
        if not user:
            return redirect("/login?next=" + request.url)
        return f(user)
    return wrapper

def check_device(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            id = request.args.get("id")
            if not id:
                return ErrResponse("請提供設備編號", HttpStatus.BAD_REQUEST).response
            device = Device.query.filter_by(id=id).first()
            if not device:
                return ErrResponse("設備不存在", HttpStatus.NOT_FOUND).response
        except Exception as e:
            return handle_exception(e)
        return f(*args, **kwargs)

    return wrapper