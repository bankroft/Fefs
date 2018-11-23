# coding:utf-8
import time
from PIL import Image
from selenium import webdriver, common
# import matplotlib.pyplot as plt
from .config import folder_temp_path
from .config import ConsoleConfig as cc
from .printinfo import print_info
from console_erya.questions import query_http_server
import os
from .automaticcompletion import AutomaticCompletion
from base64 import b64encode


class Console:
    # status = {
    #     'search_school': 0,
    #     'select_school': 0,
    #     'login': 0,
    #     'get_course': 0,
    #     'browser_watch': 0
    # }
    __base64_png = 'data:image/png;base64,'
    __select_school_result = []
    __course = []
    __course_lesson = []

    def __init__(self):
        self.options = webdriver.ChromeOptions()
        for x in cc.chrome_option:
            self.options.add_argument(x)

    def quit(self):
        self.driver.quit()

    def init(self):
        self.driver = webdriver.Chrome(cc.chrome_drive_path, chrome_options=self.options)
        self.driver.implicitly_wait(cc.timeout)
        while True:
            self.driver.get(cc.entrance_url)
            if '用户登录' not in self.driver.title:
                continue
            else:
                break

    def login(self, student_num, password, code):
        try:
            self.driver.find_element(cc.login_code['type'], cc.login_code['string']).clear()
        except common.exceptions.NoSuchElementException:
            self.driver.switch_to.frame(self.driver.find_elements_by_name('iframe')[0])
            self.driver.find_element(cc.login_code['type'], cc.login_code['string']).clear()
        self.driver.find_element(cc.login_code['type'], cc.login_code['string']).send_keys(code)
        self.driver.find_element(cc.login_username['type'], cc.login_username['string']).clear()
        self.driver.find_element(cc.login_username['type'], cc.login_username['string']).send_keys(student_num)
        self.driver.find_element(cc.login_password['type'], cc.login_password['string']).clear()
        self.driver.find_element(cc.login_password['type'], cc.login_password['string']).send_keys(password)
        self.driver.find_element(cc.login_button['type'], cc.login_button['string']).click()
        self.driver.switch_to.default_content()
        try:
            name = self.driver.find_element(cc.login_ver['type'], cc.login_ver['string']).text
        except common.exceptions.NoSuchElementException:
            try:
                result_text = self.driver.find_element(cc.login_result['type'], cc.login_result['string']).text
            except common.exceptions.NoSuchElementException:
                return 'False', False
            return str(result_text), False
        # self.status['login'] = 1
        return str(name), True

    def search_school(self, school):
        """
        院校选择
        :param school:
        :return:
        """
        self.driver.find_element(cc.select_school_button['type'], cc.select_school_button['string']).click()  # 点击选择院校按钮
        # 是否已经点击过院校选择按钮进入院校选择界面
        # self.driver.find_element('css', '#dialog2 > div > div.zw_result > p > a').click()
        self.driver.find_element(cc.select_school_search['type'], cc.select_school_search['string']).clear()  # 清除搜索框
        self.driver.find_element(cc.select_school_search['type'], cc.select_school_search['string']).send_keys(school)  # 向搜索框填入院校
        self.driver.find_element(cc.select_school_search_button['type'], cc.select_school_search_button['string']).click()  # 院校搜索
        self.__select_school_result = self.driver.find_elements(cc.select_school_result['type'], cc.select_school_result['string'])
        # self.status['search_school'] = 1
        return [x.text for x in self.__select_school_result]

    def select_school(self, id_: int):
        try:
            self.__select_school_result[id_].click()
        except (TypeError, IndexError):
            return False
        # self.status['select_school'] = 1
        return True

    def get_login_ver_code(self, refresh=False, display=False):
        """
        获取验证码图片，保存为code.png
        :param refresh: 是否刷新
        :return:
        """
        code_path = os.path.join(folder_temp_path, 'code.png')
        screen_shot = os.path.join(folder_temp_path, 'screenshot.png')
        if refresh:
            self.driver.find_element(cc.refresh_code['type'], cc.refresh_code['string']).click()
            # self.operate(refresh_code['type'], refresh_code['string'], 'click')
        self.driver.get_screenshot_as_file(screen_shot)  # 保存登陆界面截图
        a = self.driver.find_element(cc.code['type'], cc.code['string'])  # 定位验证码
        l = a.location['x'] + 1
        t = a.location['y'] + 1
        r = a.location['x'] + a.size['width']
        b = a.location['y'] + a.size['height']
        im = Image.open(screen_shot)
        im = im.crop((l, t, r, b))
        im.save(code_path)
        if display:
            os.system(code_path)
            # time.sleep(5)
            # plt.figure("验证码")
            # plt.imshow(im)
            # plt.show()
            # im.show()
        return code_path

    def get_course(self):
        self.__course = []
        self.driver.switch_to.default_content()
        try:
            self.driver.find_element(cc.lesson_index['type'], cc.lesson_index['string']).click()
        except common.exceptions.NoSuchElementException:
            pass
        except:
            pass
        for x in cc.course_name_list_frame:
            # driver.switch_to.frame(driver.find_elements_by_tag_name(x['name'])[x['index']])
            self.driver.switch_to.frame(self.driver.find_elements_by_tag_name(x['name'])[x['index']])
        for x in self.driver.find_elements(cc.course_name_list['type'], cc.course_name_list['string']):
            if not x.text:
                continue
            self.__course.append(x)
        return [x.text for x in self.__course]

    def browse_watch(self, course_id):
        try:
            course_id = int(course_id)
        except (TypeError, ValueError):
            return False
        if (course_id > (len(self.__course) - 1)) or (course_id < 0):
            return False
        course = self.__course[course_id]
        course_name = course.text
        course.click()
        time.sleep(5)
        for x in self.driver.window_handles:
            self.driver.switch_to.window(x)
            if self.driver.title == cc.course_page_title:
                break
        self.driver.find_elements(cc.first_lesson['type'], cc.first_lesson['string'])[0].click()
        # AutomaticCompletion(driver=self.driver, course_name=course_name).start()
        return AutomaticCompletion(driver=self.driver, course_name=course_name).run()
        # return True


class Exam:
    __select = ''.join([chr(x) for x in range(65, 91)])

    def __init__(self):
        self.driver = webdriver.Chrome(cc.chrome_drive_path)
        self.driver.set_window_size(1920, 1080)
        self.driver.implicitly_wait(cc.timeout)
        self.driver.get(cc.entrance_url)

    def start(self):
        self.driver.switch_to.window(self.driver.window_handles[0])
        a = self.driver.find_element_by_class_name('leftCardChild')
        typ = [(x, y.text.strip()) for x, y in enumerate(a.find_elements_by_tag_name('h3'))]
        for index, value in typ:
            z = 0
            a = self.driver.find_element_by_class_name('leftCardChild')
            le = len(a.find_elements_by_tag_name('div')[index].find_elements_by_tag_name('a'))
            for x in range(0, le):
                z += 1
                a = self.driver.find_element_by_class_name('leftCardChild')
                a.find_elements_by_tag_name('div')[index].find_elements_by_tag_name('a')[x].click()
                time.sleep(3)
                title = self.driver.find_element_by_xpath(
                    '//*[@id="submitTest"]//div[@class="Cy_TItle clearfix"]/div').text.strip().rstrip('分）').rstrip(
                    '0123456789').rstrip('.').rstrip('0123456789').rstrip('（').strip()
                # last_title = title
                right_answer = query_http_server(op='query', test_type=value, title=title)
                if value == '判断题':
                    if right_answer[0]:
                        if right_answer[2]:
                            print_info(['查询到', title, '正确'], 'info', True)
                            self.driver.find_elements_by_xpath('//*[@id="submitTest"]//ul[@class="Cy_ulBottom clearfix"]//li')[0].click()
                        else:
                            print_info(['查询到', title, '错误'], 'info', True)
                            self.driver.find_elements_by_xpath('//*[@id="submitTest"]//ul[@class="Cy_ulBottom clearfix"]//li')[1].click()
                    else:
                        print_info(['判断', title, '未查到，选择正确'], 'notice', True)
                elif value in ['单选题', '多选题']:
                    tag = 0
                    if right_answer[0]:
                        print_info(['查询到', title, ' '.join(right_answer[2])], 'info', True)
                        for y in self.driver.find_elements_by_xpath('//*[@id="submitTest"]//ul[@class="Cy_ulTop w-top"]/li'):
                            if y.text.strip().lstrip(self.__select).lstrip('、').strip() in right_answer[2]:
                                y.click()
                                tag = 1
                    if not tag:
                        if right_answer[3] in ['token', 'open']:
                            print_info(['答案错误', title, '重新查询'], 'info', True)
                            right_answer = query_http_server(op='query', defalut=False, test_type=value, title=title)
                            tag = 0
                            if right_answer[0]:
                                print_info(['查询到', title, ' '.join(right_answer[2])], 'info', True)
                                for y in self.driver.find_elements_by_xpath('//*[@id="submitTest"]//ul[@class="Cy_ulTop w-top"]/li'):
                                    if y.text.strip().lstrip(self.__select).lstrip('、').strip() in right_answer[2]:
                                        y.click()
                                        tag = 1
                            else:
                                print_info(['查询失败', title, '随机选择一项'], 'notice', True)
                        self.driver.find_elements_by_xpath('//*[@id="submitTest"]//ul[@class="Cy_ulTop w-top"]/li')[0].click()
                else:
                    print_info(['查询', value + '暂不支持', '跳过'], 'notice', True)

