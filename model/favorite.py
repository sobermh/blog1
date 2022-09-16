"""
@author:maohui
@time:2022/9/7 17:05
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

from app import db
from sqlalchemy import Table, MetaData
from flask import session

class Favorite(db.Model):
    __table__ = Table('favorite', MetaData(db.engine), autoload=True)

    # 插入文章收藏数据，或取消收藏的再次收藏
    def insert_favorite(self,articleid):
        row = db.session.query(Favorite).filter_by(articleid=articleid,userid=session.get('userid')).first()
        if row is not None:
            row.canceled = 0
        else:
            now = time.strftime('%Y-%m-%d %H:%M:%S')
            favorite = Favorite(articleid=articleid,userid=session.get('userid'),canceled=0,createtime=now,updatetime=now)
            db.session.add(favorite)
        db.session.commit()
        db.session.close()

    # 取消收藏
    def cancel_favorite(self,articleid):
        row = db.session.query(Favorite).filter_by(articleid=articleid,userid=session.get('userid')).first()
        row.canceled=1
        db.session.commit()
        db.session.close()

    #判断是否已经被收藏
    def check_favorite(self,articleid):
        row = db.session.query(Favorite).filter_by(articleid=articleid,userid=session.get('userid')).first()
        if row is None:
            return False
        elif row.canceled == 1:
            return False
        else:
            return True
