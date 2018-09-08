# coding:utf-8
from flask import Flask
from console_erya.config import ip, port, debug
from flask_restful import reqparse, Api, Resource
from console_erya.global_var import globalvar
from console_erya import console
from flask_cors import *
from utils.util import rk_code
import shutil
import os
import time
import re

r = '(?<!/)&'
app = Flask(__name__)
CORS(app, supports_credentials=True)
api = Api(app)

__author__ = 'bankroft'
__version__ = '0.60 debug'
__blog__ = 'https://www.bankroft.cn'
__web__ = 'https://www.bankroft.cn/erya-console'


class Main(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('op', type=str, location='args')
        parser.add_argument('instance_name', type=str, location='args')
        parser.add_argument('school_name', type=str, location='args')
        # parser.add_argument('get_ver_code', type=bool, location='args')
        parser.add_argument('author', type=str, location='args')
        args = parser.parse_args()
        con = globalvar.get(args['instance_name'])
        if args['author']:
            return [{'author': __author__}]
        if args['op'] == 'search_school':
            tmp = con.search_school(args['school_name'])
            return [{'status': 100, 'message': '', 'data': tmp}]
        elif args['op'] == 'get_course':
            if con.status['login']:
                tmp = con.get_course()
                return [{'status': 100, 'message': '', 'data': tmp}]
        return [{'status': 404, 'message': '参数错误'}]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('index', type=int, location='form')
        parser.add_argument('instance_name', type=str, location='form')
        parser.add_argument('student_num', type=str, location='form')
        parser.add_argument('pwd', type=str, location='form')
        parser.add_argument('ver_code', type=str, location='form')
        parser.add_argument('op', type=str, location='form')
        args = parser.parse_args()
        con = globalvar.get(args['instance_name'])
        if args['op'] == 'init':
            if globalvar.get(args['instance_name']):
                con.quit()
            globalvar.add({args['instance_name']: console.Console()})
            return [{'status': 100, 'message': ''}]
        elif args['op'] == 'select_school':
            if args['index'] is not None:
                if con.status['search_school'] and not con.status['login']:
                    return [{'status': 100, 'message': '', 'data': con.select_school(args['index'])}]
                else:
                    return [{'status': 404, 'message': '先搜索学校'}]
        elif args['op'] == 'login':
            # print(con.get_login_ver_code())
            # ver_code = args['ver_code']
            # ver_code = rk_code(con.get_login_ver_code())
            ver_code = rk_code(con.get_login_ver_code(refresh=True))
            if args['student_num'] and args['pwd'] and ver_code:
                tmp = con.login(args['student_num'], args['pwd'], ver_code)
                while tmp[0] == '验证码错误':
                    time.sleep(1)
                    ver_code = rk_code(con.get_login_ver_code(refresh=True))
                    tmp = con.login(args['student_num'], args['pwd'], ver_code)
                if tmp[1]:
                    return [{'status': 100, 'message': '', 'data': tmp[0]}]
                else:
                    return [{'status': 404, 'message': tmp[0]}]
        elif args['op'] == 'browse_watch':
            if args['index'] is not None:
                return [{'status': 100, 'message': '', 'data': con.browse_watch(args['index'])}]
        return [{'status': 404, 'message': '参数错误'}]


class GetInfo(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('start', type=int, location='args')
        parser.add_argument('status', type=str, location='args')
        args = parser.parse_args()
        if args['status']:
            return [{'status': 100, 'message': '正在运行'}]
        if args['start']:
            start = int(args['start'])
            data = []
            shutil.copyfile('erya.log', 'erya.log.tmp')
            with open('erya.log.tmp', encoding='utf-8') as f:
                for x in f.readlines():
                    try:
                        t = time.mktime(time.strptime(x.split(',')[0], '%Y-%m-%d %H:%M:%S'))
                        if t > start:
                            data.append(re.split(r, x)[1:])
                    except:
                        continue
            os.remove('erya.log.tmp')
            return [{'status': 100, 'message': '', 'data': data}]
        else:
            return [{'status': 404, 'message': '参数错误'}]


class RESTExam(Resource):
    ins = None

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('init', type=str, location='args')
        parser.add_argument('start', type=str, location='args')
        args = parser.parse_args()
        if args['init'] is not None:
            globalvar.add({'exam': console.Exam()})
            return [{'status': 100, 'message': ''}]
        elif args['start'] is not None:
            if globalvar.get('exam'):
                globalvar.get('exam').start()
                return [{'status': 100, 'message': ''}]
        return [{'status': 404, 'message': '参数错误'}]


api.add_resource(Main, '/rest_console')
# 参数待定
api.add_resource(GetInfo, '/getinfo')
api.add_resource(RESTExam, '/exam')


if __name__ == '__main__':
    print('='*60)
    print('|{0}Author:%9s{1}|'.format(' '*20, ' '*22) % __author__)
    print('|{0}Version:%10s{1}|'.format(' '*20, ' '*20) % __version__)
    print('|{0}Blog:%24.24s{1}|'.format(' '*20, ' '*9) % __blog__)
    # print('|{0}Web:%38.38s{1}|'.format(' ' * 13, ' ' * 3) % __web__)
    print('='*60)
    app.run(host=ip, port=port, debug=debug)
    # app.run(debug=True)
# from xmlrpc.server import SimpleXMLRPCServer
# from xmlrpc.server import SimpleXMLRPCRequestHandler
# from console_erya.console import Console
#
#
# # Restrict to a particular path.
# class RequestHandler(SimpleXMLRPCRequestHandler):
#     rpc_paths = ('/RPC2',)
#
#
# from jsonrpc import JSONRPCResponseManager
#
#
# if __name__ == '__main__':
#     with SimpleXMLRPCServer(("localhost", 8000),
#                             requestHandler=RequestHandler) as server:
#
#         server.register_instance(Console())
#
#         # Run the server's main loop
#         server.serve_forever()
