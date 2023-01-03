# 装饰器
from functools import wraps
from flask import g, redirect, url_for


def login_require(func):
    # 保留func的信息
    @wraps(func)
    def inner(*args, **kwargs):
        if g.user:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('auth.login'))

    return inner
