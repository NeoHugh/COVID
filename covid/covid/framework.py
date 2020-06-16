from flask import render_template, url_for, flash, redirect,session,Blueprint
from covid import db
from covid.forms import LoginForm, RegistrationForm, AdminForm, AdminLoginForm, pswForm,InfoForm
from covid.models import Users, Admin

login = Blueprint('login', __name__)

@login.before_request
def before_login():
    if 'identity' in session:
        print(session['identity'])
        pass
    else:
        session['identity']='Unknown'
        pass

@login.route("/home")
def home():
    return render_template('yourwebsite.html')


@login.route("/", methods=['GET', 'POST'])
def a():
    form = LoginForm()
    if form.validate_on_submit():
        # if form.email.data == Users.name and form.password.data == Users.pwd:
        user = Users.query.filter_by(email=form.email.data, pwd=form.password.data).first()
        print(user)
        if user:
            session['username']=user.username
            session['identity']='user'
            session['email'] = form.email.data
            session['name']=user.name
            flash('登录成功!','success')
            # db.session['email'] = form.email.data
        else:
            flash('登录失败！请重新输入账号密码','')
    return render_template('a.html', title='Login', form=form)

@login.route("/homeAdmin")
def homeAdmin():
    if 'identity' in session and session['identity']!=3:
        flash('小火汁，你的思想很危险！','danger')
        return redirect(url_for('.a'))
    admin = Admin.query.all()
    return render_template('homeAdmin.html', admin=admin)

@login.route("/info", methods=['GET', 'POST'])
def info():
    form = InfoForm()
    if 'email' not in session:
        flash('请先登录！','warning')
        return redirect(url_for('.a'))
    email=session['email']
    t_user=Users.query.filter_by(email=email).first()
    form.username.data=t_user.username
    form.name.data=t_user.name
    form.idcard.data=t_user.idcard
    form.phone.data=t_user.phone
    form.province.data=t_user.province
    form.address.data=t_user.address
    if form.validate_on_submit():
        Users.query.filter_by(email=email).update({'name':form.name.data},{'username':form.username.data},
                                                           {'idcard':form.idcard.data},{'province':form.province.data},
                                                           {'phone':form.phone.data},{'address':form.address.data})
        flash(f'个人信息更新成功','success')
        return redirect(url_for('.home'))
    return render_template('info.html', title='Info', form=form)

@login.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        email = Users.query.filter_by(email=form.email.data).all()
        username = Users.query.filter_by(username=form.username.data).all()
        idc = Users.query.filter_by(idcard=form.idcard.data).all()
        if email:
            flash('该邮箱已被注册过！')
        if username:
            flash('用户名重复！')
        if idc:
            flash('身份证号重复！')
        else:
            user = Users(username=form.username.data, pwd=form.password.data, email=form.email.data,
                         address=form.address.data, name=form.name.data, province=form.province.data,
                         idcard=form.idcard.data, phone=form.phone.data)
            db.session.add(user)
            db.session.commit()
            print(1)
            flash(f'Account created for {form.username.data}!', 'success')
            session['name']=user.username
            return redirect(url_for('login.a'))
    return render_template('register.html', title='Register', form=form)


@login.route("/forget", methods=['GET', 'POST'])
def forget():
    form = pswForm()
    # if form.idcard.data
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).all()
        if user:
            user_ok = Users.query.filter_by(idcard=form.idcard.data).all()
            if user_ok:
                Users.query.filter_by(idcard=form.idcard.data).update({'pwd': form.password.data})
                flash(f'密码更新成功!', 'success')
                return redirect(url_for('.a'))
            else:
                flash(f'身份证号验证错误！','warning')
        else:
            flash(f'用户不存在！','warning')
    return render_template('forget.html', title='forget psw', form=form)


@login.route("/adminLog", methods=['GET', 'POST'])
def adminLog():
    form = AdminLoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(name=form.name.data, pwd=form.password.data).all()
        if admin:
            session['identity']= admin[0].system
            session['province']= admin[0].province
            if 'name' in session:
                session.pop('name')
            session['name']=admin[0].name
            flash('登录成功!','success')
            if admin[0].system==1:
                return redirect(url_for('#'))
            if admin[0].system==2:
                session['province']=admin[0].province
                return redirect(url_for('situation.admin'))
            if admin[0].system==3:
                return redirect(url_for('.homeAdmin'))
            if admin[0].system==4:
                return redirect(url_for('transport_admin.index'))
            if admin[0].system==5:
                return redirect(url_for('population_admin.index'))
            if admin[0].system==6:
                return redirect(url_for('goods_admin.admin_open'))
        else:
            flash('登录失败！请重新输入账号密码','warning')
    return render_template('adminLog.html', title='Admin-Login', form=form)


@login.route("/addAdmin", methods=['GET', 'POST'])
def addAdmin():
    if 'identity' in session and session['identity']!=3:
        flash('小火汁，你的思想很危险！','danger')
        return redirect(url_for('.a'))
    form = AdminForm()
    if form.validate_on_submit():
        other = Admin.query.filter_by(name=form.name.data).all()
        if other:
            flash(f'已存在该管理员！')
        else:
            admin = Admin(name=form.name.data, pwd=form.password.data, province=form.province.data,
                          system=form.right.data, auth=1)
            db.session.add(admin)
            db.session.commit()
            flash(f'成功新增管理员 {form.name.data}!', 'success')
            return redirect(url_for('.homeAdmin'))
    return render_template('addAdmin.html', title='addAdmin', form=form)
