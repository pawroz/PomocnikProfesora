from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo


class ZapisyForm(FlaskForm):
    date = StringField('Data', validators=[DataRequired()])
    hour = StringField('Godzina', validators=[DataRequired()])
    reason = StringField('Powod', validators=[DataRequired()])
    submit = SubmitField('Zapisz')

