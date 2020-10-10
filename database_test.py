# -*- coding: utf-8 -*-
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import uuid
from database import *
 
engine = create_engine('sqlite:///database.db', echo=True)
 
# create a Session
Session = sessionmaker(bind=engine)
session = Session()
 
user = User("krzysztof", "prowadzacy@gmail.com", "prowadzacy", 1)
session.add(user)
 
user = User("pawel", "student@gmail.com", "student", 0)
session.add(user)
 
description = "Potrzebuje pomocy z matematyki"
meeting = Meeting(2,1, "10-08-2020", "08:00", description, 0)
session.add(meeting)
 
# commit the record the database
session.commit()