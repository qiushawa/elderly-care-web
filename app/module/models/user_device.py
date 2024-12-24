from . import db

# UserDevice 模型作為中介表
class UserDevice(db.Model):
    __tablename__ = 'user_device'

    user_id = db.Column(db.String(10), db.ForeignKey('user.id'), primary_key=True)
    device_id = db.Column(db.String, db.ForeignKey('device.device_id'), primary_key=True)