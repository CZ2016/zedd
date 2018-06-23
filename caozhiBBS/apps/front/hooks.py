#encoding:utf-8
from .views import bp
import config
from .models import FrontUser,UserProfileModel
from flask import g,session
from flask import render_template

@bp.before_request
def before_request():
	if config.FRONT_USER_ID in session:
		front_id=session.get(config.FRONT_USER_ID)
		user=FrontUser.query.get(front_id)
		user_profile=UserProfileModel.query.filter_by(user_id=front_id).first()
		if user:
			g.front_user=user
			g.front_profile=user_profile


@bp.errorhandler
def page_not_found():
	return render_template('front/front_404.html'),404


