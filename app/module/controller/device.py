from flask import Blueprint,  request
from app.module.models import Device
from app.module.const import HttpStatus, ErrResponse, SuccessResponse
from sqlalchemy.exc import SQLAlchemyError

bp = Blueprint("device", __name__, url_prefix="/device")

def handle_exception(e, default_message="未知錯誤"):
    if isinstance(e, SQLAlchemyError):
        return ErrResponse(f"資料庫錯誤: {str(e)}", HttpStatus.INTERNAL_SERVER_ERROR).response
    elif isinstance(e, KeyError):
        return ErrResponse(f"缺少必要的資料: {str(e)}", HttpStatus.BAD_REQUEST).response
    else:
        return ErrResponse(f"{default_message}: {str(e)}", HttpStatus.INTERNAL_SERVER_ERROR).response

def check_device(f):
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

@bp.route("/register", methods=["POST"])
def register_device():
    try:
        data = request.json
        device = Device(
            id=data["id"], name=data["name"], type=data["type"]
        )
        #{
        #   "id": "123456
        #   "name": "device1",
        #   "type": "sensor",
        #}
        device.save()
        data = {
            "id": device.id,
            "name": device.name,
            "type": device.type,
            "status": device.status,
        }
        return SuccessResponse("設備註冊成功", data, HttpStatus.CREATED).response
    except Exception as e:
        return handle_exception(e)


@bp.route("/status", methods=["GET", "POST"])
@check_device
def device_status():
    try:
        id = request.args.get("id")
        device = Device.query.filter_by(id=id).first()
        if request.method == "GET":
            return SuccessResponse("取得設備狀態成功", device.status, HttpStatus.OK).response
        else:
            data = request.json
            device.status = data["status"]
            device.save()
            return SuccessResponse("更新設備狀態成功", device.status, HttpStatus.OK).response
    except Exception as e:
        return handle_exception(e)
