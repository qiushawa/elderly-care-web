from flask import Blueprint, render_template
from app.module.util.doc_generator import generate_route_metadata
bp = Blueprint('index', __name__, url_prefix='/index')


@bp.route('/', methods=['GET'])
def html_index():
    return render_template("front_index.html")