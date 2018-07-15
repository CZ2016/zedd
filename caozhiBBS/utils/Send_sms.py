#-*- coding:utf-8 -*-
# Desc: 短信http接口的python代码调用示例


# 网站的代码是py2的，我把导入的包改成py3的了
import http.client
from urllib import parse
import json
import requests


#请求地址请只要域名就可以了，应该就是这个！
host = "http://smssh1.253.com/"
 
#端口号
port = 80
 
#版本号
version = "v1.1"
 
#查账户信息的URI
balance_get_uri = "/msg/balance/json"
 
#智能匹配模版短信接口的URI
sms_send_uri = "/msg/send/json"
 
#创蓝账号
# account  = "N7071267"
account  = "CN2363121"

#创蓝密码
# password = "CHUANGlan253"
password = "6dExQBDloU600b"


# 发送短信接口

def send_sms(phone,text):
    """
    能用接口发短信
    """
    params = {'account': account, 'password' : password, 'msg':parse.quote(text), 'phone':phone, 'report' : \
        'false'}
    params=json.dumps(params)
    # 这地方勇哥修改成requests了，网站的源代码那种方法一直报错！这个没问题！
    headers = {"Content-type": "application/json"}
    res = requests.post(host+sms_send_uri,headers=headers,data=params)
    return res.json()

