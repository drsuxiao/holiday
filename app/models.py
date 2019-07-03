from passlib.apps import custom_app_context as pwd_context
from datetime import datetime
from app import db
from flask_login import UserMixin, current_user


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def to_json(self):
        """
        完成User数据模型到JSON格式化的序列化字典转换
        """
        json_user = {
            'id': self.id,
            'username': self.username,
            'password': self.password_hash
        }
        return json_user


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(20), unique=True)


# 日期统一更为字符串类型保存，方便比较
class HolidayApply(db.Model):
    __tablename__ = 'holiday_apply'

    id = db.Column(db.Integer, primary_key=True)
    apply_man = db.Column(db.String(50))  # 申请人
    holiday_type = db.Column(db.String(10))  # 请假类型
    apply_dept = db.Column(db.String(50))  # 所在科室
    start_date = db.Column(db.String(20), default=datetime.now().strftime("%Y-%m-%d"))
    end_date = db.Column(db.String(20), default=datetime.now().strftime("%Y-%m-%d"))
    holiday_days = db.Column(db.String(10))  # 请假天数，支持手动输入：单位（天）
    holiday_reason = db.Column(db.String(100))  # 请假事由
    holiday_where = db.Column(db.String(100))  # 请假去哪
    apply_remarks = db.Column(db.String(100))  # 备注信息
    operation_date = db.Column(db.String(20), default=datetime.now().strftime("%Y-%m-%d %H:%M"))
    operator = db.Column(db.String(50))  # 操作人
    audit_status = db.Column(db.String(10))
    auditor = db.Column(db.String(50))  # 审核人
    audit_date = db.Column(db.String(20))
    audit_remarks = db.Column(db.String(100))  # 备注信息

    def to_json(self):
        """
        完成数据模型到JSON格式化的序列化字典转换
        """
        json_holiday_apply = {
            'id': self.id,
            'apply_man': self.apply_man,
            'holiday_type': self.holiday_type,
            'apply_dept': self.apply_dept,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'holiday_days': self.holiday_days,
            'holiday_reason': self.holiday_reason,
            'holiday_where': self.holiday_where,
            'apply_remarks': self.apply_remarks,
            'operation_date': self.operation_date,
            'operator': self.operator,
            'audit_status': self.audit_status,
            'auditor': self.auditor,
            'audit_date': self.audit_date,
            'audit_remarks': self.audit_remarks
        }
        return json_holiday_apply


class PersonalInformation(db.Model):
    __tablename__ = 'personal_information'

    id = db.Column(db.Integer, primary_key=True)
    info_code = db.Column(db.String(10), unique=True, index=True)
    info_name = db.Column(db.String(50), unique=True, index=True)
    info_sex = db.Column(db.String(10))
    info_birthday = db.Column(db.String(20))
    info_department = db.Column(db.String(50))
    info_workdate = db.Column(db.String(20))
    info_title = db.Column(db.String(50))  # 职称

    def to_json(self):
        """
        完成数据模型到JSON格式化的序列化字典转换
        """
        json_personal_information = {
            'id': self.id,
            'info_code': self.info_code,
            'info_name': self.info_name,
            'info_sex': self.info_sex,
            'info_birthday': self.info_birthday,
            'info_department': self.info_department,
            'info_workdate': self.info_workdate,
            'info_title': self.info_title
        }
        return json_personal_information
