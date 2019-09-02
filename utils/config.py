# coding:utf-8
import configparser
from hashlib import md5
from os import getcwd
from pathlib import Path

conf = configparser.ConfigParser()
conf.read(str(Path(getcwd()) / 'config.ini'), encoding='utf-8')

# 若快用户
rk_username = conf.get('User', 'rk_username', fallback=False)

# 若快密码
rk_password = conf.get('User', 'rk_password', fallback=False)

# if rk_password:
#     rk_password = md5(rk_password.strip().encode()).hexdigest()
