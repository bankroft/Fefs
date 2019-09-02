# coding:utf-8
from hashlib import md5

import requests

from .config import rk_password, rk_username

rk_bool = False
if rk_username and rk_password:
    rk_bool = True

rk_post_data = {
    'username': rk_username,
    'password': rk_password,
    'typeid': 3040,
    'timeout': 60,
    'softid': '107227',
    'softkey': '28e167d702f84f14b9cead7aa028eaf3'
}
rk_url = 'http://api.ruokuai.com/create.json'


def rk_code(file_name):
    files = {'image': ('test.jpg', open(file_name, 'rb').read())}
    res = requests.post(rk_url, rk_post_data, files=files).json()
    if 'Error_Code' in res.keys():
        return 'False'
    return res['Result']


ocr_url = 'https://recognition.image.myqcloud.com/ocr/bizlicense'
ocr_headers = {
    'host': 'recognition.image.myqcloud.com'
}


def ocr(filename):
    pass


def auth_ocr():
    pass
