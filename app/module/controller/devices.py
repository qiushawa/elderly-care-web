from app.module.models import Device, User
from app.module.const import HttpStatus

# __init__ 檔案中的 app

from flask import Blueprint, request, jsonify

from ...setting import device_register, device_bind
from ..util.doc_generator import route_with_description, parameters

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
