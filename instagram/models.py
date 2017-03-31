# encoding:utf-8

from instagram import db, login_manager
from datetime import datetime
import random


# 评论类
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 唯一的主键
    content = db.Column(db.String(1024))  # 评论内容
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'))  # 评论所对应的图片
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 评论对应的用户id
    status = db.Column(db.Integer, default=0)  # 评论状态 0 正常 1 被删除
    user = db.relationship('User')

    # 初始化函数
    def __init__(self, content, image_id, user_id):
        self.content = content
        self.image_id = image_id
        self.user_id = user_id

    def __repr__(self):
        return '<Comment %d %s>' % (self.id, self.content)


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 图片id
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 照片对应的用户id
    url = db.Column(db.String(512))  # 图片的url
    created_date = db.Column(db.DateTime)  # 创建时间
    comments = db.relationship('Comment')

    def __init__(self, url, user_id):
        self.url = url
        self.user_id = user_id
        self.created_date = datetime.now()

    def __repr__(self):
        return '<Image %d %s>' % (self.id, self.url)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True)  # 用户名
    password = db.Column(db.String(32))  # 密码
    salt = db.Column(db.String(32))  # 密码加盐
    head_url = db.Column(db.String(256))  # 头像的url地址
    images = db.relationship('Image', backref='user', lazy='dynamic')  # backref：反向联结(一对多)

    # 构造函数
    def __init__(self, username, password, salt=''):
        self.username = username
        self.password = password
        self.salt = salt
        self.head_url = "http://images.nowcoder.com/head/" + str(random.randint(0, 1000)) + 'm.png'

    # 返回一个描述对象
    def __repr__(self):
        return '<User %d %s>' % (self.id, self.username)

    # Flask Login接口
    @property
    def is_authenticated(self):
        print 'is_authenticated'
        return True

    @property
    def is_active(self):
        print 'is_active'
        return True

    @property
    def is_anonymous(self):
        print 'is_anonymous'
        return False

    def get_id(self):
        print 'get_id'
        return self.id


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

