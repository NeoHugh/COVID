from flask import Flask, render_template, url_for, flash, redirect
# from flask_sqlalchemy import SQLAlchemy

from forms import LoginForm, RegistrationForm, AdminForm, AdminLoginForm, pswForm
from flask_bootstrap import Bootstrap

from db import db
from models import Users, Admin

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config["SECRET_KEY"] = "123456"

app.config["SQLALCHEMY_DATABASE_URI"] = 'mssql+pyodbc://abc:123456@flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db.init_app(app)
# db = SQLAlchemy(app)
db.reflect(app=app)
tables = db.metadata.tables
print('------------')
print(tables)


@app.route("/")
@app.route("/home")
def home():
    return render_template('yourwebsite.html')


@app.route("/homeAdmin")
def homeAdmin():
    admin = Admin.query.all()
    return render_template('homeAdmin.html', admin=admin)


@app.route("/a", methods=['GET', 'POST'])
def a():
    form = LoginForm()
    if form.validate_on_submit():
        # if form.email.data == Users.name and form.password.data == Users.pwd:
        user = Users.query.filter_by(email=form.email.data, pwd=form.password.data).all()
        if user:
            flash('登录成功!')
            # db.session['email'] = form.email.data
            return redirect(url_for('home'))
        else:
            flash('登录失败！请重新输入账号密码')
    return render_template('a.html', title='Login', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        email = Users.query.filter_by(email=form.email.data).all()
        username = Users.query.filter_by(username=form.username.data).all()
        idc = Users.query.filter_by(idcard=form.idcard.data).all()
        if email:
            flash('该邮箱已被注册过！')
            # return redirect(url_for('register'))
        if username:
            flash('用户名重复！')
            # return redirect(url_for('register'))
        if idc:
            flash('身份证号重复！')
        else:
            user = Users(username=form.username.data, pwd=form.password.data, email=form.email.data,
                         address=form.address.data, name=form.name.data, province=form.province.data,
                         idcard=form.idcard.data, phone=form.phone.data, id=int(form.idcard.data))
            db.session.add(user)
            db.session.commit()

            flash(f'Account created for {form.username.data}!', 'success')

            return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/forget", methods=['GET', 'POST'])
def forget():
    form = pswForm()
    # if form.idcard.data
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data, idc=form.idcard.data).all()
        if user:
            Users.query.filter_by(idc=form.idcard.data).update(pwd=form.password.data)
            flash(f'密码更新成功!', 'success')
            return redirect(url_for('a'))
       # else:
        #    flash(f'用户不存在！')
    return render_template('forget.html', title='forget psw', form=form)


@app.route("/adminLog", methods=['GET', 'POST'])
def adminLog():
    form = AdminLoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(name=form.name.data, pwd=form.password.data).all()
        if admin:
            flash('登录成功!')
            return redirect(url_for('homeAdmin'))
        else:
            flash('登录失败！请重新输入账号密码')
    return render_template('adminLog.html', title='Admin-Login', form=form)


@app.route("/addAdmin", methods=['GET', 'POST'])
def addAdmin():
    form = AdminForm()
    if form.validate_on_submit():
        # admin=Admin(name=form.name.data,pwd=form.password.data)
        admin = Admin(name=form.name.data, pwd=form.password.data, system=form.rights.data)
        db.session.add(admin)
        db.session.commit()
        flash(f'Account created for {form.name.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('addAdmin.html', title='addAdmin', form=form)


if __name__ == '__main__':
    app.debug = True
    app.run()
