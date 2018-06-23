#encoding:utf-8

from wtforms import StringField,IntegerField
from ..forms import BaseForm
from wtforms.validators import Email,InputRequired,Length,EqualTo
from utils import zlache
from wtforms import ValidationError
from flask import g

class LoginForm(BaseForm):
    email=StringField(validators=[Email(message='请输入正确的邮箱格式'),InputRequired(message='请输入邮箱')])
    password=StringField(validators=[Length(6,20,message='密码输入不正确')])
    remember=IntegerField()

class ResetPwdForm(BaseForm):
    oldpwd = StringField(validators=[Length(6, 20, message='请输入正确格式旧密码')])
    newpwd=StringField(validators=[Length(6,20,message='请输入正确格式新密码')])
    confirmpwd=StringField(validators=[EqualTo('newpwd',message='两次密码输入不一致')])


class ResetEmialForm(BaseForm):
    email=StringField(validators=[Email(message='请输入正确格式的邮箱')])
    captcha=StringField(validators=[Length(min=6,max=6,message='请输入正确长度的验证码')])

    def validate_captcha(self,field):
        captcha=field.data

        email=self.email.data
        captcha_cache=zlache.get(email)  #从memcached中根据用户提交的email取出
        if not captcha_cache or captcha_cache.lower()!=captcha.lower():
            raise ValidationError('邮箱验证码错误')

    def validate_email(self,field):
        email=field.data
        user=g.cms_user
        if user.email==email:
            raise ValidationError('不能修改为相同的邮箱')

class AddBannersForm(BaseForm):
    banner_name=StringField(validators=[InputRequired(message='请输入轮播图名称')])
    image_url=StringField(validators=[InputRequired(message='请输入图片链接')])
    link_url=StringField(validators=[InputRequired(message='请输入跳转链接')])
    priority=IntegerField(validators=[InputRequired(message='请输入轮播图优先级')])


class UpdateBannersForm(AddBannersForm):
    banner_id=IntegerField(validators=[InputRequired(message='请输入轮播图ID')])


class AddBoardForm(BaseForm):
    board_name=StringField(validators=[InputRequired(message='请输入板块名称')])


class UpdateBoardForm(AddBoardForm):
    board_id=IntegerField(validators=[InputRequired()])