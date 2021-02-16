from flask import render_template, session, redirect, url_for, current_app
from .. import db
from ..models import User
from ..email import send_email
from . import main


# @main.route('/test')
# def test():
#     return render_template('test.html')

# @main.route('/', methods=['GET', 'POST'])
# def index():
#     form = NameForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.name.data).first()
#         if user is None:
#             user = User(username=form.name.data)
#             db.session.add(user)
#             db.session.commit()
#             session['known'] = False
#             if current_app.config['PomocnikProfesora_ADMIN']:
#                 send_email(current_app.config['PomocnikProfesora_ADMIN'], 'New User',
#                            'mail/new_user', user=user)
#         else:
#             session['known'] = True
#         session['name'] = form.name.data
#         return redirect(url_for('.index'))
#     return render_template('base.html', known=session.get('known', False))
