import re
from decimal import *

from pymysql import *
from pymysql.cursors import DictCursor

from .config import *


class Wx_Mysql(object):
    """
    create database wx_data;
    create table user_consumption(
        id int auto_increment primary key ,
        name varchar(30),
        price decimal(6,2) not null,
        price_info varchar(30),
        datetime datetime
    );
    """

    def __init__(self):
        self.conn = connect(**MYSQL_CONFIG)
        self.cursor = self.conn.cursor(DictCursor)

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def add_cost(self, name, price, price_info):
        try:
            sql = "insert into user_consumption(name, price, price_info, datetime) value(%s, %s, %s, now());"
            self.cursor.execute(sql, [name, price, price_info])
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()

    def run_sql(self, sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()

    def all_cost(self):
        """
        查询每个用户的消费总额
        :return:
        """
        sql1 = "select name,sum(price) from user_consumption group by name;"
        self.cursor.execute(sql1)
        data1 = self.cursor.fetchall()
        self.cursor.nextset()
        sql2 = "select name,price,price_info,datetime from user_consumption;"
        self.cursor.execute(sql2)
        data2 = self.cursor.fetchall()
        return data1, data2

    def this_month_cost(self):
        """
        查询用户当月的消费
        :return: data1->消费总额  data2 -> 消费详情
        """
        sql = "select name,sum(price) from user_consumption where date_format(datetime,'%Y%m') = date_format(curdate(), '%Y%m') group by name;"
        self.cursor.execute(sql)
        data1 = self.cursor.fetchall()

        self.cursor.nextset()
        sql2 = "select name,price,price_info,datetime from user_consumption where date_format(datetime,'%Y%m') = date_format(curdate(), '%Y%m')"
        self.cursor.execute(sql2)
        data2 = self.cursor.fetchall()
        return data1, data2

    def last_month_cost(self):
        """
        查询上个月的消费
        :return:
        """
        sql = "select name,sum(price) from user_consumption where period_diff(date_format(now(),'%Y%m'), date_format(datetime,'%Y%m')) = 1 group by name;"
        self.cursor.execute(sql)
        data1 = self.cursor.fetchall()

        self.cursor.nextset()
        sql2 = "select name,price,price_info,datetime from user_consumption where period_diff(date_format(now(),'%Y%m'), date_format(datetime,'%Y%m')) = 1;"
        self.cursor.execute(sql2)
        data2 = self.cursor.fetchall()
        return data1, data2


