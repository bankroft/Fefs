# coding:utf-8
import requests
from hashlib import md5


tmp = open('./raccount.txt', 'r').read()
username = tmp.split('|')[0].strip()
passwd = md5(tmp.split('|')[1].strip().encode()).hexdigest()

rk_post_data = {
    'username': username,
    'password': passwd,
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
        return False
    return res['Result']


ocr_url = 'https://recognition.image.myqcloud.com/ocr/bizlicense'
ocr_headers = {
    'host': 'recognition.image.myqcloud.com'
}


def ocr(filename):
    pass


def auth_ocr():
    pass

