# _*_coding:utf-8 _*_
# @Author　 : Ric
import datetime
import os, stat, uuid
from werkzeug.utils import secure_filename
from application import app, db
from common.models.Image import Image
from common.libs.Helper import get_current_time


class UploadService:
    """
    处理文件上传
    """

    @staticmethod
    def upload_file(file):
        config_upload = app.config['UPLOAD']
        res = {'code': 200, 'msg': '操作成功', 'data': {}}
        # 获取安全的文件名
        filename = secure_filename(file.filename)
        ext = filename.rsplit('.', 1)[1]
        if ext not in config_upload['ext']:
            res['code'] = -1
            res['msg'] = '不被允许的扩展类型'
            return res

        # 拼接文件目录
        root_path = app.root_path + config_upload['prefix_path']
        # 以当前时间创建目录，避免不兼容get_current_time
        file_dir = datetime.datetime.now().strftime('%Y%m%d')
        save_dir = root_path + file_dir
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
            # 赋予目录以及其他用户文件读写权限
            os.chmod(save_dir, stat.S_IRWXU | stat.S_IRGRP | stat.S_IRWXO)
        # 构造文件名及其扩展
        filename = str(uuid.uuid4()).replace('-', '') + '.' + ext
        # 直接保存文件
        file.save(f'{save_dir}/{filename}')

        # 将完整的文件路径加文件名存入数据库
        model_image = Image()
        model_image.file_key = file_dir + '/' + filename
        model_image.created_time = get_current_time()
        db.session.add(model_image)
        db.session.commit()

        res['data'] = {
            'file_key': model_image.file_key
        }
        return res

