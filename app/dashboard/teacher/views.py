from flask import render_template, redirect, request, url_for, flash, session
from flask_login import login_user, logout_user, login_required
from ...models import User, Permission, Entry, Decision
from ... import db
from . import teacher
from ...user.forms import TeacherRegistrationForm
import requests

@teacher.route('/dashboardTeacher', methods=['GET', 'POST'])
def dashboard():
    form = TeacherRegistrationForm()
    login = request.args.get('login')
    loginUrlResult = requests.post('http://localhost/Projekt-inzynierski/API/UsersByLogin.php?login={}'.format(login))

    try:
        teacherJson = loginUrlResult.json()
    except:
        print("login wrong")

    if User.query.filter_by(email=teacherJson['email']).first() is None:
        user = User(name=teacherJson['name'],
            surname=teacherJson['surname'],
            date="",
            time="",
            end_time="",
            email=teacherJson['email'],
            password='',
            permission=Permission.TEACHER)
        db.session.add(user)
        db.session.commit()
        #TODO- return template form tylko z godziną początek spotkania koniec spotkania zobacz register form teacher
        return render_template('user/register.html', form=form)
    else:
        print("istnieje")

    if request.method == 'POST':
        if request.form.get("accept"):
            id = request.form['accept']
            entry = Entry.query.filter_by(id=id).first()
            entry.decision = Decision.ACCEPT
            db.session.commit()
            print(id)
        elif request.form.get("decline"):
            id = request.form['decline']
            entry = Entry.query.filter_by(id=id).first()
            entry.decision = Decision.DECLINE
            db.session.commit()
    entries = Entry.query.filter_by(teacher_email=session['teacher_email'])
#   student_name = session['student_email']
    user = User.query.filter_by(email=session['teacher_email']).first()
    print(entries)
    return render_template('teacher/dashboard.html', entries=entries)


    
