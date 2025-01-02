from flask import Blueprint, render_template
from flask import session
from app.module.models import Users

bp = Blueprint("home", __name__, url_prefix="/")


@bp.route("/", methods=["GET"])
def home_page():
    avatar = None
    if session.get("user"):
        avatar = Users.query.filter_by(name=session.get("user")["name"]).first().avatar
    return render_template(
        "index.html", login_status=bool(session.get("user")), avatar=avatar, user=session.get("user")
    )
