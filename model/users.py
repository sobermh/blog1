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
import random

from flask import session

from sqlalchemy import Table, MetaData
from app import db

class Users(db.Model):

    __table__= Table('users',MetaData(db.engine),autoload=True)

    # 查询用户名（邮箱），可用于注册时判断用户名(邮箱)是否已注册，也可用于登录校验
    def find_user_by_username(self,username):
        result = db.session.query(Users).filter_by(username=username).all()
        return result

    # 实现注册，首次注册时用户只需要输入用户名和密码，所以只需要两个参数
    # 注册时，在模型类中为其他字段尽力生成一些可用的值，虽不全面，但可用
    # 通常用户注册时不建议填写太多资料，影响体验，课待用户后续逐步完善
    def do_register(self,username,password):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        nickname = username.split('@')[0]  #默认将邮箱账号前缀作为昵称
        headportrait = str(random.randint(3,4)) #从1张图片中随机选择一张
        user = Users(username=username,password=password,role='user',credit=50,
                     nickname=nickname,headportrait=headportrait+'.jpg',createtime=now)
        db.session.add(user)
        db.session.commit()
        db.session.close()
        return user

    #修改用户剩余积分，积分为正数表示增加积分，为负数表示减少积分
    def update_credit(self,credit):
        user = db.session.query(Users).filter_by(userid=session.get('userid')).one()
        user.credit = int(user.credit)+credit
        db.session.commit()
        db.session.close()

# if __name__ == "__main__":
#     Users().do_register('4097886964@qq.com','123456')