# _*_coding:utf-8 _*_
# @Author　 : Ric
import json
import re
from flask import Blueprint, request, jsonify
from application import app
from common.libs.UploadService import UploadService
from common.libs.UrlManager import UrlManager
from common.models.Image import Image

"""
Flask项目集成富文本编辑器UEditor使用
"""

route_upload = Blueprint('upload_page', __name__)


@route_upload.route('/ueditor', methods=['GET', 'POST'])
def ueditor():
    req_data = request.values
    action = req_data['action'] if 'action' in req_data else ''
    if action == 'config':
        # 返回upload_config.json文件的json格式内容。读取文件配置，过滤掉注释信息,只保留json格式的内容
        root_path = app.root_path
        config_path = f"{root_path}/web/static/plugins/ueditor/upload_config.json"
        with open(config_path) as fp:
            try:
                config_data = json.loads(re.sub(r'\/\*.*\*/', '', fp.read()))
            except:
                config_data = {}
        return jsonify(config_data)
    if action == 'uploadimage':
        return upload_image()
    if action == "listimage":
        return list_image()
    return 'upload'


def upload_image():
    """
    处理图片上传
    """
    # ueditor固定配置返回信息
    res = {'state': 'SUCCESS', 'url': '', 'title': '', 'original': ''}
    file_target = request.files
    up_file = file_target['upfile'] if 'upfile' in file_target else None
    if not up_file:
        res['state'] = '上传失败'
        return jsonify(res)

    ret = UploadService.upload_file(up_file)
    if ret['code'] != 200:
        res['state'] = '上传失败' + ret['msg']
        return jsonify(res)

    res['url'] = UrlManager.buildImageUrl(ret['data']['file_key'])
    return jsonify(res)


def list_image():
    res = {'state': 'SUCCESS', 'list': [], 'start': 0, 'total': 0}
    req_data = request.values
    start = int(req_data['start']) if 'start' in req_data else 0
    page_size = int(req_data['size']) if 'size' in req_data else 20
    query = Image.query
    if start > 0:
        query = query.fileter(Image.id < start)
    image_list = query.order_by(Image.id.desc()).limit(page_size).all()
    images = []
    if image_list:
        for item in image_list:
            images.append({'url': UrlManager.buildImageUrl(item.file_key)})
            start = item.id
    res['list'] = images
    res['start'] = start
    res['total'] = len(images)
    return jsonify(res)
