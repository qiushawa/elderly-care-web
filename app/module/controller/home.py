from flask import Blueprint, render_template
from flask import session

bp = Blueprint('home', __name__, url_prefix='/')

@bp.route('/', methods=['GET'])
def home_page():
    return render_template('index.html', login_status=bool(session.get('user')), user=session.get('user'))