 #encoding:utf-8

from flask import (Blueprint,
                   views,
                   render_template,
                   make_response,
                   request,
                   session,
                   url_for,
                   g,
                   abort)

from .forms import RegistForm,LoginForm,AddPostForm,CommentForm
from ..front.models import FrontUser,UserProfileModel
from ..models import BannerModel,BoardModel,PostModel,CommentModel,HighPostModel
from .decorators import LoginRequired
from utils import restful,safeutils
from exts import db
from flask_paginate import Pagination,get_page_parameter #分页API
from sqlalchemy.sql import func
import config


# from exts import alidayu


bp = Blueprint('front', __name__)


@bp.route('/')
def index():
	boards=BoardModel.query.all()
	board_id=request.args.get('bd',type=int,default=None)
	banners=BannerModel.query.order_by(BannerModel.priority.desc()).limit(4)
	page=request.args.get(get_page_parameter(),type=int,default=1)

	sort=request.args.get('sort',type=int,default=1)
	query_obj=None
	if sort==1:
		# 默认按照时间最新进行排序
		query_obj=PostModel.query.order_by(PostModel.create_time.desc())
	elif sort==2:
		# 按照加精进行排序
		query_obj=db.session.query(PostModel).outerjoin(HighPostModel).\
			order_by(HighPostModel.create_time.desc(),PostModel.create_time.desc())
			#两种排序方式，首先使用加精时间的先后进行排序，其次使用post的创建时间进行排序
	elif sort==3:
		# 按照点赞数量进行排序
		query_obj=PostModel.query.order_by(PostModel.create_time.desc())
	elif sort==4:
		# 按照评论数目进行排序
		query_obj=db.session.query(PostModel).outerjoin(CommentModel).\
			group_by(PostModel.id).order_by(func.count(CommentModel.id).desc(),PostModel.create_time.desc())

	start=(page-1)*config.PER_PAGE
	end=start+config.PER_PAGE     #首页帖子分页
	posts=None
	total=0


	if  board_id:
		query_obj=query_obj.filter(PostModel.board_id==board_id)
		posts=query_obj.slice(start,end)
		total=query_obj.count()
	else:
		posts=query_obj.slice(start,end)
		total=query_obj.count()

	pagination = Pagination(bs_version=3, page=page, total=total)
	context={
	 'banners':banners,
	 'boards':boards,
	 'posts':posts,
	'pagination':pagination,
	'current_board':board_id,
	'current_sort':sort
	}

	return render_template('front/front_index.html',**context)






# 验证接口
# @bp.route('/sms_captcha/')
# def sms_captcha():
#     result=Send_sms.send_sms('17606863093',text='GGG444')
#     if result:
#         return '发送成功'
#     else:
#         return '发送失败'

class LoginView(views.MethodView):
	def get(self):
		return_to=request.referrer    #重新登录后，回到跳转之前的页面
		if return_to and return_to !=request.url and \
				safeutils.is_safe_url(return_to) and return_to!=url_for('front.regist'):
			return render_template('front/front_login.html',return_to=return_to)
		else:
			return render_template('front/front_login.html')
	def post(self):
		form=LoginForm(request.form)
		if form.validate():
			telephone=form.telephone.data
			password=form.password.data
			remember=form.remember.data
			user=FrontUser.query.filter_by(telephone=telephone).first()
			if user and user.check_password(password):
				session[config.FRONT_USER_ID]= user.id
				if remember:
					session.permanent=True
					return restful.success()
			else:
				return restful.paramserror(message='手机号或者密码错误')
		else:
			return restful.paramserror(message=form.get_errors())


class RegistView(views.MethodView):
	def get(self):
		return_to=request.referrer
		if return_to and return_to!=request.url and safeutils.is_safe_url(return_to):
			return render_template('front/front_regist.html',return_to=return_to)
		else:
			return render_template('front/front_regist.html')

	def post(self):
		form=RegistForm(request.form)
		if form.validate():
			telephone=form.telephone.data
			username=form.username.data
			password=form.password.data
			user=FrontUser(telephone=telephone,username=username,password=password)
			db.session.add(user)
			db.session.commit()
			return restful.success()

		else:
			print(form.get_errors())
			return restful.paramserror()

@bp.route('/apost/',methods=['GET','POST'])
@LoginRequired
def apost():
	if request.method=='GET':
		boards=BoardModel.query.all()
		return render_template('front/front_post.html',boards=boards)
	else:
		form=AddPostForm(request.form)
		if form.validate():
			title=form.title.data
			content=form.content.data
			board_id=form.board_id.data
			board=BoardModel.query.get(board_id)

			if not board:
				return restful.paramserror(message='没有这个板块')
			post=PostModel(title=title,content=content)
			post.board=board
			post.author=g.front_user
			db.session.add(post)
			db.session.commit()
			return restful.success()
		else:
			return restful.paramserror(message=form.get_errors())


@bp.route('/p/<post_id>/')
def pdetail(post_id):
	post=PostModel.query.get(post_id)
	if not post:
		abort(404)
	else:
		return render_template('front/front_pdetail.html',post=post)


@bp.route('/comment/',methods=['POST'])
@LoginRequired
def comment():
	form=CommentForm(request.form)
	if form.validate():
		content=form.content.data
		post_id=form.post_id.data
		post= PostModel.query.get(post_id)
		if post:
			comment=CommentModel(content=content)
			comment.post=post
			comment.author=g.front_user
			db.session.add(comment)
			db.session.commit()
			return restful.success()
		else:
			return restful.paramserror(message='没有这片帖子')
	else:
		return restful.paramserror(message=form.get_errors())


@bp.route('/profile/',methods=['POST','GET'])
@LoginRequired
def profile():
	if request.method=='GET':
		return render_template('front/front_profile.html')
	else:
		user_id = request.form.get('user_id')
		print(user_id)
		user = FrontUser.query.get(user_id)
		avatar=request.form.get('avatar_image_url')
		print(avatar)
		user.avatar=avatar
		db.session.commit()
		return restful.success()

@bp.route('/uprofile/',methods=['POST','GET']) #完善个人信息
@LoginRequired
def uprofile():
	if request.method=='GET':
		user_id = request.args.get('user_id')
		# print(user_id)
		# pro=UserProfileModel.query.filter_by(user_id=user_id).first()
		# user = FrontUser.query.get(user_id)
		# p=user.profile[0]
		# p.email='33333@qq.com'
		# db.session.commit()
		# print(pro.qq)

		return render_template('front/front_updateprofile.html')
	else:
		user_id = request.form.get('user_id')
		user = FrontUser.query.get(user_id)

		realname=request.form.get('realname')

		qq=request.form.get('qq')
		email=request.form.get('email')
		singature=request.form.get('singature')
		gender=request.form.get('gender')
		dprofile=UserProfileModel.query.filter_by(user_id=user_id).first()

		profile=UserProfileModel(realname=realname,email=email,qq=qq,gender=gender,singature=singature)

		# user.profile.qq=qq
		# user.profile.realname=realname
		# user.profile.email=email
		# user.profile.singature=singature
		# user.profile.gender=gender
		# user.profile.id=user_id
		try:
			db.session.delete(dprofile)
			db.session.commit()
		except Exception:
			profile.user = user
			db.session.add(profile)
			db.session.commit()
		finally:
			profile.user = user
			db.session.add(profile)
			db.session.commit()



		# user_info=UserProfileModel(realname=realname,qq=qq,email=email,singature=singature,gender=gender)
		# user_info.user=user
		# db.session.add(user_info)
		# db.session.commit()
		return restful.success()







bp.add_url_rule('/regist/',view_func=RegistView.as_view('regist'))
bp.add_url_rule('/login/',view_func=LoginView.as_view('login'))