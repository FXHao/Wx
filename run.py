from .wx_sql import Wx_Mysql
import re
from decimal import *


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


if __name__ == '__main__':
    # record("测试2", "房租+3508")
    wx = Wx_Mysql()
