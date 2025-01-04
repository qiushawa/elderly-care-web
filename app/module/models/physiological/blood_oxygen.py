from app import db

class BloodOxygen(db.Model):
    """
    ## 血氧資料表
    
    ### Attributes
    - id: 資料編號 (唯一)
    - device_id: 裝置編號
    - user_id: 使用者編號
    - value: 血氧值
    - timestamp: 資料時間
    
    ### Method
    - save(): 儲存血氧資料
    - delete(): 刪除血氧資料
    
    """
    __tablename__ = 'blood_oxygen'
    
    id = db.Column(db.Integer, primary_key=True) # 資料編號 (唯一)
    device_id = db.Column(db.String(255), nullable=False) # 裝置編號
    user_id = db.Column(db.String(255), nullable=False) # 使用者編號
    value = db.Column(db.Float, nullable=False) # 血氧值
    timestamp = db.Column(db.DateTime, nullable=False) # 資料時間
    
    def __init__(self, device_id, user_id, value, timestamp):
        self.device_id = device_id
        self.user_id = user_id
        self.value = value
        self.timestamp = timestamp
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def __repr__(self):
        return f'<BloodOxygen {self.value}>'