"""
@author:maohui
@time:2022/9/9 13:45
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

from flask import Blueprint, request, render_template, jsonify

bp = Blueprint("ueditor", __name__, url_prefix="/post")

import sys


@bp.route('/uedit', methods=['GET', 'POST'])
def uedit():
    # 根据uedittor的接口定义规则，如果前者参数为action=config
    # 则表示试图请求后台的config.json文件，请求成功则说明后台接口能正常工作
    param = request.args.get('action')
    if request.method == 'GET' and param == 'config':
        return render_template('config.json')
    # 构造上传图片的接口
    elif request.method == 'POST' and request.args.get('action') == 'uploadimage':
        f = request.files['upfile']  # 获取前端图片文件数据
        filename = f.filename
        f.save(sys.path[0] + '/static/upload/' + filename)  # 保存图片到upload目录
        # f.save('./static/upload/' + filename)  # 保存图片到upload目录
        result = {}  # 构造响应数据
        result['state'] = 'SUCCESS'
        result['url'] = f"/static/upload/{filename}"
        result['title'] = filename
        result['original'] = filename

        return jsonify(result)  # 以json数据格式返回响应，供前端编辑器引用


@bp.route('/editormd')
def editormd():
    return render_template("post_md.html")
