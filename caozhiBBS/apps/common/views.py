 #encoding:utf-8

from flask import Blueprint,request,make_response,jsonify
from utils.captcha import Captcha
from utils import Send_sms,restful,zlache
from .forms import SMSCaptchaForm
from utils import Send_sms
from io import BytesIO
import qiniu
from tasks import send_sms_captcha

bp = Blueprint('common', __name__, url_prefix='/c')

# 未进行加密
# @bp.route('/sms_captcha/')
# def sms_captcha():
#      telephone=request.args.get('telephone')
#      if not telephone:
#           return restful.paramserror(message='请输入手机号')
#
#      captcha=Captcha.gene_text(number=4)
#      if Send_sms.send_sms(telephone,text=captcha):
#           return restful.success()
#      else:
#           return restful.paramserror(message='短信验证码发送失败')

@bp.route('/sms_captcha/',methods=['POST']) #把方法改成post请求
     # ?telephone=xxx
     # /c/sms_captcha/xxx
def sms_captcha():
     # 前台要发送过来的数据:
     # telephone
     # timestamp
     # md5(ts+telephone+salt)
     form=SMSCaptchaForm(request.form)
     if form.validate():
          telephone=form.telephone.data
          captcha=Captcha.gene_text(number=4)
          send_sms_captcha.delay(telephone,captcha) #使用celery异步发送
          # if Send_sms.send_sms(telephone,text=captcha):
          zlache.set(telephone,captcha,timeout=120)
          return restful.success()
          # else:
          #      return restful.paramserror(message='短信验证码发送失败')
     else:
          return restful.paramserror(message='参数错误')


@bp.route('/captcha/')
def graph_captcha():
    # 获取验证码,在浏览器中不能直接返回image对象,需要转化为二进制流的数据,才能识别
    text,image=Captcha.gene_graph_captcha()
    zlache.set(text.lower(),text.lower(),timeout=120)
    # print(zlache.get(text.lower()))
    # BytesIO:自截留
    out=BytesIO()
    image.save(out,'png')
    # 文件流的指针要放到开始的位置
    out.seek(0)
    resp=make_response(out.read())
    resp.content_type='image/png'
    return resp


# 七牛存储图片文件
@bp.route('/uptoken/')
def uptoken():
	access_key='-EknLGbZHMgU1lPakA5tPL_0fshHPlOVO3gQryRp'
	secret_key='AvJkiEXqYUQ80Znyrvo2JJ8UKV-K2Uc_XRFHtq_n'
	q=qiniu.Auth(access_key,secret_key)

	bucket='zed1993'
	token=q.upload_token(bucket)

	return jsonify({'uptoken':token})   #key值必须为uptoken