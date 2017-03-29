# encoding:utf-8

from instagram import app


@app.route("/")
def index():
    return "Hello"
