#encoding:utf-8
from exts import db
from datetime import datetime




class BannerModel(db.Model):
	__tablename__='banner'
	id=db.Column(db.Integer,primary_key=True,autoincrement=True)
	banner_name=db.Column(db.String(250),nullable=False)
	image_url=db.Column(db.String(250),nullable=False)
	link_url=db.Column(db.String(250),nullable=False)
	priority=db.Column(db.Integer,default=0)
	create_time=db.Column(db.DateTime,default=datetime.now)


class BoardModel(db.Model):
	__tablename__='board'
	id=db.Column(db.Integer,primary_key=True,autoincrement=True)
	board_name=db.Column(db.String(20),nullable=False)
	create_time=db.Column(db.DateTime,default=datetime.now)


class PostModel(db.Model):
	__tablename__='post'
	id=db.Column(db.Integer,primary_key=True,autoincrement=True)
	title=db.Column(db.String(200),nullable=False)
	content=db.Column(db.Text,nullable=False)
	create_time=db.Column(db.DateTime,default=datetime.now)
	hit=db.Column(db.Integer, default=1)
	comment_num=db.Column(db.Integer,nullable=True,default=0)

	author_id=db.Column(db.String(100),db.ForeignKey('front_user.id'),nullable=False)
	author=db.relationship('FrontUser',backref='posts')

	board_id=db.Column(db.Integer,db.ForeignKey('board.id'))
	board=db.relationship('BoardModel',backref='posts')


class  HighPostModel(db.Model):
	__tablename__='highlight_post'
	id=db.Column(db.Integer,primary_key=True,autoincrement=True)
	post_id=db.Column(db.Integer,db.ForeignKey('post.id',ondelete='CASCADE'))
	create_time=db.Column(db.DateTime,default=datetime.now)
	post=db.relationship('PostModel',backref='highlight')





class CommentModel(db.Model):
	__tablename__='comment'
	id=db.Column(db.Integer,primary_key=True,autoincrement=True)
	content=db.Column(db.Text,nullable=False)
	create_time=db.Column(db.DateTime,default=datetime.now)

	post_id=db.Column(db.Integer,db.ForeignKey('post.id',ondelete='CASCADE'))
	author_id=db.Column(db.String(100),db.ForeignKey('front_user.id'))

	post=db.relationship('PostModel',backref='comments')
	author=db.relationship('FrontUser',backref='comments')