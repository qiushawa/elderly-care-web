from app.module.models import User, HeartRateData, TemperatureData, BloodOxygenData,Device
from app.module.const import HttpStatus

# __init__ 檔案中的 app

from flask import Blueprint, request, jsonify

from ..util.doc_generator import parameters, route_with_description, url_parameters
from ...setting import *

bp = Blueprint("users", __name__, url_prefix="/api/v1/users")


# register
@route_with_description(
    bp,
    "/register",
    ["POST"],
    user_register.title,
    user_register.description,
    user_register.example_response,
)
@parameters("username", str, "使用者名稱")
@parameters("password", str, "使用者密碼")
@parameters("email", str, "使用者電子郵件")
def register(username, password, email):
    construct = {}
    try:
        user = User(username=username, password=password, email=email)
        user.save()
        construct["success"] = True
        construct["message"] = "User has been registered."
        construct["data"] = {"user_id": user.id}
        response = jsonify(construct)
        response.status_code = HttpStatus.CREATED
    except Exception as e:
        construct["success"] = False
        construct["error"] = str(e)
        response = jsonify(construct)
        response.status_code = HttpStatus.BAD_REQUEST
    return response


@route_with_description(
    bp,
    "/<int:user_id>",
    ["GET"],
    userData.title,
    userData.description,
    userData.example_response,
)
@url_parameters("user_id", int, "使用者 ID")
def userData(user_id):
    req = request.args.get("request")
    user = User.query.filter_by(id=user_id).first()
    construct = {}
    if user is None:
        construct["success"] = False
        construct["message"] = "User not found."
        response = jsonify(construct)
        response.status_code = HttpStatus.NOT_FOUND
        return response
    construct["success"] = True
    data = {}
    if req is None:
        # Return all user information
        heartRateData = HeartRateData.query.filter_by(user_id=user_id).all()
        temperatureData = TemperatureData.query.filter_by(user_id=user_id).all()
        bloodOxygenData = BloodOxygenData.query.filter_by(user_id=user_id).all()
        data["username"] = user.username
        data["email"] = user.email
        data["id"] = user.id
        data["devices"] = [
            {
                "id": device.device_id,
                "name": device.device_name,
            }
            for device in user.devices
        ]
        data["health"] = {
            "temperature": [
                {
                    "value": data.temperature,
                    "timestamp": data.timestamp,
                }
                for data in temperatureData
            ],
            "blood_oxygen": [
                {
                    "value": data.blood_oxygen,
                    "timestamp": data.timestamp,
                }
                for data in bloodOxygenData
            ],
            "heartrate": [
                {
                    "value": data.heart_rate,
                    "timestamp": data.timestamp,
                }
                for data in heartRateData
            ],
        }
    elif req == "health":
        # Return only health information
        heartRateData = HeartRateData.query.filter_by(user_id=user_id).all()
        temperatureData = TemperatureData.query.filter_by(user_id=user_id).all()
        bloodOxygenData = BloodOxygenData.query.filter_by(user_id=user_id).all()
        data["health"] = {
            "temperature": [
                {
                    "value": data.temperature,
                    "timestamp": data.timestamp,
                }
                for data in temperatureData
            ],
            "blood_oxygen": [
                {
                    "value": data.blood_oxygen,
                    "timestamp": data.timestamp,
                }
                for data in bloodOxygenData
            ],
            "heartrate": [
                {
                    "value": data.heart_rate,
                    "timestamp": data.timestamp,
                }
                for data in heartRateData
            ],
        }
    if req == "device":
        # Return only device information
        data["devices"] = [
            {
                "id": device.device_id,
                "name": device.device_name,
            }
            for device in user.devices
        ]
    construct["data"] = data
    response = jsonify(construct)
    response.status_code = HttpStatus.OK
    return response
