# _*_coding:utf-8 _*_
# @Author　 : Ric
import json
from flask import request, g
from application import app, db
from common.libs.Helper import get_current_time
from common.models.log.AppAccessLog import AppAccessLog
from common.models.log.AppErrorLog import AppErrorLog


class LogService:
    """
    访问url记录，访问错误信息记录
    """

    @staticmethod
    def add_access_log():
        """
        将访问url添加到日志
        """
        target = AppAccessLog()
        target.target_url = request.url
        target.referer_url = request.referrer
        target.ip = request.remote_addr
        target.query_params = json.dumps(request.values.to_dict())
        if 'current_user' in g and g.current_user:
            target.uid = g.current_user.uid
        target.ua = request.headers.get('User-Agent')
        target.created_time = get_current_time()
        db.session.add(target)
        db.session.commit()
        return True

    @staticmethod
    def add_error_log(content):
        """
        添加访问错误的信息到日志
        """
        if 'favicon.ico' in request.url:
            return
        target = AppErrorLog()
        target.target_url = request.url
        target.referer_url = request.referrer
        target.query_params = json.dumps(request.values.to_dict())
        target.content = content
        target.created_time = get_current_time()
        db.session.add(target)
        db.session.commit()
        return True
