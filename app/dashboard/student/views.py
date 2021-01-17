from flask import render_template, redirect, request, url_for, flash, session
from flask_login import login_user, logout_user, login_required
from ...models import User, Permission, Entry, Decision
from . import student
from .forms import ZapisyForm
from ... import db
import requests

# KLASA JAK NA RAZIE NIEPOTRZEBNA 
@student.route('/dashboardStudent', methods=['GET', 'POST'])
def dashboard():
    login = request.args.get('login')
    roomId = request.args.get('roomId')
    loginUrlResult = requests.post('http://localhost/Projekt-inzynierski/API/UsersByLogin.php?login={}'.format(login))
    roomIdUrlResult = requests.post('http://localhost/Projekt-inzynierski/API/UsersByRoom.php?roomId={}'.format(roomId))
    try:
        teacherJson = roomIdUrlResult.json()
        studentJson = loginUrlResult.json()
    except:
        print("roomId or login wrong")
    
    #print(teacherJson)
    if request.method == 'POST': 
        session['teacher_email'] = request.form['email']
        return redirect(url_for('student.zapisy'))
    teacher = User.query.filter_by(email=teacherJson['email']).first()
    student = User.query.filter_by(email=studentJson['email']).first()
    return render_template('student/dashboard.html', student=student, teacher=teacher)

@student.route('/zapisy', methods =['GET', 'POST'])
def zapisy():
    form = ZapisyForm()
    # print(session['teacher_email'])
    # print(session['student_email'])
    # print(User.query.filter_by(email=session['student_email']).first())

    login = request.args.get('login')
    roomId = request.args.get('roomId')
    loginUrlResult = requests.post('http://localhost/Projekt-inzynierski/API/UsersByLogin.php?login={}'.format(login))
    roomIdUrlResult = requests.post('http://localhost/Projekt-inzynierski/API/UsersByRoom.php?roomId={}'.format(roomId))
    try:
        teacherJson = roomIdUrlResult.json()
        studentJson = loginUrlResult.json()
    except:
        print("roomId or login wrong")
    if User.query.filter_by(email=studentJson['email']).first() is None:
        user = User(name=studentJson['name'],
                    surname=studentJson['surname'],
                    date="",
                    time="",
                    end_time="",
                    email=studentJson['email'],
                    password='',
                    permission=Permission.STUDENT)
        db.session.add(user)
        db.session.commit()  
    else:
        print("student istnieje")      

    if User.query.filter_by(email=teacherJson['email']).first() is None:
        print("nie ma prowadzacego")
        return render_template("student/teacherIsNone.html")

    if form.validate_on_submit():
        teacher = User.query.filter_by(email=roomIdUrlResult.json()["email"]).first()
        #teacherSession = User.query.filter_by(email=session['teacher_email']).first()
        student = User.query.filter_by(email=loginUrlResult.json()["email"]).first()
        entry = Entry(student_email = loginUrlResult.json()["email"],
        teacher_email = roomIdUrlResult.json()["email"],
        student_name = loginUrlResult.json()["name"],
        student_surname = loginUrlResult.json()["surname"],
        teacher_name = roomIdUrlResult.json()["name"],
        teacher_surname = roomIdUrlResult.json()["surname"],
        date = teacher.date,
        time = teacher.time,
        end_time = teacher.end_time,
        reason = form.reason.data,
        decision = Decision.DEFAULT)
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for('student.results', login=login, roomId=roomId)) ##
    return render_template('student/zapisy.html', form=form) 

#TODO: dorobic sprawdzenie permission 
@student.route('/resultsStudent', methods=['GET', 'POST'])
def results():
    login = request.args.get('login')
    roomId = request.args.get('roomId')
    loginUrlResult = requests.post('http://localhost/Projekt-inzynierski/API/UsersByLogin.php?login={}'.format(login))
    roomIdUrlResult = requests.post('http://localhost/Projekt-inzynierski/API/UsersByRoom.php?roomId={}'.format(roomId))
    try:
        teacherJson = roomIdUrlResult.json()
        studentJson = loginUrlResult.json()
    except:
        print("roomId or login wrong")
        
    entries = Entry.query.filter_by(student_email = loginUrlResult.json()["email"])
    #print(entries)
    return render_template('student/results.html', entries=entries)