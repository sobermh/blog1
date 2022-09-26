from flask import Flask, session, request
# from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

import config  # 导入配置文件

# app = Flask(__name__,template_folder="",static_url_path="",static_folder="")
# 默认的模板路径，默认的静态url路径，默认的静态文件路径


app = Flask(__name__)
app.config.from_object(config)  # 绑定config文件中的配置
db=SQLAlchemy(app) # 实例化数据库对象


# 定义404错误页面
@app.errorhandler(404)
def page_not_found(e):
    return "404"


# 定义500错误页面
@app.errorhandler(500)
def server_error(e):
    return "500"

# 定义全局拦截器，实现自动登录
@app.before_request
def auto_login():
    from model.users import Users  # 解决循环导入问题
    # 添加拦截白名单，这些不需要执行自动登录
    url = request.path
    pass_list = ['/user','/login','/logout']
    if url in pass_list or url.endswith('.js') or url.endswith('.jpg'):
        pass
    # 自动登录验证
    elif session.get('islogin') is None:
        username = request.cookies.get('username')
        password = request.cookies.get('password')
        if username != None and password != None:
            result = Users().find_user_by_username(username)
            if len(result) == 1 and result[0].password == password:
                session['islogin'] = 'true'
                session['userid'] = result[0].userid
                session['username'] = username
                session['nickname'] = result[0].nickname
                session['role'] = result[0].role


# 定义导航类型函数，供模板页面调用
@app.context_processor
def gettype():
    type = {
        '1': 'python',
        '2': '测试',
        '3': '后端',
        '4' : 'vlog'
    }
    return dict(article_type=type)


# 通过自定义过滤器来重构truncate原生过滤器：：：：
# 中文定义为1个字符，英文为0.5个字符
# 遍历整个字符串，获取每一个字符的ASCII码，如果是在128以内或者256，则认为是英文，否则是中文
def mytruncate(s,length,end="..."):
    count= 0
    new = ''
    for c in s:
        new += c  #每循环一次，将一个字符添加到new字符串后面
        if ord(c) <= 128:
            count += 0.5
        else:
            count +=1
        if count>=length:    #判断长度，当字符串长度大于等于指定长度时，退出循环
            break
    return new + end
#注册mytruncate过滤器，自定义函数的会覆盖原生的
app.jinja_env.filters.update(truncate=mytruncate)




# #缓解问题：QueuePool limit of size 10 overflow 10 reached, connection timed out, timeout 30.00
# @app.teardown_appcontext
# def shutdown_session(exception=None):
#     db.session.remove()




if __name__ == '__main__':

    # 将注册蓝图放在这里，解决循环导入问题（或者将蓝图中导入数据库模块的操作放在函数中）
    from apps import *  # 导入init中的蓝图
    app.register_blueprint(index_bp)  # 注册蓝图
    app.register_blueprint(user_bp)  # 注册蓝图
    app.register_blueprint(article_bp)
    app.register_blueprint(post_bp)
    app.run(debug=True, host='0.0.0.0', port=3355,threaded=True)
