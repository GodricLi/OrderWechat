# _*_coding:utf-8 _*_
# @Author　 : Ric

from application import app
from common.libs.LogService import LogService
from common.libs.Helper import ops_render


@app.errorhandler(404)
def error_404(e):
    LogService.add_error_log(e)
    return ops_render('error/error.html', {'status': 404, 'msg': '很抱歉！您访问的页面不存在'})
