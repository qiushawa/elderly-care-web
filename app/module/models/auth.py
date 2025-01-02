from app import db
import bcrypt

# 密碼表
class Auth(db.Model):
    __tablename__ = 'auth'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = self._encryption(password)

    def _encryption(self, password:str) -> str:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    def check_password(self, password:str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), self.password)
    
    def save(self) -> 'Auth':
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self) -> 'Auth':
        db.session.delete(self)
        db.session.commit()
        return self
    
    def __repr__(self):
        return f'<Auth {self.email}>'
