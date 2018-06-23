 #encoding:utf-8

from flask_script import Manager
from flask_migrate import MigrateCommand,Migrate
from exts import db
from apps.cms import models as cms_models
from apps.front import models as front_models
from bbs import create_app
from apps.models import BannerModel,BoardModel,PostModel

app=create_app()

CMSUser=cms_models.CMSUser
CMSRole=cms_models.CMSRole
FrontUser=front_models.FrontUser
CMSPermission=cms_models.CMSPermission
manager = Manager(app)
Migrate(app,db)
manager.add_command('db',MigrateCommand)

@manager.option('-u','--username',dest='username')
@manager.option('-p','--password',dest='password')
@manager.option('-e','--email',dest='email')

def create_cms_user(username,password,email):
     user=CMSUser(username=username,password=password,email=email)
     db.session.add(user)
     db.session.commit()
     print('cms用户添加成功')


@manager.command
def create_role():
     #1. 访问者
     visitor=CMSRole(name='访问者',desc='只能看相关信息，不能修改')
     visitor.permissions=CMSPermission.VISITOR

     #2. 运营角色,可以修改个人信息，管理帖子评论
     operator=CMSRole(name='运营人员',desc='可以修改个人信息，管理帖子评论,管理前台用户')
     operator.permissions=CMSPermission.VISITOR|CMSPermission.POSTER|CMSPermission.COMMENTER|CMSPermission.FRONTUSER

     #3. 管理员(拥有绝大部分权限)
     admin=CMSRole(name='管理员',desc='拥有本系统所有权限')
     admin.permissions=CMSPermission.VISITOR|CMSPermission.FRONTUSER|CMSPermission.COMMENTER|CMSPermission.POSTER|CMSPermission.BOARDER|CMSPermission.CMSUSER|CMSPermission.BOARDER

     # 4.开发者权限
     developer=CMSRole(name='开发者',desc='开发人员专用角色')
     developer.permissions=CMSPermission.ALL_PERMISSION

     db.session.add_all([visitor,operator,admin,developer])
     db.session.commit()


@manager.option('-t','--telephone--',dest='telephone')
@manager.option('-u','--username--',dest='username')
@manager.option('-p','--password--',dest='password')
def create_front_user(telephone,username,password):
     user=FrontUser(telephone=telephone,username=username,password=password)
     db.session.add(user)
     db.session.commit()
     print('前端用户添加成功')



@manager.option('-e','--email',dest='email')
@manager.option('-n','--name',dest='name')
def add_user_to_role(email,name):
     user=CMSUser.query.filter_by(email=email).first()
     if user:
          role=CMSRole.query.filter_by(name=name).first()
          if role:
               role.users.append(user)
               db.session.commit()
               print('用户添加到角色成功')
          else:
               print('不存在这个角色%s'%role)
     else:
          print('不存在这个用户%s'%email)



@manager.command
def test_permission():
     user=CMSUser.query.first()
     if user.is_developer:
          print('该用户是开发者')
     else:
          print('该用户不是开发者')


# 创建测试帖子命令
@manager.command
def create_test_post():
     for x in range(200):
          title='标题%s'%x
          content='内容:%s'%x
          board=BoardModel.query.get(11)
          author=FrontUser.query.first()
          print(author)
          post=PostModel(title=title,content=content)
          post.board=board
          post.author=author
          db.session.add(post)
          db.session.commit()
     print('测试帖子添加成功')


if __name__=='__main__':
     manager.run()