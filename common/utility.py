"""
@author:maohui
@time:2022/9/6 9:31
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
import random
import string
from io import BytesIO

from PIL import Image, ImageFont, ImageDraw


# 绘制图片验证码
class ImageCode:
    # 生成用于绘制字符串的随机颜色0,255,颜色亮的数值大，颜色暗的数值小
    def rand_color(self):
        red = random.randint(32, 200)
        green = random.randint(22, 255)
        blue = random.randint(0, 200)
        return red, green, blue

    # 生成4位随机验证码，大小写字母和数字
    def gen_text(self):
        # sample用于从一个大的列表或者字符串中，随机取得N个字符，来构建出一个子列表
        letters = string.ascii_letters + string.digits
        list = random.sample(letters, 4)
        captcha = "".join(list)
        return captcha

    # 画一些干扰线，其中draw为PIL中的ImageDraw对象
    def draw_lines(self, draw, num, width, height):
        for num in range(num):
            x1 = random.randint(0, width / 2)
            y1 = random.randint(0, height / 2)
            x2 = random.randint(0, width)
            y2 = random.randint(height / 2, height)
            draw.line(((x1, y1), (x2, y2)), fill='black', width=1)

    # 绘制验证码图片
    def draw_captcha(self):
        code = self.gen_text()
        width, height = 120, 50  # 设定图片大小，可根据实际需求调整
        # 创建图片对象，并设定背景为白色
        im = Image.new('RGB', (width, height), 'white')
        # 选择使用何种字体和字体大小
        font = ImageFont.truetype(font='arial.ttf', size=40)
        # 新建imagedraw对象
        draw = ImageDraw.Draw(im)
        # 绘制字符串
        for i in range(4):
            draw.text((5 + random.randint(-3, 3) + 23 * i, 5 + random.randint(-3, 3)),
                      text=code[i], fill=self.rand_color(), font=font)
        # 绘制干扰线
        self.draw_lines(draw, 4, width, height)
        # 如需临时调试，可以直接将生成的图片显示出来
        # im.show()
        return im, code

    # 生成图片验证码并返回给控制器
    def get_code(self):
        image, code = self.draw_captcha()
        buffer = BytesIO()
        image.save(buffer, 'jpeg')
        bsrting = buffer.getvalue()  # 返回二进制内容
        return code, bsrting


from smtplib import SMTP_SSL  # 加密及发送邮件内容
from email.mime.text import MIMEText  # 构造邮件的正文
from email.header import Header


# 发送邮件验证码
class EmailCode:
    # 发送企业微信邮箱验证码

    # 发送企业微信邮箱验证码，参数为“收件邮箱”和随机生成的“验证码”
    def send_email(self, recevier, ecode):
        # 发件人邮箱
        sender = 'maohui@well-healthcare.com'
        # 定义发送的邮件内容，支持html标签和css样式
        content = f"<br/>Welcome to sign up for my Blog？您的“林北星”正在等你!!!" \
                  f"<br/>您的邮箱验证码为：<span style='color:red;font-size=20px;'>{ecode}</span>,请复制到注册窗口注册"
        # 实例化邮件对象，并指定邮件的关键信息
        message = MIMEText(content, 'html', 'utf-8')
        # 指定邮件的标题，同样使用utf-8编码
        message['Subject'] = Header('西湖张万森给你发的验证码', 'utf-8')
        message['From'] = sender  # 指定发件人
        message['To'] = recevier  # 指定收件人

        # 与企业邮箱服务器进行连接
        stmpObj = SMTP_SSL('smtp.exmail.qq.com')
        # 通过邮箱账号和获取到的授权码进行登录
        stmpObj.login(user="maohui@well-healthcare.com", password="Txxc3yrVSSxkHFNS")
        # 指定发件人，收件人和邮件内容
        stmpObj.sendmail(sender, recevier, str(message))
        stmpObj.quit()

    # 生成4位随机字符验证码作为邮箱验证码
    def gen_email_code(self):
        str = random.sample(string.ascii_letters + string.digits, 4)
        return "".join(str)


# 模型类转化为python的list
class Model_to_list():
    # 单个模型类转换为标准的python list数据
    def model_list(self, result):
        list = []
        for row in result:
            dict = {}
            for k, v in row.__dict__.items():
                if not k.startswith('_sa_instance_state'):
                    dict[k] = v
            list.append(dict)
        return list

    # SQLALchemy连接查询两张表的结果集转换为[{},{}]
    # Comment,Users[(Comment,User),(Comment,User),(Comment,User)]
    def model_join_list(self, result):
        list = []  # 定义列表用于存放所有行
        for obj1, obj2 in result:
            dict = {}
            for k1, v1 in obj1.__dict__.items():
                if not k1.startswith('_sa_instance_state'):
                    if not k1 in dict:  # 如果字典中已经存在相同的key则跳过
                        dict[k1] = v1
            for k2, v2 in obj2.__dict__.items():
                if not k2.startswith('_sa_instance_state'):
                    if not k2 in dict:  # 如果字典中已经存在相同的key则跳过
                        dict[k2] = v2
            list.append(dict)
        return list

# if __name__ == '__main__':
# #     ImageCode().draw_captcha()
#     code= gen_email_code()
#     print(code)
#     send_email('409788696@qq.com',code)
