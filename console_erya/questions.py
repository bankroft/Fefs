# coding:utf-8
import re
import demjson
import requests
from hashlib import md5
from .config import QuestionConfig as qc


def wechat_search(title):
    return False


if len(qc.wechat_mp) >= 1:
    # from .wechatsearch import search
    from .wechat_mp import search
    wechat_search = search
string_enc = '-b?M#JvMg2y3$JMk'
table = None
r = '(?<!/)&'


"""
返回码
100 正常
101 token频率限制
102 未查到
404 未知错误
"""


def query_http_server(op, defalut=True, **kwargs):
    if qc.questions_request_query and qc.questions_request_update:
        if op == 'update':
            md = md5()
            md.update((kwargs['title']+kwargs['answer']+string_enc).encode())
            try:
                tmp = demjson.decode(requests.post(qc.questions_request_update, data={'title': kwargs['title'], 'answer': kwargs['answer'], 'enc': md.hexdigest()}).text, encoding='utf-8')
            except:
                return False, 404, '未知错误'
            if tmp['code'] == 100:
                return True, 100, ''
        elif op == 'query':
            if defalut:
                if qc.token:
                    try:
                        i = requests.get(qc.questions_request_query_token, params={'title': kwargs['title'], 'token': qc.token})
                        if i.status_code == 403:
                            return False, 403, 'token频率已达上限'
                        elif i.status_code == 200:
                            i = demjson.decode(i.text, encoding='utf-8')
                            if i['code'] == 100:
                                # sure = True
                                if kwargs['test_type'] == '判断题':
                                    if isinstance(i['data'], list):
                                        i['data'] = i['data'][0]
                                    if i['data'].lower() in ['√', '正确', 'true']:
                                        return True, 100, True
                                    else:
                                        return True, 100, False
                                else:
                                    return True, 100, re.split(r, i['data']), 'token'
                        # else:
                        #     return False, 404, '未知错误'
                    except:
                        pass
                else:
                    md = md5()
                    md.update((kwargs['title'] + string_enc).encode())
                    # sure = False
                    try:
                        i = requests.get(qc.questions_request_query_token, params={'title': kwargs['title'], 'token': qc.token})
                        if i.status_code == 200:
                            i = demjson.decode(i.text, encoding='utf-8')
                            if i['code'] == 100:
                                # sure = True
                                if kwargs['test_type'] == '判断题':
                                    if isinstance(i['data'], list):
                                        i['data'] = i['data'][0]
                                    if i['data'].lower() in ['√', '正确', 'true']:
                                        return True, 100, True
                                    else:
                                        return True, 100, False
                                else:
                                    return True, 100, re.split(r, i['data']), 'open'
                        # else:
                        #     return False, 404, '未知错误'
                    except:
                        pass
            tmp = wechat_search(kwargs['title'])
            if tmp:
                if kwargs['test_type'] == '判断题':
                    if isinstance(tmp, list):
                        tmp = tmp[0]
                    if tmp in ['√', '正确', 'true']:
                        return True, 100, True
                    else:
                        return True, 100, False
                else:
                    return True, 100, tmp, 'wechat_mp'
            return False, 102, '未查到', ' '
        elif op == 'addtitle':
            md = md5()
            md.update((kwargs['title']+string_enc).encode())
            try:
                requests.post(qc.questions_request_update, data={'title': kwargs['title'], 'enc': md.hexdigest()})
            except:
                pass
        return False
    else:
        raise ValueError('查询url配置错误')
