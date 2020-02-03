from flask import jsonify, abort, make_response, request
from app import app, db
from app.models import HolidayApply, PersonalInformation
from datetime import datetime
import json
from sqlalchemy import text


@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def myreponse(data='success', total=0):
    return jsonify({'status': 201, 'total': total, 'rows': data, 'msg': ''})


@app.route('/holiday/api/v1.0/holiday_apply', methods=['GET'])
def get_holiday_apply():
    querystr = request.args.get("querystr", ' 1=1 ')
    # querytype = request.args.get("querytype", 'json')
    offset = request.args.get("offset", '0')
    limit = request.args.get("limit", '10')
    sort = request.args.get('sort', 'id')
    order = request.args.get('order', 'desc')
    sidePagination = request.args.get('sidePagination', 'client')

    wherestr = querystr
    print(wherestr)

    orderbystr = sort + " " + order
    print(orderbystr)
    # 分页paginate的参数page，是第几页，而offset是记录的偏移量，需要转换
    # 表格标题排序，根据table提交的信息进行排序，否则排序无效
    if sidePagination == 'server':
        page = (int(offset) // int(limit)) + 1
        pagination = HolidayApply.query.filter(text(wherestr)).order_by(text(orderbystr)).paginate(page, int(limit), False)
        rows = pagination.items
        total = pagination.total
    else:
        rows = HolidayApply.query.filter(text(wherestr)).order_by(text(orderbystr))
        total = HolidayApply.query.filter(text(wherestr)).order_by(text(orderbystr)).count()
    print(total)

    if not rows:
        abort(400)
    data = [row.to_json() for row in rows]
    # data = get_data_by_model(EquipmentRepair)
    return myreponse(data, total)


@app.route('/holiday/api/v1.0/holiday_apply/add', methods=['POST'])
def new_holiday_apply():
    data = request.form
    data_dict = data.to_dict()
    print(data_dict)

    apply_man = data_dict.get('apply_man')
    holiday_type = data_dict.get('holiday_type')
    apply_dept = data_dict.get('apply_dept')
    start_date = data_dict.get('start_date')
    end_date = data_dict.get('end_date')
    holiday_days = data_dict.get('holiday_days')
    holiday_reason = data_dict.get('holiday_reason')
    holiday_where = data_dict.get('holiday_where')
    apply_remarks = data_dict.get('apply_remarks')
    operation_date = data_dict.get('operation_date', datetime.now().strftime("%Y-%m-%d %H:%M"))
    operator = data_dict.get('operator')
    audit_status = '-1'

    if HolidayApply.query.filter_by(apply_man=apply_man, holiday_type=holiday_type,
                                    start_date=start_date, end_date=end_date).first() is not None:
        abort(400)  # existing user

    row = HolidayApply(apply_man=apply_man, holiday_type=holiday_type, apply_dept=apply_dept, start_date=start_date, end_date=end_date,
                       holiday_days=holiday_days, holiday_reason=holiday_reason, holiday_where=holiday_where,
                       apply_remarks=apply_remarks, operation_date=operation_date, operator=operator, audit_status=audit_status)
    db.session.add(row)
    db.session.commit()

    return myreponse(row.to_json())


@app.route('/holiday/api/v1.0/holiday_apply/edit/<int:id>', methods=['POST'])
def update_holiday_apply(id):
    row = HolidayApply.query.filter_by(id=id).first()
    if row is None:
        abort(400)  # existing user
    if row.audit_status != '-1':
        abort(400)

    data = request.form
    data_dict = data.to_dict()
    print(data_dict)

    apply_man = data_dict.get('apply_man')
    holiday_type = data_dict.get('holiday_type')
    apply_dept = data_dict.get('apply_dept')
    start_date = data_dict.get('start_date')
    end_date = data_dict.get('end_date')
    holiday_days = data_dict.get('holiday_days')
    holiday_reason = data_dict.get('holiday_reason')
    holiday_where = data_dict.get('holiday_where')
    apply_remarks = data_dict.get('apply_remarks')
    operation_date = data_dict.get('operation_date', datetime.now().strftime("%Y-%m-%d %H:%M"))
    operator = data_dict.get('operator')

    row.apply_man = apply_man
    row.holiday_type = holiday_type
    row.apply_dept = apply_dept
    row.start_date = start_date
    row.end_date = end_date
    row.holiday_days = holiday_days
    row.holiday_reason = holiday_reason
    row.holiday_where = holiday_where
    row.apply_remarks = apply_remarks
    row.operation_date = operation_date
    row.operator = operator

    db.session.commit()
    return myreponse(row.to_json())


@app.route('/holiday/api/v1.0/holiday_apply/delete/<int:id>', methods=['POST'])
def delete_holiday_apply(id):
    row = HolidayApply.query.filter_by(id=id).first()
    if row is None:
        abort(404)  # existing user
    if row.audit_status != '-1':
        abort(400)

    db.session.delete(row)
    db.session.commit()
    return myreponse(row.to_json())


@app.route('/holiday/api/v1.0/holiday_apply/audit/<int:id>', methods=['POST'])
def audit_holiday_apply(id):
    row = HolidayApply.query.filter_by(id=id).first()
    if row is None:
        abort(400)  # existing user

    data = request.form
    data_dict = data.to_dict()
    print(data_dict)

    audit_status = data_dict.get('audit_status')
    auditor = data_dict.get('auditor', 'admin')
    audit_date = data_dict.get('audit_date', datetime.now().strftime("%Y-%m-%d %H:%M"))
    audit_remarks = data_dict.get('audit_remarks')

    row.audit_status = audit_status
    row.auditor = auditor
    row.audit_date = audit_date
    row.audit_remarks = audit_remarks

    db.session.commit()
    return myreponse(row.to_json())


@app.route('/holiday/api/v1.0/holiday_apply/cancel_audit/<int:id>', methods=['POST'])
def cancel_audit_holiday_apply(id):
    row = HolidayApply.query.filter_by(id=id).first()
    if row is None:
        abort(400)  # existing user

    data = request.form
    data_dict = data.to_dict()
    print(data_dict)

    audit_status = '-1'
    auditor = ''
    audit_date = ''
    audit_remarks = ''

    row.audit_status = audit_status
    row.auditor = auditor
    row.audit_date = audit_date
    row.audit_remarks = audit_remarks

    db.session.commit()
    return myreponse(row.to_json())


@app.route('/holiday/api/v1.0/information', methods=['GET'])
def get_information():
    querystr = request.args.get("querystr", '')
    querytype = request.args.get("querytype", 'json')
    offset = request.args.get("offset", '0')
    limit = request.args.get("limit", '10')
    sort = request.args.get('sort', 'id')
    order = request.args.get('order', 'desc')
    sidePagination = request.args.get('sidePagination', 'client')

    if querytype == 'string':
        wherestr = querystr
    else:
        wherestr = "1=1"
    print(wherestr)

    orderbystr = sort + " " + order
    print(orderbystr)
    # 分页paginate的参数page，是第几页，而offset是记录的偏移量，需要转换
    # 表格标题排序，根据table提交的信息进行排序，否则排序无效
    if sidePagination == 'server':
        page = (int(offset) // int(limit)) + 1
        pagination = PersonalInformation.query.filter(text(wherestr)).order_by(text(orderbystr)).paginate(page, int(limit), False)
        rows = pagination.items
        total = pagination.total
    else:
        rows = PersonalInformation.query.filter(text(wherestr)).order_by(text(orderbystr))
        total = PersonalInformation.query.filter(text(wherestr)).order_by(text(orderbystr)).count()
    print(total)

    if not rows:
        abort(400)
    data = [row.to_json() for row in rows]
    # data = get_data_by_model(EquipmentRepair)
    return myreponse(data, total)


@app.route('/holiday/api/v1.0/information/add', methods=['POST'])
def new_information():
    data = request.form
    data_dict = data.to_dict()
    print(data_dict)

    info_code = data_dict.get('info_code')
    info_name = data_dict.get('info_name')
    info_sex = data_dict.get('info_sex')
    info_birthday = data_dict.get('info_birthday')
    info_department = data_dict.get('info_department')
    info_workdate = data_dict.get('info_workdate')
    info_title = data_dict.get('info_title')

    if PersonalInformation.query.filter_by(info_code=info_code).first() is not None:
        abort(400)  # existing user

    row = PersonalInformation(info_code=info_code, info_name=info_name, info_sex=info_sex, info_birthday=info_birthday,
                              info_department=info_department, info_workdate=info_workdate, info_title=info_title)
    db.session.add(row)
    db.session.commit()

    return myreponse(row.to_json())


@app.route('/holiday/api/v1.0/information/edit/<int:id>', methods=['POST'])
def update_information(id):
    row = PersonalInformation.query.filter_by(id=id).first()
    if row is None:
        abort(400)  # existing user

    data = request.form
    data_dict = data.to_dict()
    print(data_dict)

    info_code = data_dict.get('info_code')
    info_name = data_dict.get('info_name')
    info_sex = data_dict.get('info_sex')
    info_birthday = data_dict.get('info_birthday')
    info_department = data_dict.get('info_department')
    info_workdate = data_dict.get('info_workdate')
    info_title = data_dict.get('info_title')

    row.info_code = info_code
    row.info_name = info_name
    row.info_sex = info_sex
    row.info_birthday = info_birthday
    row.info_department = info_department
    row.info_workdate = info_workdate
    row.info_title = info_title

    db.session.commit()
    return myreponse(row.to_json())


@app.route('/holiday/api/v1.0/information/delete/<int:id>', methods=['POST'])
def delete_information(id):
    row = PersonalInformation.query.filter_by(id=id).first()
    if row is None:
        abort(404)  # existing user

    db.session.delete(row)
    db.session.commit()
    return myreponse(row.to_json())


@app.route('/holiday/api/v1.0/holiday_statiscal', methods=['GET'])
def get_holiday_statiscal():
    querystr = request.args.get("querystr", ' 1=1 ')
    sort = request.args.get('sort', 'id')
    order = request.args.get('order', 'asc')
    sidePagination = request.args.get('sidePagination', 'client')

    orderbystr = sort + " " + order
    print(orderbystr)

    # 分页paginate的参数page，是第几页，而offset是记录的偏移量，需要转换
    # 表格标题排序，根据table提交的信息进行排序，否则排序无效
    if sidePagination == 'server':
        pass
    else:
        # 工作量统计主数据
        selectfield = 'apply_dept, apply_man, holiday_type'
        querystr = "audit_status='1' and %s" % querystr
        groupbystr = 'apply_dept, apply_man, holiday_type'
        sql_str = 'SELECT %s, sum(holiday_days) as holiday_days FROM holiday.holiday_apply ' \
                  'where %s ' \
                  'group by %s ' \
                  'order by %s;' % (selectfield, querystr, groupbystr, orderbystr)
        # sqlalchemy执行sql
        data_query = db.session.execute(sql_str)
        # 获取查询到的数据条数
        total = data_query.rowcount
        # fetchall()遍历到所有数据
        rows = data_query.fetchall()
        data = [{"apply_dept": row['apply_dept'], "apply_man": row['apply_man'], "holiday_type": row['holiday_type'],
                 "holiday_days": row['holiday_days']} for row in rows]

    return myreponse(data, total)


@app.route('/holiday/api/v1.0/holiday_days', methods=['GET'])
def get_holiday_days():
    # querystr = request.args.get("querystr", ' 1=1 ')
    department = request.args.get("department", '')
    apply_man = request.args.get("apply_man", '')
    holiday_year = request.args.get("holiday_year", '')
    sort = request.args.get('sort', 'id')
    order = request.args.get('order', 'asc')
    sidePagination = request.args.get('sidePagination', 'client')

    # 分页paginate的参数page，是第几页，而offset是记录的偏移量，需要转换
    # 表格标题排序，根据table提交的信息进行排序，否则排序无效
    if sidePagination == 'server':
        pass
    else:
        # 公休天数统计
        query_str1 = '1=1'
        query_str2 = "audit_status='1' and holiday_type = '公休' and left(start_date,4) = '%s'" % holiday_year
        if department:
            query_str1 = "info_department = '%s'" % department
            query_str2 = query_str2 + " and apply_dept = '%s'" % department
        if apply_man:
            query_str1 = query_str1 + " and info_name like '%%%s%%'" % apply_man
            query_str2 = query_str2 + " and apply_man like '%%%s%%'" % apply_man

        # querystr = "audit_status='1' and holiday_type = '公休' and %s " % querystr
        sql_str = 'select info_department, info_name, holiday_total, ifnull(holiday_used,0) as holiday_used, (holiday_total - ifnull(holiday_used,0)) as holiday_left  from(' \
                  'select info_department, info_name, case when YEAR(NOW())-left(info_workdate, 4) >=1 and YEAR(NOW())-left(info_workdate, 4) < 10 then 5 ' \
                  'when YEAR(NOW())-left(info_workdate, 4) >= 10 and YEAR(NOW())-left(info_workdate, 4) < 20 then 10 ' \
                  'when YEAR(NOW())-left(info_workdate, 4) >= 20 then 15  else 0 end as holiday_total from holiday.personal_information ' \
                  'where %s) as t1 ' \
                  'left join (' \
                  'select apply_dept, apply_man, holiday_type, sum(holiday_days) as holiday_used from holiday.holiday_apply ' \
                  'where %s ' \
                  'group by apply_dept, apply_man, holiday_type) as t2 ' \
                  'on t2.apply_dept = t1.info_department and t2.apply_man = t1.info_name' \
                  ' order by info_department, info_name;' % (query_str1, query_str2)
        print(sql_str)
        # sqlalchemy执行sql
        data_query = db.session.execute(sql_str)
        # 获取查询到的数据条数
        total = data_query.rowcount
        # fetchall()遍历到所有数据
        rows = data_query.fetchall()
        data = [{"apply_dept": row['info_department'], "apply_man": row['info_name'], "holiday_total": row['holiday_total'],
                 "holiday_used": row['holiday_used'], "holiday_left": row['holiday_left']} for row in rows]

    return myreponse(data, total)


@app.route('/holiday/api/v1.0/users', methods=['GET'])
def get_users():
    querystr = request.args.get("querystr", '')
    querytype = request.args.get("querytype", 'json')
    offset = request.args.get("offset", '0')
    limit = request.args.get("limit", '10')
    sort = request.args.get('sort', 'id')
    order = request.args.get('order', 'desc')
    sidePagination = request.args.get('sidePagination', 'client')

    if querytype == 'string':
        wherestr = querystr
    else:
        wherestr = "1=1"
    print(wherestr)

    orderbystr = sort + " " + order
    print(orderbystr)
    # 分页paginate的参数page，是第几页，而offset是记录的偏移量，需要转换
    # 表格标题排序，根据table提交的信息进行排序，否则排序无效
    if sidePagination == 'server':
        page = (int(offset) // int(limit)) + 1
        pagination = PersonalInformation.query.filter(text(wherestr)).order_by(text(orderbystr)).paginate(page, int(limit), False)
        rows = pagination.items
        total = pagination.total
    else:
        rows = PersonalInformation.query.filter(text(wherestr)).order_by(text(orderbystr))
        total = PersonalInformation.query.filter(text(wherestr)).order_by(text(orderbystr)).count()
    print(total)

    if not rows:
        abort(400)
    data = [row.to_json() for row in rows]
    # data = get_data_by_model(EquipmentRepair)
    return myreponse(data, total)


@app.route('/holiday/api/v1.0/users/add', methods=['POST'])
def new_user():
    data = request.form
    data_dict = data.to_dict()
    print(data_dict)

    info_code = data_dict.get('info_code')
    info_name = data_dict.get('info_name')
    info_sex = data_dict.get('info_sex')
    info_birthday = data_dict.get('info_birthday')
    info_department = data_dict.get('info_department')
    info_workdate = data_dict.get('info_workdate')
    info_title = data_dict.get('info_title')

    if PersonalInformation.query.filter_by(info_code=info_code).first() is not None:
        abort(400)  # existing user

    row = PersonalInformation(info_code=info_code, info_name=info_name, info_sex=info_sex, info_birthday=info_birthday,
                              info_department=info_department, info_workdate=info_workdate, info_title=info_title)
    db.session.add(row)
    db.session.commit()

    return myreponse(row.to_json())


@app.route('/holiday/api/v1.0/users/edit/<int:id>', methods=['POST'])
def update_user(id):
    row = PersonalInformation.query.filter_by(id=id).first()
    if row is None:
        abort(400)  # existing user

    data = request.form
    data_dict = data.to_dict()
    print(data_dict)

    info_code = data_dict.get('info_code')
    info_name = data_dict.get('info_name')
    info_sex = data_dict.get('info_sex')
    info_birthday = data_dict.get('info_birthday')
    info_department = data_dict.get('info_department')
    info_workdate = data_dict.get('info_workdate')
    info_title = data_dict.get('info_title')

    row.info_code = info_code
    row.info_name = info_name
    row.info_sex = info_sex
    row.info_birthday = info_birthday
    row.info_department = info_department
    row.info_workdate = info_workdate
    row.info_title = info_title

    db.session.commit()
    return myreponse(row.to_json())


@app.route('/holiday/api/v1.0/users/delete/<int:id>', methods=['POST'])
def delete_user(id):
    row = PersonalInformation.query.filter_by(id=id).first()
    if row is None:
        abort(404)  # existing user

    db.session.delete(row)
    db.session.commit()
    return myreponse(row.to_json())
