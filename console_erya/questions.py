# coding:utf-8
import re
import demjson
import requests
from hashlib import md5
from .config import questions_request_update, questions_request_query, wechat_mp


def wechat_search(title):
    return False


if len(wechat_mp) >= 1:
    from .wechatsearch import search
    wechat_search = search
string_enc = '-b?M#JvMg2y3$JMk'
table = None
r = '(?<!/)&'


# def query_mongodb(op, **kwargs):
#     """
#     暂不考虑多选题
#     :param op:
#     :param kwargs:
#     :return:
#     """
#     if not table:
#         raise ValueError('数据库参数配置出错')
#     if op == 'update':
#         table.update_one(filter={'title': kwargs['title']}, update={'$set': {'answer': kwargs['answer']}}, upsert=True)
#     elif op == 'query':
#         tmp = table.find_one({'title': kwargs['title']})
#         if tmp and ('answer' in tmp.keys()):
#             if kwargs['test_type'] != '判断题':
#                 return re.split(r, tmp['answer'])
#             else:
#                 if tmp['answer'].upper() in ['√', '正确', 'TRUE', ]:
#                     return True
#                 else:
#                     return False
#         else:
#             return False


def query_http_server(op, **kwargs):
    if questions_request_query and questions_request_update:
        if op == 'update':
            md = md5()
            md.update((kwargs['title']+kwargs['answer']+string_enc).encode())
            try:
                tmp = demjson.decode(requests.post(questions_request_update, data={'title': kwargs['title'], 'answer': kwargs['answer'], 'enc': md.hexdigest()}).text, encoding='utf-8')
            except:
                return False
            if tmp['code'] == 100:
                return True
        elif op == 'query':
            md = md5()
            md.update((kwargs['title'] + string_enc).encode())
            sure = False
            try:
                i = demjson.decode(requests.get(questions_request_query, params={'title': kwargs['title'], 'enc': md.hexdigest()}).text, encoding='utf-8')
                if i['code'] == 100:
                    sure = True
                    if kwargs['test_type'] == '判断题':
                        if isinstance(i['data'], list):
                            i['data'] = i['data'][0]
                        if i['data'].lower() in ['√', '正确', 'true']:
                            return True
                        else:
                            return False
                    else:
                        return re.split(r, i['data'])
            except:
                pass
            if not sure:
                tmp = wechat_search(kwargs['title'])
                if tmp:
                    if kwargs['test_type'] == '判断题':
                        if isinstance(tmp, list):
                            tmp = tmp[0]
                        if tmp in ['√', '正确', 'true']:
                            return True
                    else:
                        return tmp
                return False
        elif op == 'addtitle':
            md = md5()
            md.update((kwargs['title']+string_enc).encode())
            try:
                requests.post(questions_request_update, data={'title': kwargs['title'], 'enc': md.hexdigest()})
            except:
                pass
        return False
    else:
        raise ValueError('查询url配置错误')
