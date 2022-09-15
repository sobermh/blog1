"""
@author:maohui
@time:2022/9/14 11:56
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
import redis
from app import db

from common.utility import Model_to_list

from model.users import Users




class RedisDB():
    # 连接redis服务器
    def redis_connect(self):
        # 指定Redis服务器的IP地址，端口号和数据库进行连接
        # red= redis.Redis(host='127.0.0.1',port= 6379,decode_response=True,db=0)
        # 使用连接池进行连接，推荐使用此方式
        pool = redis.ConnectionPool(host='127.0.0.1', port=6379, decode_responses=True, db=0)
        red = redis.Redis(connection_pool=pool)
        return red

    # 以用户名作为key存入redis
    def redis_mysql_hash(self):
        red = self.redis_connect()  #连接到Redis服务器
        #获取数据库连接信息
        result = db.session.query(Users).all()
        user_list =Model_to_list().model_list(result)
        for user in user_list:
            red.hset('user_hash',user['username'],user['password'])

if __name__ == '__main__':
    RedisDB().redis_mysql_hash()