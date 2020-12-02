from flask import render_template, redirect, request, url_for, flash, session
from flask_login import login_user, logout_user, login_required
from ...models import User, Permission, Entry, Decision
from ... import db
from . import teacher


@teacher.route('/dashboardTeacher', methods=['GET', 'POST'])
def dashboard():
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
#    student_name = session['student_email']
    user = User.query.filter_by(email=session['teacher_email']).first()
    print(entries)
    return render_template('teacher/dashboard.html', entries=entries, teacher_name=user.name)


    
