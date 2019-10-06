# _*_coding:utf-8 _*_
# @Author　 : Ric
SERVER_PORT = 5000
DEBUG = False
SQLALCHEMY_ECHO = False
SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@localhost/food_db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ENCODING = "utf8mb4"
AUTH_COOKIE_NAME = 'food'

"""过滤url，不需要登录就能访问的"""
# 登录页面
IGNORE_URLS = [
    '^/user/login'
]
# 静态文件
IGNORE_CHECK_LOGIN_URLS = [
    '^/static',
    '^/favicon.ico'
]

"""自定义分页设置"""
PAGE_SIZE = 10
PAGE_DISPLAY = 10

STATUS_MAPPING = {
    "1": "正常",
    "0": "已删除"
}

RELEASE_VERSION = None

# 文件上传配置
UPLOAD = {
    'ext': ['jpg', 'gif', 'bmp', 'jpeg', 'png'],
    'prefix_path': '/web/static/upload/',
    'prefix_url': '/static/upload/'
}
# 配置文件上传至服务器的路径
APP = {
    # 服务器域名及端口
    'image': 'http://0.0.0.0:5000'
}
