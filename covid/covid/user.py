from flask import render_template, url_for,redirect, Blueprint, request, flash,session
from covid import models,db
from datetime import datetime

user = Blueprint('goods_user', __name__)

@user.before_request
def before_user():
    if 'identity' in session and session['identity']==6:
        return redirect(url_for('goods_admin.admin_open'))
    else:
        pass

@user.route("/",methods=('GET', 'POST'))
def supply():
    if 'identity' in session and session['identity']=='user':
        NAME = session['name']
        IDCARD = models.Users.query.filter_by(name=NAME).first().idcard
        G = models.GoodsInfo.query.filter(models.GoodsInfo.DDL >= datetime.utcnow()).all()
        G_amount = models.GoodsInfo.query.filter(models.GoodsInfo.DDL >= datetime.utcnow()).count()
        if request.method == 'POST':
            goodsid = request.form['goods_id']
            name = request.form['name']
            idcards = request.form['id']
            address = request.form['address']
            sums = request.form['sum']
            orders = models.GoodsInfo.query.filter_by(id=goodsid).first()
            if orders.OrderLimitPerPerson < int(sums):
                flash("申领数量超过每人限制！",'warning')
                return render_template('supply.html', amount=G_amount, goods=G)
            if int(sums) > orders.OrderLimit:
                flash("剩余数量不足！",'warning')
                return render_template('supply.html', amount=G_amount, goods=G)
            if models.OrderInfo.query.filter_by(userid=IDCARD, GoodsID=goodsid, OrderState=0).first():
                flash("您已申领过该物资，不可重复申领",'warning')
                return render_template('supply.html', amount=G_amount, goods=G)
            if not models.Users.query.filter_by(name=NAME, idcard=IDCARD).first():
                flash("身份证号错误",'warning')
                return render_template('supply.html', amount=G_amount, goods=G)
            if not models.Users.query.filter_by(idcard=IDCARD, name=NAME).first():
                flash("姓名错误",'warning')
                return render_template('supply.html', amount=G_amount, goods=G)
            if len(address) > 30:
                flash("过长的地址输入！",'warning')
                return render_template('supply.html', amount=G_amount, goods=G)
            if int(sums) <= 0:
                flash("申领数量应该为正整数",'warning')
                return render_template('supply.html', amount=G_amount, goods=G)
            newobj = models.OrderInfo(userid=IDCARD, GoodsID=goodsid, Goodsname=orders.Goodsname, idcards=IDCARD, username=NAME,
                                    address=address, OrderNum=sums, CreateTime=datetime.utcnow(), OrderState=0)
            db.session.add(newobj)
            db.session.commit()
            return render_template('supply.html', amount=G_amount, goods=G)
        return render_template('supply.html', amount=G_amount, goods=G)
    else:
        flash("请先登录",'warning')
    return redirect(url_for('login.a'))
    
    

@user.route("/received", methods=('GET', 'POST'))
def received():
    if 'identity' in session and session['identity']=='user':
        NAME = session['name']
        IDCARD = models.Users.query.filter_by(name=NAME).first().idcard
        user_orders = models.OrderInfo.query.filter_by(userid=IDCARD, OrderState=3).all()
        user_orders_sum = models.OrderInfo.query.filter_by(userid=IDCARD, OrderState=3).count()
        if request.method == 'POST':
            order_id = request.form['order_id']
            order_name = request.form['order_name']
            reason = 0
            if request.form.get('reason1'):
                reason = reason + 1
            if request.form.get('reason2'):
                reason = reason + 1
            if request.form.get('reason3'):
                reason = reason + 1
            if request.form.get('reason4'):
                reason = reason + 1
            if reason==0:
                flash("请至少选择一个投诉内容")
                return render_template('received.html', amount=user_orders_sum, orders=user_orders)
            text = request.form['text']
            if len(text)==0:
                flash("请描述出现的问题，以便我们为您解决")
                return render_template('received.html', amount=user_orders_sum, orders=user_orders)
            if len(text)>20000:
                flash("过长的问题描述，请简要描述")
                return render_template('received.html', amount=user_orders_sum, orders=user_orders)
            newobj = models.Complaint(Orderid=order_id, Goodsname=order_name, Content=text, ComplaintReason=reason,
                                    ComplaintState=0)
            db.session.add(newobj)
            db.session.commit()
            return render_template('received.html', amount=user_orders_sum, orders=user_orders)
        return render_template('received.html', amount=user_orders_sum, orders=user_orders)
    else:
        flash("请先登陆",'warning')
        return redirect(url_for('login.a'))


@user.route("/can_require",methods=('GET', 'POST'))
def can_require():
    if 'identity' in session and session['identity']=='user':
        NAME = session['name']
        IDCARD = models.Users.query.filter_by(name=NAME).first().idcard
        G = models.GoodsInfo.query.filter(models.GoodsInfo.DDL >= datetime.utcnow()).all()
        G_amount = models.GoodsInfo.query.filter(models.GoodsInfo.DDL >= datetime.utcnow()).count()
        if request.method == 'POST':
            goodsid = request.form['goods_id']
            name = request.form['name']
            idcards = request.form['id']
            address = request.form['address']
            sums = request.form['sum']
            orders = models.GoodsInfo.query.filter_by(id=goodsid).first()
            if orders.OrderLimitPerPerson < int(sums):
                flash("申领数量超过每人限制！",'warning')
                return render_template('supply.html', amount=G_amount, goods=G)
            if int(sums) > orders.OrderLimit:
                flash("剩余数量不足！",'warning')
                return render_template('supply.html', amount=G_amount, goods=G)
            if models.OrderInfo.query.filter_by(userid=IDCARD, GoodsID=goodsid, OrderState=0).first():
                flash("您已申领过该物资，不可重复申领",'warning')
                return render_template('supply.html', amount=G_amount, goods=G)
            if not models.Users.query.filter_by(name=NAME, idcard=IDCARD).first():
                flash("身份证号错误",'warning')
                return render_template('supply.html', amount=G_amount, goods=G)
            if not models.Users.query.filter_by(idcard=IDCARD, name=NAME).first():
                flash("姓名错误",'warning')
                return render_template('supply.html', amount=G_amount, goods=G)
            if len(address) > 30:
                flash("过长的地址输入！",'warning')
                return render_template('supply.html', amount=G_amount, goods=G)
            if int(sums) <= 0:
                flash("申领数量应该为正整数",'warning')
                return render_template('supply.html', amount=G_amount, goods=G)
            newobj = models.OrderInfo(userid=IDCARD, GoodsID=goodsid, Goodsname=orders.Goodsname, idcards=IDCARD, username=NAME,
                                    address=address, OrderNum=sums, CreateTime=datetime.utcnow(), OrderState=0)
            db.session.add(newobj)
            db.session.commit()
            return render_template('supply.html', amount=G_amount, goods=G)
        return render_template('supply.html', amount=G_amount, goods=G)
    else:
        flash("请先登录",'warning')
        return redirect(url_for('login.a'))
    

@user.route("/required")
def required():
    if 'identity' in session and session['identity']=='user':
        NAME = session['name']
        IDCARD = models.Users.query.filter_by(name=NAME).first().idcard
        user_orders = models.OrderInfo.query.filter_by(userid=IDCARD).all()
        user_orders_sum = models.OrderInfo.query.filter_by(userid=IDCARD).count()
        return render_template('required.html', amount=user_orders_sum, orders=user_orders)
    else:
        flash("请先登录",'warning')
        return redirect(url_for('login.a'))
    

@user.route("/deleteorder/<orderid>", methods=('POST', 'GET'))
def delete(orderid):
    g = models.OrderInfo.query.filter_by(id=orderid).first()
    if g:
        g.OrderState = 4
        db.session.commit()
        flash("取消申领成功",'success')
        return redirect(url_for('.required'))
    return redirect(url_for('.required'))

@user.route("/win")
def win():
    if 'identity' in session and session['identity']=='user':
        NAME = session['name']
        IDCARD = models.Users.query.filter_by(name=NAME).first().idcard
        user_orders = models.OrderInfo.query.filter_by(userid=IDCARD, OrderState=1).all()
        user_orders_sum = models.OrderInfo.query.filter_by(userid=IDCARD, OrderState=1).count()
        return render_template('win.html', amount=user_orders_sum, orders=user_orders)
    else:
        flash("请先登录",'warning')
        return redirect(url_for('login.a'))

@user.route("/wait_receive", methods=('GET', 'POST'))
def wait_receive():
    if 'identity' in session and session['identity']=='user':
        NAME = session['name']
        IDCARD = models.Users.query.filter_by(name=NAME).first().idcard
        user_orders = models.OrderInfo.query.filter_by(userid=IDCARD, OrderState=2).all()
        user_orders_sum = models.OrderInfo.query.filter_by(userid=IDCARD, OrderState=2).count()
        if request.method == 'POST':
            if request.form['id']:
                order_id = request.form['id']
                order = models.OrderInfo.query.filter_by(id=order_id).first()
                order.OrderState = 4
                order.CancelTime = datetime.utcnow()
                db.session.commit()
                user_orders = models.OrderInfo.query.filter_by(userid=IDCARD, OrderState=2).all()
                user_orders_sum = models.OrderInfo.query.filter_by(userid=IDCARD, OrderState=2).count()
            else:
                order_id = request.form['-id']
                order = models.OrderInfo.query.filter_by(id=order_id).first()
                order.OrderState = 3
                order.ReceiveTime = datetime.utcnow()
                db.session.commit()
                user_orders = models.OrderInfo.query.filter_by(userid=IDCARD, OrderState=2).all()
                user_orders_sum = models.OrderInfo.query.filter_by(userid=IDCARD, OrderState=2).count()
            return render_template('wait_receive.html', amount=user_orders_sum, orders=user_orders)
        return render_template('wait_receive.html', amount=user_orders_sum, orders=user_orders)
    else:
        flash("请先登录",'warning')
        return redirect(url_for('login.a'))
