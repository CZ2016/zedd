#encoding: utf-8

from urllib.parse import urlparse,urljoin
from flask import request

def is_safe_url(target):
    ref_url = urlparse(request.host_url) #对url进行解析，分成域名部分，path部分和参数部分
    test_url = urlparse(urljoin(request.host_url, target)) #对传进来的target进行组装并解析
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc
