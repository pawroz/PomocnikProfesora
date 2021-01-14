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
    # name = StringField('Imie', validators=[
    #     DataRequired(), Length(1, 64),
    #     Regexp('^[A-Za-z][A-Za-z_.]*$', 0, 'Imie musi miec tylko litery')])
    # surname = StringField('Nzwisko', validators=[
    #     DataRequired(), Length(1, 64),
    #     Regexp('^[A-Za-z][A-Za-z_.]*$', 0, 'Nzwisko musi miec tylko litery')])
    date = DateField('Termin',format='%Y-%m-%d', validators=[DataRequired()], default=datetime.now())
    time = TimeField('Poczatek spotkania',format='%H:%M', validators=[DataRequired()])
    end_time = TimeField('Koniec spotkania',format='%H:%M', validators=[DataRequired()])
    # email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    # password = PasswordField('Haslo', validators=[
    #     DataRequired(), EqualTo('password2', message='Passwords must match.')])
    # password2 = PasswordField('Powtorz haslo', validators=[DataRequired()])
    # secret = PasswordField('Secret', validators=[DataRequired(), Regexp('^ABCD1234$', 0, 'Must provide valid secret!')])
    submit = SubmitField('ZAPISZ')

class StudentRegistrationForm(FlaskForm):
    name = StringField('Imie', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Imie musi miec tylko litery')])
    surname = StringField('Nzwisko', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z_.]*$', 0, 'Nzwisko musi miec tylko litery')])
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Haslo', validators=[
        DataRequired(), EqualTo('password2', message='Hasla nie sa indentyczne')])
    password2 = PasswordField('Powtorz haslo', validators=[DataRequired()])
    submit = SubmitField('Zarejestruj')



