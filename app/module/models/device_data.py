from app.module.models.auth import User
from app.module.models.device import Device
from . import db

# 體溫資料表


class TemperatureData(db.Model):
    __tablename__ = "temperature_data"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey("user.id"), nullable=False)
    device_id = db.Column(db.String, db.ForeignKey("device.device_id"), nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    def __init__(self, device_id,user_id, temperature, timestamp):
        self.device_id = device_id
        self.user_id = user_id
        self.temperature = temperature
        self.timestamp = timestamp

    def __repr__(self):
        return "<Temperature: {}, Device ID: {}, Timestamp: {}>".format(
            self.temperature, self.device_id, self.timestamp
        )

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def getAll():
        return [
            {
                "temperature": data.temperature,
                "device_id": data.device_id,
                "timestamp": data.timestamp,
            }
            for data in TemperatureData.query.all()
        ]

    @staticmethod
    def getTemperatureByDevice(device_id):
        return [
            {
                "temperature": data.temperature,
                "device_id": data.device_id,
                "timestamp": data.timestamp,
            }
            for data in TemperatureData.query.filter_by(device_id=device_id).all()
        ]
    
    @staticmethod
    def getTemperatureByUser(user_id):
        return [
            {
                "temperature": data.temperature,
                "device_id": data.device_id,
                "timestamp": data.timestamp,
            }
            for data in TemperatureData.query.filter_by(user_id=user_id).all()
        ]
    
    
#心率資料表
class HeartRateData(db.Model):
    __tablename__ = "heart_rate_data"

    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.String, db.ForeignKey("device.device_id"), nullable=False)
    user_id = db.Column(db.String, db.ForeignKey("user.id"), nullable=False)
    heart_rate = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    
    def __init__(self, device_id,user_id ,heart_rate, timestamp):
        self.device_id = device_id
        self.user_id = user_id
        self.heart_rate = heart_rate
        self.timestamp = timestamp
        
    def __repr__(self):
        return "<Heart Rate: {}, Device ID: {}, Timestamp: {}>".format(
            self.heart_rate, self.device_id, self.timestamp
        )
        
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    @staticmethod
    def getAll():
        return [
            {
                "heart_rate": data.heart_rate,
                "device_id": data.device_id,
                "timestamp": data.timestamp,
            }
            for data in HeartRateData.query.all()
        ]
        
    @staticmethod
    def getHeartRateByDevice(device_id):
        return [
            {
                "heart_rate": data.heart_rate,
                "device_id": data.device_id,
                "timestamp": data.timestamp,
            }
            for data in HeartRateData.query.filter_by(device_id=device_id).all()
        ]
        
    @staticmethod
    def getHeartRateByUser(user_id):
        return [
            {
                "heart_rate": data.heart_rate,
                "device_id": data.device_id,
                "timestamp": data.timestamp,
            }
            for data in HeartRateData.query.filter_by(user_id=user_id).all()
        ]
        
#血氧資料表
class BloodOxygenData(db.Model):
    __tablename__ = "blood_oxygen_data"

    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.String, db.ForeignKey("device.device_id"), nullable=False)
    user_id = db.Column(db.String, db.ForeignKey("user.id"), nullable=False)
    blood_oxygen = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    
    def __init__(self, device_id,user_id,blood_oxygen, timestamp):
        self.device_id = device_id
        self.user_id = user_id
        self.blood_oxygen = blood_oxygen
        self.timestamp = timestamp
        
    def __repr__(self):
        return "<Blood Oxygen: {}, Device ID: {}, Timestamp: {}>".format(
            self.blood_oxygen, self.device_id, self.timestamp
        )
        
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    @staticmethod
    def getAll():
        return [
            {
                "blood_oxygen": data.blood_oxygen,
                "device_id": data.device_id,
                "timestamp": data.timestamp,
            }
            for data in BloodOxygenData.query.all()
        ]
        
    @staticmethod
    def getBloodOxygenByDevice(device_id):
        return [
            {
                "blood_oxygen": data.blood_oxygen,
                "device_id": data.device_id,
                "timestamp": data.timestamp,
            }
            for data in BloodOxygenData.query.filter_by(device_id=device_id).all()
        ]
        
    @staticmethod
    def getBloodOxygenByUser(user_id):
        return [
            {
                "blood_oxygen": data.blood_oxygen,
                "device_id": data.device_id,
                "timestamp": data.timestamp,
            }
            for data in BloodOxygenData.query.filter_by(user_id=user_id).all()
        ]
        
