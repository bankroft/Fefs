# coding:utf-8
from xml.dom import minidom
import re
from random import choice
from wxpy import Bot, ensure_one, SHARING
import threading
from .config import QuestionConfig as qc
import time
from logzero import logger
import sys
import os
r = '[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）“”]+'
r2 = '(?<!/)&'

messages = []


# def qrcode_wechat(uuid, status, qrcode):
#     with open('wxlogin.png', 'wb') as f:
#         f.write(qrcode)


# bot = Bot(cache_path=True, console_qr=1)
bot = Bot(cache_path=True)
try:
    target = [ensure_one(bot.search(x)) for x in qc.wechat_mp]
except ValueError:
    print('请先关注config.ini文件里所配置的wechat公众号，如已关注请反馈该BUG')
    os.system('pause')
    sys.exit(0)


def run_wechat():
    @bot.register(target, SHARING)
    def handle_receive_msg(msg):
        global messages
        try:
            answer = minidom.parseString(msg.raw['Content'].replace('\x01', '&')).getElementsByTagName('des')[0].firstChild.nodeValue
            print(answer)
            if answer:
                messages.append(answer)
        except:
            pass
    # embed()
    t = threading.Thread(target=bot.join)
    t.setDaemon(True)
    t.start()


def search(title):
    global messages
    try:
        choice(target).send_msg(title)
    except IndexError:
        # 修改
        logger.error('微信可能掉了，重开程序')
        sys.exit(1)
    for _ in range(3):
        time.sleep(5)
        answer = None
        for tmp in messages:
            if similarity(re.sub(r, "", tmp.split('\n')[0].strip()), re.sub(r, "", title)) > 0.75:
                answer = tmp.split('\n')[1].strip().strip('参考答案：').strip()
                break
        if answer:
            return re.split(r2, answer)
    return False


run_wechat()


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
