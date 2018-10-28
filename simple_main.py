# coding:utf-8
import __version__
from console_erya import log
from console_erya import console
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
        self.read_account()

    def save_account(self):
        with open('account', 'wb') as f:
            f.write(base64.b64encode(json.dumps(self.account).encode()))

    def read_account(self):
        try:
            with open('account', 'rb') as f:
                self.account = json.loads(base64.b64decode(f.read()).decode())
        except:
            pass

    def input_select(self, hint, start, end):
        while True:
            try:
                i = input(hint+'(按q退出): ').strip()
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
        self.ui.ex_info(info)
        # self.check_version()
        self.ui.ex_info(function)
        i = self.input_select('请输入选项数字', 1, 4)
        if i == 1:
            # 刷课
            self.console.init()
            self.autolearn()
        elif i == 2:
            # 考试
            self.exam()
        elif i == 3:
            # 设置
            self.setting()
        elif i == 4:
            # 关于
            print('E-mail: bankroftvayne@gmail.com')
            print('Blog: https://www.bankroft.cn')
            webbrowser.open('https://www.bankroft.cn')
        else:
            print('输入错误')

    def autolearn(self):
        self.login()
        self.save_account()
        course = self.console.get_course()
        # i = {str(key+1)+':': value for key, value in enumerate(course)}
        # i[''] = '请选择观看的课程'
        # self.ui.ex_info(i)
        self.ui.pretty_table(['编号', '课程'], [[key+1, value] for key, value in enumerate(course)])
        self.console.browse_watch(self.input_select('请选择', 1, len(course)) - 1)
        print('开始...')
        while True:
            time.sleep(10)
    
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
            log.logger.error(log.log_template, '选择学校', '错误', '请重启重试')
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
            self.console.get_login_ver_code(refresh=code_error, display=True)
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
                print('登 录 失 败 :'+r[0])


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
        with open(str(Path(os.getcwd()) / 'config.ini'), 'w', encoding='utf-8') as f:
            conf.write(f)

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