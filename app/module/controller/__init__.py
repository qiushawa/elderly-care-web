from app import app
from app.module.controller import auth, devices, home

# *******************************************************
# * Register Blueprint
# *******************************************************

app.register_blueprint(home.bp)
app.register_blueprint(auth.bp)
app.register_blueprint(devices.bp)