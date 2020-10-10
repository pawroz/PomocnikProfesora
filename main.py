from flask import Flask, request, session, jsonify
from sqlalchemy.orm import sessionmaker
from database import *
import uuid
 
engine = create_engine('sqlite:///database.db', echo=True)
 
app = Flask(__name__)
 
# @app.route('/api/login', methods=['POST'])
# def login():
 
#     data = request.get_json()
 
#     email = data["email"]
 
#     password = data["password"]
 
#     Session = sessionmaker(bind=engine)
#     session = Session()
#     query = session.query(User).filter(User.email.in_([email]), User.password.in_([password]) )
#     result = query.first()
#     if result:
#         return jsonify({'result':'OK'})
#     else:
#         return jsonify({'result':'BAD'})
 
# @app.route('/api/register', methods=['POST'])
# def register():
 
#     data = request.get_json()
 
#     Session = sessionmaker(bind=engine)
#     session = Session()
 
#     email = data["email"]
#     password = data["password"]
 
#     user = User(email, password)
#     session.add(user)
 
#     session.commit()
 
#     return jsonify({'result':'OK'})

@app.route('/api/getUsers', methods=['GET'])
def getUsers():
 
    result = engine.execute('SELECT * FROM users')
    titles = []
    print(result)
    for row in result:
        titles.append(dict({'email':''+row[1]+'','password':''+row[2]+'','permission': row[3]}))
    return jsonify(titles)
 
@app.route('/api/getMeetings', methods=['GET'])
def getMeetings():
 
    result = engine.execute('SELECT * FROM meetings')
    titles = []
    for row in result:
        titles.append(dict({'student id': row[1],'teacher id': row[2],'date':''+row[3]+'','hour':''+row[4]+'','description':''+row[5]+'','approved': row[6]}))
    return jsonify(titles)
 
if __name__ == "__main__":
    app.debug = True
    app.run(host = '0.0.0.0',port=5000)