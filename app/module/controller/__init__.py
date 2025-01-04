from app import app
from app.module.controller import auth, devices, home, physiological, stream

# *******************************************************
# * Register Blueprint
# *******************************************************

app.register_blueprint(home.bp)
app.register_blueprint(auth.bp)
app.register_blueprint(devices.bp)
app.register_blueprint(physiological.bp)
app.register_blueprint(stream.bp)