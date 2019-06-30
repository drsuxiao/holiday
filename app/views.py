from flask import request, render_template
from app import app
from app.forms import HolidayApplyForm, PersonalInformationForm, HolidayAuditForm


@app.route('/', methods=['GET'])
def index():
    return render_template('base.html')


@app.route('/apply', methods=['GET'])
def show_apply():
    form = HolidayApplyForm()
    return render_template('holiday_apply.html', form=form, modal_title='请假申请编辑窗')


@app.route('/audit', methods=['GET'])
def show_audit():
    form = HolidayAuditForm()
    return render_template('holiday_audit.html', form=form, modal_title='请假申请审核窗')


@app.route('/information', methods=['GET'])
def show_information():
    form = PersonalInformationForm()
    return render_template('information.html', form=form, modal_title='个人信息编辑窗')


@app.route('/apply/detail', methods=['GET'])
def show_apply_detail():
    return render_template('holiday_detail.html')


@app.route('/apply/statistical', methods=['GET'])
def show_apply_statistical():
    return render_template('holiday_statistical.html')


@app.route('/apply/holidays', methods=['GET'])
def show_apply_holidays():
    return render_template('holiday_holidays.html')
