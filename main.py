from flask import Flask, request, session, jsonify, render_template, redirect, url_for
from sqlalchemy.orm import sessionmaker
from database import *
from flask_bootstrap import Bootstrap
import uuid
from flask_sqlalchemy import SQLAlchemy
 
#engine = create_engine('sqlite:///database.db', echo=True)
 
app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route("/")
def index():
    return render_template("layout.html")

@app.route('/api/getUsers', methods=['GET'])
def getUsers():
 
    result = engine.execute('SELECT * FROM users')
    titles = []
    print(result)
    for row in result:
        titles.append(dict({'name':''+row[1]+'','email':''+row[2]+'', 'password':''+row[3]+'','permission': row[4]}))
    return jsonify(titles)
 
@app.route('/api/getMeetings', methods=['GET'])
def getMeetings():
 
    result = engine.execute('SELECT * FROM meetings')
    titles = []
    for row in result:
        titles.append(dict({'student id': row[1],'teacher id': row[2],'date':''+row[3]+'','hour':''+row[4]+'','description':''+row[5]+'','approved': row[6]}))
    return jsonify(titles)
 
@app.route("/login",methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        passw = request.form["passw"]
        
        Session = sessionmaker(bind=engine)
        session = Session()
        query = session.query(User).filter(User.email.in_([email]), User.password.in_([passw]) )
        result = query.first()

        if result is not None:
            return redirect(url_for("index"))

    return render_template("login.html")

@app.route("/register_teacher", methods=["GET", "POST"])
def register_teacher():
    if request.method == "POST":
        uname = request.form['uname']
        mail = request.form['mail']
        passw = request.form['passw']
        code = request.form['code']

        if code == "123":
            Session = sessionmaker(bind=engine)
            session = Session()
            user = User(uname, mail, passw, 1)
            session.add(user)
            session.commit()

            return redirect(url_for("login"))

    return render_template("register_teacher.html")

@app.route("/register_student", methods=["GET", "POST"])
def register_student():
    if request.method == "POST":
        uname = request.form['uname']
        mail = request.form['mail']
        passw = request.form['passw']

        Session = sessionmaker(bind=engine)
        session = Session()
        user = User(uname, mail, passw, 0)
        session.add(user)
        session.commit()

        return redirect(url_for("login"))

    return render_template("register_student.html")



if __name__ == "__main__":
    app.debug = True
    app.run(host = '0.0.0.0',port=5000)



    # Bootstrap(app)

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