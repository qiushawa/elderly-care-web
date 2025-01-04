from flask import Blueprint, request, render_template
from app.module.util.validators import check_device, check_login, handle_exception
from app.module.models import Device
from app.module.const import ErrResponse, HttpStatus, SuccessResponse

bp = Blueprint("device", __name__, url_prefix="/device")


@bp.route("/register", methods=["POST"])
def register_device():
    try:
        data = request.json
        device = Device(id=data["id"], name=data["name"], type=data["type"])
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
def device_status():  # sourcery skip: avoid-builtin-shadow
    try:
        id = request.args.get("id")
        device = Device.query.filter_by(id=id).first()
        if request.method == "GET":
            return SuccessResponse(
                "取得設備狀態成功", device.status, HttpStatus.OK
            ).response
        
        data = request.json
        device.status = data["status"]
        device.save()
        return SuccessResponse(
            "更新設備狀態成功", device.status, HttpStatus.OK
        ).response
    except Exception as e:
        return handle_exception(e)


@bp.route("/owner/register", methods=["POST"])
@check_device
@check_login
def bind_device(user):  # sourcery skip: avoid-builtin-shadow
    try:
        # 從請求中取得設備 ID
        id = request.args.get("id")
        device = Device.query.filter_by(id=id).first()

        # 取得提交的表單資料
        data = request.form
        # 更新設備名稱（如果提供了新的名稱）
        if new_name := data.get("name", "").strip():
            device.name = new_name

        # 綁定設備所有者
        device.set_owner(user["email"])
        device.save()

        # 返回成功回應
        return render_template("success.html", message="設備綁定成功", next_page="/")

    except Exception as e:
        # 處理例外並返回適當的錯誤回應
        return handle_exception(e)


# bind page
@bp.route("/bind", methods=["GET"])
@check_login
def bind_page(user):  # sourcery skip: avoid-builtin-shadow
    id = request.args.get("id")
    if not id:
        return render_template(
            "error.html",
            error_message="請提供設備編號",
            error_code=HttpStatus.BAD_REQUEST,
            previous_page=request.referrer,
        )
    if not (device := Device.query.filter_by(id=id).first()):
        return render_template(
            "error.html",
            error_message="設備不存在",
            error_code=HttpStatus.NOT_FOUND,
            previous_page=request.referrer,
        )
    if device.owner:
        return render_template(
            "error.html",
            error_message="設備已綁定",
            error_code=HttpStatus.FORBIDDEN,
            previous_page=request.referrer,
        )
    return render_template("bind.html", user=user, device=device)
