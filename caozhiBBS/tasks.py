#encoding:utf-8
from celery import Celery
import config
from flask_mail import Message
from exts import mail
from flask import Flask
from utils.aliyunSDK import alidayu

app=Flask(__name__)
app.config.from_object(config)
mail.init_app(app)


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

celery=make_celery(app)

#终端命令:celery -A tasks.celery worker --loglevel=info;

@celery.task
def send_mail(subject,recipients,body):
	print('邮件开始发送')
	message=Message(subject=subject,recipients=recipients,body=body)
	mail.send(message)
	print('邮件发送成功')


#终端命令:celery -A tasks.celery worker --loglevel=info;
@celery.task
def send_sms_captcha(telephone,captcha):
	alidayu.send_sms(telephone,code=captcha)
	print('发送验证码成功')