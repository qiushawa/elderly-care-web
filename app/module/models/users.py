from app import db

class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    gender = db.Column(db.String(255), nullable=False)
    birthday = db.Column(db.String(255), nullable=False)
    avatar = db.Column(db.String(255), nullable=True)
    stream_hash = db.Column(db.String(255), nullable=True)
    def __init__(self, name, email, gender, birthday, stream_hash=None):
        self.name = name
        self.email = email
        self.gender = gender
        if not self.check_birthday(birthday): raise ValueError('birthday format error')
        self.birthday = birthday
        self.avatar = None
        self.stream_hash = stream_hash

    def check_birthday(self, birthday:str) -> bool:
        # 檢查生日格式 yyyy-mm-dd
        if len(birthday) != 10: return False
        if birthday[4] != '-' or birthday[7] != '-': return False
        return bool(
            birthday[:4].isnumeric()
            and birthday[5:7].isnumeric()
            and birthday[8:].isnumeric()
        )

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