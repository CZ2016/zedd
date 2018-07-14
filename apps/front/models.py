#encoding:utf-8

from exts import db
import shortuuid
from werkzeug.security import generate_password_hash,check_password_hash
import enum
from datetime import datetime
from ..models import PostModel

class GenderEnum(enum.Enum):
    MALE=1
    FEMALE=2
    SECRET=3
    UNKNOWN=4



class Follow(db.Model):
    __tablename__='follow'
    follower_id=db.Column(db.String(100),db.ForeignKey('front_user.id'),primary_key=True)
    followed_id=db.Column(db.String(100),db.ForeignKey('front_user.id'),primary_key=True)
    create_time=db.Column(db.DateTime,default=datetime.now)

class FrontUser(db.Model):
    __tablename__='front_user'
    id=db.Column(db.String(100),primary_key=True,default=shortuuid.uuid)
    telephone=db.Column(db.String(12),nullable=True,unique=True)
    username=db.Column(db.String(100),nullable=False)
    _password = db.Column(db.String(1500), nullable=False)
    email=db.Column(db.String(30),unique=True)
    realname=db.Column(db.String(50))
    avatar=db.Column(db.String(100))
    singature=db.Column(db.String(100))
    gender = db.Column(db.String(10))
    join_time=db.Column(db.DateTime,default=datetime.now)

    # 关注者和粉丝
    followed=db.relationship('Follow',foreign_keys=[Follow.follower_id],backref=db.backref('follower',lazy='joined'),
                             lazy='dynamic',cascade='all,delete-orphan')
    follower = db.relationship('Follow', foreign_keys=[Follow.followed_id],
                               backref=db.backref('followed', lazy='joined'),
                               lazy='dynamic', cascade='all,delete-orphan')

    def __init__(self,*args,**kwargs):
        if 'password' in kwargs:
            self.password=kwargs.get('password')
            kwargs.pop('password')
        super(FrontUser, self).__init__(*args,**kwargs)




    @property
    def password(self):
        return self._password
    @password.setter
    def password(self,newpassword):
        self._password=generate_password_hash(newpassword)

    def check_password(self,rawpwd):
        return check_password_hash(self._password,rawpwd)



    # 关注关系的辅助方法

    def follow(self, user):
        if not self.is_following(user):
            f=Follow(follower=self,followed=user)
            db.session.add(f)

    def unfollow(self, user):
        f = self.followed.filter_by(followed_id=user.id).first()
        if f:
            self.followed.remove(f)

    def is_following(self, user):
        if user.id is None:
            return False
        return self.followed.filter_by(
            followed_id=user.id).first() is not None

    def is_followed_by(self, user):
        if user.id is None:
            return False
        return self.followers.filter_by(
            follower_id=user.id).first() is not None

    @property
    def followed_posts(self):
        return PostModel.query.join(Follow,Follow.followed_id==PostModel.author_id).filter(Follow.follower_id==self.id)

# class UserProfileModel(db.Model):
#     __tablename__='userprofile'
#     id=db.Column(db.Integer,primary_key=True,autoincrement=True)
#     realname = db.Column(db.String(50),nullable=True)
#     qq=db.Column(db.String(20),nullable=True)
#     singature = db.Column(db.String(100))
#     gender=db.Column(db.String(10))
#     email=db.Column(db.String(20),nullable=True)
#
#     user_id=db.Column(db.String(100),db.ForeignKey('front_user.id',ondelete='CASCADE'),unique=True)
#     user=db.relationship('FrontUser',backref='profile',uselist=False)



