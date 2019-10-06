# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify, make_response, redirect, g
from common.models.User import User
from common.libs.user.UserService import UserService
from common.libs.UrlManager import UrlManager
from common.libs.Helper import ops_render
from application import app, db
import json

"""后台账号登录相关设置"""
route_user = Blueprint("user_page", __name__)


@route_user.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return ops_render("user/login.html")
    res = {"code": None, "msg": "登录成功", "data": {}}
    req = request.values
    login_name = req["login_name"] if "login_name" in req else ""
    login_pwd = req["login_pwd"] if "login_pwd" in req else ""

    if login_name is None or len(login_name) < 1:
        res["code"] = -1
        res["msg"] = "请输入正确的用户名或密码"
        return jsonify(res)

    if login_pwd is None or len(login_pwd) < 1:
        res["code"] = -1
        res["msg"] = "请输入正确的用户名或密码"
        return jsonify(res)

    # 查询数据库记录，取第一条,返回一个对象
    user_info = User.query.filter_by(login_name=login_name).first()
    if not user_info:
        res["code"] = -1
        res["msg"] = "请输入正确的用户名或密码"
        return jsonify(res)

    # 将输入的密码传入加密方法与数据库加密数据对比
    if user_info.login_pwd != UserService.gene_pwd(login_pwd, user_info.login_salt):
        res["code"] = -1
        res["msg"] = "请输入正确的用户名或密码"
        return jsonify(res)

    # 验证账户的状态是否有效
    if user_info.status != 1:
        res['code'] = -1
        res['msg'] = "账号已被禁用，请联系管理员处理"
        return jsonify(res)
    response = make_response(json.dumps({"code": 200, "msg": "登录成功"}))
    response.set_cookie(app.config["AUTH_COOKIE_NAME"],
                        f"{UserService.gene_auth_code(user_info)}#{user_info.uid}",
                        60 * 60 * 24 * 120)  # 保存120天

    return response


@route_user.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "GET":
        return ops_render("user/edit.html", {"current": "edit"})

    res = {"code": 200, "msg": "操作成功", "data": {}}
    request_data = request.values
    nickname = request_data["nickname"] if "nickname" in request_data else ""
    email = request_data["email"] if "email" in request_data else ""

    # 验证邮箱和姓名是否符合规范
    if not nickname or len(nickname) < 1:
        res["code"] = -1
        res["msg"] = "请输入规范的姓名"
        return jsonify(res)

    if not email or len(email) < 1:
        res["code"] = -1
        res["msg"] = "请输入规范的邮箱"
        return jsonify(res)

    # 通过验证
    user_info = g.current_user
    user_info.nickname = nickname
    user_info.email = email

    # 数据库更新user对象
    db.session.add(user_info)
    db.session.commit()
    return jsonify(res)


@route_user.route("/reset-pwd", methods=["GET", "POST"])
def reset_pwd():
    if request.method == "GET":
        return ops_render("user/reset_pwd.html", {"current": "reset-pwd"})
    res = {"code": 200, "msg": "操作成功", "data": {}}
    request_data = request.values

    old_password = request_data["old_password"] if "old_password" in request_data else ""
    new_password = request_data["new_password"] if "new_password" in request_data else ""

    if not old_password or len(old_password) < 6:
        res["code"] = -1
        res["msg"] = "请输入不少于6位的新密码~~"
        return jsonify(res)

    if old_password == new_password:
        res["code"] = -1
        res["msg"] = "新密码不能与原密码相同~~"
        return jsonify(res)

    user_info = g.current_user
    # 修改密码后更新user对象的加密字符串
    user_info.login_pwd = UserService.gene_pwd(new_password, user_info.login_salt)
    # 数据库更新
    db.session.add(user_info)
    db.session.commit()

    # 更新新密码的cookie值，避免cookie验证不通过造成的页面退出,跳转到登录页面
    response = make_response(json.dumps({"code": 200, "msg": "修改成功"}))
    response.set_cookie(app.config["AUTH_COOKIE_NAME"],
                        f"{UserService.gene_auth_code(user_info)}#{user_info.uid}",
                        60 * 60 * 24 * 120)  # 保存120天

    return response


@route_user.route("/logout")
def logout():
    response = make_response(redirect(UrlManager.buildUrl("/user/login")))
    response.delete_cookie(app.config["AUTH_COOKIE_NAME"])
    return response
