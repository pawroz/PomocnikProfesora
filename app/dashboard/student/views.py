from flask import render_template, redirect, request, url_for, flash, session, jsonify
from flask_login import login_user, logout_user, login_required
from ...models import User, Permission, Entry, Decision
from . import student
from .forms import ZapisyForm
from ... import db
import requests
import datetime


@student.route('/dashboardStudent', methods=['GET', 'POST'])
def dashboard():
    login = request.args.get('login')
    roomId = request.args.get('roomId')
    loginUrlResult = requests.post(
        'https://s153070.projektstudencki.pl/API/UsersByLogin.php?login={}'.format(login))
    roomIdUrlResult = requests.post(
        'https://s153070.projektstudencki.pl/API/UsersByRoom.php?roomId={}'.format(roomId))
    try:
        teacherJson = roomIdUrlResult.json()
        studentJson = loginUrlResult.json()
    except:
        print("roomId or login wrong")

    # print(teacherJson)
    if request.method == 'POST':
        session['teacher_email'] = request.form['email']
        return redirect(url_for('student.zapisy'))
    teacher = User.query.filter_by(email=teacherJson['email']).first()
    student = User.query.filter_by(email=studentJson['email']).first()
    return render_template('student/dashboard.html', student=student, teacher=teacher)


@student.route('/zapisy', methods=['GET', 'POST'])
def zapisy():
    form = ZapisyForm()
    # if request.method == 'POST':
    data = request.form
    print(data['roomId'])
    login = data['roomId']
    roomId = data['login']
    loginUrlResult = requests.post(
        'https://s153070.projektstudencki.pl/API/UsersByLogin.php?login={}'.format(login))
    roomIdUrlResult = requests.post(
        'https://s153070.projektstudencki.pl/API/UsersByRoom.php?roomId={}'.format(roomId))
    try:
        teacherJson = roomIdUrlResult.json()
        studentJson = loginUrlResult.json()
    except:
        print("roomId or login wrong")
    teacher = User.query.filter_by(
        email=roomIdUrlResult.json()["email"]).first()
    # entryDate = teacher.date
    # today = datetime.date.today()
    # entryDateobj = datetime.datetime.strptime(entryDate, '%Y-%m-%d')
    # entryDateWeekLater = entryDateobj + datetime.timedelta(days=7)
    # if entryDateobj.date() < today:
    #     entryDate = str(entryDateWeekLater)
    #     print(entryDateobj)
    #     print(entryDateWeekLater)
    #     db.session.commit()
    # print(entryDate)
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
        return render_template("student/teacherIsNone.html", login=login)

    if form.validate_on_submit():
        teacher = User.query.filter_by(
            email=roomIdUrlResult.json()["email"]).first()
        #teacherSession = User.query.filter_by(email=session['teacher_email']).first()
        student = User.query.filter_by(
            email=loginUrlResult.json()["email"]).first()
        entry = Entry(student_email=loginUrlResult.json()["email"],
                      teacher_email=roomIdUrlResult.json()["email"],
                      student_name=loginUrlResult.json()["name"],
                      student_surname=loginUrlResult.json()["surname"],
                      teacher_name=roomIdUrlResult.json()["name"],
                      teacher_surname=roomIdUrlResult.json()["surname"],
                      date=teacher.date,
                      time=teacher.time,
                      end_time=teacher.end_time,
                      reason=form.reason.data,
                      decision=Decision.DEFAULT)
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for('student.results', login=login, roomId=roomId))
    return render_template('student/zapisy.html', form=form, login=login, teacher=teacher)


@student.route('/resultsStudent', methods=['GET', 'POST'])
def results():
    data = request.form
    login = data['login']
    roomId = data['roomId']
    loginUrlResult = requests.post(
        'https://s153070.projektstudencki.pl/API/UsersByLogin.php?login={}'.format(login))
    roomIdUrlResult = requests.post(
        'https://s153070.projektstudencki.pl/API/UsersByRoom.php?roomId={}'.format(roomId))
    try:
        teacherJson = roomIdUrlResult.json()
        studentJson = loginUrlResult.json()
    except:
        print("roomId or login wrong")

    entries = Entry.query.filter_by(
        student_email=loginUrlResult.json()["email"])
    print(login)
    return render_template('student/results.html', entries=entries)
