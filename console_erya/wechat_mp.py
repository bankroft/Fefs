# coding:utf-8
import os
import re
import sys
import threading
import time
from random import choice
from xml.dom import minidom

from logzero import logger

import itchat

try:
    from .config import QuestionConfig as qc
    wechat_mps = qc.wechat_mp  # ['校查']
except ImportError:
    wechat_mps = ['校查']


r = '[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）“”]+'
r2 = '(?<!/)&'

# 微信公众号

# 收到的消息
messages = []
# 当前登陆状态
status = False
# 配置的微信公众号itchat中username
target = []


def login_callback():
    global status
    status = True


def exit_callback():
    global status
    status = False


def init_wechat():
    global target
    itchat.auto_login(hotReload=True, exitCallback=exit_callback,
                      loginCallback=login_callback)
    for x in wechat_mps:
        res = itchat.search_mps(x)
        if len(res) == 1:
            target.append(res[0]['UserName'])
        elif len(res) == 0:
            print('请先关注所配置的微信公众号[{0}], 如已关注请反馈该BUG'.format(x))
            os.system('pause')
            sys.exit(0)
        else:
            print('微信公众号[{0}]存在多个'.format(x))
            os.system('pause')
            sys.exit(0)


@itchat.msg_register(itchat.content.SHARING, isMpChat=True)
def handle_receive_msg(msg):
    global messages
    # print(msg)
    try:
        answer = minidom.parseString(msg['Content'].replace(
            '\x01', '&')).getElementsByTagName('des')[0].firstChild.nodeValue
        if answer:
            messages.append(answer)
    except:
        pass


def search(title):
    global messages
    if not status:
        print('微信可能掉了，重开程序')
        sys.exit(0)
    for _ in range(10):
        itchat.send_msg(title, choice(target))
        time.sleep(5)
        answer = None
        for tmp in messages:
            if similarity(re.sub(r, "", tmp.split('\n')[0].strip()), re.sub(r, "", title)) > 0.75:
                answer = tmp.split('\n')[1].strip().strip('参考答案：').strip()
                while True:
                    try:
                        messages.remove(tmp)
                    except ValueError:
                        break
                break
        if answer:
            return re.split(r2, answer)
    return False


def similarity(a, b):
    lena = len(a)
    lenb = len(b)
    if lena == 0 or lenb == 0:
        return 0
    c = [[0 for _ in range(lenb+1)] for _ in range(lena+1)]
    for i in range(lena):
        for j in range(lenb):
            if a[i] == b[j]:
                c[i+1][j+1] = c[i][j]+1
            elif c[i+1][j] > c[i][j+1]:
                c[i+1][j+1] = c[i+1][j]
            else:
                c[i+1][j+1] = c[i][j+1]
    return float(c[lena-1][lenb-1])/max(lena, lenb)


init_wechat()
# itchat.start_receiving()
itchat.run(blockThread=False, debug=False)
