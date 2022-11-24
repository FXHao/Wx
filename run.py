from .wx_sql import Wx_Mysql
import re
from decimal import *

from flask import Flask
from flask import request
import hashlib

app = Flask(__name__)


class Wx_Reply(Wx_Mysql):

    def get_user_input(self, name, s):
        wx_mysql = Wx_Mysql()
        ret = re.match(r"([\u4E00-\u9FA5A-Za-z0-9_]+)\s*[+\-=]*\s*(\d*.?\d*)", s)
        if ret:
            price_info, price = ret.groups()
            if (price and price_info) != "":
                wx_mysql.add_cost(name, price, price_info)

    def accounting(self):
        """
        计算当月费用
        :return:
        """
        data_price, data_info, all_price = self.all_cost()
        all = all_price.get("sum(price)")
        account_payable = (all / int(len(data_price))).quantize(Decimal('0.00'))
        user_info = {}
        shou_user = []
        fu_user = []
        for i in data_price:
            user = i.get("name")
            price = i.get("sum(price)")
            difference = (price - account_payable)
            shou_user.append(user) if difference > 0 else fu_user.append(user)
            user_info["{}".format(user)] = [price, difference]


@app.route('/wechat')
def wechat():
    signature = request.args.get("signature", "")
    timestamp = request.args.get("timestamp", "")
    nonce = request.args.get("nonce", "")
    echostr = request.args.get("echostr", "")
    print(signature, timestamp, nonce, echostr)

    token = "fxhaoo"

    # 2、 进行字典排序
    data = [token, timestamp, nonce]
    data.sort()

    # 3、三个参数拼接成一个字符串并进行sha1加密
    temp = ''.join(data)
    sha1 = hashlib.sha1(temp.encode('utf-8'))
    hashcode = sha1.hexdigest()
    print(hashcode)

    # 4、对比获取到的signature与根据上面token生成的hashcode，如果一致，则返回echostr，对接成功
    if hashcode == signature:
        return echostr
    else:
        return "error"


if __name__ == '__main__':
    # record("测试2", "房租+3508")
    wx = Wx_Mysql()
