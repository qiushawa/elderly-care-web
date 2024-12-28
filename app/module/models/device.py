from . import db

class Device(db.Model):
    __tablename__ = 'device'

    device_id = db.Column(db.String, unique=True, primary_key=True, nullable=False)
    device_name = db.Column(db.String, nullable=False)
    users = db.relationship(
        'User',
        secondary='user_device',
        back_populates='devices',
        lazy='dynamic'
    )
    status = db.Column(db.Boolean, default=False)
    def __init__(self, device_id, device_name):
        self.device_id = device_id
        self.device_name = device_name
        self.status = False

    def __repr__(self):
        return "<Device Name: {}, Device ID: {}>".format(self.name, self.id)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def getAll():
        return [{'device_id': device.device_id, 'device_name': device.device_name} for device in Device.query.all()]

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    # check status
    def check_status(self):
        return self.status
    
    # update status
    def update_status(self, status):
        self.status = status
        self.save()
        return self.status
    
