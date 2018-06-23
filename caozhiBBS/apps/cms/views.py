 #encoding:utf-8

from flask import ( Blueprint,
                    views,
                    render_template,
                    request,
                    session,
                    redirect,
                    url_for,
                    g,
                    jsonify
                    )
from .forms import LoginForm,ResetPwdForm,ResetEmialForm,AddBannersForm,UpdateBannersForm,AddBoardForm,UpdateBoardForm
from .models import CMSUser,CMSPermission
from ..models import BannerModel,BoardModel,PostModel,HighPostModel
from .decorators import LoginRequired,Permission_Required
from exts import db,mail
from utils import restful,zlache
import config
from flask_mail import Message
from flask_paginate import get_page_parameter,Pagination
import string,random,qiniu
from tasks import send_mail


bp=Blueprint('cms',__name__,url_prefix='/cms')

@bp.route('/')
@LoginRequired
def index():
      return render_template('cms/cms_index.html')


@bp.route('/logout/')
@LoginRequired
def logout():
      del session[config.CMS_USER_ID]
      return redirect(url_for('cms.login'))


@bp.route('/banners/')
@LoginRequired
def banners():
    banners=BannerModel.query.order_by(BannerModel.priority.desc()).all()
    return render_template('cms/cms_banners.html',banners=banners)


@bp.route('/abanners/',methods=['POST'])
@LoginRequired
def abanners():
    form=AddBannersForm(request.form)
    if form.validate():
        banner_name=form.banner_name.data
        image_url=form.image_url.data
        link_url=form.link_url.data
        priority=form.priority.data
        banner=BannerModel(banner_name=banner_name,image_url=image_url,link_url=link_url,priority=priority)
        db.session.add(banner)
        db.session.commit()
        return restful.success()
    else:
        return restful.paramserror(message=form.get_errors())


@bp.route('/ubanners/',methods=['POST'])
@LoginRequired
def ubanner():
    form=UpdateBannersForm(request.form)
    if form.validate():
        banner_id=form.banner_id.data
        banner_name = form.banner_name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner=BannerModel.query.get(banner_id)
        if banner:
            banner.banner_name=banner_name
            banner.image_url=image_url
            banner.link_url=link_url
            banner.priority=priority
            db.session.commit()
            return restful.success()
        else:
            return restful.paramserror(message='没有这个轮播图')
    else:
        return restful.paramserror(message=form.get_errors())



@bp.route('/dbanner/',methods=['POST'])
@LoginRequired
def dbanner():
    banner_id=request.form.get('banner_id')
    if not banner_id:
        return restful.paramserror(message='没有这个轮播图')
    else:
        banner=BannerModel.query.get(banner_id)
        if not banner:
            return restful.paramserror(message='没有这个轮播图')
        else:
            db.session.delete(banner)
            db.session.commit()
            return restful.success()





@bp.route('/profile/')
@LoginRequired
def profile():
     return render_template('cms/cms_profile.html')


@bp.route('/posts/')
@LoginRequired
@Permission_Required(CMSPermission.POSTER)
def posts():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * 20
    end = start + 20
    posts = None
    total = 0

    posts = PostModel.query.order_by(PostModel.create_time.desc()).slice(start,end)
    total = PostModel.query.count()
    pagination = Pagination(bs_version=3, page=page, total=total)

    context={
        'posts':posts,
        'pagination':pagination
    }

    return render_template('cms/cms_posts.html',**context)


@bp.route('/highlight/',methods=['POST']) #给帖子加精
@LoginRequired
@Permission_Required(CMSPermission.POSTER)
def highp():
    post_id=request.form.get('post_id')
    if not post_id:
        return restful.paramserror(message='请传入帖子ID')
    else:
        post=PostModel.query.get(post_id)
        if not post:
            return restful.paramserror(message='不存在该帖子')
        highpost=HighPostModel()
        highpost.post=post
        db.session.add(highpost)
        db.session.commit()
        return restful.success()


@bp.route('/unhighlight/',methods=['POST']) #取消加精
@LoginRequired
@Permission_Required(CMSPermission.POSTER)
def unhighp():
    post_id=request.form.get('post_id')
    if not post_id:
        return restful.paramserror(message='请传入帖子ID')
    else:
        post=PostModel.query.get(post_id)
        if not post:
            return restful.paramserror(message='不存在该帖子')
        else:
            highlight=HighPostModel.query.filter_by(post_id=post_id).first()
            db.session.delete(highlight)
            db.session.commit()
            return restful.success()



@bp.route('/comments/')
@LoginRequired
@Permission_Required(CMSPermission.COMMENTER)
def comments():
    return render_template('cms/cms_comments.html')


@bp.route('/boards/')
@LoginRequired
@Permission_Required(CMSPermission.BOARDER)
def boards():
    board_models=BoardModel.query.all()
    context={
        'boards':board_models
    }
    return render_template('cms/cms_boards.html',**context)


@bp.route('/aboards/',methods=['POST'])
@LoginRequired
@Permission_Required(CMSPermission.BOARDER)
def aboards():
    form=AddBoardForm(request.form)
    if form.validate():
        board_name=form.board_name.data
        board=BoardModel(board_name=board_name)
        db.session.add(board)
        db.session.commit()
        return restful.success()
    else:
        return restful.paramserror(message=form.get_errors())


@bp.route('/uboard/',methods=['POST'])
@LoginRequired
@Permission_Required(CMSPermission.BOARDER)
def uaborad():
    form=UpdateBoardForm(request.form)
    if form.validate():
        board_id=form.board_id.data

        name=form.board_name.data
        board=BoardModel.query.get(board_id)
        if board:
            board.board_name=name
            db.session.commit()
            return restful.success()
        else:
            return restful.paramserror(message='没有这个板块')

    else:
        return restful.paramserror(message=form.get_errors())


@bp.route('/dboard/',methods=['POST'])
@LoginRequired
@Permission_Required(CMSPermission.BOARDER)
def dboard():
    board_id=request.form.get('board_id')
    if not board_id:
        return restful.paramserror(message='请传入板块ID')
    board = BoardModel.query.get(board_id)
    if not board:
        return restful.paramserror(message='没有这个板块')
    else:
        db.session.delete(board)
        db.session.commit()
        return restful.success()


@bp.route('/fusers/')
@LoginRequired
@Permission_Required(CMSPermission.FRONTUSER)
def fusers():
    return render_template('cms/cms_fusers.html')


@bp.route('/cusers/')
@LoginRequired
@Permission_Required(CMSPermission.CMSUSER)
def cusers():
    return render_template('cms/cms_cusers.html')



@bp.route('/croles/')
@LoginRequired
@Permission_Required(CMSPermission.ALL_PERMISSION)
def croles():
    return render_template('cms/cms_croles.html')


@bp.route('/email_captcha/')
    #/email_captcha/?email=xxx@qq.com
def email_captcha():
    email=request.args.get('email')
    if not email:
        return restful.paramserror('请传递邮箱参数')
    else:
        source=list(string.ascii_letters)
        source.extend(map(lambda x:str(x),range(10)))
        captcha="".join(random.sample(source,6))
        # message=Message('华山论坛验证码',recipients=[email],body='您的验证码是%s'%(captcha))
        # try:
        #     mail.send(message)
        # except:
        #     return restful.server_error()
        send_mail.delay('华山论坛验证码',recipients=[email],body='您的验证码是%s'%(captcha))
        zlache.set(email,captcha)
        return restful.success()

    # 如果有邮箱，就给这个邮箱发送邮件


@bp.route('/email/')  #测试用邮箱
def send_email():
    message=Message('知了课堂邮件发送',recipients=['13732913015@163.com'],body='测试')
    mail.send(message)
    return 'success'


class LoginView(views.MethodView):
     def get(self,message=None):
          return render_template('cms/cms_login.html',message=message)

     def post(self):
          form=LoginForm(request.form)
          if form.validate():
               email=form.email.data
               password=form.password.data
               remember=form.remember.data
               user=CMSUser.query.filter_by(email=email).first()
               if user and user.check_password(password):
                    session[config.CMS_USER_ID]=user.id
                    if remember:
                         # 如果设置session.permanent=True,那么过期时间就是31天
                         session.permanent=True
                    return redirect(url_for('cms.index'))
               else:
                    return self.get(message='邮箱或密码错误')


          else:
               message=form.get_errors()
               return self.get(message=message)

class ResetPwdView(views.MethodView):
    decorators = [LoginRequired]
    def get(self):
        return render_template('cms/cms_resetpwd.html')

    def post(self):
        form=ResetPwdForm(request.form)
        if form.validate():
            oldpwd=form.oldpwd.data
            newpwd=form.newpwd.data
            user=g.cms_user
            if user.check_password(oldpwd):
                user.password=newpwd
                db.session.commit()
                # {'code':200,message=''}
                return restful.success()
            else:
                return restful.paramserror('旧密码错误')

        else:
            return restful.paramserror(message=form.get_errors())

class ResetEmailView(views.MethodView):
    decorators =[LoginRequired]
    def get(self):
        return render_template('cms/cms_resetemail.html')

    def post(self):
        form=ResetEmialForm(request.form)
        if form.validate():
            email=form.email.data
            g.cms_user.email=email
            db.session.commit()
            return restful.success()
        else:
            return restful.paramserror(form.get_errors())



bp.add_url_rule('/login/',view_func=LoginView.as_view('login'))
bp.add_url_rule('/resetpwd/',view_func=ResetPwdView.as_view('resetpwd'))
bp.add_url_rule('/resetemail/',view_func=ResetEmailView.as_view('resetemail'))
