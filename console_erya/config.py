# coding:utf-8
import configparser
from pathlib import Path
from os import getcwd, listdir, mkdir, system
from utils.utils import rk_bool
import requests
import demjson
from hashlib import md5
from console_erya.printinfo import print_info
import sys


conf = configparser.ConfigParser()
conf.read(str(Path(getcwd()) / 'config.ini'), encoding='utf-8')
url_get_config = 'http://123.207.19.72/api/get-config'

config_string_enc = '9HE7T?K?Vh9y+l@YefYd'

# 打码平台
use_rk_code = rk_bool

# temp文件夹
folder_temp_path = str(Path(getcwd()) / 'temp')
if 'temp' not in listdir(str(Path(getcwd()))):
    mkdir(folder_temp_path)


token = conf.get('User', 'token', fallback=False)
if not token:
    print('未配置token')
    system('pause')
    sys.exit(0)


def get_config(name):
    i = 1
    while i <= 3:
        enc = md5((name + config_string_enc).encode()).hexdigest()
        i += 1
        try:
            res = requests.get(url_get_config, params={'name': name, 'enc': enc, 'token': token}).json()
        except:
            continue
        if res['code'] == 100:
            data = res['data']
            if data['kind'] == 'list':
                try:
                    return demjson.decode(data['string'], encoding='utf-8')
                except demjson.JSONDecodeError:
                    continue
            else:
                return {'type': data['kind'], 'string': data['string']}
        else:
            print('非法参数')
            exit(0)
    print_info(['获取参数', '失败', '尝试继续运行'], 'error', False)
    return {'type': 'xpath', 'string': ''}


class ConsoleConfig:
    # chrome options
    chrome_option = [
        '--disable-extensions', 
        '--log-level=3', 
        '--slient', 
        '--disable-logging', 
        '--mute-audio', 
        '--headless', 
        '--disable-gpu', 
        '--window-size=1920,1080',
    ]

    # chrome 驱动
    chrome_drive_path = str(Path(getcwd()) / 'chromedriver.exe') if not conf.get('chromedriver', 'path', fallback=False) else conf.get('chromedriver', 'path', fallback=False)

    # driver超时设置
    timeout = 10

    # 入口url
    entrance_url = 'https://passport2.chaoxing.com/login?fid=145&refer=http://i.mooc.chaoxing.com'

    # 登陆验证码位置
    login_code = get_config('login_code')

    # 登陆账号输入框位置
    login_username = get_config('login_username')


    # 登陆密码输入框位置
    login_password = get_config('login_password')

    # 登陆按钮位置
    login_button = get_config('login_button')

    # 登陆验证
    login_ver = get_config('login_ver')

    # 登陆错误结果
    login_result = get_config('login_result')

    # 选择院校
    select_school_button = get_config('select_school_button')

    # 院校搜索框
    select_school_search = get_config('select_school_search')

    # 院校搜索按钮
    select_school_search_button = get_config('select_school_search_button')

    # 院校搜索结果
    select_school_result = get_config('select_school_result')
    
    # 刷新验证码
    refresh_code = get_config('refresh_code')

    # 登陆验证码框
    code = get_config('code')

    # 首页课程
    lesson_index = get_config('lesson_index')

    # 待刷课程frame
    course_name_list_frame = get_config('course_name_list_frame')

    # 课程列表
    course_name_list = get_config('course_name_list')

    # 课程页面标题
    course_page_title = '学习进度页面'
  
    # 第一节课程xpath
    first_lesson = get_config('first_lesson')


class AutomaticcompletionConfig:
    # 学习页面未完成课程
    not_completed_lesson = get_config('not_completed_lesson')

    # 课程名称
    lesson_name = get_config('lesson_name')

    # 学习页面视频iframe
    learn_page_video_iframe = get_config('learn_page_video_iframe')

    # 视频答题获取URL
    video_answer_url = 'https://mooc1-1.chaoxing.com/richvideo/initdatawithviewer?mid={0}&_dc={1}'

    # 学习页面进入视频部分iframe
    learn_page_video_part_iframe = get_config('learn_page_video_part_iframe')

    # 视频完成状态，如果xpath不报错则表示已完成
    video_complete_status = get_config('video_complete_status')

    # 任务未完成
    video_not_complete_status = get_config('video_not_complete_status')

    # 学习页面[视频]按钮
    learn_page_video_button = get_config('learn_page_video_button')

    # 学习页面章节测验按钮
    learn_page_test_button = get_config('learn_page_test_button')

    # 章节测试加载完成标志iframe
    test_load_complete_tag_iframe = get_config('test_load_complete_tag_iframe')

    # 章节测试加载完成标志
    test_load_complete_tag = get_config('test_load_complete_tag')

    # 学习页面章节测试完成状态iframe
    learn_page_test_status_iframe = get_config('learn_page_test_status_iframe')

    # 章节测验完成状态，如果xpath不报错则表示已完成
    test_complete_stataus = get_config('test_complete_stataus')

    # 章节测试内容iframe
    learn_page_test_iframe = get_config('learn_page_test_iframe')

    # 题目
    Timu = get_config('Timu')

    # 未查到答案等待时间
    noanswer_sleep = conf.getint('User', 'noanswer_sleep', fallback=5) if conf.getint('User', 'noanswer_sleep', fallback=5) >= 1 else 5

    # 章节测试提交frame
    test_submit_iframe = get_config('test_submit_iframe')

    # 章节测验提交 //*[@id="ZyBottom"]/div/div[4]/div[4]/div[5]/a[2]  //*[@id="ZyBottom"]/div[1]/div[4]/div[5]/a[2]
    submit_test = get_config('submit_test')

    # 章节测验确认提交
    submit_test_confirm = get_config('submit_test_confirm')

    # 章节测验确认后验证码区域
    submit_test_validate = get_config('submit_test_validate')

    # 章节测验提交验证码输入框
    submit_test_code_input = get_config('submit_test_code_input')

    # 章节测验提交验证码按钮
    submit_test_code_button = get_config('submit_test_code_button')

    # 章节测试内容更新数据库iframe
    learn_page_test_iframe_updatedb = get_config('learn_page_test_iframe_updatedb')

    # 章节测验提交后验证码
    submit_test_imgcode = get_config('submit_test_imgcode')

    # 线路(本校/公网等)
    internet_line = conf.get('User', 'internet_line', fallback='公网1')

    # video_object
    video_object = get_config('video_object')



class QuestionConfig:
    # http请求地址(查询)
    questions_request_query = 'http://123.207.19.72/api/query' # conf.get('queryHTTP', 'url_query', fallback=False)

    # http请求地址(查询/token)
    questions_request_query_token = 'http://123.207.19.72/api/token-query' # conf.get('queryHTTP', 'url_query_token', fallback=False)

    # http请求地址(更新)
    questions_request_update = 'http://123.207.19.72/api/update' # conf.get('queryHTTP', 'url_update', fallback=False)

    # 微信题库公众号
    wechat_mp = [x for x in conf.get('User', 'wechat_mp').split()]

    # 题库token
    token = token
