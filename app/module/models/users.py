from app import db

class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    gender = db.Column(db.String(255), nullable=False)
    birthday = db.Column(db.String(255), nullable=False)

    def __init__(self, name, email, gender, birthday):
        self.name = name
        self.email = email
        self.gender = gender
        if not self.check_birthday(birthday): raise ValueError('birthday format error')
        self.birthday = birthday

    def check_birthday(self, birthday:str) -> bool:
        # 檢查生日格式 yyyy-mm-dd
        if len(birthday) != 10: return False
        if birthday[4] != '-' or birthday[7] != '-': return False
        if not birthday[:4].isnumeric() or not birthday[5:7].isnumeric() or not birthday[8:].isnumeric(): return False
        return True

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    # get user by email
    @staticmethod
    def get_user(email):
        return Users.query.filter_by(email=email).first()
    
    def __repr__(self):
        return f'<Users {self.name}>'