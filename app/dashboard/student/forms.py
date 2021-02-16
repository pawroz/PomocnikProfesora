from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo


class ZapisyForm(FlaskForm):
    reason = StringField('Powód', validators=[DataRequired()])
    submit = SubmitField('Zapisz')  

