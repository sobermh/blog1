"""
@author:maohui
@time:2022/9/8 14:23
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

from app import db
from sqlalchemy import Table, MetaData

from common.utility import Model_to_list

from model.users import Users


class Comment(db.Model):
    __table__ = Table("comment", MetaData(db.engine), autoload=True)

    # 新增一条评论
    def insert_comment(self, articleid, content, ipaddr):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        comment = Comment(userid=session.get('userid'), articleid=articleid, content=content
                          , ipaddr=ipaddr, createtime=now, updatetime=now)
        db.session.add(comment)
        db.session.commit()

    # 根据文章编号查询所有评论
    def find_by_articleid(self, articleid):
        result = db.session.query(Comment).filter_by(articleid=articleid).all()
        return result

    # 根据用户编号和日期进行查询是否已经超过每天5条限制
    def check_limit_per_5(self):
        start = time.strftime('%Y-%m-%d 00:00:00')  # 当天的起始时间
        end = time.strftime('%Y-%m-%d 23:59:59')  # 当天的结束时间
        result = db.session.query(Comment).filter(Comment.userid == session.get('userid')
                                                  , Comment.createtime.between(start, end)).all()
        if len(result) > 5:
            return False  # 返回True表示今天已经不能再发表评论
        else:
            return True

    # 查询评论与用户信息，注意评论也需要分页[(Comment,Users),(Comment,Users)]
    def find_limit_with_user(self, articleid, start, count):
        result = db.session.query(Comment, Users).join(Users, Users.userid == Comment.userid) \
            .filter(Comment.articleid == articleid, ).order_by(Comment.commentid.desc()) \
            .limit(count).offset(start).all()
        return result

    # 新增一条回复，将原始评论的ID作为新评论的replyid字段来进行关联
    def insert_reply(self, articleid, commentid, content, ipaddr):
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        comment = Comment(userid=session.get('userid'), articleid=articleid
                          , content=content, ipaddr=ipaddr, replyid=commentid,
                          createtime=now, updatetime=now)
        db.session.add(comment)
        db.session.commit()

    # 查询原始评论与对应的用户信息，带分页参数
    def find_comment_with_user(self,articleid,start,count):
        result = db.session.query(Comment,Users).join(Users,Users.userid==Comment.userid)\
            .filter(Comment.articleid == articleid,Comment.replyid==0)\
            .order_by(Comment.commentid.desc()).limit(count).offset(start).all()
        return result

    # 查询回复评论，回复评论不需要分页
    def find_reply_with_user(self,replyid):
        result = db.session.query(Comment,Users).join(Users,Users.userid==Comment.userid)\
            .filter(Comment.replyid == replyid).all()
        return result

    # 根据原始评论和回复评论生成一个关联列表
    def get_comment_user_list(self,articleid,start,count):
        result = self.find_comment_with_user(articleid,start,count)
        comment_list = Model_to_list().model_join_list(result)  #原始评论的连接结果
        for comment in comment_list:
            #查询原始评论对应的回复评论,并转换为列表保存到comment_list中
            result = self.find_reply_with_user(comment['commentid'])
            # 为comment_list列表中的原始评论字典对象添加一个新的key叫reply_list
            # 用于存储当前这条原始评论的所有回复评论，如果无回复则列表值为空
            comment['reply_list'] =Model_to_list().model_join_list(result)
        return comment_list #将新的数据结构返回给控制器接口
