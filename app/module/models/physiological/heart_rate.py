from datetime import datetime
from app import db

class HeartRate(db.Model):
    """
    ## 心率資料表
    
    ### Attributes
    - id: 資料編號 (唯一)
    - device_id: 裝置編號
    - user_id: 使用者編號
    - value: 心率值
    - timestamp: 資料時間
    
    ### Method
    - save(): 儲存心率資料
    - delete(): 刪除心率資料
    
    """
    __tablename__ = 'heart_rate'
    
    id = db.Column(db.Integer, primary_key=True) # 資料編號 (唯一)
    device_id = db.Column(db.String(255), nullable=False) # 裝置編號
    email = db.Column(db.String(255), nullable=False) # 使用者編號
    value = db.Column(db.Float, nullable=False) # 心率值
    timestamp = db.Column(db.DateTime, nullable=False) # 資料時間
    
    def __init__(self, device_id, email, value):
        self.device_id = device_id
        self.email = email
        self.value = value
        self.timestamp = datetime.now()
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'value': self.value,
            'timestamp': self.timestamp.isoformat()
        }
    
    def __repr__(self):
        return f'<HeartRate {self.value}>'