# coding:utf-8
import requests
import rk_user

rk_post_data = {
    'username': rk_user.username,
    'password': rk_user.passwd,
    'typeid': 3040,
    'timeout': 60,
    'softid': '107206',
    'softkey': '8114ba5ebe954375809d65b1c3e9b4cd'
}
rk_url = 'http://api.ruokuai.com/create.json'


def rk_code(file_name):
    files = {'image': ('test.jpg', open(file_name, 'rb').read())}
    res = requests.post(rk_url, rk_post_data, files=files).json()
    if 'Error_Code' in res.keys():
        return False
    return res['Result']