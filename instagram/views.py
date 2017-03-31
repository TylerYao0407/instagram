# encoding:utf-8

from instagram import app, db
from models import Image, User
from flask import render_template, redirect, request, flash, get_flashed_messages
from flask_login import login_user, logout_user, current_user, login_required
import random
import hashlib
import json


@app.route("/")
def index():
    images = Image.query.order_by(db.desc(Image.id)).limit(10).all()
    return render_template('index.html', images=images)


@app.route("/image/<int:image_id>")
def image(image_id):
    images = Image.query.get(image_id)
    if image is None:
        return redirect('/')
    return render_template('pageDetail.html', image=images)


@app.route('/profile/<int:user_id>/')
@login_required
def profile(user_id):
    user = User.query.get(user_id)
    if user is None:
        return redirect('/')
    paginate = Image.query.filter_by(user_id=user_id).paginate(page=1, per_page=3, error_out=False)
    return render_template('profile.html', user=user, images=paginate.items, has_next=paginate.has_next)


@app.route('/profile/images/<int:user_id>/<int:page>/<int:per_page>/')
def user_images(user_id, page, per_page):
    paginate = Image.query.filter_by(user_id=user_id).paginate(page=page, per_page=per_page, error_out=False)
    map = {'has_next': paginate.has_next}
    images = []
    for img in paginate.items:
        img_vo = {'id': img.id, 'url': img.url, 'comment_count': len(img.comments)}
        images.append(img_vo)
    map['images'] = images
    return json.dumps(map)


@app.route('/register_login/')
def register_login():
    msg = ''
    for m in get_flashed_messages(with_categories=False, category_filter=['reg_login']):
        msg = msg + m
    return render_template('login.html', msg=msg, next=request.values.get('next'))


def redirect_with_msg(target, msg, category):
    if msg is not None:
        flash(msg, category=category)
    return redirect(target)


@app.route('/login/', methods={'get', 'post'})
def login():
    username = request.values.get('username').strip()
    password = request.values.get('password').strip()
    if username == '' and password == '':
        return redirect_with_msg('/register_login/', u'用户名和密码不能为空', 'reg_login')
    if username == '':
        return redirect_with_msg('/register_login/', u'用户名不能为空', 'reg_login')
    if password == '':
        return redirect_with_msg('/register_login/', u'密码不能为空', 'reg_login')
    user = User.query.filter_by(username=username).first()
    if user is None:
        return redirect_with_msg('/register_login/', u'用户不存在', 'reg_login')
    m = hashlib.md5()
    m.update(password + user.salt)
    if m.hexdigest() != user.password:
        return redirect_with_msg('/register_login/', u'密码错误', 'reg_login')
    login_user(user)

    next_par = request.values.get('next')
    if next_par is not None and next_par.startswith('/'):
        return redirect(next_par)
    return redirect('/')


@app.route('/reg/', methods={'post', 'get'})
def reg():
    username = request.values.get('username').strip()
    password = request.values.get('password').strip()
    if username == '' and password == '':
        return redirect_with_msg('/register_login/', u'用户名和密码不能为空', 'reg_login')
    if username == '':
        return redirect_with_msg('/register_login/', u'用户名不能为空', 'reg_login')
    if password == '':
        return redirect_with_msg('/register_login/', u'密码不能为空', 'reg_login')
    user = User.query.filter_by(username=username).first()
    if user is not None:
        return redirect_with_msg('/register_login/', u'用户名不存在', 'reg_login')
    # 更多判断
    salt = ''.join(random.sample("I love you,I am a Chinese boy,I love coding,This is salt", 10))
    m = hashlib.md5()
    m.update(password+salt)
    password = m.hexdigest()
    user = User(username, password, salt)
    db.session.add(user)
    db.session.commit()
    # 注册成功之后，自动登录
    login_user(user)
    return redirect('/')


@app.route('/logout/')
def logout():
    logout_user()
    return redirect('/')
