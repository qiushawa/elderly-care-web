from app.module.models import Device, User
from app.module.const import HttpStatus

# __init__ 檔案中的 app

from flask import Blueprint, request, jsonify

from ...setting import device_register, device_bind, device_status_get, device_status_post
from ..util.doc_generator import route_with_description, parameters, url_parameters

bp = Blueprint("devices", __name__, url_prefix="/api/v1/devices")


# register
@route_with_description(
    bp,
    "/register",
    ["POST"],
    device_register.title,
    device_register.description,
    device_register.example_response,
)
@parameters("device_id", str, "裝置 ID")
@parameters("device_name", str, "裝置名稱")
def register(device_id, device_name):
    construct = {}
    try:
        device = Device(device_id, device_name)
        device.save()
        construct["success"] = True
        construct["message"] = "Device has been registered."
        response = jsonify(construct)
        response.status_code = HttpStatus.CREATED
    except Exception as e:
        construct["success"] = False
        construct["error"] = str(e)
        response = jsonify(construct)
        response.status_code = HttpStatus.BAD_REQUEST
    return response


# bind
@route_with_description(
    bp,
    "/bind",
    ["POST"],
    device_bind.title,
    device_bind.description,
    device_bind.example_response,
)
@parameters("device_id", str, "裝置 ID")
@parameters("user_id", int, "使用者 ID")
def bind(device_id, user_id):
    device = Device.query.filter_by(device_id=device_id).first()
    user = User.query.filter_by(id=user_id).first()
    construct = {}
    if device is None or user is None:
        construct["success"] = False
        construct["message"] = "Device or User not found."
        response = jsonify(construct)
        response.status_code = HttpStatus.NOT_FOUND
        return response
    device.users.append(user)
    device.save()
    construct["success"] = True
    construct["message"] = "Device has been binded."
    response = jsonify(construct)
    response.status_code = HttpStatus.CREATED
    return response
@route_with_description(
    bp,
    "/status",
    ["GET"],
    device_status_get.title,
    device_status_get.description,
    device_status_get.example_response,
)
@url_parameters("device_id", str, "裝置 ID")
def status_get(device_id):
    user = User.query.filter_by(device_id=device_id).first()
    construct = {}
    if user is None:
        construct["success"] = False
        construct["message"] = "此裝置尚未綁定使用者"
        response = jsonify(construct)
        response.status_code = HttpStatus.NOT_FOUND
        return response
    Device = Device.query.filter_by(device_id=device_id).first()
    if Device is None:
        construct["success"] = False
        construct["message"] = "此裝置不存在"
        response = jsonify(construct)
        response.status_code = HttpStatus.NOT_FOUND
        return response
    now_status = Device.check_status()
    if now_status == False:
        # 使用者沒有穿戴裝置
        construct["success"] = True
        construct["message"] = "使用者未穿戴裝置"
        response = jsonify(construct)
        response.status_code = HttpStatus.OK
        return response
    else:
        # 使用者穿戴裝置
        construct["success"] = True
        construct["message"] = "使用者已穿戴裝置"
        response = jsonify(construct)
        response.status_code = HttpStatus.OK
        return response

# update status
@route_with_description(
    bp,
    "/status",
    ["POST"],
    device_status_post.title,
    device_status_post.description,
    device_status_post.example_response,
)
@parameters("device_id", str, "裝置 ID")
@parameters("status", bool, "裝置狀態")
def status_post(device_id, status):
    Device = Device.query.filter_by(device_id=device_id).first()
    construct = {}
    if Device is None:
        construct["success"] = False
        construct["message"] = "此裝置不存在"
        response = jsonify(construct)
        response.status_code = HttpStatus.NOT_FOUND
        return response
    now_status = Device.update_status(status)
    construct["success"] = True
    construct["message"] = "裝置狀態已更新"
    response = jsonify(construct)
    response.status_code = HttpStatus.OK
    return response