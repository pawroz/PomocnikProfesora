from flask import render_template, session, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required
from . import user
from .. import db
from ..models import User, Permission
from .forms import LoginForm, StudentRegistrationForm, TeacherRegistrationForm


@user.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                if user.permission == Permission.STUDENT:
                    session['student_email'] = form.email.data
                    next = url_for('student.dashboard')
                    print('student')
                elif user.permission == Permission.TEACHER:
                    session['teacher_email'] = form.email.data
                    next = url_for('teacher.dashboard')
                    print('prowadzacy')
                else:
                    next = url_for('main.index')
                    flash('Nieprawidlowa nazwa uzytkownika lub haslo')
            return redirect(next)
        
    return render_template('user/login.html', form=form)


@user.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Zostales wylogowany')
    return redirect(url_for('main.index'))

@user.route('/student_register', methods=['GET', 'POST'])
def student_register():
    form = StudentRegistrationForm()
    if form.validate_on_submit():
        user = User(name=form.name.data.lower(),
                    surname=form.surname.data.lower(),
                    date="",
                    time="",
                    end_time="",
                    email=form.email.data.lower(),
                    password=form.password.data,
                    permission=Permission.STUDENT)
        db.session.add(user)
        db.session.commit()
        # token = user.generate_confirmation_token()
        # send_email(user.email, 'Confirm Your Account',
        #            'auth/email/confirm', user=user, token=token)
        # flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('main.index'))
    return render_template('user/register.html', form=form)

@user.route('/teacher_register', methods=['GET', 'POST'])
def teacher_register():
    form = TeacherRegistrationForm()
    if form.validate_on_submit():
        user = User(name=form.name.data.lower(),
                    surname=form.surname.data.lower(),
                    date=str(form.date.data),
                    time=str(form.time.data),
                    end_time=str(form.end_time.data),
                    email=form.email.data.lower(),
                    password=form.password.data,
                    permission=Permission.TEACHER)
        print(str(form.time.data))
        db.session.add(user)
        db.session.commit()
        # token = user.generate_confirmation_token()
        # send_email(user.email, 'Confirm Your Account',
        #            'auth/email/confirm', user=user, token=token)
        # flash('A confirmation email has been sent to you by email.')
        return render_template('base.html')
    return render_template('user/register.html', form=form)

