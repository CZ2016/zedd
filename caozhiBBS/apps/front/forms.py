#encoding:utf-8
from ..forms import BaseForm
from wtforms import StringField,IntegerField
from wtforms.validators import EqualTo,Regexp,ValidationError,Length,InputRequired
from utils import zlache
from .models import FrontUser

class RegistForm(BaseForm):
	telephone=StringField(validators=[Regexp(r"1[345789]\d{9}",message='请输入正确格式手机号')])
	sms_captcha = StringField(validators=[Regexp(r'\w{4}', message='请输入正确格式的短信验证码！')])
	username = StringField(validators=[Regexp(r".{2,20}", message='请输入正确格式的用户名！')])
	password=StringField(validators=[Regexp(r"[0-9a-zA-Z_\.]{6,20}",message='请输入正确格式的密码！')])
	confirmpwd=StringField(validators=[EqualTo('password',message='两次密码输入不一致')])
	graph_captcha = StringField(validators=[Regexp(r"\w{4}", message='请输入正确格式的短信验证码！')])

	def validate_sms_captcha(self,field):
		sms_captcha=field.data
		telephone=self.telephone.data
		sms_captcha_mem=zlache.get(telephone)
		if not sms_captcha_mem and sms_captcha.lower()!=sms_captcha_mem:
			raise ValidationError(message='短信验证码错误!')

	def validate_graph_captcha(self,field):
		graph_captcha=field.data
		graph_captcha_mem=zlache.get(graph_captcha.lower())
		if not graph_captcha_mem:
			raise ValidationError(message='图形验证码错误')

	def validate_telephone(self,field):
		telephone=field.data
		have_telephone=FrontUser.query.filter_by(telephone=telephone).first()
		if have_telephone:
			raise ValidationError(message='该手机号已被注册')

	def validate_username(self,field):
		username=field.data
		have_username=FrontUser.query.filter_by(username=username).first()
		if have_username:
			raise ValidationError(message='用户名已经存在')






class LoginForm(BaseForm):
	telephone = StringField(validators=[Regexp(r"1[345789]\d{9}", message='请输入正确格式手机号')])
	password = StringField(validators=[Regexp(r"[0-9a-zA-Z_\.]{6,20}", message='请输入正确格式的密码！')])
	remember=StringField()


class AddPostForm(BaseForm):
	title=StringField(validators=[InputRequired(message='请输入帖子标题')])
	content=StringField(validators=[InputRequired(message='请输入内容')])
	board_id=IntegerField(validators=[InputRequired(message='请输入板块ID')])


class CommentForm(BaseForm):
	content=StringField(validators=[InputRequired(message='请输入评论内容')])
	post_id=IntegerField(validators=[InputRequired(message='请输入帖子ID')])