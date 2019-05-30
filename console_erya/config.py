# coding:utf-8
import configparser
from pathlib import Path
from os import getcwd, listdir, mkdir
from utils.utils import rk_bool
import requests
import demjson
from hashlib import md5
from console_erya.printinfo import print_info


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
    login_code = {
        'type': 'id',
        'string': 'numcode'
    }

    # 登陆账号输入框位置
    login_username = {
        'type': 'id',
        'string': 'unameId'
    }


    # 登陆密码输入框位置
    login_password = {
        'type': 'id',
        'string': 'passwordId'
    }

    # 登陆按钮位置
    login_button = {
        'type': 'xpath',
        'string': '//*[@id="form"]/table/tbody/tr[7]/td[2]/label/input'
    }

    # 登陆验证
    login_ver = {
        'type': 'xpath',
        'string': '//*[@id="space_nickname"]/p'
    }

    # 登陆错误结果
    login_result = {
        'type': 'xpath',
        'string': '//*[@id="show_error"]'
    }

    # 选择院校
    select_school_button = {
        'type': 'xpath',
        'string': '//*[@id="selectSchoolA"]'
    }

    # 院校搜索框
    select_school_search = {
        'type': 'id',
        'string': 'searchSchool1'
    }

    # 院校搜索按钮
    select_school_search_button = {
        'type': 'xpath',
        'string': '//*[@id="dialog1"]/div/div[1]/ul/li[2]/input[2]'
    }

    # 院校搜索结果
    select_school_result = {
        'type': 'xpath',
        'string': '//*[@id="searchForms"]/li[@class="zw_m_li"]/span/a'
    }
    
    # 刷新验证码
    refresh_code = {
        'type': 'xpath',
        'string': '//*[@id="numVerCode_tr"]//a'
    }

    # 验证码框
    code = {
        'type': 'id',
        'string': 'numVerCode'
    }

    # 首页课程
    lesson_index = {
        'type': 'id',
        'string': 'zne_kc_icon'
    }

    # 待刷课程frame
    course_name_list_frame = [
        {
            'name': 'iframe',
            'index': 0
        }
    ]

    # 课程列表
    course_name_list = {
        'type': 'xpath',
        'string': '//div[@class="Mconright httpsClass"]/h3/a'
        #'string': '/html/body/div/div[2]/div[2]/ul/li'
    }

    # 课程页面标题
    course_page_title = '学习进度页面'
  
    # 第一节课程xpath
    first_lesson = {
        'type': 'xpath',
        'string': '//div[@class="leveltwo"]//span[@class="articlename"]',
        # 'string': '/html/body/div[7]/div[1]/div[2]/div[3]/div[1]/div[1]/h3/span[2]/a'
    }


class AutomaticcompletionConfig:
    # 学习页面未完成课程
    not_completed_lesson = {
        'type': 'xpath',
        # 'string': [
        #     '//div[@class="ncells"]/a//span[@class="roundpointStudent  orange01 a002"]/../..', 
        #     '//div[@class="ncells"]/a//span[@class="roundpoint  orange01"]/../..',
        #     '//div[@class="ncells"]/a//span[@class="roundpointStudent"]/../..',
        #     ]
        'string': '//div[@class="ncells"]//span[@class="roundpointStudent  orange01 a002" or @class="roundpoint  orange01" or @class="roundpointStudent" or @class="roundpointStudent  orange01 a002 jobCount"]/../..'
    }

    # 课程名称
    lesson_name = {
        'type': 'xpath',
        'string': '//div[@id="mainid"]/h1'
    }

    # 学习页面视频iframe
    learn_page_video_iframe = [
        {
            'name': 'iframe',
            'index': 0
        },
        {
            'name': 'iframe',
            'index': 0
        }
    ]

    # 视频答题获取URL
    video_answer_url = 'https://mooc1-1.chaoxing.com/richvideo/initdatawithviewer?mid={0}&_dc={1}'

    # 学习页面进入视频部分iframe
    learn_page_video_part_iframe = [
        {
            'name': 'iframe',
            'index': 0
        }
    ]

    # 视频完成状态，如果xpath不报错则表示已完成
    video_complete_status = {
        'type': 'xpath',
        'string': '//div[@class="ans-attach-ct ans-job-finished"]'
    }

    # 任务未完成
    video_not_complete_status = {
        'type': 'xpath',
        'string': '//div[@class="ans-attach-ct"]/div[@class="ans-job-icon"]'
    }

    # 学习页面[视频]按钮
    learn_page_video_button = {
        'type': 'xpath',
        'string': '//span[contains(@title, "视频")]'
        # 'string': '//span[starts-with(@title, "视频")]'
    }

    # 学习页面章节测验按钮
    learn_page_test_button = {
        'type': 'xpath',
        # 'string': ['//span[contains(@title, "章节测验")]', '//span[contains(@title, "作业")]']
        'string': '//span[contains(@title, "章节测验")]|//span[contains(@title, "作业")]'
    }

    # 章节测试加载完成标志iframe
    test_load_complete_tag_iframe = [
        {
            'name': 'iframe',
            'index': 0
        },
        {
            'name': 'iframe',
            'index': 0
        },
        {
            'name': 'iframe',
            'index': 0
        }
    ]

    # 章节测试加载完成标志
    test_load_complete_tag = {
        'type': 'xpath',
        'string': '//*[@id="RightCon"]/div/div/div[1]/h3'
    }

    # 学习页面章节测试完成状态iframe
    learn_page_test_status_iframe = [
        {
            'name': 'iframe',
            'index': 0
        }
    ]

    # 章节测验完成状态，如果xpath不报错则表示已完成
    test_complete_stataus = {
        'type': 'xpath',
        'string': '//div[@class="ans-attach-ct ans-job-finished"]/div'
    }

    # 章节测试内容iframe
    learn_page_test_iframe = [
        {
            'name': 'iframe',
            'index': 0
        },
        {
            'name': 'iframe',
            'index': 0
        },
        {
            'name': 'iframe',
            'index': 0
        }
    ]

    Timu = {
        'type': 'class_name',
        'string': 'TiMu'
    }

    # 未查到答案等待时间
    noanswer_sleep = conf.getint('User', 'noanswer_sleep', fallback=5) if conf.getint('User', 'noanswer_sleep', fallback=5) >= 1 else 5

    # 章节测试提交frame
    test_submit_iframe = [
        {
            'name': 'iframe',
            'index': 0
        },
        {
            'name': 'iframe',
            'index': 0
        },
        {
            'name': 'iframe',
            'index': 0
        }
    ]

    # 章节测验提交 //*[@id="ZyBottom"]/div/div[4]/div[4]/div[5]/a[2]  //*[@id="ZyBottom"]/div[1]/div[4]/div[5]/a[2]
    submit_test = {
        'type': 'xpath',
        'string': '//div[@class="ZY_sub clearfix"]/a[2]'
    }

    # 章节测验确认提交
    submit_test_confirm = {
        'type': 'xpath',
        'string': '//*[@id="confirmSubWin"]/div/div/a[1]'
    }

    # 章节测验确认后验证码区域
    submit_test_validate = {
        'type': 'id',
        'string': 'validate'
    }

    # 章节测验提交验证码输入框
    submit_test_code_input = {
        'type': 'id',
        'string': 'code'
    }

    # 章节测验提交验证码按钮
    submit_test_code_button = {
        'type': 'id',
        'string': 'sub'
    }

    # 章节测试内容更新数据库iframe
    learn_page_test_iframe_updatedb = [
        {
            'name': 'iframe',
            'index': 0
        },
        {
            'name': 'iframe',
            'index': 0
        },
        {
            'name': 'iframe',
            'index': 0
        }
    ]

    # 章节测验提交后验证码
    submit_test_imgcode = {
        'type': 'id',
        'string': 'imgVerCode'
    }

    # 线路(本校/公网等)
    internet_line = conf.get('User', 'internet_line', fallback='公网1')

    # video_object
    video_object = {
        'type': 'id',
        'string': 'video_html5_api'
    }



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
    token = conf.get('User', 'token')
