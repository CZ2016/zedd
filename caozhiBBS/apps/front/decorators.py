#encoding:utf-8
from flask import session,redirect,url_for,g
from functools import wraps
import config

def LoginRequired(func):
    @wraps(func)
    def inner(*args,**kwargs):
        if config.FRONT_USER_ID in session:
            return func(*args,**kwargs)
        else:
            return redirect(url_for('front.login'))
    return inner