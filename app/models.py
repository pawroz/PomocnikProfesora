from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager

class Permission():
    STUDENT = 1
    TEACHER = 2


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index= True)
    password_hash = db.Column(db.String(128))
    username = db.Column(db.String(64), unique=True, index=True)
    permission = db.Column(db.Integer, index=True)
    
    @property
    def password(self):
        raise AttributeError("Nie do odczytania")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username

class Entry(db.Model):
    __tablename__ = 'entries'
    id = db.Column(db.Integer, primary_key=True)
    student_email = db.Column(db.String(64), index= True)
    teacher_email = db.Column(db.String(64), index= True)
    date = db.Column(db.String(64), index= True)
    hour = db.Column(db.String(64), index= True)
    reason = db.Column(db.String(64), index= True)

    def __repr__(self):
        return '<Entry %r>' % self.id