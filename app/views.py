from flask import request, render_template, redirect, flash, url_for
from app import app
from app.forms import HolidayApplyForm, PersonalInformationForm, HolidayAuditForm, LoginForm
from app.models import User
from flask_login import login_user, logout_user, login_required
from passlib.apps import custom_app_context as pwd_context


@app.route('/', methods=['GET'])
@login_required
def index():
    return render_template('base.html')


@app.route('/apply', methods=['GET'])
@login_required
def show_apply():
    form = HolidayApplyForm()
    return render_template('holiday_apply.html', form=form, modal_title='请假申请编辑窗')


@app.route('/audit', methods=['GET'])
@login_required
def show_audit():
    form = HolidayAuditForm()
    return render_template('holiday_audit.html', form=form, modal_title='请假申请审核窗')


@app.route('/information', methods=['GET'])
@login_required
def show_information():
    form = PersonalInformationForm()
    return render_template('information.html', form=form, modal_title='个人信息编辑窗')


@app.route('/apply/detail', methods=['GET'])
@login_required
def show_apply_detail():
    return render_template('holiday_detail.html')


@app.route('/apply/statistical', methods=['GET'])
@login_required
def show_apply_statistical():
    return render_template('holiday_statistical.html')


@app.route('/apply/holidays', methods=['GET'])
@login_required
def show_apply_holidays():
    return render_template('holiday_holidays.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = request.form.get('username')
        user = User.query.filter_by(username=username).first()
        # password = pwd_context.encrypt(request.form['password'])
        password = request.form['password']
        if user is not None and user.password_hash == password:

            # 通过Flask-Login的login_user方法登录用户
            login_user(user)

            return redirect(url_for('index'))

        flash('用户名或密码错误!')

    # GET 请求
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

