"""
@author:maohui
@time:2022/9/13 17:32
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

#指定Redis服务器的IP地址，端口号和数据库进行连接
# red= redis.Redis(host='127.0.0.1',port= 6379,decode_response=True,db=0)

#使用连接池进行连接，推荐使用此方式
pool = redis.ConnectionPool(host='127.0.0.1',port=6379,decode_responses=True,db=0)
red =redis.Redis(connection_pool=pool)

# print(red.get('phone'))

# red.hsetnx(name='mykey',mapping={'addr':'杭州','tel':'3123131'})
# red.hset(name='article',key='name',value='maohui')  #新增一条哈希值到mykey中
# red.hsetnx(name='mykey',key='name',value='maohui2') #在mykey中不存在name时新增
# dict = red.hgetall('mykey')  #获取mykey的所有值
