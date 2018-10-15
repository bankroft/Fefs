# coding:utf-8
import curses
import sys
import time
import os
from console_erya import log
from console_erya import console
from curses.textpad import Textbox, rectangle
import locale
locale.setlocale(0, '')

welcome_sleep = 2
menu = {
    1: ['刷 课 ', '考 试 ', '方 向 键 ↑ or ↓ 选 择; s 确 认']
}

class UI:
    def __init__(self):
        self.display = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.display.keypad(True)
        curses.curs_set(False)

        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_RED, -1)
        curses.init_pair(2, curses.COLOR_GREEN, -1)
        # curses.init_pair(3, curses.COLOR_CYAN, -1)
        # curses.init_pair(4, curses.COLOR_YELLOW, -1)

    # 终端大小判断
    def _terminal_size(self, need=(0, 30)):
        tsize = os.get_terminal_size()
        while (tsize[0] < need[0]) or (tsize[1] < need[1]):
            self.display.addstr(0, 0, '窗口太小，请调整')
            self.display.refresh()
            time.sleep(100)
            tsize = os.get_terminal_size()
            self.clear()

    # 启动动画
    def start_animation(self):
        self._terminal_size()
        tsize = os.get_terminal_size()
        self.display.addstr(tsize[1] // 2, tsize[0] // 2 - 10, 'Welcome to use Fefs', curses.A_BOLD|curses.A_UNDERLINE)
        # self.display.clear()
        self.display.refresh()
        time.sleep(welcome_sleep)
    
    # 考试或刷课选择
    def exam_or_autolearn(self):
        self._terminal_size((2, 30))
        tsize = os.get_terminal_size()
        self.clear()
        index = [curses.A_REVERSE, 0]
        while True:
            self.clear()
            self.display.addstr(tsize[1] // 2 - 1, tsize[0] // 2 -1, menu[1][0], index[0])
            self.display.addstr(tsize[1] // 2, tsize[0] // 2 -1, menu[1][1], index[1])
            self.display.addstr(tsize[1] // 2 + 2, tsize[0] // 2 -10, menu[1][2])
            key = self.display.getkey()
            if (key == 'KEY_UP') or (key == 'KEY_DOWN'):
                index.reverse()
            elif key == 's':
                self.clear()
                return 1 if index[0] else 2
        self.display.refresh()
    
    # 选择
    def select(self, s, tips):
        self._terminal_size((2, 30))
        tsize = os.get_terminal_size()
        self.clear()
        index = [curses.A_REVERSE] + [0] * (len(s) - 1)
        pos = 0
        while True:
            self.clear()
            self.display.addstr(tsize[1] // 2 - 5, tsize[0] // 2 -10, tips)
            self.display.addstr(tsize[1] // 2 - 3, tsize[0] // 2 -10, menu[1][2])
            for i, x in enumerate(s):
                self.display.addstr(tsize[1] // 2 + i - 1, tsize[0] // 2 -1, ' '.join(list(x))+' ', index[(i+pos) % len(s)])
            key = self.display.getkey()
            if key == 'KEY_UP':
                pos = (pos + 1) if (pos < len(s) - 1) else 0
            elif key == 'KEY_DOWN':
                pos = (pos - 1) if (pos > 0) else (len(s) - 1)
            elif key == 's':
                return pos

    def clear(self):
        self.display.clear()
        self.display.refresh()
    
    def exit_(self):
        curses.nocbreak()
        self.display.keypad(False)
        curses.echo()
        curses.endwin()
    
    def error(self, info, color):
        self._terminal_size((2, 30))
        tsize = os.get_terminal_size()
        self.clear()
        self.display.addstr(tsize[1] // 2 - 3, tsize[0] // 2 -10, info, curses.color_pair(color)|curses.A_BOLD)
        self.display.refresh()
        time.sleep(2)
    
    def input_box(self, hits):
        self.clear()
        self.display.addstr(0, 0, hits)
        editwin = curses.newwin(5,30, 2,1)
        rectangle(self.display, 1,0, 1+5+1, 1+30+1)
        self.display.refresh()
        box = Textbox(editwin, insert_mode=True)
        # box = Textbox(self.display)
        box.edit()
        message = box.gather().strip()
        return message

    def test(self):
        for x in range(20):
            self.display.addstr(1, x, self.display.getkey())
            # print(self.display.getch())


class Main:
    
    def __init__(self):
        self.ui = UI()
        self.console = console.Console()

    def start(self):
        # self.ui.error('test')
        self.ui.start_animation()
        # s = self.ui.exam_or_autolearn()
        s = self.ui.select(['刷课', '考试'], '请 选 择 一 项 功 能 ( 考 试 暂 不 可 用 ) ')
        if s == 0:
            self.autolearn()
        else:
            self.exam()

    def autolearn(self):
        self.login()
        course = self.console.get_course()
        scourse = self.ui.select(course, '请 选 择 要 观 看 的 课 程 ')
        self.console.browse_watch(scourse)
        self.ui.exit_()
        while True:
            time.sleep(10)

    def login(self):
        self.ui.exit_()
        school = input('请输入学校: ').strip()
        self.ui = UI()
        rschool = self.console.search_school(school)
        sschool = self.ui.select(rschool, '请 选 择 学 校 ')
        if self.console.select_school(sschool):
            pass
        else:
            self.ui.exit_()
            log.logger.error(log.log_template, '选择学校', '错误', '请重启重试')
            sys.exit(0)
        while True:
            num = self.ui.input_box(hits="输 入 学 号 : (Ctrl-G 结 束 )")
            pwd = self.ui.input_box(hits='输 入 密 码 : (Ctrl-G 结 束 )')
            code = self.ui.input_box(hits='输 入 验 证 码 : (Ctrl-G 结 束 )')
            r = self.console.login(num, pwd, code)
            if r[1]:
                self.ui.error('登 陆 成 功 :'+' '.join(list(r[0])) + ' ', 2)
                break
            else:
                self.ui.error('登 陆 失 败 :'+' '.join(list(r[0])) + ' ', 1)
                time.sleep(2)

    def exam(self):
        pass


if __name__ == '__main__':
    Main().start()
    # display = curses.initscr()
    # main(display)