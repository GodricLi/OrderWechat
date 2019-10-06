# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify, redirect
from application import app, db
from common.libs.Helper import ops_render, pagination
from common.models.food.Food import Food
from common.models.food.FoodCat import FoodCat
from common.libs.Helper import get_current_time
from common.libs.UrlManager import UrlManager
from sqlalchemy import or_

route_food = Blueprint('food_page', __name__)


@route_food.route("/index")
def index():
    res = {}
    req_data = request.values
    page = int(req_data['p']) if ('p' in req_data and req_data['p']) else 1
    query = Food.query
    if 'mix_kw' in req_data:
        rule = or_(Food.name.ilike(f'%{req_data["mix_kw"]}%'),
                   Food.tags.ilike(f'%{req_data["mix_kw"]}%'))
        query = query.filter(rule)

    if 'status' in req_data and int(req_data['status']) > -1:
        query = query.filter(Food.cat_id == int(req_data['cat_id']))

    page_params = {
        'total': query.count(),
        'page_size': app.config['PAGE_SIZE'],
        'page': page,
        'display': app.config['PAGE_DISPLAY'],
        'url': request.full_path.replace("&p={}".format(page), "")
    }
    pages = pagination(page_params)
    offset = (page - 1) * app.config['PAGE_SIZE']
    food_list = query.order_by(Food.id.desc()).offset(offset).limit(app.config['PAGE_SIZE']).all()

    res['list'] = food_list
    res['pages'] = pages
    res['search_on'] = req_data
    res['status_mapping'] = app.config['STATUS_MAPPING']
    res['current'] = 'index'

    return ops_render("food/index.html", res)


@route_food.route("/info")
def info():
    return ops_render("food/info.html")


@route_food.route("/set", methods=['GET', 'POST'])
def food_set():
    """编辑、添加美食"""
    if request.method == 'GET':
        res = {}
        req_data = request.args
        fid = int(req_data.get('id', 0))
        food_info = Food.query.filter_by(id=fid).first()
        if food_info and food_info.status != 1:
            return redirect(UrlManager.buildUrl('/food/index'))
        cat_list = FoodCat.query.all()
        res['info'] = food_info
        res['cat_list'] = cat_list
        res['current'] = 'index'
        return ops_render("food/set.html", res)
    res = {'code': 200, 'msg': '操作成功', 'data': {}}
    req_data = request.values
    fid = int(req_data['id']) if 'id' in req_data and req_data['id'] else 0



@route_food.route("/cat")
def cat():
    res = {}
    req_data = request.values
    query = FoodCat.query

    if 'status' in req_data and int(req_data['status']) > -1:
        query = query.filter(FoodCat.status == int(req_data['status']))
    cat_list = query.order_by(FoodCat.weight.desc(), FoodCat.id.desc()).all()
    res['list'] = cat_list
    res['search_on'] = req_data
    res['status_mapping'] = app.config['STATUS_MAPPING']
    res['current'] = 'cat'
    return ops_render("food/cat.html", res)


@route_food.route("/cat-set", methods=['GET', 'POST'])
def cat_set():
    if request.method == 'GET':
        res = {}
        req_data = request.values
        uid = int(req_data.get('id', 0))
        food_info = None
        if uid:
            food_info = FoodCat.query.filter_by(id=uid).first()
        res['info'] = food_info
        return ops_render("food/cat_set.html", res)
    # POST：修改或者添加操作
    res = {'code': 200, 'msg': '操作成功', 'data': {}}
    req_data = request.values
    uid = req_data['id'] if 'id' in req_data else 0
    name = req_data['name'] if 'name' in req_data else ''
    weight = int(req_data['weight']) if ('weight' in req_data and int(req_data['weight']) > 0) else 1

    if not name or len(name) < 1:
        res['code'] = -1
        res['msg'] = '分类名不规范'
        return jsonify(res)

    food_cat_info = FoodCat.query.filter_by(id=uid).first()
    if food_cat_info:
        model_food_cat = food_cat_info
    else:
        # 查询不到说明是添加操作
        model_food_cat = FoodCat()
        model_food_cat.created_time = get_current_time()
    # 添加和修改的共用代码
    model_food_cat.name = name
    model_food_cat.weight = weight
    model_food_cat.update_time = get_current_time()
    db.session.add(model_food_cat)
    db.session.commit()
    return jsonify(res)


@route_food.route("/cat-ops", methods=['POST'])
def cat_ops():
    """美食分类的删除恢复操作"""
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

    food_info = FoodCat.query.filter_by(id=uid).first()
    if not food_info:
        res['code'] = -1
        res['msg'] = '分类不存在'
        return jsonify(res)

    if act == "remove":
        food_info.status = 0
    elif act == "recover":
        food_info.status = 1

    food_info.update_time = get_current_time()
    db.session.add(food_info)
    db.session.commit()
    return jsonify(res)
