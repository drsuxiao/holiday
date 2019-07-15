from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length
from app.models import HolidayApply, PersonalInformation


class HolidayApplyForm(FlaskForm):
    """
        创建/编辑请假申请表单
     """
    # SelectField 这里务必注意coerce=int/str选项的添加，否则提交时，下拉表单中的内容无法通过validate_on_submit的 验证
    # Text Field类型，文本输入框，必须输入是"年-月-日"格式的日期
    apply_man = SelectField('申请人', validators=[DataRequired()], coerce=str, render_kw={'class': "form-control select-sm", "style": "width: 200px", "title": "请选择"})  # 优先级
    holiday_type = SelectField('请假类型', validators=[DataRequired()], coerce=str, render_kw={'class': "form-control input-sm", "style": "width: 200px", "title": "请选择"})  # 优先级
    apply_dept = SelectField('科室', validators=[DataRequired()], coerce=str, render_kw={'class': "form-control select-sm", "style": "width: 200px", "title": "请选择"})  # 优先级
    start_date = StringField('开始日期', validators=[DataRequired()], render_kw={'class': "form-control input-sm", "style": "width: 200px"})
    end_date = StringField('结束日期', validators=[DataRequired()], render_kw={'class': "form-control input-sm", "style": "width: 200px"})
    holiday_days = StringField('天数', validators=[DataRequired()], render_kw={'class': "form-control input-sm", "style": "width: 200px"})  # 设备编号
    holiday_reason = StringField('请假原因', validators=[DataRequired()], render_kw={'class': "form-control input-sm", "style": "width: 200px"})  # 备注
    holiday_where = StringField('去向', validators=[DataRequired()], render_kw={'class': "form-control input-sm", "style": "width: 200px"})  # 备注
    apply_remarks = StringField('备注', render_kw={'class': "form-control input-sm", "style": "width: 200px"})  # 备注

    # 在构造化Form实例时指定selectField的choices内容,
    def __init__(self, *args, **kwargs):
        super(HolidayApplyForm, self).__init__(*args, **kwargs)
        self.holiday_type.choices = [('公休', '公休'), ('病假', '病假'), ('事假', '事假'), ('婚假', '婚假'), ('产假', '产假'), ('陪产假', '陪产假'), ('探亲假', '探亲假'), ('丧假', '丧假')]
        self.apply_dept.choices = [('(新阳)网络信息科', '(新阳)网络信息科'), ('(厢竹)网络信息科', '(厢竹)网络信息科')]
        self.apply_man.choices = [(data.info_name, data.info_name) for data in PersonalInformation.query.order_by(PersonalInformation.info_code).all()]


class HolidayAuditForm(FlaskForm):
    audit_status = SelectField('审核状态', validators=[DataRequired()], render_kw={'class': "form-control input-sm", "style": "width: 200px", "title": "请选择"})  # 备注
    audit_remarks = StringField('批示信息', render_kw={'class': "form-control input-sm", "style": "width: 200px"})  # 备注

    # 在构造化Form实例时指定selectField的choices内容,
    def __init__(self, *args, **kwargs):
        super(HolidayAuditForm, self).__init__(*args, **kwargs)
        self.audit_status.choices = [('1', '审核通过'), ('0', '审核不通过')]


class PersonalInformationForm(FlaskForm):
    info_code = StringField('编号', validators=[DataRequired()], render_kw={'class': "form-control input-sm", "style": "width: 200px"})
    info_name = StringField('姓名', validators=[DataRequired()], render_kw={'class': "form-control input-sm", "style": "width: 200px"})
    info_sex = SelectField('性别', validators=[DataRequired()], render_kw={'class': "form-control select-sm", "style": "width: 200px", "title": "请选择"})
    info_birthday = StringField('出生日期', validators=[DataRequired()], render_kw={'class': "form-control input-sm", "style": "width: 200px"})
    info_department = SelectField('科室', validators=[DataRequired()], render_kw={'class': "form-control select-sm", "style": "width: 200px", "title": "请选择"})
    info_workdate = StringField('入职日期', validators=[DataRequired()], render_kw={'class': "form-control input-sm", "style": "width: 200px"})
    info_title = SelectField('职称', validators=[DataRequired()], render_kw={'class': "form-control select-sm", "style": "width: 200px", "title": "请选择"})

    # 在构造化Form实例时指定selectField的choices内容,
    def __init__(self, *args, **kwargs):
        super(PersonalInformationForm, self).__init__(*args, **kwargs)
        self.info_sex.choices = [('0', '男'), ('1', '女'), ('2', '未知')]
        self.info_department.choices = [('(新阳)网络信息科', '(新阳)网络信息科'), ('(厢竹)网络信息科', '(厢竹)网络信息科')]
        self.info_title.choices = [('0', '助理工程师'), ('1', '程序员'), ('2', '网络管理员'), ('3', '网络工程师'), ('4', '其它职称')]


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()], render_kw={'class': "form-control input-sm", 'placeholder': "用户名"})
    password = PasswordField('密码', render_kw={'class': "form-control input-sm", 'placeholder': "密码"})
    remember_me = BooleanField('记住密码')
    submit = SubmitField('登录')

