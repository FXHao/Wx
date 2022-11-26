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
    if len(ret) > 3:
        for i in range(len(ret)):
            ret[i] = ret[i].strip()
        if ret[1] == '':
            return "昵称不可为空"
        if ret[2] == '':
            return "城市不可为空"
        if ret[3] == '':
            return "分组不可为空"
        if ret[0] == '注册':
            res = insert_user(name=ret[1], city=ret[2], gruop=ret[3], openid=openid)
            return res
        if ret[0] == '更新':
            res = update_user(name=ret[1], city=ret[2], gruop=ret[3], openid=openid)
            return res
        return content
    return content


# if __name__ == '__main__':
#     msg = "更新+fxhaoo+广州+123"
#     print(reg_msg(msg, '111'))
