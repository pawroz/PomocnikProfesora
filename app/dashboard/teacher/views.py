from flask import render_template, redirect, request, url_for, flash, session
from flask_login import login_user, logout_user, login_required
from ...models import User, Permission, Entry, Decision
from ... import db
from . import teacher
from ...user.forms import TeacherRegistrationForm
import requests
from .forms import ChangeHoursForm


@teacher.route('/dashboardTeacher', methods=['GET', 'POST'])
def dashboard():
    form = TeacherRegistrationForm()
    roomId = request.args.get('roomId', timeout=50)
    # login = request.args.get('login')

    # loginUrlResult = requests.post(
    #     'http://localhost/Projekt-inzynierski/API/UsersByLogin.php?login={}'.format(login))
    roomIdUrlResult = requests.post(
        'https://s153070.projektstudencki.pl/API/UsersByRoom.php?roomId={}'.format(roomId))
    try:
        teacherJson = roomIdUrlResult.json()
    except:
        print("login wrong")

    if request.method == 'POST':
        if request.form.get("submit"):
            user = User(name=teacherJson['name'],
                        surname=teacherJson['surname'],
                        date=str(form.date.data),
                        time=str(form.time.data),
                        end_time=str(form.end_time.data),
                        email=teacherJson['email'],
                        password='',
                        permission=Permission.TEACHER)
            print(str(form.date.data))
            print(str(form.time.data))
            print(str(form.end_time.data))
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
    if User.query.filter_by(email=teacherJson['email']).first() is None:
        return render_template('user/register.html', form=form)
    else:
        print("prowadzacy istnieje")

    entries = Entry.query.filter_by(teacher_email=teacherJson['email'])
    user = User.query.filter_by(email=session['teacher_email']).first()
    print(entries)
    return render_template('teacher/dashboard.html', entries=entries, roomId=roomId)


# po changeEntryHours podac wartosc roomId
@teacher.route('/changeEntryHours', methods=['GET', 'POST'])
def changeEntryHours():
    form = ChangeHoursForm()
    roomId = request.args.get('roomId', timeout=50)
    roomIdUrlResult = requests.post(
        'https://s153070.projektstudencki.pl/API/UsersByRoom.php?roomId={}'.format(roomId))
    try:
        teacherJson = roomIdUrlResult.json()
    except:
        print("login wrong")

    if form.validate_on_submit():
        teacher = User.query.filter_by(
            email=roomIdUrlResult.json()["email"]).first()
        teacher.date = str(form.changeDateField.data)
        teacher.time = str(form.changeTimeField.data)
        teacher.end_time = str(form.changeEndTimeField.data)
        # user = User(date=str(form.changeDateField.data),
        # time=str(form.changeTimeField.data),
        # end_time=str(form.changeEndTimeField.data))
        print(str(form.changeDateField.data))
        print(str(form.changeTimeField.data))
        print(str(form.changeEndTimeField.data))
        db.session.commit()
        return redirect(url_for('teacher.dashboard', roomId=roomId))
    return render_template('teacher/changeEntryHours.html', form=form, roomId=roomId)
