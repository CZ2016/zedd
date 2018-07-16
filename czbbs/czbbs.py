#encoding:utf-8
from flask import Flask
from apps.cms import bp as cms_bp
from apps.common import bp as common_bp
from apps.front import bp as front_bp
from apps.ueditor.ueditor import bp as ueditor_bp
import config
from exts import db,mail
from flask_wtf import CSRFProtect


def create_app():
    app=Flask(__name__)

    app.config.from_object(config)
    app.register_blueprint(cms_bp)
    app.register_blueprint(common_bp)
    app.register_blueprint(front_bp)
    app.register_blueprint(ueditor_bp)

    db.init_app(app)
    mail.init_app(app)
    CSRFProtect(app)
    return app

app=create_app()
app.run(host='0.0.0.0',port=8000)
