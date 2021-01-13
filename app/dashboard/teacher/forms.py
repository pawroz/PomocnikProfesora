from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms.fields.html5 import DateField, TimeField
from datetime import datetime


class ChangeHoursForm(FlaskForm):
    changeDateField = DateField('Termin',format='%Y-%m-%d', validators=[DataRequired()], default=datetime.now())
    changeTimeField = TimeField('Poczatek spotkania',format='%H:%M', validators=[DataRequired()])
    changeEndTimeField = TimeField('Koniec spotkania',format='%H:%M', validators=[DataRequired()])
    submit = SubmitField('Zapisz')  