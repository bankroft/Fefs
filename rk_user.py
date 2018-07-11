# coding:utf-8
from hashlib import md5


tmp = open('raccount.txt', 'r').read()
username = tmp.split('|')[0].strip()
passwd = md5(tmp.split('|')[1].strip().encode()).hexdigest()
