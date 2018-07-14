 #encoding:utf-8

from flask import (Blueprint,
                   views,
                   render_template,
                   make_response,
                   request,
                   session,
                   url_for,
                   g,
                   abort,
                   redirect)

from .forms import RegistForm,LoginForm,AddPostForm,CommentForm,ChangePwdForm
from ..front.models import FrontUser,Follow
from ..models import BannerModel,BoardModel,PostModel,CommentModel,HighPostModel
from .decorators import LoginRequired
from utils import restful,safeutils
from exts import db
from flask_paginate import Pagination,get_page_parameter #分页API
from sqlalchemy.sql import func
import config
from werkzeug.security import generate_password_hash
from utils.aliyunSDK import alidayu

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
	elif sort==5:
		# 我关注的人的帖子
		query_obj=g.front_user.followed_posts.order_by(PostModel.create_time.desc())
	# print(pos)
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
#     result=alidayu.send_sms('17606863093',code='GGG444')
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


@bp.route('/logout/')
@LoginRequired
def logout():
	del session[config.FRONT_USER_ID]
	return redirect(url_for('front.index'))


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
			# print(form.get_errors())
			# message=form.get_errors()
			# print(message)
			return restful.paramserror(form.get_errors())
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
	comment_num=CommentModel.query.filter(post_id==CommentModel.post_id).count()
	post.comment_num=comment_num
	db.session.commit()
	if not post:
		abort(404)
	else:
		post.hit=post.hit+1
		db.session.commit()

		return render_template('front/front_pdetail.html',post=post,comment_num=comment_num)


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


@bp.route('/changepwd/',methods=['POST','GET'])
@LoginRequired
def changepwd():
	if request.method=='GET':
		return_to = request.referrer
		if return_to and return_to != request.url and safeutils.is_safe_url(return_to):
			return render_template('front/front_changepwd.html', return_to=return_to)
		else:
			return render_template('front/front_regist.html')
	else:
		user=g.front_user
		oldpwd=request.form.get('oldpwd')
		if user.check_password(oldpwd):
			form=ChangePwdForm(request.form)
			if form.validate():
				newpwd=form.newpwd.data
				user.password=newpwd
				db.session.commit()
			else:
				return restful.paramserror(message=form.get_errors())
		else:
			return restful.paramserror(message='原始密码输入错误')
		return restful.success()


@bp.route('/profile/',methods=['POST','GET'])
@LoginRequired
def profile():
	if request.method=='GET':
		user_id = g.front_user.id

		sort=request.args.get('sort',type=int,default=1)

		page = request.args.get(get_page_parameter(), type=int, default=1)
		start = (page - 1) * config.PER_PAGE
		end = start + config.PER_PAGE
		posts = PostModel.query.filter_by(author_id=user_id).order_by(PostModel.create_time.desc()).slice(start,end)
		total=PostModel.query.filter_by(author_id=user_id).count()
		pagination = Pagination(bs_version=3, page=page, total=total)

		follower_num = Follow.query.filter(Follow.followed_id == user_id).count()
		followed_num = Follow.query.filter(Follow.follower_id == user_id).count()
		context = {
			'follower': follower_num,
			'followed': followed_num,
			'pagination':pagination,
			'current_sort':sort,
			'posts':posts
		}

		return render_template('front/front_profile.html',**context)

	else:
		# user_id = request.form.get('user_id')
		# user = FrontUser.query.get(user_id)
		user=g.front_user
		avatar=request.form.get('avatar_image_url')

		user.avatar=avatar
		db.session.commit()
		return restful.success()

@bp.route('/uprofile/',methods=['POST','GET']) #完善个人信息
@LoginRequired
def uprofile():
	if request.method=='GET':
		user_id = request.args.get('user_id')
		return render_template('front/front_updateprofile.html')
	else:
		# user_id = request.form.get('user_id')
		#
		# user = FrontUser.query.get(user_id)
		user=g.front_user
		realname=request.form.get('realname')
		qq=request.form.get('qq')
		email=request.form.get('email')
		singature=request.form.get('singature')
		gender=request.form.get('gender')

		user.realname=realname
		user.qq=qq
		user.email=email
		user.singature=singature
		user.gender=gender
		db.session.commit()
		return restful.success()

@bp.route('/profile1/')
def profile1():
	user_id=request.args.get('user_id')
	sort=request.args.get('sort',type=int,default=1)
	user=FrontUser.query.filter_by(id=user_id).first()
	posts = PostModel.query.filter_by(author_id=user_id).order_by(PostModel.create_time.desc()).all()
	follower_num=Follow.query.filter(Follow.followed_id==user_id).count()
	followed_num=Follow.query.filter(Follow.follower_id==user_id).count()
	context={
		'user':user,
		'current_sort':sort,
		'posts':posts,
		'follower':follower_num,
		'followed':followed_num
	}
	if user:
		return render_template('front/front_profile1.html',**context)
	else:
		return restful.paramserror(message='没有该用户')


@bp.route('/follow/',methods=['POST'])
def follow():
	other_user_id=request.form.get('other_user_id')
	current_user=g.front_user
	other_user=FrontUser.query.filter_by(id=other_user_id).first()
	current_user.follow(other_user)
	db.session.commit()
	return restful.success()


@bp.route('/unfollow/',methods=['POST'])
def unfollow():
	other_user_id=request.form.get('other_user_id')
	current_user=g.front_user
	other_user=FrontUser.query.filter_by(id=other_user_id).first()
	current_user.unfollow(other_user)
	db.session.commit()
	return restful.success()



bp.add_url_rule('/regist/',view_func=RegistView.as_view('regist'))
bp.add_url_rule('/login/',view_func=LoginView.as_view('login'))