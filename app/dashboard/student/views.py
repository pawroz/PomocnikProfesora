from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required
from ...models import User, Permission
from . import student


@student.route('/dashboardStudent', methods=['GET', 'POST'])
def dashboard():
    users = User.query.filter_by(permission=Permission.TEACHER)
    return render_template('student/dashboard.html', users=users)
