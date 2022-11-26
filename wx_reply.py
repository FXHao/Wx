# from wx_sql import *
import re
# from decimal import *


# class Wx_Reply(Wx_Mysql):
#
#     def get_user_input(self, name, msg):
#         wx_mysql = Wx_Mysql()
#         ret = re.match(r"([\u4E00-\u9FA5A-Za-z0-9_]+)\s*[+\-=]*\s*(\d*.?\d*)", msg)
#         if ret:
#             price_info, price = ret.groups()
#             if (price and price_info) != "":
#                 wx_mysql.add_cost(name, price, price_info)
#
#     def accounting(self):
#         """
#         计算当月费用
#         :return:
#         """
#         data_price, data_info, all_price = self.all_cost()
#         all = all_price.get("sum(price)")
#         account_payable = (all / int(len(data_price))).quantize(Decimal('0.00'))
#         user_info = {}
#         shou_user = []
#         fu_user = []
#         for i in data_price:
#             user = i.get("name")
#             price = i.get("sum(price)")
#             difference = (price - account_payable)
#             shou_user.append(user) if difference > 0 else fu_user.append(user)
#             user_info["{}".format(user)] = [price, difference]


from sql_mode import *


def reg_msg(content, openid):
    # 注册 昵称 城市 群组
    ret = re.split('[+=.]', content)
    for i in range(len(ret)):
        if ret[i] == "":
            ret[i] = None
        ret[i] = ret[i].strip()
    tag = ret[0]
    name = ret[1]
    city = ret[2]
    gruop = ret[3]
    if name == '':
        return "昵称不可为空"
    if city == '':
        return "城市不可为空"
    if gruop == '':
        return "分组不可为空"
    if tag == '注册':
        res = insert_user(name=name, city=city, gruop=gruop, openid=openid)
        return res
    if tag == '更新':
        res = update_user(name, city=city, gruop=gruop, openid=openid)
        return res
    return content


# if __name__ == '__main__':
#     msg = " 1  + fxhao+广州+M78星云"
