

from flask import Blueprint, render_template
from ...setting import docs_data
from app.module.util.doc_generator import generate_route_metadata
bp = Blueprint('docs', __name__, url_prefix='/docs')



@bp.route('/', methods=['GET'])
def api_documentation():
    from ..controller import users, devices, update
    return render_template('docs.html', api_data=docs_data)