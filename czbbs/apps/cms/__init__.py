#encoding:utf-8

from .views import bp
import apps.cms.hooks  #不能采用import hooks 这种方式，而是需要层层导入