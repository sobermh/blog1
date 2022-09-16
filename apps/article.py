"""
@author:maohui
@time:2022/9/7 13:19
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

from flask import Blueprint, abort, render_template, request, session

from model.articles import Articles
from model.credit import Credit
from model.users import Users
from model.favorite import Favorite
from model.comment import Comment

bp = Blueprint("article", __name__, url_prefix="/article")


# 定义局部拦截器，未登录无法评论
@bp.before_request
def before_comment():
    # 添加拦截黑名单，这些不需要执行自动登录
    url = request.path
    pass_list = ['/article/comment', '/article/reply', '/article/post']
    if url in pass_list and (session.get('islogin') is None or session.get('islogin') != 'true'):
        return "not-login"


# 按要求展示文章
@bp.route('/<int:articleid>')
def read(articleid):
    try:
        # 数据格式：（article,'nickname'）
        result = Articles().find_article_by_id(articleid)
        if result is None:
            abort(404)
    except:
        abort(500)

    # 将查找的内容按照字典的方式存储并作为返回，为后期调用一半做准备
    dict = {}
    for k, v in result[0].__dict__.items():
        if not k.startswith('_sa_instance_state'):
            dict[k] = v
    dict['nickname'] = result.nickname
    # 如果已经消耗积分，则不再截取文章内容
    payed = Credit().check_payed_article(articleid)
    position = 0
    # 选取一半的内容显示，但是需要闭合最近的</p>标签，防止对页面其他标签产生影响
    # 但是只有该文章积分不是0的，且没有被当前用户购买过，才会显示一半，不然的话就是显示所有的页面
    if not payed and dict['credit'] != 0:
        content = dict['content']
        temp = content[0:int(len(content) / 2)]
        # 有些文章没有</p>,直接显示全部
        try:
            position = temp.rindex('</p>') + 4  # 从后向前数到</p>，+4是加上p
            dict['content'] = temp[0:position]
        except:
            pass
    Articles().update_read_count(articleid)  # 阅读次数+1
    is_favorited = Favorite().check_favorite(articleid)  # 判断当前用户文章是否被收藏
    # 获取当前文章的上一篇和下一篇
    prev_next = Articles().find_prev_next_by_id(articleid)
    # 显示当前文章对于的评论
    # comment_user = Comment().find_limit_with_user(articleid, 0, 50)
    comment_list = Comment().get_comment_user_list(articleid, 0, 50)
    return render_template('article.html', article=dict, position=position, payed=payed, is_favorited=is_favorited,
                           prev_next=prev_next, comment_list=comment_list)


# 展示所有文章
@bp.route('/readall', methods=['POST'])
def read_all():
    position = int(request.form.get('position'))
    articleid = request.form.get('articleid')
    result = Articles().find_article_by_id(articleid)
    content = result[0].content[position:]

    # 如果已经消耗积分，则不再扣除
    # (避免前端界面操作ok了，但是后台接口没有同步，前端界面无法调用接口了，但是用直接接口请求，会发生逻辑错误)
    payed = Credit().check_payed_article(articleid)
    if not payed:
        # 添加积分明细
        Credit().insert_detail(category="阅读文章", target=articleid, credit=-1 * result[0].credit)
        # 减去用户表的剩余积分
        Users().update_credit(credit=-1 * result[0].credit)

    return content


# 新增\取消收藏文章
@bp.route('/favorite', methods=['POST', 'DELETE'])
def add_favorite():
    articleid = request.form.get('articleid')
    if request.method == 'POST':
        if session.get('islogin') is None:
            return 'not-login'
        else:
            try:
                Favorite().insert_favorite(articleid)
                return 'favorite-pass'
            except:
                return 'favorite-fail'
    elif request.method == 'DELETE':
        try:
            Favorite().cancel_favorite(articleid)
            return 'cancel-pass'
        except:
            print(1)
            return 'cancel-fail'


# 添加评论
@bp.route('/comment', methods=['POST'])
def add():
    articleid = request.form.get('articleid')
    content = request.form.get('content')
    ipaddr = request.remote_addr
    # 对评论内容进行简单校验
    if len(content) < 3 or len(content) > 1000:
        return 'content-invalid'
    # 没有超出限制才能评论
    if Comment().check_limit_per_5():
        try:
            Comment().insert_comment(articleid, content, ipaddr)
            # 评论成功后，更新积分明细和剩余积分，及文章回复数量
            Credit().insert_detail(category='添加评论', target=articleid, credit=2)
            Users().update_credit(2)
            Articles().update_replycount(articleid)
            return 'add-pass'
        except:
            return 'add-fail'
    else:
        return 'add-limit'


# 添加回复的评论
@bp.route('/reply', methods=['POST'])
def reply():
    articleid = request.form.get('articleid')
    commentid = request.form.get('commentid')
    content = request.form.get('content')
    ipaddr = request.remote_addr
    # 对评论内容进行简单校验
    if len(content) < 3 or len(content) > 1000:
        return 'content-invalid'
    # 没有超出限制才能回复
    if Comment().check_limit_per_5():
        try:
            Comment().insert_reply(articleid=articleid, commentid=commentid, content=content, ipaddr=ipaddr)
            # 回复评论成功后，更新积分明细和剩余积分，及文章回复数量
            Credit().insert_detail(category='回复评论', target=articleid, credit=2)
            Users().update_credit(2)
            Articles().update_replycount(articleid)
            return 'reply-pass'
        except:
            return 'reply-fail'
    else:
        return 'reply-limit'


# 打开上传文章页面,新增文章
@bp.route('/post', methods=['GET', 'POST'])
def post():
    import markdown
    if request.method == 'GET':
        return render_template('post.html')
    else:
        headline = request.form.get('headline')
        content = request.form.get('content')
        type = int(request.form.get('type'))
        credit = int(request.form.get('credit'))
        drafted = int(request.form.get('drafted'))
        if session.get('userid') is None:
            return 'perm-denied'
        else:
            try:
                print(1)
                id = Articles().insert_article(type=type, headline=headline, content=markdown.markdown(content)
                                               , credit=credit)
                print(id)
                return str(id)
            except Exception as e:
                return 'post-fail'

# # 新增文章
# @bp.route('',methods=['POST'])
# def add_article('')
