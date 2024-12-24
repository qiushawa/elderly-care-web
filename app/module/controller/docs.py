

from flask import Blueprint, render_template

from app.module.util.doc_generator import generate_route_metadata
bp = Blueprint('docs', __name__, url_prefix='/docs')



@bp.route('/', methods=['GET'])
def api_documentation():
    from ..controller import users, devices, update
    # return render_template('index.html', api_data=api_data)
    data={
        "Users": {
            f"/users{users.register.route}":generate_route_metadata(users.register),
            f"/users{users.userData.route}":generate_route_metadata(users.userData),
        },
        "Devices": {
            f"/devices{devices.register.route}":generate_route_metadata(devices.register),
            f"/devices{devices.bind.route}":generate_route_metadata(devices.bind)
        },
        "Update": {
            f"/update{update.update_data.route}":generate_route_metadata(update.update_data)
        }
    }
    return render_template('index.html', api_data=data)