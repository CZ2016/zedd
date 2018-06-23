#encoding:utf-8

from exts import db
import shortuuid
from werkzeug.security import generate_password_hash,check_password_hash
import enum
from datetime import datetime

class GenderEnum(enum.Enum):
    MALE=1
    FEMALE=2
    SECRET=3
    UNKNOWN=4

class FrontUser(db.Model):
    __tablename__='front_user'
    id=db.Column(db.String(100),primary_key=True,default=shortuuid.uuid)
    telephone=db.Column(db.String(12),nullable=True,unique=True)
    username=db.Column(db.String(100),nullable=False)
    _password = db.Column(db.String(1500), nullable=False)
    email=db.Column(db.String(30),unique=True)
    # realname=db.Column(db.String(50))
    avatar=db.Column(db.String(50))
    # singature=db.Column(db.String(100))
    # gender=db.Column(db.Enum(GenderEnum),default=GenderEnum.UNKNOWN)
    join_time=db.Column(db.DateTime,default=datetime.now)


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


class UserProfileModel(db.Model):
    __tablename__='userprofile'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    realname = db.Column(db.String(50),nullable=True)
    qq=db.Column(db.String(20),nullable=True)
    singature = db.Column(db.String(100))
    gender=db.Column(db.String(10))
    email=db.Column(db.String(20),nullable=True)

    user_id=db.Column(db.String(100),db.ForeignKey('front_user.id'))
    user=db.relationship('FrontUser',backref='profile')



