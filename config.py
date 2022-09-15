"""
@author:maohui
@time:2022/8/31 13:45
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

#数据库的配置信息
HOSTNAME = '47.97.118.247'
PORT = '3306'
DATABASE = 'blog'   #数据库名称
USERNAME = 'root'
PASSWORD = '123456'



DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'\
    .format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)

SQLALCHEMY_DATABASE_URI = DB_URI      #sqlalchemy专用
SQLALCHEMY_TRACK_MODIFICATIONS = False  #跟踪数据库的修改，及时发送信号

# #缓解问题：QueuePool limit of size 10 overflow 10 reached, connection timed out, timeout 30.00
# pool_size = 100
# max_overflow = 20

SECRET_KEY = "maohuidsd"

JSON_AS_ASCII = False  # 默认是true，中文会返回unicode，false会返回中文
