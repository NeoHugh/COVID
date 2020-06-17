# encoding:utf-8
import importlib
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from covid.config import Config
import sys
from flask_mail import Mail
import flask_excel as excel
#from flask_wtf import CSRFProtect


db = SQLAlchemy()
mail = Mail()
bootstrap = Bootstrap()
importlib.reload(sys)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    excel.init_excel(app)
#    CSRFProtect(app)

    from covid.transport_user import transport_user
    from covid.transport_admin import transport_admin
    from covid.population_admin import population_admin
    from covid.poppulation_user import population_user
    from covid.framework import login
    from covid.situation import situation_bp
    from covid.admin import admin
    from covid.user import user
    app.register_blueprint(transport_admin, url_prefix='/transport_admin')
    app.register_blueprint(transport_user, url_prefix='/transport_user')
    app.register_blueprint(population_admin, url_prefix='/population_admin')
    app.register_blueprint(population_user, url_prefix='/population_user')
    app.register_blueprint(situation_bp, url_prefix='/situation')
    app.register_blueprint(login, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/goods_admin')
    app.register_blueprint(user, url_prefix='/good_user')
    # from covid.transportation_models import Transport, USER
    # from covid.models import Users, Admin, Information, Comment, Popflow
    # db.drop_all()
    # db.create_all()
    # plane1 = Transport(number='TB127', type='1', start='杭州',
    #                    end='成都', time='2020-06-06')
    # plane2 = Transport(number='TB128', type='1', start='杭州',
    #                    end='成都', time='2020-06-06')
    # plane3 = Transport(number='TB129', type='1', start='杭州',
    #                    end='成都', time='2020-06-06')
    # plane4 = Transport(number='TB110', type='0', start='杭州',
    #                    end='成都', time='2020-06-08')
    # db.session.add_all([plane1, plane2, plane3, plane4])
    # db.session.commit()
    # user1 = USER(name='张三', email='2569535507@qq.com', address='浙江大学', phone_number='13711111111',
    #              identity_number='511133200001153022', transport_number='TB127')
    # user2 = USER(name='李四', email='15944065615@163.com', address='浙江大学', phone_number='13711111112',
    #              identity_number='511133200001153023', transport_number='TB127')
    # user3 = USER(name='王五', email='2983096055@qq.com', address='浙江大学', phone_number='13711111113',
    #              identity_number='511133200001153024', transport_number='TB128')
    # db.session.add_all([user1, user2, user3])
    # db.session.commit()
    # U1 = Users(name='test', pwd='123456', phone='1371111111', idcard='511133200001153018',
    #            email='111@qq.com', province='', address='浙江大学', username='Tom')
    # db.session.add(U1)
    # db.session.commit()
    # A1 = Admin(name='transport', pwd='123456', system=4, province='浙江')
    # A2 = Admin(name='population', pwd='123456', system=5, province='浙江')
    # A3 = Admin(name='superadmin', pwd='123456', system=3, province='浙江')
    # A4 = Admin(name='situation', pwd='123456', system=2, province='浙江')
    # A5 = Admin(name='supply', pwd='123456', system=6, province='浙江')
    # db.session.add_all([A1, A2, A3, A4, A5])
    # db.session.commit()
    # # 测试数据(重复部分测试数据库聚合运算功能)
    # rd1 = Popflow(people_province='河北', people_inflow=1, people_outflow=1)
    # rd2 = Popflow(people_province='上海', people_inflow=1, people_outflow=1)
    # rd3 = Popflow(people_province='浙江', people_inflow=1, people_outflow=1)
    # rd4 = Popflow(people_province='湖北', people_inflow=1, people_outflow=1)
    # rd5 = Popflow(people_province='广东', people_inflow=1, people_outflow=1)

    # # 测试数据(初始绘制地图)

    # rd6 = Popflow(people_province='北京',
    #               people_inflow=11111, people_outflow=100)
    # rd7 = Popflow(people_province='天津', people_inflow=222, people_outflow=100)
    # rd8 = Popflow(people_province='上海', people_inflow=333, people_outflow=100)
    # rd9 = Popflow(people_province='重庆', people_inflow=444, people_outflow=100)
    # rd10 = Popflow(people_province='河北', people_inflow=555, people_outflow=100)
    # rd11 = Popflow(people_province='河南', people_inflow=666, people_outflow=100)
    # rd12 = Popflow(people_province='云南', people_inflow=311, people_outflow=100)
    # rd13 = Popflow(people_province='辽宁', people_inflow=233, people_outflow=100)
    # rd14 = Popflow(people_province='黑龙江',
    #                people_inflow=888, people_outflow=100)
    # rd15 = Popflow(people_province='湖南', people_inflow=777, people_outflow=100)
    # rd16 = Popflow(people_province='安徽',
    #                people_inflow=1057, people_outflow=100)
    # rd17 = Popflow(people_province='山东', people_inflow=80, people_outflow=100)
    # rd18 = Popflow(people_province='新疆', people_inflow=999, people_outflow=100)
    # rd19 = Popflow(people_province='江苏', people_inflow=318, people_outflow=100)
    # rd20 = Popflow(people_province='浙江', people_inflow=581, people_outflow=100)
    # rd21 = Popflow(people_province='江西', people_inflow=180, people_outflow=100)
    # rd22 = Popflow(people_province='湖北', people_inflow=317, people_outflow=100)
    # rd23 = Popflow(people_province='广西', people_inflow=600, people_outflow=100)
    # rd24 = Popflow(people_province='甘肃', people_inflow=250, people_outflow=100)
    # rd25 = Popflow(people_province='山西', people_inflow=521, people_outflow=100)
    # rd26 = Popflow(people_province='内蒙古',
    #                people_inflow=1517, people_outflow=100)
    # rd27 = Popflow(people_province='陕西',
    #                people_inflow=1777, people_outflow=100)
    # rd28 = Popflow(people_province='吉林',
    #                people_inflow=2990, people_outflow=100)
    # rd29 = Popflow(people_province='福建', people_inflow=100, people_outflow=100)
    # rd30 = Popflow(people_province='贵州', people_inflow=51, people_outflow=100)
    # rd31 = Popflow(people_province='广东', people_inflow=0, people_outflow=100)
    # rd32 = Popflow(people_province='青海', people_inflow=89, people_outflow=100)
    # rd33 = Popflow(people_province='西藏', people_inflow=976, people_outflow=100)
    # rd34 = Popflow(people_province='四川', people_inflow=546, people_outflow=100)
    # rd35 = Popflow(people_province='宁夏', people_inflow=338, people_outflow=100)
    # rd36 = Popflow(people_province='海南', people_inflow=220, people_outflow=100)
    # rd37 = Popflow(people_province='台湾', people_inflow=667, people_outflow=100)
    # rd38 = Popflow(people_province='香港', people_inflow=990, people_outflow=100)
    # rd39 = Popflow(people_province='澳门', people_inflow=88, people_outflow=100)

    # db.session.add_all(
    #     [rd1, rd2, rd3, rd4, rd5, rd6, rd7, rd8, rd9, rd10, rd11, rd12, rd13, rd14, rd15, rd16, rd17, rd18, rd19, rd20,
    #      rd21, rd22, rd23, rd24, rd25, rd26, rd27, rd28, rd29, rd30, rd31, rd32, rd33, rd34, rd35, rd36, rd37, rd38, rd39, ]
    # )
    # db.session.commit()

    # info1 = Information(info_type=0, info_province='浙江',
    #                     info_title='测试数据1', info_text='0 浙江')
    # info2 = Information(info_type=0, info_province='北京',
    #                     info_title='测试数据2', info_text='0 北京')
    # info3 = Information(info_type=2, info_province='浙江',
    #                     info_title='测试数据3', info_text='2 浙江')
    # info4 = Information(info_type=1, info_province='浙江',
    #                     info_title='测试数据4', info_text='1 浙江')
    # info5 = Information(info_type=3, info_province='江苏',
    #                     info_title='测试数据5', info_text='3 江苏')

    # db.session.add_all([info1, info2, info3, info4, info5])
    # db.session.commit()
    situation.initSituation()
    return app

