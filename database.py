# -*- coding: utf-8 -*-
from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
 
engine = create_engine('sqlite:///database.db', echo=True)
Base = declarative_base()
 
########################################################################
class User(Base):
    __tablename__ = "users"
 
    id = Column(Integer, primary_key=True)
    email = Column(String)
    password = Column(String)
    permision = Column(Integer)
 
    def __init__(self, email, password, permision):
 
        self.email = email
        self.password = password
        self.permision = permision
 
class Meeting(Base):
    __tablename__ = "meetings"
 
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer)
    teacher_id = Column(Integer)
    date = Column(String)
    hour = Column(String)
    description = Column(String)
    approved = Column(Integer)
 
    def __init__(self, student_id, teacher_id, date, hour, description, approved):
 
        self.student_id = student_id
        self.teacher_id = teacher_id
        self.date = date
        self.hour = hour
        self.description = description
        self.approved = approved

# create tables
Base.metadata.create_all(engine)