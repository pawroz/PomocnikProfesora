from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required
from . import teacher


@teacher.route('/dashboardTeacher', methods=['GET', 'POST'])
def dashboard():
    print('viewTeacher')
    return render_template('teacher/dashboard.html')
    
