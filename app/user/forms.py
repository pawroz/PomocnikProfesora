from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms.fields.html5 import DateField, TimeField
from datetime import datetime

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Haslo', validators=[DataRequired()])
    remember_me = BooleanField('Zapamietaj mnie')
    submit = SubmitField('Zaloguj')

class TeacherRegistrationForm(FlaskForm):
    name = StringField('Imie', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Usernames must have only letters, numbers, dots or underscores')])
    surname = StringField('Surname', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Usernames must have only letters, numbers, dots or underscores')])
    date = DateField('Date',format='%Y-%m-%d', default=datetime.now())
    time = TimeField('Poczatek spotkania',format='%H:%M', default=datetime.now())
    end_time = TimeField('Koniec spotkania',format='%H:%M', default=datetime.now())
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    secret = PasswordField('Secret', validators=[DataRequired(), Regexp('^ABCD1234$', 0, 'Must provide valid secret!')])
    submit = SubmitField('Register')

class StudentRegistrationForm(FlaskForm):
    name = StringField('Imie', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Usernames must have only letters, numbers, dots or underscores')])
    surname = StringField('Username', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Usernames must have only letters, numbers, dots or '
               'underscores')])
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')



