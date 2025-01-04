from flask import Blueprint, Response, jsonify, render_template
from flask import session
from app.module.models import Users, Device
from app import manager, state
from app.module.util import ffmpeg, tcp, validators

bp = Blueprint("stream", __name__, url_prefix="/stream")


@bp.route("/add_stream/<device_id>", methods=["POST"])
def add_stream(device_id):
    """新增一個串流"""
    device:Device = Device.query.filter_by(id=device_id).first()
    device_owner:Users = Users.query.filter_by(email=device.owner).first()
    stream_id = device_owner.stream_hash
    message, status = manager.add_stream(stream_id, tcp.server, ffmpeg.server)
    return jsonify({"message": message}), status


@bp.route("/remove_stream/<device_id>", methods=["DELETE"])
def remove_stream(device_id):
    """移除一個串流"""
    device:Device = Device.query.filter_by(id=device_id).first()
    device_owner:Users = Users.query.filter_by(email=device.owner).first()
    stream_id = device_owner.stream_hash
    message, status = manager.remove_stream(stream_id)
    return jsonify({"message": message}), status


@bp.route("/video_feed/<stream_id>")
def video_feed(stream_id):
    """提供指定 stream_id 的串流"""
    user = session.get("user")
    if not user:
        return jsonify({"message": "Unauthorized"}), 401
    if user["stream_hash"] != stream_id:
        return jsonify({"message": "Forbidden"}), 403
    
    
    def generate():
        while True:
            frame = state.get_stream(stream_id)
            lock = state.get_lock(stream_id)
            if frame and lock:
                with lock:
                    yield (
                        b"--frame\r\n"
                        b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
                    )
            else:
                yield (
                    b"--frame\r\n"
                    b"Content-Type: text/plain\r\n\r\nStream not found\r\n"
                )

    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")


# stream page
@bp.route("/")
@validators.check_login
def stream_page(user):
    """串流頁面"""
    return render_template("stream.html", id=user["stream_hash"])
