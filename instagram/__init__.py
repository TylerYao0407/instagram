# encoding:utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
app.config.from_pyfile("app.conf")  # 加载数据库配置文件
app.secret_key = 'tyler'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = '/register_login/'
from instagram import views, models
# 58min