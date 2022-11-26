import datetime
import logging

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DECIMAL, DATETIME, Boolean
from sqlalchemy import exists, create_engine, func

config = "mysql+pymysql://root:HAOhao123@localhost:3306/wx_data"
engine = create_engine(config)
Base = declarative_base(engine)
session = sessionmaker(engine)()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    city = Column(String(50))
    group = Column(String(50), nullable=False)
    openid = Column(String(50), nullable=False, unique=True)


class User_cost(Base):
    __tablename__ = 'user_cost'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    price = Column(DECIMAL(6, 2), nullable=False)
    price_info = Column(String(50))
    time = Column(DATETIME)
    is_delete = Column(Boolean, default=True)  # True-记录 False-删除


def init_db():
    """创建数据库"""
    Base.metadata.create_all(engine)


def drop_db():
    Base.metadata.drop_all(engine)


def insert_user(name, city, gruop, openid):
    """
    注册用户
    :param name:昵称
    :param city:城市
    :param gruop:分组
    :return:
    """
    user = User(name=name, city=city, group=gruop, openid=openid)
    # 判断数据是否存在
    try:
        it_exists = session.query(
            exists().where(User.openid == openid)
        ).scalar()
    except Exception as e:
        print(e)
    try:
        if not it_exists:
            # 不存在，进行新增
            session.add(user)
            session.commit()
            return "注册成功"
        else:
            return "用户已存在，若需要请用【更新+昵称+城市+群组】更新"
    except Exception as e:
        print(e)
        session.rollback()


def update_user(name, city, gruop, openid):
    """
    更新用户数据
    :param name:
    :param city:
    :param gruop:
    :param openid:
    :return:
    """
    try:
        it_exists = session.query(
            exists().where(User.openid == openid)
        ).scalar()
    except Exception as e:
        print(e)

    try:
        if not it_exists:
            # 不存在
            return "用户不存在，请用【注册+昵称+城市+群组】注册"
        else:
            # 存在，进行更新
            session.query(User).filter(User.openid == openid).update(dict(name=name, city=city, group=gruop))
            session.commit()
            name_list = select_gruop(gruop)
            msg = """更新成功\n当前分组的用户有:\n{}
            """.format(name_list)
            return msg
    except Exception as e:
        session.rollback()
        return "更新失败, errormsg:{}".format(e)


def insert_cost(name, price, price_info):
    cost_info = User_cost(name=name, price=price, price_info=price_info, time=func.now())
    try:
        session.add(cost_info)
        session.commit()
        print("记录成功")
    except Exception as e:
        print("更新失败, errormsg:{}".format(e))
        session.rollback()


def this_month_cost():
    pass


def select_user(openid):
    """
    查询用户
    :param openid:
    :return:
    """
    user = session.query(User).filter(User.openid == openid).first()
    if user is None:
        return None
    return user.openid, user.name, user.group, user.openid


def select_gruop(group):
    data = session.query(User).filter(User.group == group).all()
    if data is None:
        return None
    user_list = []
    for user in data:
        user_list.append(user.name)
    return user_list


if __name__ == '__main__':
    select_user(1112)
    # init_db()
    # print(insert_user('fxhao3', '广州', 'M78', '3'))
    # print(select_gruop('M78星云'))
    # select_gruop('M78星云')
    # print(update_user('fxhao', '广州', 'M78星云', '3'))
