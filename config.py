#encoding:utf-8

import os

HOSTNAME='127.0.0.1'
PORT='3306'
DATABASE='czbbs'
USERNAME='root'
PASSWORD='caozhi1993'

DB_URI="mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=utf8".format(
    username=USERNAME,password=PASSWORD,host=HOSTNAME,port=PORT,db=DATABASE)

SQLALCHEMY_DATABASE_URI=DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS=False

debug=True

# SECRET_KEY=os.urandom(24)
SECRET_KEY='asdfv9ioiujj434'

CMS_USER_ID='cmscao'
FRONT_USER_ID='frontcao'




# 图片上传到七牛云配置信息
UEDITOR_UPLOAD_PATH =os.path.join(os.path.dirname(__file__),'images')
UEDITOR_UPLOAD_TO_QINIU = True
UEDITOR_QINIU_ACCESS_KEY = "-EknLGbZHMgU1lPakA5tPL_0fshHPlOVO3gQryRp"
UEDITOR_QINIU_SECRET_KEY = "AvJkiEXqYUQ80Znyrvo2JJ8UKV-K2Uc_XRFHtq_n"
UEDITOR_QINIU_BUCKET_NAME = "zed1993"
UEDITOR_QINIU_DOMAIN = "http://pa97eo8ux.bkt.clouddn.com/"

#发送者邮箱服务器地址
#TLS:端口号587
#SSL:端口号465
#QQ邮箱不支持非加密方式发送邮件
# MAIL_USE_SSL : default False
MAIL_SERVER ="smtp.qq.com"
MAIL_PORT =587
MAIL_USE_TLS =True
MAIL_USERNAME='471794267@qq.com'
MAIL_PASSWORD ='cqcincfobmnhbjca'
MAIL_DEFAULT_SENDER ='471794267@qq.com'



# flask-paginate的相关配置
PER_PAGE=10


ALLOWED_HOST='192.168.0.100'

# 阿里大鱼相关配置
# ALIDAYU_APP_KEY='LTAIY5tfW7WLdsns'
# ALIDAYU_APP_SECRET='XJNZSkV5fAOZegqSag5jsybOEDxVZk'
# ALIDAYU_SIGN_NAME='子建论坛'
# ALIDAYU_TEMPLATE_CODE='SMS_136865516'

# celery配置
CELERY_RESULT_BACKEND='redis://:caozhi1993@127.0.0.1/1'
CELERY_BROKER_URL='redis://:caozhi1993@127.0.0.1/1'
