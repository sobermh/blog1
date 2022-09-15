"""
@author:maohui
@time:2022/8/22 17:19
  　　　　　　　 ┏┓    ┏┓+ +
  　　　　　　　┏┛┻━━━━┛┻┓ + +
  　　　　　　　┃        ┃ 　 
  　　　　　　　┃     ━  ┃ ++ + + +
  　　　　　 　████━████ ┃+
  　　　　　　　┃        ┃ +
  　　　　　　　┃   ┻    ┃
  　　　　　　　┃        ┃ + +
  　　　　　　　┗━┓   ┏━━┛
  　　　　　　　  ┃   ┃
  　　　　　　　  ┃   ┃ + + + +
  　　　　　　　  ┃   ┃　　　Code is far away from bug with the animal protecting
  　　　　　　　  ┃   ┃+ 　　　　神兽保佑,代码无bug
  　　　　　　　  ┃   ┃
  　　　　　　　  ┃   ┃　　+
  　　　　　　　  ┃   ┗━━━━━━━┓ + +     
  　　　　　　　  ┃           ┣┓
  　　　　　　　  ┃           ┏┛
  　　　　　　　  ┗┓┓┏━━━━━┳┓┏┛ + + + +
  　　　　　　　   ┃┫┫     ┃┫┫
  　　　　　　　   ┗┻┛     ┗┻┛+ + + +
"""
import json

from flask import Blueprint, render_template, abort, jsonify, session, request
import math

from model.articles import Articles  # （因为注册蓝图的放在了'__main__'后面，不存在循环导入的问题）
from model.users import Users

bp = Blueprint("/", __name__, url_prefix="/")


# 首页地址和显示
@bp.route("/")
def index_home():
    pagesize = 4
    articles = Articles()
    result = articles.find_limit_with_users(0, pagesize)  # 从0开始一共2篇
    total = math.ceil(articles.get_total_count() / pagesize)  # 总页数
    #推荐
    last,most,recommended = articles.find_last_most_recommended()
    return render_template("index.html", result=result, page=1, total=total,last=last,most=most,recommended=recommended)


# 首页分页
@bp.route('/page/<int:page>')
def paginate(page):
    pagesize = 4
    start = (page - 1) * pagesize  # 1==>0  2==>2
    articles = Articles()
    result = articles.find_limit_with_users(start, pagesize)  # 从start开始，数2个，左闭右开
    total = math.ceil(articles.get_total_count() / pagesize)  # 总页数

    return render_template("index.html", result=result, page=page, total=total)


# 按照文章类型分类，并分页
@bp.route('/type/<int:type>-<int:page>')
def classify(type, page):
    pagesize = 4
    start = (page - 1) * pagesize  # 1==>0  2==>2
    articles = Articles()
    result = articles.find_by_type(start, pagesize, type)
    total = math.ceil(articles.get_count_by_type(type) / pagesize)  # 指定类型的总页数
    print(total)
    print(page)
    print(result)

    return render_template('type.html', result=result, type=type, page=page, total=total)


# 按照搜索关键字筛选，并分页
@bp.route('/search/<int:page>-<keyword>')
def search(page,keyword):
    pagesize = 4
    #后台验证输入参数是否异常
    keyword = keyword.strip()
    if keyword is None or keyword == ' 'or '%' in keyword or len(keyword)>10:
        abort(404)
    #筛选并输出指定页数的文章
    start = (page - 1) * pagesize  # 1==>0  2==>2
    articles =Articles()
    result = articles.find_by_headline(start, pagesize, keyword)
    total = math.ceil(articles.get_count_by_headline(keyword) / pagesize)  # 指定类型的总页数
    return render_template('search.html', result=result, page=page, total=total,keyword=keyword)


# 向前端返回三个推荐的数据
@bp.route('/recommend')
def recommend():
    articles = Articles()
    last,most,recommended = articles.find_last_most_recommended()

    # 解决error:TypeError: Object of type Row is not JSON serializable
    list_last=[]
    list_most=[]
    list_recommended=[]
    for items in last:
        list_last.append(list(items))
    for items in most :
        list_most.append(list(items))
    for items in recommended:
        list_recommended.append(list(items))
    return jsonify(list_last,list_most,list_recommended)



