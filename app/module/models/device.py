from app import db

class Device(db.Model):
    """
    ## 裝置資料表
    
    ### Attributes
    - id: 裝置編號 (唯一)
    - name: 裝置名稱 (使用者可自訂)
    - type: 裝置類型 (ex: ESP32, MAX30102)
    - status: 裝置狀態 (active, inactive)
    - owner: 裝置擁有者 (使用者 id)
    
    ### Method
    - save(): 儲存裝置資料
    - delete(): 刪除裝置資料
    - set_owner(owner): 設定裝置擁有者

    """
    __tablename__ = 'device'
    
    id = db.Column(db.String(255), primary_key=True) # 裝置編號 (唯一)
    name = db.Column(db.String(255), nullable=False) # 裝置名稱 (使用者可自訂)
    type = db.Column(db.String(255), nullable=False) # 裝置類型 (ex: ESP32, MAX30102)
    status = db.Column(db.String(255), nullable=False) # 裝置狀態 (active, inactive)
    owner = db.Column(db.String(255), nullable=True) # 裝置擁有者 (使用者 email)
    
    def __init__(self, id, name, type, status="inactive", owner=None):
        self.id = id
        self.name = name
        self.type = type
        self.status = status # 判斷裝置是否被配帶 (配帶為"active", 未配帶為"inactive")
        self.owner = owner
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def set_owner(self, owner):
        self.owner = owner
        self.save()
    
    def __repr__(self):
        return f'<Device {self.name}>'
