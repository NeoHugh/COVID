from flask import Flask, render_template, url_for,redirect, Blueprint, request, flash,session
from covid import db
import time
from covid.models import WareHouse
from covid.models import GoodsInfo
from covid.models import OrderInfo
from covid.models import Complaint
from covid.models import Users
import flask_excel as excel
from sqlalchemy import func

admin = Blueprint('goods_admin', __name__)

@admin.before_request
def before_admin():
    if 'identity' in session and session['identity']==6: #如果身份是管理员就通过
        pass
    else:#否则返回用户界面
        flash('小火汁，你的思想很危险！','danger')
        return redirect(url_for('goods_user.supply'))

@admin.route("/")
def adminfirst():
    return render_template('admin_open.html')


@admin.route("/admin_open", methods=('GET', 'POST'))
def admin_open():
    goods = WareHouse.query.filter(WareHouse.number > 0);
    if request.method=='POST':
        Sum = request.form['sum']
        number = request.form['number']
        goodsname = request.form['goodsname']
        deadline = request.form['deadline']
        g = GoodsInfo.query.filter(GoodsInfo.Goodsname==goodsname).first()
        o = WareHouse.query.filter(WareHouse.Goodsname==goodsname).first()
        if int(Sum) > o.number:
            flash("数量大于库存量，请重新输入!",'warning')
            return render_template('admin_open.html', goods=goods)
        if int(Sum) < int(number):
            flash("个人申领数量大于可申领总数，请重新输入！",'warning')
            return render_template('admin_open.html', goods=goods)
        if g:
            flash("该物资已经发布，添加数量成功！",'success')
            g.OrderLimit += int(Sum)
            o.number -= int(Sum)
            if o.number == 0: # when the number is zero.
                db.session.delete(o)
            db.session.commit()
            return render_template('admin_open.html', goods=goods)
        newObj = GoodsInfo(Goodsname=goodsname, OrderLimit=Sum, OrderLimitPerPerson = number, DDL=deadline)
        db.session.add(newObj)
        o.number -= int(Sum)
        db.session.commit()
        return render_template('admin_open.html', goods=goods)
    return render_template('admin_open.html', goods=goods)

@admin.route("/view_win")
def view_win():
    goods = GoodsInfo.query.all();
    return render_template('view_win.html', goods=goods)

@admin.route("/deleteWare/<goodsname>", methods=('POST', 'GET'))
def delete(goodsname):
    g = GoodsInfo.query.filter(GoodsInfo.Goodsname==goodsname).first()
    if g:
        flash("该物资已经发布，无法删除！",'warning')
        return redirect(url_for('goods_admin.admin_open'))
    d = WareHouse.query.filter(WareHouse.Goodsname==goodsname).first()
    db.session.delete(d)
    db.session.commit()
    flash("删除成功",'success')
    return redirect(url_for('goods_admin.admin_open'))


@admin.route("/deleteGoodsInfo/<goodsname>", methods=('POST', 'GET'))
def deleteGoodsInfo(goodsname):
    u = OrderInfo.query.filter(OrderInfo.Goodsname==goodsname).first()
    if u:
        flash("已经有用户申请，不可撤销！",'warning')
        return redirect(url_for('goods_admin.view_win'))
        
    g = GoodsInfo.query.filter(GoodsInfo.Goodsname==goodsname).first()
    p = WareHouse.query.filter(WareHouse.Goodsname==goodsname).first()
    p.number += g.OrderLimit
    db.session.delete(g)
    db.session.commit()
    flash("删除成功",'success')
    return redirect(url_for('goods_admin.view_win'))


@admin.route("/complain_deal") # 投诉处理
def complain_deal():
    complaints = Complaint.query.filter(Complaint.ComplaintState==0)
    return render_template('complain_deal.html', complaints=complaints)

@admin.route("/putin", methods=('GET', 'POST'))
def putin():
    if request.method == 'POST':
        name = request.form['goodsname']
        number = request.form['number']
        usage = request.form['usage']
        
        q_id = WareHouse.query.filter(WareHouse.Goodsname==name).first()
        if not q_id:
            newObj = WareHouse(Goodsname=name, number=number, usage=usage)
            db.session.add(newObj)
            db.session.commit()
            flash('提交成功','success')
        else:
            q_id.number += number
            db.session.commit()
            flash('该物资存在，已经更新数量','warning')
    return render_template('putin.html')

@admin.route("/sent_deal") # 订单提交成功界面
def sent_deal():
    orders = OrderInfo.query.filter(OrderInfo.OrderState==1)
    return render_template('sent_deal.html', orders=orders)

@admin.route("/sending") # 订单运输中界面
def sending():
    orders = OrderInfo.query.filter(OrderInfo.OrderState==2)
    return render_template('sending.html', orders=orders)

@admin.route("/completed") # 订单完成界面 
def completed():
    orders = OrderInfo.query.filter(OrderInfo.OrderState==3)
    return render_template('completed.html', orders=orders)

@admin.route("/send/<orderid>") # 进行发货操作
def send(orderid):
    order = OrderInfo.query.filter(OrderInfo.id==orderid).first()
    order.OrderState = 2
    order.DeliveryTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    db.session.commit()
    return redirect(url_for('goods_admin.sent_deal'))

@admin.route("/processComplaint/<complaintid>") #  处理投诉
def processComplaint(complaintid):
    complaint = Complaint.query.filter(Complaint.id==complaintid).first()
    complaint.ComplaintState = 1
    db.session.commit()
    return redirect(url_for('goods_admin.complain_deal')) 

@admin.route("/download/<goodsid>")
def download(goodsid):
    good = GoodsInfo.query.filter(GoodsInfo.id==goodsid).first() # 相对应的物资
# 检查是否到达抽签时间
    curdate = time.strftime("%Y-%m-%d", time.localtime())
    ddl = GoodsInfo.query.filter(GoodsInfo.id==goodsid).first()
    if curdate < str(ddl.DDL):
        flash("抽签时候未到！",'warning')
        return redirect(url_for('goods_admin.view_win'))

# 开始进行抽签工作
    # 计算申领人数
    count = db.session.query(func.count(OrderInfo.id)).filter(OrderInfo.GoodsID==goodsid).scalar()
    # 进行Excel准备
    q = db.session.query(
        OrderInfo.userid.label('用户编号'),
        OrderInfo.id.label('订单编号'),
        Users.name.label('姓名'),
        Users.email.label('邮箱'),
        Users.address.label('地址')
    )
    if count == 0: # 目前无人申领
        flash("目前还没有人申领！",'warning')
        return redirect(url_for('goods_admin.view_win'))
    elif count <= good.OrderLimit: # 如果人数小于限制人数 则全部抽取
        OrderInfo.query.filter(OrderInfo.GoodsID==goodsid, OrderInfo.OrderState==0).update({"OrderState": 1})
        db.session.commit()
        query_sets = q.filter(OrderInfo.OrderState==1).filter(Users.idcard==OrderInfo.userid)\
        .filter(OrderInfo.GoodsID==goodsid).all()
    else: # 如果人数大于限制 则进行抽签
        OrderInfo.query.filter(OrderInfo.GoodsID==goodsid, OrderInfo.OrderState==0).limit(good.OrderLimit).update({"OrderState": 1})
        query_sets = q.filter(OrderInfo.OrderState==1).filter(Users.idcard==OrderInfo.userid)\
        .filter(OrderInfo.GoodsID==goodsid).order_by(func.random()).limit(good.OrderLimit).all()

    return excel.make_response_from_query_sets(
        query_sets,
        column_names=[
            '用户编号',
            '订单编号',
            '姓名',
            '邮箱',
            '地址'
        ],
        file_type='xlsx',
        file_name='中签信息.xlsx'
    )
