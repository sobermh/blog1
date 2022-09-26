"""
@author:maohui
@time:2022/8/31 13:54
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
import time

from flask import session
from sqlalchemy import Table, MetaData, func

from app import db

from model.users import Users


# from .users import Users
# ImportError: attempted relative import with no known parent package(可能是该父目录没有加载进来)


class Articles(db.Model):
    __table__ = Table('articles', MetaData(db.engine), autoload=True)

    # 根据id查询文章,数据格式：（Atticle,'nickname'）
    def find_article_by_id(self, articleid):
        row = db.session.query(Articles, Users.nickname).join(Users, Users.userid == Articles.userid) \
            .filter(Articles.drafted == 0, Articles.articleid == articleid).first()
        db.session.close()
        return row

    # 查询所有文章
    def find_all_article(self):
        result = db.session.query(Articles).all()
        db.session.close()
        return result

    # 指定分页的limit和offset的参数值，同时与用户表做连接查询
    def find_limit_with_users(self, start, count):
        result = db.session.query(Articles, Users).join(Users, Users.userid == Articles.userid) \
            .filter(Articles.drafted == 0) \
            .order_by(Articles.articleid.desc()).limit(count).offset(start).all()
        db.session.close()
        return result

    # 统计当前文章的总数量,
    def get_total_count(self):
        count = db.session.query(Articles).filter(Articles.drafted == 0).count()
        # print(count)
        db.session.close()
        return count

    # 根据文章类型获取文章，同时与用户表做连接查询，同时分页
    def find_by_type(self, start, count, type):
        result = db.session.query(Articles, Users).join(Users, Users.userid == Articles.userid) \
            .filter(Articles.drafted == 0, Articles.type == type) \
            .order_by(Articles.articleid.desc()).limit(count).offset(start).all()
        db.session.close()
        return result

    # 根据文章类型来获取总数量
    def get_count_by_type(self, type):
        count = db.session.query(Articles).filter(Articles.drafted == 0, Articles.type == type).count()
        db.session.close()
        return count

    # 根据文章标题进行模糊搜索
    def find_by_headline(self, start, count, headline):
        result = db.session.query(Articles, Users).join(Users, Users.userid == Articles.userid) \
            .filter(Articles.drafted == 0, Articles.headline.like('%' + headline + '%')) \
            .order_by(Articles.articleid.desc()).limit(count).offset(start).all()
        db.session.close()
        return result

    # 根据搜索结果统计分页总数量
    def get_count_by_headline(self, headline):
        count = db.session.query(Articles). \
            filter(Articles.drafted == 0, Articles.headline.like('%' + headline + '%')).count()
        db.session.close()
        return count

    # 推荐-最新文章:3篇
    def find_last_article(self):
        result = db.session.query(Articles.articleid, Articles.headline) \
            .filter(Articles.drafted == 0) \
            .order_by(Articles.articleid.desc()).limit(3).all()
        db.session.close()
        return result

    # 推荐-最多阅读推荐：3
    def find_most_read(self):
        result = db.session.query(Articles.articleid, Articles.headline) \
            .filter(Articles.drafted == 0) \
            .order_by(Articles.readcount.desc()).limit(3).all()
        db.session.close()
        return result

    # 推荐-特别推荐的文章：3,如果超过3篇随机显示
    def find_recommend(self):
        result = db.session.query(Articles.articleid, Articles.headline) \
            .filter(Articles.drafted == 0, Articles.recommended == 1) \
            .order_by(func.rand()).limit(3).all()
        db.session.close()
        return result

    # 封装三个推荐数据
    def find_last_most_recommended(self):
        last = self.find_last_article()
        most = self.find_most_read()
        recommended = self.find_recommend()
        db.session.close()
        return last, most, recommended

    # 每阅读一次文章，阅读的次数加1
    def update_read_count(self, articleid):
        article = db.session.query(Articles).filter_by(articleid=articleid).first()
        # print(article.readcount)
        article.readcount += 1
        db.session.commit()
        db.session.close()

    # 根据文章编号查询文章标题
    def find_headline_by_id(self, articleid):
        row = db.session.query(Articles.headline).filter_by(articleid=articleid).first()
        # print(row)   ('标题2dvsduhvuhbnvh',)
        # print(type(row))  <class 'sqlalchemy.engine.row.Row'>
        # print(row.headline)   标题2dvsduhvuhbnvh
        db.session.close()
        return row.headline

    # 获取当前文章的上一篇和下一篇
    def find_prev_next_by_id(self, articleid):
        dict = {}
        # 上一篇
        # 查询id比当前编号小的所有文章中，id最大的一个
        row = (db.session.query(Articles).filter(Articles.drafted == 0, Articles.articleid < articleid)) \
            .order_by(Articles.articleid.desc()).limit(1).first()
        # 如果当前已经是第一篇，上一篇也是当前文章
        if row is None:
            prev_id = articleid
        else:
            prev_id = row.articleid
        dict['prev_id'] = prev_id
        dict['prev_headline'] = self.find_headline_by_id(prev_id)
        #下一篇
        # 查询id比当前编号大的所有文章中，id最小的一个
        row = (db.session.query(Articles).filter(Articles.drafted == 0, Articles.articleid > articleid)) \
            .order_by(Articles.articleid).limit(1).first()
        # 如果当前已经是最后一篇，下一一篇也是当前文章
        if row is None:
            next_id = articleid
        else:
            next_id = row.articleid
        dict['next_id'] = next_id
        dict['next_headline'] = self.find_headline_by_id(next_id)
        # print(dict)
        db.session.close()
        return dict

    # 当发表或者回复评论后，为文章表字段replycount加1
    def update_replycount(self,articleid):
        row = db.session.query(Articles).filter_by(articleid=articleid).first()
        row.replycount +=1
        db.session.commit()
        db.session.close()


    # 插入一篇新的文章，草稿或投稿通过参数进行区分
    def insert_article(self,type,headline,content,credit,drafted=0):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        userid = session.get('userid')
        # 其他字段的数据库中均已设置好默认值，无须手工插入
        article = Articles(userid=userid,type=type,headline=headline,content=content
                           ,credit=credit,drafted=drafted,createtime=now,updatetime=now)
        db.session.add(article)
        db.session.commit()
        # db.session.close()
        return article.articleid     #讲新的文章编号返回，便于前端页面跳




# if __name__=='__main__':
#     Articles().insert_article(type=1,headline=2,content=2,credit=2)
