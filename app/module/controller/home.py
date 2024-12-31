from flask import Blueprint, render_template
from flask import session
from flask import request
from app.module.models import Auth, Users
bp = Blueprint('home', __name__, url_prefix='/')

@bp.route('/', methods=['GET'])
def home_page():
    user = session.get('user')
    if user:return render_template('index.html', login_status=True, user=user)
    return render_template('index.html', login_status=False)