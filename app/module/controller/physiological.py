from flask import Blueprint, render_template, request, session
from app.module.models.device import Device
from app.module.models.users import Users
from app.module.models.physiological.blood_oxygen import BloodOxygen
from app.module.models.physiological.heart_rate import HeartRate
from app.module.util import validators
from app.module import const
bp = Blueprint("physio", __name__, url_prefix="/physio")

@bp.route("/", methods=["GET"])
@validators.check_login
def physio_page(user):
    return render_template('physio.html', user=user)

# 上傳生理資料
@bp.route("/upload", methods=["POST"])
@validators.check_device
def upload_physio():

    try:
        # 從請求中取得設備 ID
        id = request.args.get("id")
        device:Device = Device.query.filter_by(id=id).first()
        if not device:
            return const.ErrResponse("設備不存在", const.HttpStatus.NOT_FOUND).response
        data = request.json
        # 處理生理資料的上傳
        if data["type"] == "blood_oxygen":
            blood_oxygen_data = BloodOxygen(id, device.owner, data["value"])
            blood_oxygen_data.save()
            return const.SuccessResponse("血氧資料上傳成功", None, const.HttpStatus.CREATED).response
        elif data["type"] == "heart_rate":
            heart_rate_data = HeartRate(id, device.owner, data["value"])
            heart_rate_data.save()
            return const.SuccessResponse("心率資料上傳成功", None, const.HttpStatus.CREATED).response
        else:
            return const.ErrResponse("未知的生理資料類型", const.HttpStatus.BAD_REQUEST).response
    except Exception as e:
        # 處理例外並返回適當的錯誤回應
        return validators.handle_exception(e)

@bp.route("/get_physio", methods=["GET"])
@validators.check_device
def get_physio():
    user = session.get("user")
    if not user:
        return const.ErrResponse("使用者未登入", const.HttpStatus.UNAUTHORIZED).response
    
    # 顯示幾筆資料
    limit = request.args.get("limit")
    try:
        user = Users.query.filter_by(id=user['id']).first()
        if not user:
            return const.ErrResponse("使用者不存在", const.HttpStatus.NOT_FOUND).response
        # 取得生理資料
        blood_oxygen_data = BloodOxygen.query.filter_by(email=user.email).order_by(BloodOxygen.timestamp.desc()).limit(limit).all()
        heart_rate_data = HeartRate.query.filter_by(email=user.email).order_by(HeartRate.timestamp.desc()).limit(limit).all()
        return const.SuccessResponse("生理資料取得成功", 
            {
                "blood_oxygen": [data.serialize() for data in blood_oxygen_data],
                "heart_rate": [data.serialize() for data in heart_rate_data]
            },
            const.HttpStatus.OK
            ).response
    except Exception as e:
        return validators.handle_exception(e)
    