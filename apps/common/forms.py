 #encoding:utf-8
from apps.forms import BaseForm
from wtforms import StringField
from wtforms.validators import regexp,InputRequired
import hashlib

class SMSCaptchaForm(BaseForm):
    telephone = StringField(validators=[regexp(r'1[34578]\d{9}')])
    timestamp = StringField(validators=[regexp(r'\d{13}')])
    sign = StringField(validators=[InputRequired()])
    salt = 'caozhi1993'
    def validate(self):
        result = super(SMSCaptchaForm, self).validate()
        if not result:
            return False
        telephone = self.telephone.data
        timestamp = self.timestamp.data
        sign = self.sign.data
         # md5(timestamp+telephone+salt)
         # md5必须要传一个bytes类型的字符串进去
        sign2=hashlib.md5((timestamp+telephone+self.salt).encode('utf-8')).hexdigest()
        if sign==sign2:
            return True
        else:
            return False