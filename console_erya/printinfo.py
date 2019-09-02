# coding :utf-8
import ctypes
import sys
import time

STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11
STD_ERROR_HANDLE = -12

# 字体颜色定义 ,关键在于颜色编码，由2位十六进制组成，分别取0~f，前一位指的是背景色，后一位指的是字体色

# Windows CMD命令行 字体颜色定义 text colors
FOREGROUND_BLACK = 0x00  # black.
FOREGROUND_DARKBLUE = 0x01  # dark blue.
FOREGROUND_DARKGREEN = 0x02  # dark green.
FOREGROUND_DARKSKYBLUE = 0x03  # dark skyblue.
FOREGROUND_DARKRED = 0x04  # dark red.
FOREGROUND_DARKPINK = 0x05  # dark pink.
FOREGROUND_DARKYELLOW = 0x06  # dark yellow.
FOREGROUND_DARKWHITE = 0x07  # dark white.
FOREGROUND_DARKGRAY = 0x08  # dark gray.
FOREGROUND_BLUE = 0x09  # blue.
FOREGROUND_GREEN = 0x0a  # green.
FOREGROUND_SKYBLUE = 0x0b  # skyblue.
FOREGROUND_RED = 0x0c  # red.
FOREGROUND_PINK = 0x0d  # pink.
FOREGROUND_YELLOW = 0x0e  # yellow.
FOREGROUND_WHITE = 0x0f  # white.


# Windows CMD命令行 背景颜色定义 background colors
BACKGROUND_BLUE = 0x10  # dark blue.
BACKGROUND_GREEN = 0x20  # dark green.
BACKGROUND_DARKSKYBLUE = 0x30  # dark skyblue.
BACKGROUND_DARKRED = 0x40  # dark red.
BACKGROUND_DARKPINK = 0x50  # dark pink.
BACKGROUND_DARKYELLOW = 0x60  # dark yellow.
BACKGROUND_DARKWHITE = 0x70  # dark white.
BACKGROUND_DARKGRAY = 0x80  # dark gray.
BACKGROUND_BLUE = 0x90  # blue.
BACKGROUND_GREEN = 0xa0  # green.
BACKGROUND_SKYBLUE = 0xb0  # skyblue.
BACKGROUND_RED = 0xc0  # red.
BACKGROUND_PINK = 0xd0  # pink.
BACKGROUND_YELLOW = 0xe0  # yellow.
BACKGROUND_WHITE = 0xf0  # white.


# get handle
std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

print_template = 'OPERATE:{0[0]: <10}  INFO:{0[1]: <21}  STATUS:{0[2]: <19}\n'


def set_cmd_text_color(color, handle=std_out_handle):
    Bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
    return Bool

# reset white


def resetColor():
    set_cmd_text_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE)

###############################################################

# 暗绿色
# dark green


def print_dark_green(mess):
    set_cmd_text_color(FOREGROUND_DARKGREEN)
    sys.stdout.write(mess)
    resetColor()

# 暗黄色
# dark yellow


def print_dark_yellow(mess):
    set_cmd_text_color(FOREGROUND_DARKYELLOW)
    sys.stdout.write(mess)
    resetColor()

# 红色
# red


def print_red(mess):
    set_cmd_text_color(FOREGROUND_RED)
    sys.stdout.write(mess)
    resetColor()

# 黄色
# yellow


def print_yellow(mess):
    set_cmd_text_color(FOREGROUND_YELLOW)
    sys.stdout.write(mess)
    resetColor()

##################################################


# 黄底红字
# white bkground and black text
def print_yellow_red(mess):
    set_cmd_text_color(BACKGROUND_YELLOW | FOREGROUND_RED)
    sys.stdout.write(mess)
    resetColor()


##############################################################

last_print = 1
last_progress_len = 0


def print_info(mes, level, timz=False, all_output=False):
    global last_print
    if last_print == 1:
        pass
    elif last_print == 2:
        print_progress('', end='\r')
    last_print = 1
    if not all_output:
        for i, v in enumerate(mes):
            if len(v) > 17:
                mes[i] = v[:10] + '...'
            else:
                mes[i] = v
    mes = print_template.format(mes)
    if timz:
        mes = time.strftime("%H:%M:%S", time.localtime()) + \
            ' - ' + level.upper() + ' - ' + mes
    if level == 'info':
        print_dark_green(mes)
    elif level == 'warning':
        print_dark_yellow(mes)
    elif level == 'notice':
        print_dark_yellow(mes)
    elif level == 'debug':
        print_dark_green(mes)
    elif level == 'error':
        print_red(mes)
    elif level == 'verbose':
        print_yellow_red(mes)
    else:
        print(mes)


def print_progress(mes, end='\r'):
    global last_print, last_progress_len
    print_dark_green(' '*last_progress_len+end)
    last_print = 2
    print_dark_green(str(mes)+end)
    last_progress_len = len(str(mes))


if __name__ == '__main__':
    pass
