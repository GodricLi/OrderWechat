# _*_coding:utf-8 _*_
# @Author　 : Ric
from flask import Flask
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
import os


class Application(Flask):

    def __init__(self, import_name, template_folder=None, root_path=None):
        super().__init__(import_name,
                         template_folder=template_folder,
                         root_path=root_path,
                         static_folder=None)
        self.config.from_pyfile('config/base_setting.py')
        if "ops_config" in os.environ:
            # 终端执行export ops_config=local，就会加载local_setting里面的配置文件
            self.config.from_pyfile(f'config/{os.environ["ops_config"]}_setting.py')

        db.init_app(self)


db = SQLAlchemy()
app = Application(__name__,
                  template_folder=os.getcwd() + '/web/templates',
                  root_path=os.getcwd())
manager = Manager(app)

"""函数模板：将python类方法添加到模板文件,相互导入的包不能放在顶部"""
from common.libs.UrlManager import UrlManager

app.add_template_global(UrlManager.buildStaticUrl, 'buildStaticUrl')
app.add_template_global(UrlManager.buildUrl, 'buildUrl')
