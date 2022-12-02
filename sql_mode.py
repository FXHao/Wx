from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DECIMAL, DATETIME, Boolean
from sqlalchemy import exists, create_engine, func

# 云托管
# config = "mysql+pymysql://fxhaoo:HAOhao123@10.2.100.220:3306/wx_data"
# 云服务器
# config = "mysql+pymysql://fxhaoo:HAOhao123@42.192.46.164:3306/wx_data"
# 测试
config = "mysql+pymysql://root:HAOhao123@localhost:3306/wx_data"

engine = create_engine(config)
Base = declarative_base(engine)
session = sessionmaker(engine)()


class User(Base):
    __tablename__ = 'user'
    __table_args__ = {
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_general_ci'
    }
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    city = Column(String(50))
    group = Column(String(50), nullable=False)
    openid = Column(String(50), nullable=False, unique=True)


class User_cost(Base):
    __tablename__ = 'user_cost'
    __table_args__ = {
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_general_ci'
    }
    id = Column(Integer, primary_key=True, autoincrement=True)
    openid = Column(String(50), nullable=False)
    group = Column(String(50), nullable=False)
    price = Column(DECIMAL(6, 2), nullable=False)
    price_info = Column(String(50))
    time = Column(DATETIME)
    is_delete = Column(Boolean, default=False)  # True-记录 False-删除


def init_db():
    """创建数据库"""
    Base.metadata.create_all(engine)


def drop_db():
    Base.metadata.drop_all(engine)


def insert_user(name, city, gruop, openid):
    """
    注册用户
    :param openid:
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
    except Exception as e:
        print(e)


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
    except Exception as e:
        print(e)


def insert_cost(openid, group, price, price_info):
    cost_info = User_cost(openid=openid, group=group, price=price, price_info=price_info, time=func.now())
    try:
        session.add(cost_info)
        session.commit()
        print("记录成功")
    except Exception as e:
        print("更新失败, errormsg:{}".format(e))
        session.rollback()


def this_month_cost(openid):
    # 获取分组
    user_group = session.query(User.group).filter(User.openid == openid).scalar()
    if user_group is None:
        return "尚未注册，请用【注册+昵称+城市+群组】进行注册~"
    # 根据分组查询用户
    openid_list = session.query(User.openid, User.name).filter(User.group == user_group).all()
    # # 根据分组查询当月消费
    cost_all = session.query(func.sum(User_cost.price)).filter(User_cost.group == user_group,
                                                               User_cost.is_delete == 0).scalar()
    cost_all = 0 if cost_all is None else cost_all
    msg = "当月总消费为：{}".format(cost_all)
    # # 根据openid查询每个用户消费及详情
    for oid in openid_list:
        n = oid[1]
        cost_data = session.query(func.sum(User_cost.price)).filter(User_cost.openid == oid[0],
                                                                    User_cost.is_delete == 0).scalar()
        cost_data = 0 if cost_data is None else cost_data
        msg = msg + "\n\n" + "{}本月共消费：{}，消费详情如下".format(n, cost_data)
        if cost_data == 0:
            continue
        cost_info = session.query(User_cost).filter(User_cost.openid == oid[0]).all()
        for info in cost_info:
            p = info.price
            p_i = info.price_info
            u_msg = "{}：{}".format(p_i, p)
            msg = msg + '\n' + u_msg
    print(msg)
    # return msg


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


# if __name__ == '__main__':
#     #     select_user(1112)
#     drop_db()
#     init_db()
#     print(insert_user('fxhao1', '广州', 'M78', '1'))
#     # print(insert_user('fxhao2', '广州', 'M78', '2'))
#     # print(insert_user('fxhao3', '广州', 'M78', '3'))
#     #     # print(select_gruop('M78星云'))
#     #     # select_gruop('M78星云')
#     #     # print(update_user('fxhao3', '广州', 'M78', '3'))
#     # print(insert_cost('1', 'M78', 19.2, '牙膏'))
#     #     # print(insert_cost('2', 'M78', 19.2, '粮食'))
#     #     # print(insert_cost('3', 'M78', 20, '饮料'))
#     this_month_cost('1')
