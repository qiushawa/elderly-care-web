from app.module.models import user_device
from . import db
import bcrypt
import time


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.String(10), unique=True, primary_key=True, nullable=False, default=lambda: str(int(time.time())))
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    devices = db.relationship(
        'Device',
        secondary='user_device',
        back_populates='users',
        lazy='dynamic'
    )
    def __init__(self, username, password, email):
        self.username = username
        self.password = self._hash_password(password)
        self.email = email

    def __repr__(self):
        return f"<User Name: {self.username}, User Email: {self.email}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def getAll():
        return [{'id': user.id, 'username': user.username, 'email': user.email} for user in User.query.all()]

    @staticmethod
    def _hash_password(password):
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
    