from flask import render_template, redirect, request, url_for, flash, session, jsonify
from flask_login import login_user, logout_user, login_required
from ...models import User, Permission, Entry, Decision
from . import student
from .forms import ZapisyForm
from ... import db
import requests
from flask_wtf import csrf

# noneeded function
# @student.route('/dashboardStudent', methods=['GET', 'POST'])
# def dashboard():
#     login = request.args.get('login')
#     roomId = request.args.get('roomId')
#     loginUrlResult = requests.post(
#         'https://s153070.projektstudencki.pl/API/UsersByLogin.php?login={}'.format(login))
#     roomIdUrlResult = requests.post(
#         'https://s153070.projektstudencki.pl/API/UsersByRoom.php?roomId={}'.format(roomId))
#     try:
#         teacherJson = roomIdUrlResult.json()
#         studentJson = loginUrlResult.json()
#     except:
#         print("roomId or login wrong")

#     # print(teacherJson)
#     if request.method == 'POST':
#         session['teacher_email'] = request.form['email']
#         return redirect(url_for('student.zapisy'))
#     teacher = User.query.filter_by(email=teacherJson['email']).first()
#     student = User.query.filter_by(email=studentJson['email']).first()
#     return render_template('student/dashboard.html', student=student, teacher=teacher)


@student.route('/zapisy', methods=['GET', 'POST'])
def zapisy():
    form = ZapisyForm()
    # print(session['teacher_email'])
    # print(session['student_email'])
    # print(User.query.filter_by(email=session['student_email']).first())
    if 'login' in request.form and 'roomId' in request.form and 'roomAuthtoken' in request.form and 'userAuthtoken' in request.form:
        login = request.form.get('login')
        roomId = request.form.get('roomId')
        roomToken = request.form.get('roomAuthtoken')
        userToken = request.form.get('userAuthtoken')
        print(login)
        print(roomId)
        print(roomToken)
        print(userToken)
        # roomId = request.args.get('roomId')
        # roomIdUrlResult = requests.post(
        #     'https://s153070.projektstudencki.pl/API/UsersByRoom.php?roomId={}'.format(roomId))
        roomIdUrlResult = requests.post(
            'https://s153070.projektstudencki.pl/API/UsersByRoom.php?roomId={}&token={}'.format(roomId, roomToken))

        loginUrlResult = requests.post(
            'https://s153070.projektstudencki.pl/API/UsersByLogin.php?login={}&token={}'.format(login, userToken))

        try:
            teacherJson = roomIdUrlResult.json()
            studentJson = loginUrlResult.json()
            print(teacherJson)
            print(studentJson)
        except:
            print("roomId or token wrong")

        session['teacher'] = teacherJson
        session['student'] = studentJson
        session['roomId'] = roomId
        session['login'] = login
        # print(User.query.filter_by(email=session['teacher']))
        #session['token'] = token

    # login = request.args.get('login')
    # roomId = request.args.get('roomId')
    # loginUrlResult = requests.post(
    #     'https://s153070.projektstudencki.pl/API/UsersByLogin.php?login={}'.format(login))
    # roomIdUrlResult = requests.post(
    #     'https://s153070.projektstudencki.pl/API/UsersByRoom.php?roomId={}'.format(roomId))
    # try:
    #     teacherJson = roomIdUrlResult.json()
    #     studentJson = loginUrlResult.json()
    # except:
    #     print("roomId or login wrong")

    teacher = User.query.filter_by(email=session['teacher']["email"]).first()
    student = User.query.filter_by(
        email=session['student']["email"]).first()

    if User.query.filter_by(email=session['student']['email']).first() is None:
        user = User(name=session['student']['name'],
                    surname=session['student']['surname'],
                    date="",
                    time="",
                    end_time="",
                    email=session['student']['email'],
                    password='',
                    permission=Permission.STUDENT)
        db.session.add(user)
        db.session.commit()
    else:
        print("student istnieje")

    if User.query.filter_by(email=session['teacher']['email']).first() is None:
        print("nie ma prowadzacego")
        return render_template("student/teacherIsNone.html", login=login)

    if form.validate_on_submit():
        #teacherSession = User.query.filter_by(email=session['teacher_email']).first()
        entry = Entry(student_email=session['student']["email"],
                      teacher_email=session['teacher']["email"],
                      student_name=session['student']["name"],
                      student_surname=session['student']["surname"],
                      teacher_name=session['teacher']["name"],
                      teacher_surname=session['teacher']["surname"],
                      date=teacher.date,
                      time=teacher.time,
                      end_time=teacher.end_time,
                      reason=form.reason.data,
                      decision=Decision.DEFAULT)
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for('student.results', login=session['login']))
    csrf.generate_csrf()
    return render_template('student/zapisy.html', form=form, login=session['login'], teacherSession=session['teacher'], teacher=teacher)


@student.route('/resultsStudent', methods=['GET', 'POST'])
def results():
    if 'login' in request.form and 'userAuthtoken' in request.form:
        login = request.form.get('login')
        userToken = request.form.get('userAuthtoken')
        # roomId = request.form.get('roomId')
        loginUrlResult = requests.post(
            'https://s153070.projektstudencki.pl/API/UsersByLogin.php?login={}&token={}'.format(login, userToken))
        # roomIdUrlResult = requests.post(
        #     'http://localhost/API/UsersByRoom.php?login={}&token={}'.format(roomId, roomToken))
        try:
            # teacherJson = roomIdUrlResult.json()
            studentJson = loginUrlResult.json()
        except:
            print("roomId or login wrong")

        # session['teacher'] = teacherJson
        session['student'] = studentJson
        # session['roomId'] = roomId
        session['login'] = login

    entries = Entry.query.filter_by(
        student_email=session['student']["email"])
    # print(login)
    return render_template('student/results.html', entries=entries, student=session['student'])
