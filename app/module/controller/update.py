from app.module.const import HttpStatus
from app.module.models import TemperatureData, BloodOxygenData, HeartRateData
from app.module.models.device import Device
from app.setting import update_max30102
from ..util.doc_generator import parameters, route_with_description, url_parameters
from flask import Blueprint, request, jsonify
from datetime import datetime

bp = Blueprint("update", __name__, url_prefix="/api/v1/update")

# 在確保資安的情況下，可以透過此 API 上傳設備獲取的數據


# Max30102
@route_with_description(
    bp,
    "/<int:device_id>",
    ["POST"],
    update_max30102.title,
    update_max30102.description,
    update_max30102.example_response,
)
@url_parameters("device_id", int, "設備 ID, 用於識別設備, 放置在 URL 中")
@parameters("heartrate", int, "心率", required=False)
@parameters("spo2", int, "血氧", required=False)

def update_data(device_id, heartrate=None, pressure=None, spo2=None):
    construct = {}
    try:
        # 檢查設備是否存在
        device = Device.query.filter_by(device_id=device_id).first()
        if device is None:
            raise ValueError("Device not found.")
        # 檢查數據是否存在
        user_id = device.users.first().id
        if heartrate is not None:
            data = HeartRateData(device_id,user_id,heartrate, datetime.now())
            data.save()
        if spo2 is not None:
            data = BloodOxygenData(device_id,user_id, spo2, datetime.now())
            data.save()

        construct["success"] = True
        construct["message"] = "Data has been updated."
        response = jsonify(construct)
        response.status_code = HttpStatus.CREATED
    except Exception as e:
        construct["success"] = False
        construct["error"] = str(e)
        response = jsonify(construct)
        response.status_code = HttpStatus.BAD_REQUEST
    return response