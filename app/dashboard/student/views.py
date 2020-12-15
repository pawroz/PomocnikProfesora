from flask import render_template, redirect, request, url_for, flash, session
from flask_login import login_user, logout_user, login_required
from ...models import User, Permission, Entry, Decision
from . import student
from .forms import ZapisyForm
from ... import db
import requests


@student.route('/dashboardStudent', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST': 
        session['teacher_email'] = request.form['email']
        return redirect(url_for('student.zapisy'))
    users = User.query.filter_by(permission=Permission.TEACHER)
    user = User.query.filter_by(email=session['student_email']).first()
    return render_template('student/dashboard.html', users=users, user_name=user.name)

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
        print(loginUrlResult.json()["email"])
        print(roomIdUrlResult.json()["login"])
    except:
        print("roomId or login wrong")
    #TODO data from roomName cant download correctly
    # Change session variables to fit requirenments of provided API :)
    if form.validate_on_submit():
        teacher = User.query.filter_by(email=roomIdUrlResult.json()["login"]).first()
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
        print("DUPA")
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for('student.dashboard'))
    return render_template('student/zapisy.html', form=form)


@student.route('/resultsStudent', methods=['GET', 'POST'])
def results():
    entries = Entry.query.filter_by(student_email=session['student_email'])
    print(entries)
    print(session['student_email'])
    return render_template('student/results.html', entries=entries)