# -*- coding: utf-8 -*-
from sqlalchemy import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from main import app

# engine = create_engine('sqlite:///database.db', echo=True)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# Base = declarative_base()

########################################################################
class User(db.Model):
    __tablename__ = "users"
 
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String)
    email = db.Column(String)
    password = db.Column(String)
    permission = db.Column(Integer)
    meettings = db.relationship('Meeting', backref='user')
 
    def __repr__(self):
        return '<User %r>' % self.name
 
class Meeting(db.Model):
    __tablename__ = "meetings"
 
    id = db.Column(Integer, primary_key=True)
    student_id = db.Column(Integer)
    teacher_id = db.Column(Integer)
    date = db.Column(String)
    hour = db.Column(String)
    description = db.Column(String)
    approved = db.Column(Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def __repr__(self):
        return '<taecher Id %r>' % self.teacher_id  
    # def __init__(self, student_id, teacher_id, date, hour, description, approved):
 
    #     self.student_id = student_id
    #     self.teacher_id = teacher_id
    #     self.date = date
    #     self.hour = hour
    #     self.description = description
    #     self.approved = approved

# create tables
# Base.metadata.create_all(engine)