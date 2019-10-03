# _*_coding:utf-8 _*_
# @Author　 : Ric
import re
from application import app
from flask import request, redirect, g
from common.libs.UrlManager import UrlManager
from common.models.User import User
from common.libs.user.UserService import UserService
from common.libs.LogService import LogService


@app.before_request
def before_request():
    ignore_urls = app.config['IGNORE_URLS']
    ignore_check_login_urls = app.config['IGNORE_CHECK_LOGIN_URLS']
    path = request.path
    # 如果是静态文件就不用查询用户信息
    pattern = re.compile('|'.join(ignore_check_login_urls))
    if pattern.match(path):
        return
    user_info = check_login()

    # 登录成功之后设置一个user_info对象全局变量
    g.current_user = None
    if user_info:
        g.current_user = user_info
    # 登录之后url加入日志
    LogService.add_access_log()
    pattern = re.compile('%s' % "|".join(ignore_urls))
    if pattern.match(path):
        return
    if not user_info:
        return redirect(UrlManager.buildUrl('/user/login'))
    return


def check_login():
    """
    判断用户是否登录
    :return:
    """
    cookies = request.cookies
    auth_cookie = cookies[app.config["AUTH_COOKIE_NAME"]] if app.config["AUTH_COOKIE_NAME"] in cookies else None
    if not auth_cookie:
        return False
    auth_info = auth_cookie.split('#')
    if len(auth_info) != 2:
        return False
    try:
        user_info = User.query.filter_by(uid=auth_info[1]).first()
    except Exception:
        return False
    if not user_info:
        return False
    if auth_info[0] != UserService.gene_auth_code(user_info):
        return False
    if user_info.status != 1:
        return False
    return user_info
