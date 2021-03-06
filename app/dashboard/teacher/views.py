from flask import render_template, redirect, request, url_for, flash, session
from flask_login import login_user, logout_user, login_required
from ...models import User, Permission, Entry, Decision
from ... import db
from . import teacher
from ...user.forms import TeacherRegistrationForm
import requests
from .forms import ChangeHoursForm
import datetime


@teacher.route('/dashboardTeacher', methods=['GET', 'POST'])
def dashboard():
    form = TeacherRegistrationForm()
    if 'roomId' in request.form and 'roomAuthtoken' in request.form:
        roomId = request.form.get('roomId')
        token = request.form.get('roomAuthtoken')
        print(roomId)
        print(token)
        # roomId = request.args.get('roomId')
        # roomIdUrlResult = requests.post(
        #     'https://s153070.projektstudencki.pl/API/UsersByRoom.php?roomId={}'.format(roomId))
        roomIdUrlResult = requests.post(
            'https://s153070.projektstudencki.pl/API/UsersByRoom.php?roomId={}&token={}'.format(roomId, token))

        try:
            teacherJson = roomIdUrlResult.json()
            print(teacherJson)
        except:
            print("roomId or token wrong")

        session['teacher'] = teacherJson
        session['roomId'] = roomId
        session['token'] = token

    # teacher = User.query.filter_by(email=teacherJson['email']).first()

    if request.method == 'POST':
        if request.form.get("submit"):
            user = User(name=session['teacher']['name'],
                        surname=session['teacher']['surname'],
                        date=str(form.date.data),
                        time=str(form.time.data),
                        end_time=str(form.end_time.data),
                        email=session['teacher']['email'],
                        password='',
                        permission=Permission.TEACHER)
            db.session.add(user)
            db.session.commit()
        if request.form.get("accept"):
            id = request.form['accept']
            entry = Entry.query.filter_by(id=id).first()
            entry.decision = Decision.ACCEPT
            db.session.commit()
        if request.form.get("decline"):
            id = request.form['decline']
            entry = Entry.query.filter_by(id=id).first()
            entry.decision = Decision.DECLINE
            db.session.commit()

    #  prowadzacy1 = User.query.filter_by(email='student1@wp.pl').first() -> prowadzacy1.date
    if User.query.filter_by(email=session['teacher']['email']).first() is None:
        return render_template('user/register.html', form=form)
    else:
        print("prowadzacy istnieje")

    entries = Entry.query.filter_by(teacher_email=session['teacher']['email'])
    # user = User.query.filter_by(email=session['teacher_email']).first()
    # prowadzacy1 = User.query.filter_by(email='testMail@test.pl').first()
    # print(prowadzacy1.date)
    for entry in entries:
        today = datetime.datetime.today()
        todayOnlyDay = today.strftime('%d')
        date_time_str = entry.date
        date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d')
        entryTime = date_time_obj.strftime('%d')
        expectedDate = int(todayOnlyDay) - int(entryTime)
        print(expectedDate)
        if expectedDate > 7:
            db.session.delete(entry)
            db.session.commit()
    return render_template('teacher/dashboard.html', entries=entries, roomId=session['roomId'],
                           teacher=session['teacher'], roomAuthtoken=session['token'])


# po changeEntryHours podac wartosc roomId
@teacher.route('/changeEntryHours', methods=['GET', 'POST'])
def changeEntryHours():
    form = ChangeHoursForm()
    # roomId = request.form.get('roomId')
    # token = request.form.get('roomAuthtoken')
    # roomIdUrlResult = requests.post(
    #     'http://localhost/API/UsersByRoom.php?roomId={}&token={}'.format(roomId, token))
    # try:
    #     teacherJson = roomIdUrlResult.json()
    # except:
    #     print("login wrong")
    print(session['teacher'])

    if form.validate_on_submit():
        teacher = User.query.filter_by(
            email=session['teacher']["email"]).first()
        teacher.date = str(form.changeDateField.data)
        teacher.time = str(form.changeTimeField.data)
        teacher.end_time = str(form.changeEndTimeField.data)
        # user = User(date=str(form.changeDateField.data),
        # time=str(form.changeTimeField.data),
        # end_time=str(form.changeEndTimeField.data))

        # print(str(form.changeDateField.data))
        # print(str(form.changeTimeField.data))
        # print(str(form.changeEndTimeField.data))
        db.session.commit()
        # po zmienie dyzuru idą args w params
        return redirect(url_for('teacher.dashboard'))
    return render_template('teacher/changeEntryHours.html', form=form, roomId=session['roomId'])
