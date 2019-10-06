# -*- coding: utf-8 -*-
from flask import Blueprint, request, redirect, jsonify
from common.libs.Helper import ops_render, get_current_time
from common.libs.user.UserService import UserService
from common.models.User import User
from common.libs.UrlManager import UrlManager
from application import app, db
from common.libs.Helper import pagination
from sqlalchemy import or_

"""后台账号管理"""
route_account = Blueprint('account_page', __name__)


@route_account.route("/index")
def index():
    request_data = request.values
    res = {"code": 200}
    query = User.query

    # 关键字搜索功能，%模糊查询
    if 'mix_kw' in request_data:
        rule = or_(User.nickname.ilike(f"%{request_data['mix_kw']}%"),  # 用户名查询
                   User.mobile.ilike(f"%{request_data['mix_kw']}%"))  # 手机号查询
        query = query.filter(rule)

    if 'status' in request_data and int(request_data['status']) > -1:
        query = query.filter(User.status == int(request_data['status']))

    # 分页设置
    page = int(request_data['p']) if ('p' in request_data and request_data['p']) else 1
    page_params = {
        "total": query.count(),
        "page_size": app.config['PAGE_SIZE'],
        "page": page,
        "display": app.config["PAGE_DISPLAY"],
        "url": request.full_path.replace(f"&p={page}", "")
    }
    pages = pagination(page_params)
    offset = (page - 1) * app.config['PAGE_SIZE']
    limit = app.config['PAGE_SIZE'] * page
    account_list = query.order_by(User.uid.desc()).all()[offset:limit]

    res["list"] = account_list
    res["pages"] = pages
    res['search_on'] = request_data
    res['status_mapping'] = app.config['STATUS_MAPPING']
    return ops_render("account/index.html", res)


@route_account.route("/info")
def info():
    res = {}
    request_data = request.values
    uid = int(request_data.get('id', 0))
    back_url = UrlManager.buildUrl("/account/index")
    if uid < 1:
        return redirect(back_url)
    user_info = User.query.filter_by(uid=uid).first()
    if not user_info:
        return redirect(back_url)

    res['info'] = user_info

    return ops_render("account/info.html", res)


@route_account.route("/set", methods=["GET", "POST"])
def set_info():
    default_pwd = "******"
    if request.method == "GET":
        res = {}
        request_data = request.args  # 只能回去get请求的参数
        uid = int(request_data.get('id', 0))
        user_info = None
        if uid:
            user_info = User.query.filter_by(uid=uid).first()
        res['info'] = user_info
        return ops_render('account/set.html', res)

    res = {'code': 200, 'msg': '操作成功', 'data': {}}
    # 获取请求传过来参数
    request_data = request.values
    uid = request_data['id'] if 'id' in request_data else ''
    nickname = request_data['nickname'] if 'nickname' in request_data else ''
    mobile = request_data['mobile'] if 'mobile' in request_data else ''
    email = request_data['email'] if 'email' in request_data else ''
    login_name = request_data['login_name'] if 'login_name' in request_data else ''
    login_pwd = request_data['login_pwd'] if 'login_pwd' in request_data else ''
    # 验证参数是否合法
    if nickname is None or len(nickname) < 1:
        res['code'] = -1
        res['msg'] = "请输入符合规范的姓名~~"
        return jsonify(res)

    if mobile is None or len(mobile) < 1:
        res['code'] = -1
        res['msg'] = "请输入符合规范的手机号码~~"
        return jsonify(res)

    if email is None or len(email) < 1:
        res['code'] = -1
        res['msg'] = "请输入符合规范的邮箱~~"
        return jsonify(res)

    if login_name is None or len(login_name) < 1:
        res['code'] = -1
        res['msg'] = "请输入符合规范的登录用户名~~"
        return jsonify(res)

    if login_pwd is None or len(email) < 6:
        res['code'] = -1
        res['msg'] = "请输入符合规范的登录密码~~"
        return jsonify(res)
    # 验证登录名是否存在数据库其他用户信息里面,filter传入多个查询条件
    has_in = User.query.filter(User.login_name == login_name, User.uid != uid).first()
    if has_in:
        res['code'] = -1
        res['msg'] = "该登录名已存在，请换一个试试~~"
        return jsonify(res)

    # 数据库验证后修改，filter_by传入单个查询条件
    user_info = User.query.filter_by(uid=uid).first()
    if user_info:
        user_obj = user_info
    else:
        # 查询不到用户信息，说明为新增用户
        user_obj = User()
        user_obj.created_time = get_current_time()
        user_obj.login_salt = UserService.get_salt()
    user_obj.nickname = nickname
    user_obj.mobile = mobile
    user_obj.email = email
    user_obj.login_name = login_name
    if login_pwd != default_pwd:
        # 说明修改了密码
        user_obj.login_pwd = UserService.gene_pwd(login_pwd, user_obj.login_salt)
    user_obj.updated_time = get_current_time()

    db.session.add(user_obj)
    db.session.commit()
    return jsonify(res)


@route_account.route("/ops", methods=['POST'])
def ops():
    """
    后台账号的删除、恢复操作
    通过修改账号状态删除恢复账号
    """
    res = {'code': 200, 'msg': "操作成功", 'data': {}}
    request_data = request.values

    uid = request_data['id'] if 'id' in request_data else 0
    act = request_data['act'] if 'act' in request_data else ''
    if not uid:
        res['code'] = -1
        res['msg'] = '选择的账号不存在'
        return jsonify(res)
    if act not in ['remove', 'recover']:
        res['code'] = -1
        res['msg'] = '操作有误，请重试'
        return jsonify(res)

    user_info = User.query.filter_by(uid=uid).first()
    if not user_info:
        res['code'] = -1
        res['msg'] = '账号不存在'
        return jsonify(res)

    if act == "remove":
        user_info.status = 0
    elif act == "recover":
        user_info.status = 1

    user_info.update_time = get_current_time()
    db.session.add(user_info)
    db.session.commit()
    return jsonify(res)
