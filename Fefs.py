# coding:utf-8
print('软件初始化中...')
import __version__
from console_erya.printinfo import print_info
from console_erya import console
from console_erya.config import use_rk_code
from utils.utils import rk_code
import os
import json
import base64
import sys
import time
from pathlib import Path
from prettytable import PrettyTable
import configparser
import webbrowser
import requests


info = {
    'Version: ': __version__.__version__,
    'Author: ': __version__.__author__,
    'Blog: ': __version__.__blog__,
}

function = {
    '': '请选择一项功能',
    '1: ': '刷课',
    '2: ': '考试',
    '3: ': '设置',
    '4: ': '联系作者',
}


class UI:
    def __init__(self):
        self.terminal_size = os.get_terminal_size()

    # 格式化输出信息
    def ex_info(self, info):
        row = self.terminal_size[0] - 1
        print('*' * (self.terminal_size[0]-1), end='\n\n')
        for key, value in info.items():
            i = str(key) + str(value)
            tmp = (row - len(i)) // 2
            print(' ' * tmp, end='')
            print(i)
        print('\n', '*' * (self.terminal_size[0]-1))

    def pretty_table(self, head, content):
        print('\n\n\n\n\n')
        table = PrettyTable(head)
        for x in content:
            table.add_row(x)
        print(table)
        print('\n\n\n\n\n')


class Main:
    
    def __init__(self):
        self.ui = UI()
        self.console = console.Console()
        self.auto_login = False
        self.account = {}
        self.function = {}
        self.read_account()
        self.register_function(description='刷课', func=self.autolearn)
        self.register_function(description='刷课(自动重登)', func=self.while_true_learn)
        self.register_function(description='考试', func=self.exam)
        self.register_function(description='设置', func=self.setting)
        self.register_function(description='关于', func=self.about)
        self.ui.ex_info(info)

    def save_account(self):
        with open('./temp/account.b4', 'wb') as f:
            f.write(base64.b64encode(json.dumps(self.account).encode()))

    def read_account(self):
        try:
            with open('./temp/account.b4', 'rb') as f:
                self.account = json.loads(base64.b64decode(f.read()).decode())
        except:
            pass
    
    def register_function(self, **kwargs):
        self.function[len(self.function.keys()) + 1] = {'desc': kwargs['description'], 'func': kwargs['func']}

    def input_select(self, hint, start, end):
        while True:
            try:
                i = input(hint+'(按q or Ctrl-C退出): ').strip()
                if i == 'q':
                    sys.exit(0)
                i = int(i)
            except (TypeError, ValueError):
                print('输入错误')
                continue
            if (i >= start) and (i <= end):
                return i
            print('输入错误')
    
    def input_confirm(self, hint):
        while True:
            i = input(hint+'(Y/N): ').strip().upper()
            if i == 'Y':
                return True
            elif i == 'N':
                return False
    
    def start(self):
        # self.check_version()
        self.ui.ex_info({k.__str__()+': ': v['desc'] for k, v in self.function.items()})
        i = self.input_select('请输入选项数字', 1, len(self.function.keys()))
        self.function[i]['func']()

    def while_true_learn(self):
        if set(['course', 'school', 'sschool', 'num', 'pwd']) - set(self.account.keys()):
            print('信息不完整，请重新运行功能: 1')
            return False
        if not use_rk_code:
            print('请运行功能：4，设置若快平台账号和密码')
            return False
        while True:
            try:
                self.console = console.Console()
                self.console.init()
                self.console.search_school(self.account['school'])
                self.console.select_school(self.account['sschool'])
                code_error = False
                pwd_error = False
                while True:
                    if pwd_error:
                        print('密码错误，请重新运行功能：1')
                        return False
                    file_name = self.console.get_login_ver_code(refresh=code_error, display=not use_rk_code)
                    code = rk_code(file_name)
                    print('登陆验证码为：', code)
                    print('登录中...')
                    r = self.console.login(self.account['num'], self.account['pwd'], code)
                    if r[1]:
                        print('登 录 成 功 :'+r[0])
                        break
                    else:
                        if '密码错误' == r[0]:
                            pwd_error = True
                        elif '验证码错误' == r[0]:
                            code_error = True
                        print('登 录 失 败:', r[0])
                course = self.console.get_course()
                print_info(['课程', course[self.account['course']], '开始'], 'info', True)
                if self.console.browse_watch(self.account['course']):
                    break
                else:
                    continue
            except KeyboardInterrupt:
                print('结束')
                return False
            # except:
            #     print('错误，重新开始')
            #     self.console.quit()
            #     continue

    def autolearn(self):
        self.console.init()
        self.login()
        course = self.console.get_course()
        # i = {str(key+1)+':': value for key, value in enumerate(course)}
        # i[''] = '请选择观看的课程'
        # self.ui.ex_info(i)
        self.ui.pretty_table(['编号', '课程'], [[key+1, value] for key, value in enumerate(course)])
        s = self.input_select('请选择', 1, len(course)) - 1
        self.account['course'] = s
        self.save_account()
        self.console.browse_watch(s)
        print('开始...')
        try:
            while True:
                time.sleep(10)
        except KeyboardInterrupt:
            print('KeyboardInterrupt')
            exit(0)
    
    def login(self):
        if self.account:
            if self.input_confirm('是否使用上次的账号({0})登录'.format(self.account['name'])):
                self.auto_login = True
        if self.auto_login:
            school = self.account['school']
        else:
            school = input('请输入学校: ').strip()
            self.account['school'] = school
        rschool = self.console.search_school(school)
        # i = {str(key+1)+':': value for key, value in enumerate(rschool)}
        # i[''] = '请选择学校'
        if self.auto_login:
            sschool = self.account['sschool']
        else:
            # self.ui.ex_info(i)
            self.ui.pretty_table(['编号', '学校'], [[key+1, value] for key, value in enumerate(rschool)])
            sschool = self.input_select('请选择学校', 1, len(rschool)) - 1
            self.account['sschool'] = sschool
        if self.console.select_school(sschool):
            pass
        else:
            print_info(['选择学校', '错误', '请重启重试'], 'warning', True)
            import sys
            sys.exit(0)
        pwd_error = False
        code_error = False
        if self.auto_login:
            num = self.account['num']
            pwd = self.account['pwd']
        else:
            num = input('输入学号：').strip()
            pwd = input('输入密码：').strip()
            self.account['num'] = num
            self.account['pwd'] = pwd
        while True:
            if pwd_error:
                pwd = input('输入密码：').strip()
                self.account['pwd'] = pwd
            file_name = self.console.get_login_ver_code(refresh=code_error, display=not use_rk_code)
            if use_rk_code:
                code = rk_code(file_name)
                print('登陆验证码为：', code)
            else:
                code = input('输入验证码：').strip()
            print('登录中...')
            r = self.console.login(num, pwd, code)
            if r[1]:
                print('登 录 成 功 :'+r[0])
                self.account['name'] = r[0]
                break
            else:
                if '密码错误' == r[0]:
                    pwd_error = True
                elif '验证码错误' == r[0]:
                    code_error = True
                print('登 录 失 败:', r[0])


    def exam(self):
        t = console.Exam()
        while True:
            print('请调整到考试页面，关闭其他所有页面')
            re = input('是否开始?(Y/N): ').upper()
            if re == 'Y':
                t.start()
            elif re == 'N':
                sys.exit(0)
    
    def setting(self):
        conf = configparser.ConfigParser()
        conf.read(str(Path(os.getcwd()) / 'config.ini'), encoding='utf-8')
        wechat_mp = input('查题微信公众号(我的博客有推荐)：')
        conf.set('User', 'wechat_mp', wechat_mp)
        while True:
            try:
                slp = int(input('章节测验存在未查到答案试题的等待提交时间(分钟)'))
                break
            except(ValueError, TypeError):
                continue
        conf.set('User', 'noanswer_sleep', str(slp))
        inl = input('默认线路无法播放时切换到：')
        conf.set('User', 'internet_line', inl)
        token = input('题库token: ')
        conf.set('User', 'token', token)
        rk_username = input('若快平台账号：')
        conf.set('User', 'rk_username', rk_username.strip())
        rk_pwd = input('若快平台密码：')
        conf.set('User', 'rk_password', rk_pwd.strip())
        with open(str(Path(os.getcwd()) / 'config.ini'), 'w', encoding='utf-8') as f:
            conf.write(f)

    def about(self):
        print('E-mail: bankroftvayne@gmail.com')
        print('Blog: https://www.bankroft.cn')
        webbrowser.open('https://www.bankroft.cn')

    @staticmethod
    def check_version():
        try:
            res = requests.get('https://raw.githubusercontent.com/bankroft/Fefs/master/__version__.py').text.split('\n')
        except:
            print('无法检测新版本，如果无法观看请手动检查')
            return False
        new_version = ''
        for x in res:
            if '__version__' in x:
                new_version = x.split('=')[1].strip().strip('\'')
                break
        if __version__.__version__ != new_version:
            print('检测到新版本: ', new_version)
    

    
if __name__ == '__main__':
    Main().start()