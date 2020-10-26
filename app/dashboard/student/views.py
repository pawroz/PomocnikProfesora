from flask import render_template, redirect, request, url_for, flash, session
from flask_login import login_user, logout_user, login_required
from ...models import User, Permission, Entry
from . import student
from .forms import ZapisyForm
from ... import db


@student.route('/dashboardStudent', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        session['teacher_email'] = request.form['email']
        return redirect(url_for('student.zapisy'))
    users = User.query.filter_by(permission=Permission.TEACHER)
    return render_template('student/dashboard.html', users=users)

@student.route('/zapisy', methods =['GET', 'POST'])
def zapisy():
    form = ZapisyForm()
    print(session['teacher_mail'])
    if form.validate_on_submit():
        entry = Entry(student_email = session['student_email'],
        teacher_email = session['teacher_email'],
        date = form.date.data,
        hour = form.hour.data,
        reason = form.reason.data)
        print("DUPA")
        db.session.add(entry)
        db.session.commit()
    return render_template('student/zapisy.html', form=form)
