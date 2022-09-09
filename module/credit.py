"""
@author:maohui
@time:2022/9/6 13:29
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
from sqlalchemy import Table,MetaData
from app import db



class Credit(db.Model):
    __table__= Table('credit',MetaData(db.engine),autoload=True)

    # 插入积分明细数据
    def insert_detail(self,category,target,credit):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        credit = Credit(userid=session.get('userid'),category=category,target=target,
                        credit=credit,createtime=now,updatetime=now)
        db.session.add(credit)
        db.session.commit()

    # 判断用户是否已经消耗积分
    def check_payed_article(self,articleid):
        result = db.session.query(Credit).filter_by(userid=session.get('userid'),target=articleid).all()
        if len(result) >0 :
            return True
        else:
            return False